import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv  # Thư viện để đọc file .env

def load_data_to_postgres(parquet_path, engine, table_name="global_catalogue"):
    print(f" Đang đọc dữ liệu từ: {parquet_path}")
    df = pd.read_parquet(parquet_path)
    
    print(f" Đang kết nối tới PostgreSQL...")
    print(f" Đang nạp {len(df):,} dòng vào bảng '{table_name}'...")
    
    # Nạp dữ liệu qua SQLAlchemy. 
    # Mẹo tối ưu: Giảm chunksize xuống một chút vì mạng nội bộ của PostgreSQL xử lý khác file vật lý của SQLite
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=50000)
    
    # Tạo chỉ mục (Index) bằng SQLAlchemy
    print(" Đang tạo chỉ mục (Index) để tối ưu tốc độ truy vấn SQL...")
    with engine.connect() as conn:
        conn.execute(text(f"CREATE INDEX idx_country ON {table_name} (country_code);"))
        conn.execute(text(f"CREATE INDEX idx_model ON {table_name} (model_number);"))
        conn.commit() # Bắt buộc phải có commit trong SQLAlchemy 2.0
    
    # Chạy thử truy vấn
    print("\nChạy thử lệnh SQL kiểm tra:")
    test_query = f"""
        SELECT country_code, COUNT(*) as total_rows 
        FROM {table_name} 
        GROUP BY country_code 
        LIMIT 5;
    """
    test_result = pd.read_sql_query(test_query, engine)
    print(test_result)
    
    print("\n Quá trình nạp PostgreSQL hoàn tất!")

def main():
    # Tải các biến môi trường từ file .env
    load_dotenv()

    # Cấu hình đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    PROCESSED_PATH = os.path.join(project_root, "dataset", "processed", "nike_global_processed.parquet")
    
    if not os.path.exists(PROCESSED_PATH):
        print(" Lỗi: Không tìm thấy file processed!")
        return
        
    # ---------------------------------------------------------
    # CẤU HÌNH THÔNG TIN KẾT NỐI TỪ BIẾN MÔI TRƯỜNG
    # ---------------------------------------------------------
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASSWORD") 
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    # Kiểm tra an toàn: Đảm bảo file .env đã được cấu hình đủ
    if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
        print("Lỗi: Không tìm thấy thông tin kết nối Database. Hãy kiểm tra lại file .env!")
        return
    
    # Tạo chuỗi kết nối (Connection String)
    connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Khởi tạo Engine
    engine = create_engine(connection_string)
    
    try:
        load_data_to_postgres(PROCESSED_PATH, engine)
    except Exception as e:
        print(f"Có lỗi xảy ra trong quá trình nạp: {e}")
    finally:
        engine.dispose() # Đóng kết nối gọn gàng

if __name__ == "__main__":
    main()