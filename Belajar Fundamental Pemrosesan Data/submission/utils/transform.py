import pandas as pd
import logging
from typing import Optional, Union
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_title(title: Union[str, None]) -> Optional[str]:
    """
    Membersihkan judul produk
    
    Args:
        title (str): Judul dalam format string
        
    Returns:
        Optional[str]: Judul yang sudah dibersihkan
    """
    try:
        if not isinstance(title, str):
            logger.error(f"Error cleaning title: invalid type {type(title)}")
            return None
            
        if pd.isna(title) or title == "Unknown Product":
            return None
            
        # Hapus whitespace di awal dan akhir
        cleaned_title = title.strip()
        
        # Jika title kosong setelah dibersihkan
        if not cleaned_title:
            return None
            
        return cleaned_title
    except Exception as e:
        logger.error(f"Error cleaning title {title}: {str(e)}")
        return None
    
def clean_price(price: str) -> Optional[float]:
    """
    Membersihkan dan mengkonversi harga dari USD ke IDR
    
    Args:
        price (str): Harga dalam format string
        
    Returns:
        Optional[float]: Harga dalam IDR atau None jika invalid
    """
    try:
        if not isinstance(price, str):
            logger.error(f"Error cleaning price: invalid type {type(price)}")
            return None
        
        if pd.isna(price) or price == "Price Unavailable":
            return None
        
        # ekstrak angka dari string (misal $1.00 menjadi 1.00)
        match = re.search(r'\$?(\d+\.?\d*)', price)
        if match:
            usd_price = float(match.group(1))
            # konversi ke IDR (1 USD = 16000 IDR)
            idr_price = usd_price * 16000
            # bulatkan ke 2 desimal
            return round(idr_price, 2)
        else:
            logger.warning(f"couldn't extract numeric value from price: {price}")
            return None
        
    except Exception as e:
        logger.error(f"Error converting price {price}: {str(e)}")
        return None

def clean_rating(rating: str) -> Optional[float]:
    """
    Membersihkan rating
    
    Args:
        rating (str): Rating dalam format string
        
    Returns:
        Optional[float]: Rating dalam float atau None jika invalid
    """
    try:
        if not isinstance(rating, str):
            logger.error(f"Error cleaning rating: invalid type {type(rating)}")
            return None
        
        if pd.isna(rating) or "Invalid Rating" in rating or "Not Rated" in rating:
            return None
        
        # ekstrak angka rating (misal "Rating: ⭐ 3.9 / 5" menjadi 3.9)
        match = re.search(r'(\d+\.?\d*)\s*\/?\s*5?', rating)
        if match:
            rating_value = float(match.group(1))
            # pastikan rating dalam range 0-5 dan bulatkan ke 1 desimal
            if 0 <= rating_value <= 5:
                return round(rating_value, 1)
            return None
        else:
            logger.warning(f"couldn't extract numeric value from rating: {rating}")
            return None
    except Exception as e:
        logger.error(f"Error converting rating {rating}: {str(e)}")
        return None

def clean_colors(colors: str) -> Optional[int]:
    """
    Membersihkan jumlah warna
    
    Args:
        colors (str): Jumlah warna dalam format string
        
    Returns:
        Optional[int]: Jumlah warna dalam integer atau None jika invalid
    """
    try:
        if not isinstance(colors, str):
            logger.error(f"Error cleaning colors: invalid type {type(colors)}")
            return None
        
        if pd.isna(colors) or colors == "Colors Not Available":
            return None
        
        # ekstrak angka dari string (misal "5 Colors" menjadi 5)
        match = re.search(r'(\d+)', colors)
        if match:
            return int(match.group(1))
        else:
            logger.warning(f"couldn't extract numeric value from colors: {colors}")
            return None
    except Exception as e:
        logger.error(f"Error converting colors {colors}: {str(e)}")
        return None

def clean_size(size: Union[str, None]) -> Optional[str]:
    """
    Membersihkan ukuran
    
    Args:
        size (str): Ukuran dalam format string
        
    Returns:
        str: Ukuran yang sudah dibersihkan
    """
    try:
        if not isinstance(size, str):
            logger.error(f"Error cleaning size: invalid type {type(size)}")
            return None
        
        if pd.isna(size) or size == "Size Not Available":
            return None
        
        # hapus prefix "Size: " dan whitespace
        cleaned_size = size.replace('Size:', '').strip()
        
        # jika size kosong setelah dibersihkan
        if not cleaned_size:
            return None
            
        return cleaned_size
    except Exception as e:
        logger.error(f"Error cleaning size {size}: {str(e)}")
        return None

def clean_gender(gender: Union[str, None]) -> Optional[str]:
    """
    Membersihkan gender
    
    Args:
        gender (str): Gender dalam format string
        
    Returns:
        str: Gender yang sudah dibersihkan
    """
    try:
        if not isinstance(gender, str):
            logger.error(f"Error cleaning gender: invalid type {type(gender)}")
            return None
            
        if pd.isna(gender) or gender == "Gender Not Available":
            return None
        
        # hapus prefix "Gender: " dan whitespace
        cleaned_gender = gender.replace('Gender:', '').strip()
        
        # jika gender kosong setelah dibersihkan
        if not cleaned_gender:
            return None
            
        return cleaned_gender
    except Exception as e:
        logger.error(f"Error cleaning gender {gender}: {str(e)}")
        return None

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformasi data dari DataFrame mentah ke DataFrame yang sudah dibersihkan
    
    Args:
        df (pd.DataFrame): DataFrame mentah dari proses ekstraksi
        
    Returns:
        pd.DataFrame: DataFrame yang sudah dibersihkan
    """
    try:
        logger.info(f"Starting transformation of DataFrame with shape {df.shape}")
        
        # pastikan data tidak kosong
        if df.empty:
            raise ValueError("cannot transform empty dataframe")
            
        # lowercase column names untuk konsistensi
        df.columns = [col.lower() for col in df.columns]
        logger.info(f"columns after normalization: {list(df.columns)}")
        
        # buat salinan dataframe
        df_clean = df.copy()
        
        # bersihkan semua kolom
        logger.info("cleaning title column")
        df_clean['title'] = df_clean['title'].apply(clean_title)
        
        logger.info("cleaning price column")
        df_clean['price'] = df_clean['price'].apply(clean_price)
        
        logger.info("cleaning rating column")
        df_clean['rating'] = df_clean['rating'].apply(clean_rating)
        
        logger.info("cleaning colors column")
        df_clean['colors'] = df_clean['colors'].apply(clean_colors)
        
        logger.info("cleaning size column")
        df_clean['size'] = df_clean['size'].apply(clean_size)
        
        logger.info("cleaning gender column")
        df_clean['gender'] = df_clean['gender'].apply(clean_gender)
        
        # hapus baris dengan nilai null
        before_dropna = len(df_clean)
        df_clean = df_clean.dropna()
        logger.info(f"removed {before_dropna - len(df_clean)} rows with null values")
        
        # hapus duplikat
        before_drop_duplicates = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        logger.info(f"removed {before_drop_duplicates - len(df_clean)} duplicate rows")
        
        logger.info(f"transformation complete. final dataframe shape: {df_clean.shape}")
        
        # verifikasi bahwa DataFrame tidak kosong
        if df_clean.empty:
            raise ValueError("transformation resulted in empty dataframe! check data quality.")
        
        return df_clean
    except Exception as e:
        logger.error(f"error transforming data: {str(e)}")
        raise