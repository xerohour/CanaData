import sys
from unittest.mock import patch, MagicMock, mock_open
import pytest
import CanaData
from CanaData import main

@pytest.fixture
def mock_cana_data():
    with patch('CanaData.CanaData') as MockCana:
        yield MockCana.return_value

@patch('builtins.input', return_value='test-slug')
def test_main_interactive_mode(mock_input, mock_cana_data):
    # Patch CanaData.argv
    with patch('CanaData.argv', ['CanaData.py']):
        main()

        # Verify user input was requested
        mock_input.assert_called()

        # Verify CanaData methods were called
        mock_cana_data.setCitySlug.assert_called_with('test-slug')
        mock_cana_data.getLocations.assert_called()
        mock_cana_data.getMenus.assert_called()
        mock_cana_data.dataToCSV.assert_called()
        mock_cana_data.resetDataSets.assert_called()
        mock_cana_data.identifyNaughtyStates.assert_called()

def test_main_quick_run(mock_cana_data):
    with patch('CanaData.argv', ['CanaData.py', '-go', 'quick-slug']):
        main()

        # Verify proper flow
        mock_cana_data.setCitySlug.assert_called_with('quick-slug')
        mock_cana_data.getLocations.assert_called()
        mock_cana_data.getMenus.assert_called()

def test_main_all_states(mock_cana_data):
    # Mock states.txt reading
    mock_file = mock_open(read_data="state1\nstate2")

    # We need to mock open specifically within CanaData logic
    # But since main uses open directly, we can patch builtins.open
    # However, main also reads other files, so we should be careful.
    # The current implementation reads states.txt, slugs.txt, mylist.txt at the start of main.

    # Let's create a side_effect for open to handle different files
    def open_side_effect(file, *args, **kwargs):
        if 'states.txt' in str(file):
            return mock_open(read_data="state1\nstate2").return_value
        return mock_open(read_data="").return_value

    with patch('builtins.open', side_effect=open_side_effect):
        with patch('CanaData.argv', ['CanaData.py', '-go', 'all']):
            main()

            # Should be called for each state
            assert mock_cana_data.setCitySlug.call_count == 2
            mock_cana_data.setCitySlug.assert_any_call('state1')
            mock_cana_data.setCitySlug.assert_any_call('state2')

def test_main_metadata_only(mock_cana_data):
    with patch('CanaData.argv', ['CanaData.py', '-brands']):
        main()

        mock_cana_data.getBrands.assert_called()
        mock_cana_data.setCitySlug.assert_called_with('global')
        mock_cana_data.dataToCSV.assert_called()

def test_main_brands_and_scrape(mock_cana_data):
    with patch('CanaData.argv', ['CanaData.py', '-brands', '-go', 'test']):
        main()

        mock_cana_data.getBrands.assert_called()
        mock_cana_data.setCitySlug.assert_any_call('test')
        mock_cana_data.getLocations.assert_called()
