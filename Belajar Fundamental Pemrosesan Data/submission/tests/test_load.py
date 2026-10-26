import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import (
    save_to_csv,
    save_to_google_sheets,
    save_to_postgresql,
    load_data
)

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'title': ['T-shirt 2', 'Hoodie 3', 'Pants 4'],
        'price': [1634400.0, 7950080.0, 7476960.0],
        'rating': [3.9, 4.8, 3.3],
        'colors': [3, 3, 3],
        'size': ['M', 'L', 'XL'],
        'gender': ['Women', 'Unisex', 'Men'],
        'timestamp': ['2025-05-01T15:06:56.241342'] * 3
    })

def test_save_to_csv(sample_data, tmp_path):
    file_path = tmp_path / "test.csv"
    result = save_to_csv(sample_data, str(file_path))
    assert isinstance(result, str)
    assert file_path.exists()
    
    # baca file untuk verifikasi
    df = pd.read_csv(file_path)
    assert len(df) == 3
    assert list(df.columns) == ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
    assert df['title'].tolist() == ['T-shirt 2', 'Hoodie 3', 'Pants 4']

def test_save_to_csv_empty_dataframe():
    with pytest.raises(IOError) as excinfo:
        save_to_csv(pd.DataFrame(), "test.csv")
    assert "empty dataframe cannot be saved to csv" in str(excinfo.value)

@patch('google.oauth2.service_account.Credentials.from_service_account_file')
@patch('googleapiclient.discovery.build')
def test_save_to_google_sheets(mock_build, mock_credentials, sample_data):
    # setup mock untuk service
    mock_service = MagicMock()
    mock_spreadsheets = MagicMock()
    mock_values = MagicMock()
    mock_update = MagicMock()

    # setup chain pemanggilan
    mock_service.spreadsheets.return_value = mock_spreadsheets
    mock_spreadsheets.values.return_value = mock_values
    mock_values.update.return_value = mock_update

    # setup mock untuk execute
    mock_update.execute.return_value = {
        'spreadsheetId': '1D0ZMfA7PIVfRjpNpkJyuXN...',
        'updatedRange': 'Sheet1!A1:G4',
        'updatedRows': len(sample_data) + 1,
        'updatedColumns': len(sample_data.columns),
        'updatedCells': (len(sample_data) + 1) * len(sample_data.columns)
    }

    # test fungsi dengan service yang sudah dimock
    result = save_to_google_sheets(
        sample_data,
        '1D0ZMfA7PIVfRjpNpkJyuXN...',
        'google-sheets-api.json',
        _service=mock_service  # berikan mock service langsung
    )

    # assertions
    assert result is True
    mock_values.update.assert_called_once()
    
    # verifikasi parameter yang dikirim ke update
    call_args = mock_values.update.call_args[1]
    assert call_args['spreadsheetId'] == '1D0ZMfA7PIVfRjpNpkJyuXN...'
    assert call_args['range'] == 'Sheet1!A1'
    assert call_args['valueInputOption'] == 'RAW'
    assert 'values' in call_args['body']
    assert len(call_args['body']['values']) == len(sample_data) + 1  # header + data rows

def test_save_to_google_sheets_empty_dataframe():
    result = save_to_google_sheets(pd.DataFrame(), 'test_id', 'test.json')
    assert result is False

def test_save_to_google_sheets_credential_error():
    with patch('os.path.exists', return_value=True), \
         patch('google.oauth2.service_account.Credentials.from_service_account_file', 
               side_effect=Exception("Credential error")):
        result = save_to_google_sheets(sample_data, 'test_id', 'test.json')
        assert result is False

def test_save_to_google_sheets_service_error():
    with patch('os.path.exists', return_value=True), \
         patch('google.oauth2.service_account.Credentials.from_service_account_file', return_value=MagicMock()), \
         patch('googleapiclient.discovery.build', side_effect=Exception("Service error")):
        result = save_to_google_sheets(sample_data, 'test_id', 'test.json')
        assert result is False

def test_save_to_google_sheets_update_error():
    mock_service = MagicMock()
    mock_spreadsheets = MagicMock()
    mock_values = MagicMock()
    mock_update = MagicMock()
    
    mock_service.spreadsheets.return_value = mock_spreadsheets
    mock_spreadsheets.values.return_value = mock_values
    mock_values.update.return_value = mock_update
    mock_update.execute.side_effect = Exception("Update error")
    
    result = save_to_google_sheets(sample_data, 'test_id', 'test.json', _service=mock_service)
    assert result is False

