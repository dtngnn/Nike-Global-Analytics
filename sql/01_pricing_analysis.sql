-- 1.1 Tính giá trung bình toàn danh mục của mỗi quốc gia
-- Mục tiêu: Tìm ra nước nào mua giày đắt nhất / rẻ nhất.
WITH DistinctModels AS (
    -- Bước 1: Lấy ra danh sách các mẫu giày duy nhất và giá của chúng ở từng nước
    SELECT DISTINCT 
        country_code, 
        model_number, 
        current_price_usd
    FROM global_catalogue
    WHERE current_price_usd IS NOT NULL
)
-- Bước 2: Tính toán thống kê
SELECT 
    country_code,
    COUNT(model_number) AS total_unique_models,
    ROUND(AVG(current_price_usd)::numeric, 2) AS avg_price_usd
FROM DistinctModels
GROUP BY country_code
ORDER BY avg_price_usd DESC;


-- 1.2: Phân tích chênh lệch giá (Price Discrimination) của 5 mẫu giày phổ biến nhất
-- Mục tiêu: Cùng một đôi giày, Nike có bán đồng giá trên toàn cầu không hay "nhìn mặt gửi vàng"?
WITH DistinctShoePrices AS (
    SELECT DISTINCT 
        country_code, 
        model_number, 
        current_price_usd
    FROM global_catalogue
    WHERE current_price_usd IS NOT NULL
)
SELECT 
    model_number,
    COUNT(country_code) AS countries_sold_in,
    MAX(current_price_usd) AS max_price_usd,
    MIN(current_price_usd) AS min_price_usd,
    (MAX(current_price_usd) - MIN(current_price_usd)) AS price_gap_usd
FROM DistinctShoePrices
GROUP BY model_number
-- Chỉ xét những mẫu giày "toàn cầu" (bán ở ít nhất 10 quốc gia)
HAVING COUNT(country_code) >= 10
ORDER BY price_gap_usd DESC
LIMIT 5;

SELECT 
    country_code, 
    model_number,
    current_price_usd
FROM global_catalogue
WHERE model_number = 'HV0360' AND current_price_usd IS NOT NULL
-- Dùng GROUP BY để gộp các size lại, chỉ lấy 1 mức giá duy nhất cho mỗi nước
GROUP BY country_code, model_number, current_price_usd
ORDER BY current_price_usd DESC;

-- 1.3: Phân khúc giá sản phẩm tại thị trường Việt Nam (VN)
-- Mục tiêu: Cấu trúc danh mục hàng hóa (Assortment) tại VN đang tập trung đánh vào tệp khách hàng bình dân hay cao cấp?
WITH VNShoes AS (
    SELECT DISTINCT 
        model_number, 
        current_price_usd
    FROM global_catalogue
    WHERE country_code = 'VN' AND current_price_usd IS NOT NULL
)
SELECT 
    CASE 
        WHEN current_price_usd < 50 THEN '1. Gia re (< 50$)'
        WHEN current_price_usd BETWEEN 50 AND 120 THEN '2. Tam trung (50$ - 120$)'
        ELSE '3. Cao cap (> 120$)'
    END AS price_segment,
    COUNT(model_number) AS total_models,
    -- Ép phép chia phần trăm về numeric trước khi làm tròn 1 chữ số
    ROUND((COUNT(model_number) * 100.0 / (SELECT COUNT(*) FROM VNShoes))::numeric, 1) AS percentage
FROM VNShoes
GROUP BY 
    CASE 
        WHEN current_price_usd < 50 THEN '1. Gia re (< 50$)'
        WHEN current_price_usd BETWEEN 50 AND 120 THEN '2. Tam trung (50$ - 120$)'
        ELSE '3. Cao cap (> 120$)'
    END
ORDER BY price_segment ASC;