-- 2.1: Quốc gia nào đang "Sale" diện rộng nhất? (Tỷ lệ Sale)
-- Mục tiêu: Tính tỷ lệ phần trăm số mẫu giày đang được giảm giá so với tổng danh mục của từng nước.

WITH UniqueModels AS (
    SELECT DISTINCT 
        country_code, 
        model_number, 
        is_on_sale
    FROM global_catalogue
)
SELECT 
    country_code,
    COUNT(model_number) AS total_models,
    -- Ép kiểu về text và dùng ILIKE để bất chấp chữ True viết hoa hay viết thường
    SUM(CASE WHEN is_on_sale::text ILIKE 'true' OR is_on_sale::text = '1' THEN 1 ELSE 0 END) AS models_on_sale,
    
    -- Ép kiểu logic tương tự cho phép tính phần trăm
    ROUND((SUM(CASE WHEN is_on_sale::text ILIKE 'true' OR is_on_sale::text = '1' THEN 1 ELSE 0 END) * 100.0 / COUNT(model_number))::numeric, 2) AS sale_percentage
FROM UniqueModels
GROUP BY country_code
ORDER BY sale_percentage DESC;


-- 2.2 Độ sâu khuyến mãi (Markdown Depth) nước nào khủng nhất?
-- Mục tiêu: Tỷ lệ sale diện rộng là một chuyện, nhưng giảm "bao nhiêu phần trăm" (discount_percent) lại là câu chuyện khác. 
-- Nước nào đang có mức giảm giá trung bình mạnh tay nhất?
WITH SaleModels AS (
    SELECT DISTINCT 
        country_code, 
        model_number, 
        discount_percent
    FROM global_catalogue
    -- Áp dụng phép ép kiểu để nhận diện đúng hàng Sale
    WHERE (is_on_sale::text ILIKE 'true' OR is_on_sale::text = '1') 
      AND discount_percent > 0
)
SELECT 
    country_code,
    COUNT(model_number) AS items_on_sale,
    ROUND(AVG(discount_percent)::numeric, 2) AS avg_discount_percent
FROM SaleModels
GROUP BY country_code
HAVING COUNT(model_number) > 50
ORDER BY avg_discount_percent DESC
LIMIT 10;


-- 2.3: "Săn sale" - Tìm đôi giày bị rớt giá thảm nhất ở mỗi quốc gia
-- Mục tiêu: Dùng Window Function để tìm ra đúng 1 mẫu giày có mức giảm giá (tính bằng số tiền USD được bớt)
-- lớn nhất ở từng thị trường.
WITH DiscountedItems AS (
    SELECT DISTINCT 
        country_code, 
        model_number, 
        price_usd,          
        current_price_usd,  
        (price_usd - current_price_usd) AS discount_amount_usd
    FROM global_catalogue
    -- Áp dụng phép ép kiểu tại đây
    WHERE (is_on_sale::text ILIKE 'true' OR is_on_sale::text = '1') 
      AND price_usd IS NOT NULL 
      AND current_price_usd IS NOT NULL
),
RankedDiscounts AS (
    SELECT 
        country_code, 
        model_number,
        price_usd,
        current_price_usd,
        discount_amount_usd,
        DENSE_RANK() OVER (PARTITION BY country_code ORDER BY discount_amount_usd DESC) as rank_discount
    FROM DiscountedItems
)
SELECT 
    country_code, 
    model_number,
    discount_amount_usd,
    price_usd AS original_price,
    current_price_usd AS sale_price
FROM RankedDiscounts
WHERE rank_discount = 1
ORDER BY discount_amount_usd DESC;