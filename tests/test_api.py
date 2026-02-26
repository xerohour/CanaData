import pytest
import responses
from cana_data import CanaData
from CannMenusClient import CannMenusClient
from LeaflyScraper import scrape_leafly
import json

@pytest.fixture
def cana():
    return CanaData()

@responses.activate
def test_get_brands_success(cana):
    mock_url = "https://api-g.weedmaps.com/discovery/v1/brands?offset=0&page_size=100&size=100"
    mock_response = {
        "meta": {"total_brands": 1},
        "data": {
            "brands": [{"id": 1, "name": "Test Brand", "slug": "test-brand"}]
        }
    }
    responses.add(responses.GET, mock_url, json=mock_response, status=200)
    
    cana.getBrands()
    assert len(cana.brands) == 1
    assert cana.brands[0]['name'] == 'Test Brand'
    assert cana.brandsFound == 1

@responses.activate
def test_get_strains_success(cana):
    mock_url = "https://api-g.weedmaps.com/discovery/v1/strains?offset=0&page_size=100&size=100"
    mock_response = {
        "meta": {"total_strains": 1},
        "data": {
            "strains": [{"id": 101, "name": "Blue Dream", "slug": "blue-dream"}]
        }
    }
    responses.add(responses.GET, mock_url, json=mock_response, status=200)
    
    cana.getStrains()
    assert len(cana.strains) == 1
    assert cana.strains[0]['name'] == 'Blue Dream'
    assert cana.strainsFound == 1

@responses.activate
def test_cannmenus_get_retailers(monkeypatch):
    monkeypatch.setenv('CANNMENUS_API_TOKEN', 'dummy-token')
    client = CannMenusClient()
    mock_url = "https://api.cannmenus.com/v1/retailers?state=NY"
    mock_response = {
        "data": [{"id": "shop-1", "name": "NYC Dispensary"}]
    }
    responses.add(responses.GET, mock_url, json=mock_response, status=200)
    
    retailers = client.get_retailers("NY")
    assert len(retailers) == 1
    assert retailers[0]['name'] == "NYC Dispensary"

@responses.activate
def test_cannmenus_get_menu(monkeypatch):
    monkeypatch.setenv('CANNMENUS_API_TOKEN', 'dummy-token')
    client = CannMenusClient()
    mock_url = "https://api.cannmenus.com/v1/retailers/shop-1/menu"
    mock_response = {
        "data": [{"name": "Item 1", "price": 50}]
    }
    responses.add(responses.GET, mock_url, json=mock_response, status=200)
    
    menu = client.get_menu("shop-1")
    assert len(menu) == 1
    assert menu[0]['name'] == "Item 1"

def test_extract_strains_from_menu(cana):
    # Mock menu response with strain data
    mock_item = {
        "name": "OG Kush",
        "strain_data": {
            "slug": "og-kush",
            "name": "OG Kush",
            "genetics": "hybrid"
        },
        "id": 101,
        "price": {"amount": 50, "currency": "USD"}
    }
    
    # We need to construct a menu dict that mimics the API response
    # process_menu_json expects keys like 'listing' and 'categories'
    mock_menu_json = {
        "listing": {"id": 1, "slug": "test-dispensary", "wmid": 123},
        "categories": [
            {
                "title": "Flower",
                "items": [mock_item]
            }
        ]
    }
    
    # Process the mock menu
    cana.process_menu_json(mock_menu_json)
    
    # Verify extraction
    assert "og-kush" in cana.extractedStrains
    assert cana.extractedStrains["og-kush"]["genetics"] == "hybrid"
