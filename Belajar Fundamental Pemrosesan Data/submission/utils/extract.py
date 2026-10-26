import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
import time
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def scrape_page(page_number: int = 1) -> List[Dict]:
    """
    Scrape data dari satu halaman website Fashion Studio
    """
    try:
        # URL: format pagination yang benar
        if page_number == 1:
            url = "https://fashion-studio.dicoding.dev/"
        else:
            url = f"https://fashion-studio.dicoding.dev/page{page_number}"
        
        products = []
        html_content = None
        
        try:
            logger.info(f"Trying URL: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                html_content = response.text
                logger.info(f"Successfully accessed: {url}")
            else:
                logger.warning(f"Failed to access {url}: HTTP {response.status_code}")
                error = requests.HTTPError(f"HTTP {response.status_code}")
                error.response = response
                raise error
        except requests.HTTPError as e:
            logger.error(f"HTTP error accessing {url}: {str(e)}")
            raise  # lempar kembali exception
        except Exception as e:
            logger.error(f"Error accessing {url}: {str(e)}")
            raise  # lempar kembali exception
        
        # parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # cari semua produk cards
        product_cards = soup.find_all('div', class_='collection-card')
        logger.info(f"Found {len(product_cards)} product cards on page {page_number}")
        
        # ekstrak data dari setiap card
        for card in product_cards:
            try:
                # cari product details
                product_details = card.find('div', class_='product-details')
                if not product_details:
                    logger.warning("Product details not found in card")
                    continue
                
                # title
                title_tag = product_details.find('h3', class_='product-title')
                title = title_tag.text.strip() if title_tag else "Unknown Product"
                
                # price
                price_container = product_details.find('div', class_='price-container')
                price_tag = price_container.find('span', class_='price') if price_container else None
                price = price_tag.text.strip() if price_tag else "Price Unavailable"
                
                # cari semua p tag untuk data lainnya
                p_tags = product_details.find_all('p')
                
                # inisialisasi default values
                rating = "Invalid Rating"
                colors = "Colors Not Available"
                size = "Size Not Available"
                gender = "Gender Not Available"
                
                # parse data dari p tags
                for p in p_tags:
                    text = p.text.strip()
                    if 'Rating:' in text:
                        rating = text  # ambil seluruh teks rating
                    elif 'Color' in text:
                        colors = text
                    elif 'Size:' in text:
                        size = text  # ambil seluruh teks size
                    elif 'Gender:' in text:
                        gender = text  # ambil seluruh teks gender
                
                # tambahkan produk ke list
                product = {
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'colors': colors,
                    'size': size,
                    'gender': gender,
                    'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                }
                
                products.append(product)
                logger.debug(f"Extracted product: {title}")
                
            except Exception as e:
                logger.error(f"Error parsing product: {str(e)}")
                continue
        
        logger.info(f"Successfully extracted {len(products)} products from page {page_number}")
        return products
        
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Page {page_number} not found (404). This may be the end of pagination")
            return []
        else:
            logger.error(f"HTTP error scraping page {page_number}: {str(e)}")
            raise
    except Exception as e:
        logger.error(f"Error scraping page {page_number}: {str(e)}")
        raise

def scrape_all_pages() -> pd.DataFrame:
    """
    Scrape data dari semua halaman website Fashion Studio
    """
    all_products = []
    max_pages = 50
    
    for page in range(1, max_pages + 1):
        logger.info(f"Scraping page {page} of {max_pages}")
        
        try:
            products = scrape_page(page)
            
            if not products:
                logger.info(f"No products found on page {page}, checking next pages")
                empty_count = 1
                
                while empty_count < 3 and page + empty_count <= max_pages:
                    logger.info(f"Checking page {page + empty_count}")
                    next_products = scrape_page(page + empty_count)
                    
                    if next_products:
                        logger.info(f"Found products on page {page + empty_count}, continuing")
                        all_products.extend(next_products)
                        page = page + empty_count - 1
                        empty_count = 0
                        break
                    
                    empty_count += 1
                
                if empty_count >= 3:
                    logger.info(f"Three consecutive empty pages, ending pagination at page {page}")
                    break
            else:
                all_products.extend(products)
            
            # Delay untuk menghindari overloading server
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error on page {page}: {str(e)}")
            continue
    
    logger.info(f"Total products collected: {len(all_products)}")
    return pd.DataFrame(all_products)

# Untuk testing modul secara independen
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     df = scrape_all_pages()
#     print(f"Extracted {len(df)} products")
#     print(df.head())
#     df.to_csv("test_extract.csv", index=False)