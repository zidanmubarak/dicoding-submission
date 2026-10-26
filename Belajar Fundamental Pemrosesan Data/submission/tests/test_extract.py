import pytest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_page, scrape_all_pages
import pandas as pd
import requests

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.text = """
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">T-shirt 2</h3>
            <div class="price-container">
                <span class="price">$102.15</span>
            </div>
            <p>Rating: ⭐ 3.9 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Women</p>
        </div>
    </div>
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">Hoodie 3</h3>
            <div class="price-container">
                <span class="price">$496.88</span>
            </div>
            <p>Rating: ⭐ 4.8 / 5</p>
            <p>3 Colors</p>
            <p>Size: L</p>
            <p>Gender: Unisex</p>
        </div>
    </div>
    """
    mock.status_code = 200
    return mock

def test_scrape_page_success(mock_response):
    with patch('requests.get', return_value=mock_response):
        result = scrape_page(1)
        assert len(result) == 2
        assert result[0]['title'] == 'T-shirt 2'
        assert result[0]['price'] == '$102.15'
        assert result[0]['rating'] == 'Rating: ⭐ 3.9 / 5'
        assert result[0]['colors'] == '3 Colors'
        assert result[0]['size'] == 'Size: M'
        assert result[0]['gender'] == 'Gender: Women'

def test_scrape_page_error():
    with patch('requests.get', side_effect=Exception("Connection error")):
        with pytest.raises(Exception):
            scrape_page(1)

def test_scrape_page_http_error():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP 500")
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.HTTPError):
            scrape_page(1)

def test_scrape_page_general_error():
    with patch('requests.get', side_effect=Exception("General error")):
        with pytest.raises(Exception):
            scrape_page(1)

def test_scrape_page_parse_error():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <div class="price-container">
                <span class="price">$10.00</span>
            </div>
            <p>Invalid Rating</p>
        </div>
    </div>
    """
    
    with patch('requests.get', return_value=mock_response):
        result = scrape_page(1)
        assert len(result) == 1
        assert result[0]['title'] == 'Test Product'
        assert result[0]['price'] == '$10.00'
        assert result[0]['rating'] == 'Invalid Rating'

def test_scrape_all_pages():
    with patch('utils.extract.scrape_page') as mock_scrape:
        mock_scrape.return_value = [
            {
                'title': 'Test Product',
                'price': '$10.99',
                'rating': '4.5/5',
                'colors': '3 Colors',
                'size': 'Size: M',
                'gender': 'Gender: Male',
                'timestamp': '2024-01-01 00:00:00'
            }
        ]
        
        result = scrape_all_pages()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 50  # Karena kita scrape 50 halaman
        assert 'title' in result.columns
        assert 'price' in result.columns
        assert 'rating' in result.columns
        assert 'colors' in result.columns
        assert 'size' in result.columns
        assert 'gender' in result.columns
        assert 'timestamp' in result.columns

def test_scrape_all_pages_consecutive_empty():
    with patch('utils.extract.scrape_page') as mock_scrape:
        # Simulasi 3 halaman kosong berturut-turut
        mock_scrape.side_effect = [[], [], []]
        result = scrape_all_pages()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

def test_scrape_all_pages_with_error():
    with patch('utils.extract.scrape_page') as mock_scrape:
        # Simulasi error pada halaman kedua
        mock_scrape.side_effect = [
            [{'title': 'Test', 'price': '$10', 'rating': '4.5/5', 'colors': '2 Colors', 'size': 'M', 'gender': 'Men'}],
            Exception("Test error"),
            []
        ]
        result = scrape_all_pages()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

def test_scrape_page_empty_product_details():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <div class="collection-card">
        <div class="wrong-class">
            <h3>Invalid Product</h3>
        </div>
    </div>
    """
    
    with patch('requests.get', return_value=mock_response):
        result = scrape_page(1)
        assert len(result) == 0 