@patch('utils.load.create_engine')  # Perubahan di sini
def test_save_to_postgresql(mock_engine, sample_data):
    # Setup mock engine dan connection
    mock_conn = MagicMock()
    mock_engine_instance = MagicMock()
    mock_engine.return_value = mock_engine_instance
    mock_engine_instance.connect.return_value = mock_conn
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None
    
    # Mock DataFrame.to_sql
    with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
        result = save_to_postgresql(
            sample_data,
            'postgresql+psycopg2://developer:lupa@localhost:5432/companydb',
            'product'
        )
        
        assert result is True
        mock_engine.assert_called_once_with(
            'postgresql+psycopg2://developer:lupa@localhost:5432/companydb'
        )
        mock_to_sql.assert_called_once()

def test_save_to_postgresql_empty_dataframe():
    result = save_to_postgresql(pd.DataFrame(), 'test_connection', 'test_table')
    assert result is False

def test_save_to_postgresql_connection_error():
    with patch('utils.load.create_engine', side_effect=Exception("Connection error")):
        result = save_to_postgresql(sample_data, 'invalid_connection', 'test_table')
        assert result is False

def test_save_to_postgresql_write_error():
    with patch('utils.load.create_engine') as mock_engine:
        mock_engine.return_value = MagicMock()
        with patch.object(pd.DataFrame, 'to_sql', side_effect=Exception("Write error")):
            result = save_to_postgresql(sample_data, 'test_connection', 'test_table')
            assert result is False

def test_load_data(sample_data, tmp_path):
    # Setup config
    csv_file = str(tmp_path / "test.csv")
    google_sheets_config = {
        'spreadsheet_id': '1D0ZMfA7PIVfRjpNpkJyuXN...',
        'credentials_file': 'google-sheets-api.json'
    }
    postgresql_config = {
        'connection_string': 'postgresql+psycopg2://developer:lupa@localhost:5432/companydb',
        'table_name': 'product'
    }
    
    # Mock external dependencies
    with patch('utils.load.save_to_google_sheets', return_value=True), \
         patch('utils.load.save_to_postgresql', return_value=True):
        
        results = load_data(
            sample_data,
            csv_file=csv_file,
            google_sheets_config=google_sheets_config,
            postgresql_config=postgresql_config
        )
        
        assert isinstance(results, dict)
        assert isinstance(results['csv'], str)
        assert results['google_sheets'] == f"https://docs.google.com/spreadsheets/d/{google_sheets_config['spreadsheet_id']}/edit"
        assert results['postgresql'] is True

def test_load_data_empty_dataframe():
    with pytest.raises(Exception):
        load_data(pd.DataFrame())

def test_load_data_all_failures():
    with patch('utils.load.save_to_csv', side_effect=Exception("CSV error")), \
         patch('utils.load.save_to_google_sheets', return_value=False), \
         patch('utils.load.save_to_postgresql', return_value=False):
        
        with pytest.raises(Exception):
            load_data(
                sample_data,
                csv_file="test.csv",
                google_sheets_config={'spreadsheet_id': 'test', 'credentials_file': 'test.json'},
                postgresql_config={'connection_string': 'test', 'table_name': 'test'}
            )

def test_save_to_google_sheets_missing_credentials():
    with patch('os.path.exists', return_value=False):
        result = save_to_google_sheets(sample_data, 'test_id', 'test.json')
        assert result is False

def test_save_to_google_sheets_service_build_error():
    with patch('os.path.exists', return_value=True), \
         patch('google.oauth2.service_account.Credentials.from_service_account_file', return_value=MagicMock()), \
         patch('googleapiclient.discovery.build', side_effect=Exception("Service build error")):
        result = save_to_google_sheets(sample_data, 'test_id', 'test.json')
        assert result is False

def test_save_to_postgresql_engine_error():
    with patch('utils.load.create_engine') as mock_engine:
        mock_engine.side_effect = Exception("Engine error")
        result = save_to_postgresql(sample_data, 'test_connection', 'test_table')
        assert result is False

def test_load_data_partial_success():
    with patch('utils.load.save_to_csv', return_value="test.csv"), \
         patch('utils.load.save_to_google_sheets', return_value=True), \
         patch('utils.load.save_to_postgresql', side_effect=Exception("PostgreSQL error")):
        
        results = load_data(
            sample_data,
            csv_file="test.csv",
            google_sheets_config={'spreadsheet_id': 'test', 'credentials_file': 'test.json'},
            postgresql_config={'connection_string': 'test', 'table_name': 'test'}
        )
        
        assert results['csv'] == "test.csv"
        assert results['google_sheets'] == "https://docs.google.com/spreadsheets/d/test/edit"
        assert results['postgresql'] is False 