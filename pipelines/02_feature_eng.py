import os
import pandas as pd
import numpy as np

def get_exchange_rates():
    """Từ điển tỷ giá hối đoái quy đổi từ Nội tệ sang 1 USD."""
    return {
        'US': 1.0, 'GB': 0.79, 'JP': 150.5, 'VN': 25400.0, 'CN': 7.23, 
        'KR': 1350.0, 'CA': 1.36, 'AU': 1.52, 'SG': 1.35, 'TH': 36.5, 
        'ID': 15800.0, 'MY': 4.75, 'IN': 83.3, 
        'FR': 0.92, 'DE': 0.92, 'IT': 0.92, 'ES': 0.92, 'NL': 0.92, 
        'BE': 0.92, 'IE': 0.92, 'PT': 0.92, 'AT': 0.92, 'GR': 0.92, 'FI': 0.92
    }

def engineer_features(df):
    print("Bắt đầu xử lý Feature Engineering...")
    df['country_code'] = df['country_code'].str.replace('Nike_', '', regex=False)
    
    # 1. LÀM SẠCH VÀ ÉP KIỂU DỮ LIỆU SỐ
    print("   - Đang làm sạch và ép kiểu cột giá...")
    # Loại bỏ mọi ký tự không phải là số hoặc dấu chấm (ví dụ: dấu phẩy, chữ cái, $)
    # Lưu ý: 'nan' sẽ biến thành '' và to_numeric sẽ tự động đưa về NaN
    df['price_local'] = df['price_local'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['sale_price_local'] = df['sale_price_local'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    
    df['price_local'] = pd.to_numeric(df['price_local'], errors='coerce')
    df['sale_price_local'] = pd.to_numeric(df['sale_price_local'], errors='coerce')
    
    # 2. XỬ LÝ LOGIC KHUYẾN MÃI (CHỐNG LỖI CỘT)
    print("   - Đang tính toán logic khuyến mãi...")
    
    # Lấy số lớn hơn làm Giá gốc (Original Price)
    original_price = np.maximum(df['price_local'], df['sale_price_local'].fillna(df['price_local']))
    # Lấy số nhỏ hơn làm Giá bán thực tế (Current Sale Price)
    current_price = np.minimum(df['price_local'], df['sale_price_local'].fillna(df['price_local']))
    
    # Đang sale nếu Giá bán thực tế NHỎ HƠN Giá gốc
    df['is_on_sale'] = current_price < original_price
    
    # Tính phần trăm giảm giá
    df['discount_percent'] = np.where(
        df['is_on_sale'],
        round((original_price - current_price) / original_price * 100, 1),
        0.0
    )
    
    # 3. QUY ĐỔI TIỀN TỆ VỀ USD
    print("   - Đang quy đổi tỷ giá sang USD...")
    rates = get_exchange_rates()
    df['exchange_rate_to_usd'] = df['country_code'].map(rates)
    
    # Lưu giá gốc USD và giá hiện hành USD
    df['price_usd'] = round(original_price / df['exchange_rate_to_usd'], 2)
    df['current_price_usd'] = round(current_price / df['exchange_rate_to_usd'], 2)
    
    return df

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    INTERIM_PATH = os.path.join(project_root, "dataset", "interim", "cleaned_nike_data.parquet")
    PROCESSED_PATH = os.path.join(project_root, "dataset", "processed", "nike_global_processed.parquet")
    
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    
    print(f"Đang đọc dữ liệu từ: {INTERIM_PATH}")
    if not os.path.exists(INTERIM_PATH):
        print("Lỗi: Không tìm thấy file interim.")
        return
        
    df = pd.read_parquet(INTERIM_PATH)
    df_processed = engineer_features(df)
    
    print("\nĐang xuất file Parquet...")
    df_processed.to_parquet(PROCESSED_PATH, index=False)
    print(f"Pipeline hoàn tất! {PROCESSED_PATH}")
    
    columns_to_show = ['country_code', 'model_number', 'is_on_sale', 'discount_percent', 'price_usd', 'current_price_usd']
    print("\nMẫu dữ liệu sau xử lý:")
    print(df_processed[columns_to_show].head(10))

if __name__ == "__main__":
    main()