import os
import glob
import pandas as pd

def extract_and_clean_data(raw_data_path):
    all_cleaned_dfs = []
    csv_files = glob.glob(os.path.join(raw_data_path, "*.csv"))
    
    if not csv_files:
        print("❌ Không tìm thấy file CSV nào.")
        return None

    print(f" Bắt đầu xử lý {len(csv_files)} file CSV...")

    for file_path in csv_files:
        country_code = os.path.basename(file_path).replace('.csv', '')
        
        # SỬA LỖI LOGIC: Bỏ qua file Global_Nike để không bị nhân đôi dữ liệu
        if "Global" in country_code or "global" in country_code.lower():
            print(f" Bỏ qua file tổng hợp: {country_code}")
            continue
            
        try:
            # Thêm low_memory=False để Pandas không cảnh báo về mixed-types khi đọc
            df = pd.read_csv(file_path, low_memory=False)
            df['country_code'] = country_code
            
            df = df.drop_duplicates()
            
            critical_columns = ["product_name", "model_number", "price_local"]
            df = df.dropna(subset=critical_columns)
            
            # SỬA LỖI KỸ THUẬT: Ép kiểu dữ liệu chuẩn xác cho các cột định danh
            # Tránh lỗi pyarrow không lưu được file Parquet
            df['model_number'] = df['model_number'].astype(str)
            df['product_name'] = df['product_name'].astype(str)
            
            all_cleaned_dfs.append(df)
            print(f" Đã xử lý: {country_code} ({len(df):,} dòng)")
            
        except Exception as e:
            print(f" Lỗi khi đọc file {country_code}: {e}")
    
    print("\n🔄 Đang gộp toàn bộ dữ liệu...")
    final_df = pd.concat(all_cleaned_dfs, ignore_index=True)
    final_df = final_df.drop_duplicates()
    
    return final_df

def main():
    # 1. Xác định vị trí tuyệt đối của dự án
    # Lấy đường dẫn của chính file script này (thư mục pipelines)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lùi lại 1 cấp để ra thư mục gốc của dự án (thư mục nike)
    project_root = os.path.dirname(script_dir)
    
    # 2. Ghép nối đường dẫn động 
    RAW_PATH = os.path.join(project_root, "dataset", "raw")
    INTERIM_PATH = os.path.join(project_root, "dataset", "interim", "cleaned_nike_data.parquet")
    
    # In ra để kiểm tra xem Python đã tìm đúng đường dẫn chưa
    print(f"Thư mục đang quét: {RAW_PATH}")
    
    # Đảm bảo thư mục interim đã tồn tại
    os.makedirs(os.path.dirname(INTERIM_PATH), exist_ok=True)
    
    # 3. Chạy hàm xử lý
    final_df = extract_and_clean_data(RAW_PATH)
    
    # 4. Xuất file kết quả
    if final_df is not None:
        print(f"\n Tổng số dòng dữ liệu sau khi gộp và làm sạch: {len(final_df):,}")
        print("Đang xuất file Parquet...")
        final_df.to_parquet(INTERIM_PATH, index=False)
        print(f" Pipeline hoàn tất! Dữ liệu đã lưu tại: {INTERIM_PATH}")

if __name__ == "__main__":
    main()