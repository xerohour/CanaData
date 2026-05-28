import responses
from CanaData import CanaData

@responses.activate
def test_high_concurrency_race_conditions():
    """Test race conditions when many threads process menus concurrently."""
    cana = CanaData(interactive_mode=False)

    total_locations = 50
    locations = [{'slug': f'loc-{i}', 'type': 'dispensary', 'id': i} for i in range(total_locations)]

    # Mock legacy API endpoint
    for loc in locations:
        responses.add(
            responses.GET,
            f"https://weedmaps.com/api/web/v1/listings/{loc['slug']}/menu?type={loc['type']}",
            json={
                "listing": {"id": loc['id'], "slug": loc['slug'], "wmid": f"wm-{loc['id']}"},
                "categories": [
                    {
                        "title": "Flower",
                        "items": [
                            {"id": f"item-{loc['id']}-1", "name": "Item 1", "strain_data": {"slug": f"strain-{loc['id']}"}},
                            {"id": f"item-{loc['id']}-2", "name": "Item 2"}
                        ]
                    }
                ]
            },
            status=200
        )

    cana.locations = locations
    cana._getMenusConcurrent()

    assert len(cana.allMenuItems) == total_locations
    assert len(cana.totalLocations) == total_locations
    assert cana.menuItemsFound == total_locations * 2
    assert len(cana.extractedStrains) == total_locations

@responses.activate
def test_failure_modes_and_timeouts():
    """Simulate 429 Too Many Requests and 500 Internal Server Errors during concurrent scraping."""
    cana = CanaData(interactive_mode=False, max_workers=5, rate_limit=0.0)

    total_locations = 20
    locations = [{'slug': f'loc-{i}', 'type': 'dispensary', 'id': i} for i in range(total_locations)]

    # Mix of 200, 429, and 500
    for i, loc in enumerate(locations):
        if i % 3 == 0:
            status = 429
        elif i % 3 == 1:
            status = 500
        else:
            status = 200

        responses.add(
            responses.GET,
            f"https://weedmaps.com/api/web/v1/listings/{loc['slug']}/menu?type={loc['type']}",
            json={"listing": {"id": loc['id'], "slug": loc['slug']}, "categories": []} if status == 200 else {"error": "failed"},
            status=status
        )

    cana.locations = locations
    cana._getMenusConcurrent()

    # Roughly 1/3 of the locations should succeed
    expected_success = len([i for i in range(total_locations) if i % 3 == 2])
    assert len(cana.totalLocations) == expected_success
