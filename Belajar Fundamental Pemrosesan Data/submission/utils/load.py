import pandas as pd
import logging
from sqlalchemy import create_engine
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_to_csv(df: pd.DataFrame, filename: str = 'products.csv') -> str:
    """
    Menyimpan data ke file CSV
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        filename (str): Nama file CSV
        
    Returns:
        str: path ke file yang akan disimpan
    """
    try:
        # verifikasi data tidak kosong
        if df.empty:
            logger.warning("cannot save empty dataframe to csv")
            raise ValueError("empty dataframe cannot be saved to csv")
         
        df.to_csv(filename, index=False)
        logger.info(f"Data berhasil disimpan ke {filename}")
        return os.path.abspath(filename)
    except Exception as e:
        logger.error(f"Error saving to CSV: {str(e)}")
        raise IOError(f"Failed to save data to CSV: {str(e)}")

def save_to_google_sheets(df: pd.DataFrame, spreadsheet_id: str, credentials_file: str, 
                         _service=None) -> bool:
    """
    Menyimpan data ke Google Sheets
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        spreadsheet_id (str): ID spreadsheet Google Sheets
        credentials_file (str): Path ke file credentials Google Sheets API
        _service: Optional service untuk memudahkan testing
        
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        # verifikasi data tidak kosong
        if df.empty:
            logger.warning("cannot save dataframe to google sheet")
            return False
        
        # jika sudah disediakan service (untuk testing)
        if _service:
            service = _service
        else:
            # verifikasi file credensial ada
            if not os.path.exists(credentials_file):
                logger.error(f"credensial file not found: {credentials_file}")
                return False
            
            # load credentials
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_file,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
            except Exception as e:
                logger.error(f"error loading credential: {str(e)}")
                return False
            
            # buat service
            try:
                service = build('sheets', 'v4', credentials=credentials)
            except Exception as e:
                logger.error(f"error creating google sheet service: {str(e)}")
                return False
        
        # konversi DataFrame ke format yang bisa dibaca Google Sheets
        values = [df.columns.tolist()] + df.values.tolist()
        
        # update spreadsheet
        try:
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
        
            logger.info("Data berhasil disimpan ke Google Sheets")

            sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit?usp=sharing"
            logger.info(f"google sheet url: {sheet_url}")

            return True
        
        except Exception as e:
            logger.error(f"error updating google sheet: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"Error saving to Google Sheets: {str(e)}")
        return False

def save_to_postgresql(df: pd.DataFrame, connection_string: str, table_name: str) -> bool:
    """
    Menyimpan data ke PostgreSQL
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        connection_string (str): String koneksi PostgreSQL
        table_name (str): Nama tabel di PostgreSQL
        
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        # verifikasi data tidak kosong
        if df.empty:
            logger.warning("cannot save empty dataframe to postgreSQL")
            return False
        
        # coba buat engine
        try:
            engine = create_engine(connection_string)
        except Exception as e:
            logger.error(f"error connecting to postgreSQL: {str(e)}")
            return False
        
        # simpan data ke database
        try:
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            logger.info(f"Data berhasil disimpan ke PostgreSQL table {table_name}")
            return True
        except Exception as e:
            logger.error(f"error writing to postgreSQL: {str(e)}")
            return False
        
    except Exception as e:
        logger.error(f"Error saving to PostgreSQL: {str(e)}")
        return False

def load_data(df: pd.DataFrame, 
              csv_file: Optional[str] = 'products.csv',
              google_sheets_config: Optional[dict] = None,
              postgresql_config: Optional[dict] = None) -> dict:
    """
    Menyimpan data ke berbagai repositori yang ditentukan
    
    Args:
        df (pd.DataFrame): DataFrame yang akan disimpan
        csv_file (Optional[str]): Path ke file CSV
        google_sheets_config (Optional[dict]): Konfigurasi Google Sheets
        postgresql_config (Optional[dict]): Konfigurasi PostgreSQL
        
    Returns:
        dict: Status penyimpanan untuk setiap repositori
    """
    results = {
        'csv': None,
        'postgresql': False,
        'google_sheets': None
    }

    errors = []
    
    # simpan ke CSV
    if csv_file:
        try:
            results['csv'] = save_to_csv(df, csv_file)
            logger.info(f"data berhasil disimpan ke csv: {results['csv']}")
        except Exception as e:
            logger.error(f"error saving to csv: {str(e)}")
            errors.append(f"CSV: {str(e)}")
    
    # simpan ke Google Sheets
    if google_sheets_config:
        try:
            success = save_to_google_sheets(
                df,
                google_sheets_config['spreadsheet_id'],
                google_sheets_config['credentials_file']
            )
            results['google_sheets'] = f"https://docs.google.com/spreadsheets/d/{google_sheets_config['spreadsheet_id']}/edit" if success else None
            logger.info(f"google sheet status: {success}")
        except Exception as e:
            logger.error(f"error saving to google sheet: {str(e)}")
            errors.append(f"google sheet: {str(e)}")
    
    # simpan ke PostgreSQL
    if postgresql_config:
        try:
            results['postgresql'] = save_to_postgresql(
                df,
                postgresql_config['connection_string'],
                postgresql_config['table_name']
            )
            logger.info(f"postgreSQL status: {results['postgresql']}")
        except Exception as e:
            logger.error(f"error saving to postgreSQL: {str(e)}")
            errors.append(f"postgreSQL: {str(e)}")
    
    # check if any repository was successful
    if any(v for v in results.values() if v):
        return results
    else:
        error_msg = f"failed to save data to any repository. Errors: {errors}"
        logger.error(error_msg)
        raise Exception(error_msg) 