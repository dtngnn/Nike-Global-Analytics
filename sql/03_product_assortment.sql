
-- 3.1: "Con cưng" của Nike - Quy mô danh mục thị trường
-- Mục tiêu: Đếm chính xác số lượng mã giày duy nhất đang được mở bán tại mỗi quốc gia.
SELECT 
    country_code,
    COUNT(DISTINCT model_number) AS total_unique_models
FROM global_catalogue
GROUP BY country_code
ORDER BY total_unique_models DESC;




-- 3.2: Sản phẩm độc quyền (Regional Exclusives)
-- Mục tiêu: Tìm những mẫu giày "phiên bản giới hạn địa phương" - tức là mã giày đó chỉ xuất hiện duy nhất ở 1 quốc gia.

WITH ModelCountryCount AS (
    -- Đếm xem mỗi mẫu giày đang được bán ở bao nhiêu nước
    SELECT 
        model_number,
        COUNT(DISTINCT country_code) AS num_countries,
        MAX(country_code) AS exclusive_country -- Nếu count = 1, đây chính là nước độc quyền
    FROM global_catalogue
    GROUP BY model_number
)
SELECT 
    exclusive_country AS country_code,
    COUNT(model_number) AS total_exclusive_models
FROM ModelCountryCount
-- Lọc ra những đôi chỉ bán ở đúng 1 nước
WHERE num_countries = 1
GROUP BY exclusive_country
ORDER BY total_exclusive_models DESC;


-- 3.3: Sự tương đồng danh mục (Assortment Overlap)
-- Mục tiêu: So sánh mức độ giống nhau về sản phẩm giữa 2 quốc gia. 
-- Ví dụ: Khách hàng ở Anh (GB) và Pháp (FR) đang mua chung bao nhiêu mẫu giày?
WITH GB_Models AS (
    SELECT DISTINCT model_number FROM global_catalogue WHERE country_code = 'GB'
),
FR_Models AS (
    SELECT DISTINCT model_number FROM global_catalogue WHERE country_code = 'FR'
)
SELECT 
    (SELECT COUNT(*) FROM GB_Models) AS gb_total_models,
    (SELECT COUNT(*) FROM FR_Models) AS fr_total_models,
    -- Dùng INNER JOIN để tìm phần giao (những đôi giày bán ở cả 2 nước)
    (SELECT COUNT(*) 
     FROM GB_Models 
     INNER JOIN FR_Models ON GB_Models.model_number = FR_Models.model_number) AS shared_models
;