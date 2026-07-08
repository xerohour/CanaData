from CanaData import CanaData

cana = CanaData()

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

mock_menu_json = {
    "listing": {"id": 1, "slug": "test-dispensary", "wmid": 123},
    "categories": [
        {
            "title": "Flower",
            "items": [mock_item]
        }
    ]
}

cana.process_menu_json(mock_menu_json)

# Now we need to drain the queue for extractedStrains to be populated!
cana._drain_menu_data_queue()
print("Extracted strains after drain:", cana.extractedStrains)
