import pytest
import pandas as pd
from utils.transform import (
    clean_title,
    clean_price,
    clean_rating,
    clean_colors,
    clean_size,
    clean_gender,
    transform_data
)
from unittest.mock import patch

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        'title': ['Unknown Product', 'T-shirt 2', 'Hoodie 3', 'Pants 4'],
        'price': ['$100.00', '$102.15', '$496.88', '$467.31'],
        'rating': ['Rating: ⭐ Invalid Rating / 5', 'Rating: ⭐ 3.9 / 5', 'Rating: ⭐ 4.8 / 5', 'Rating: ⭐ 3.3 / 5'],
        'colors': ['5 Colors', '3 Colors', '3 Colors', '3 Colors'],
        'size': ['Size: M', 'Size: M', 'Size: L', 'Size: XL'],
        'gender': ['Gender: Men', 'Gender: Women', 'Gender: Unisex', 'Gender: Men'],
        'timestamp': ['2025-05-01T15:29:28.537885'] * 4
    })

@pytest.fixture
def sample_transformed_data():
    return pd.DataFrame({
        'title': ['T-shirt 2', 'Hoodie 3', 'Pants 4'],
        'price': [1634400.0, 7950080.0, 7476960.0],
        'rating': [3.9, 4.8, 3.3],
        'colors': [3, 3, 3],
        'size': ['M', 'L', 'XL'],
        'gender': ['Women', 'Unisex', 'Men'],
        'timestamp': ['2025-05-01T15:06:56.241342'] * 3
    })

def test_clean_title():
    assert clean_title('T-shirt 2') == 'T-shirt 2'
    assert clean_title('Unknown Product') is None
    assert clean_title(None) is None
    assert clean_title('') is None
    assert clean_title('   ') is None

def test_clean_price():
    assert clean_price('$100.00') == 1600000.00
    assert clean_price('$102.15') == 1634400.00
    assert clean_price('Price Unavailable') is None
    assert clean_price(None) is None
    assert clean_price('Invalid Price') is None

def test_clean_rating():
    assert clean_rating('Rating: ⭐ 3.9 / 5') == 3.9
    assert clean_rating('Rating: ⭐ 4.8 / 5') == 4.8
    assert clean_rating('Rating: ⭐ Invalid Rating / 5') is None
    assert clean_rating('Not Rated') is None
    assert clean_rating(None) is None

def test_clean_colors():
    assert clean_colors('3 Colors') == 3
    assert clean_colors('5 Colors') == 5
    assert clean_colors('Colors Not Available') is None
    assert clean_colors(None) is None
    assert clean_colors('Invalid Colors') is None

def test_clean_size():
    assert clean_size('Size: M') == 'M'
    assert clean_size('Size: L') == 'L'
    assert clean_size('Size: XL') == 'XL'
    assert clean_size('Size Not Available') is None
    assert clean_size(None) is None

def test_clean_gender():
    assert clean_gender('Gender: Men') == 'Men'
    assert clean_gender('Gender: Women') == 'Women'
    assert clean_gender('Gender: Unisex') == 'Unisex'
    assert clean_gender('Gender Not Available') is None
    assert clean_gender(None) is None

def test_clean_title_invalid_type():
    with patch('logging.Logger.error') as mock_logger:
        result = clean_title(123)  # Non-string input
        assert result is None
        mock_logger.assert_called_once()

def test_clean_price_invalid_type():
    with patch('logging.Logger.error') as mock_logger:
        result = clean_price(123)  # Non-string input
        assert result is None
        mock_logger.assert_called_once()

def test_clean_rating_invalid_type():
    with patch('logging.Logger.error') as mock_logger:
        result = clean_rating(123)  # Non-string input
        assert result is None
        mock_logger.assert_called_once()

def test_clean_colors_invalid_type():
    with patch('logging.Logger.error') as mock_logger:
        result = clean_colors(123)  # Non-string input
        assert result is None
        mock_logger.assert_called_once()

def test_clean_size_invalid_type():
    with patch('logging.Logger.error') as mock_logger:
        result = clean_size(123)  # Non-string input
        assert result is None
        mock_logger.assert_called_once()

def test_clean_gender_invalid_type():
    with patch('logging.Logger.error') as mock_logger:
        result = clean_gender(123)  # Non-string input
        assert result is None
        mock_logger.assert_called_once()

def test_clean_price_invalid_format():
    with patch('logging.Logger.warning') as mock_logger:
        result = clean_price("Invalid Price")
        assert result is None
        mock_logger.assert_called_once()

def test_clean_rating_invalid_format():
    result = clean_rating("Invalid Rating")
    assert result is None

def test_clean_colors_invalid_format():
    with patch('logging.Logger.warning') as mock_logger:
        result = clean_colors("Invalid Colors")
        assert result is None
        mock_logger.assert_called_once()

def test_transform_data(sample_raw_data, sample_transformed_data):
    result = transform_data(sample_raw_data)
    
    # test shape
    assert len(result) == len(sample_transformed_data)
    
    # test data types
    assert result['price'].dtype == 'float64'
    assert result['rating'].dtype == 'float64'
    assert result['colors'].dtype == 'int64'
    assert result['size'].dtype == 'object'
    assert result['gender'].dtype == 'object'
    
    # Test values
    pd.testing.assert_series_equal(result['title'].reset_index(drop=True), 
                                 sample_transformed_data['title'].reset_index(drop=True))
    pd.testing.assert_series_equal(result['price'].reset_index(drop=True), 
                                 sample_transformed_data['price'].reset_index(drop=True))
    pd.testing.assert_series_equal(result['rating'].reset_index(drop=True), 
                                 sample_transformed_data['rating'].reset_index(drop=True))
    pd.testing.assert_series_equal(result['colors'].reset_index(drop=True), 
                                 sample_transformed_data['colors'].reset_index(drop=True))
    pd.testing.assert_series_equal(result['size'].reset_index(drop=True), 
                                 sample_transformed_data['size'].reset_index(drop=True))
    pd.testing.assert_series_equal(result['gender'].reset_index(drop=True), 
                                 sample_transformed_data['gender'].reset_index(drop=True))

def test_transform_data_empty():
    with pytest.raises(ValueError):
        transform_data(pd.DataFrame())

def test_transform_data_empty_result():
    df = pd.DataFrame({
        'title': ['Unknown Product'],
        'price': ['Invalid Price'],
        'rating': ['Invalid Rating'],
        'colors': ['Invalid Colors'],
        'size': ['Invalid Size'],
        'gender': ['Invalid Gender'],
        'timestamp': ['2024-01-01']
    })
    
    with pytest.raises(ValueError):
        transform_data(df)

def test_transform_data_error():
    with patch('logging.Logger.error') as mock_logger:
        with pytest.raises(ValueError):
            transform_data(pd.DataFrame())

def test_transform_data_missing_columns():
    df = pd.DataFrame({
        'title': ['Test Product'],
        'price': ['$10.00']
    })
    
    with pytest.raises(KeyError):
        transform_data(df)

def test_transform_data_all_invalid():
    df = pd.DataFrame({
        'title': ['Unknown Product'],
        'price': ['Invalid Price'],
        'rating': ['Invalid Rating'],
        'colors': ['Invalid Colors'],
        'size': ['Size Not Available'],
        'gender': ['Gender Not Available'],
        'timestamp': ['2024-01-01']
    })
    
    with pytest.raises(ValueError):
        transform_data(df) 