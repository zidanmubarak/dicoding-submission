import os
from dotenv import load_dotenv
from utils.extract import scrape_all_pages
from utils.transform import transform_data
from utils.load import load_data
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Extract data
        logger.info("Memulai proses ekstraksi data...")
        raw_data = scrape_all_pages()
        
        # Transform data
        logger.info("Memulai proses transformasi data...")
        clean_data = transform_data(raw_data)
        
        # Load data
        logger.info("Memulai proses penyimpanan data...")
        
        # Konfigurasi Google Sheets
        google_sheets_config = {
            'spreadsheet_id': '1D0ZMfA7PIVfRjpNpkJyuXN...',
            'credentials_file': 'google-sheets-api.json'
        }
        
        # Konfigurasi PostgreSQL
        postgresql_config = {
            'connection_string': 'postgresql+psycopg2://developer:lupa@localhost:5432/companydb',
            'table_name': 'product'
        }
        
        # Simpan data ke semua repositori
        results = load_data(
            clean_data,
            csv_file='products.csv',
            google_sheets_config=google_sheets_config,
            postgresql_config=postgresql_config
        )
        
        # Log hasil penyimpanan
        for repo, success in results.items():
            if success:
                logger.info(f"Data berhasil disimpan ke {repo}")
            else:
                logger.error(f"Gagal menyimpan data ke {repo}")
                
    except Exception as e:
        logger.error(f"Error dalam menjalankan pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main() 