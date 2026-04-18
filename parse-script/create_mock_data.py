import csv


def create_mock_csv(filename="mock_data.csv"):
    # CanaParse expects about 30 columns check CanaParse.py for indices
    # We will create a list of sufficient length and populate specific indices

    headers = ["col_" + str(i) for i in range(35)]
    # Just setting meaningful headers for the ones we use, though CanaParse
    # might not use headers by name for everything
    headers[1] = "description"
    headers[2] = "name"
    headers[9] = "price_gram"
    headers[10] = "price_2g"
    headers[11] = "price_eighth"
    headers[12] = "price_quarter"
    headers[13] = "price_half_ounce"
    headers[14] = "price_ounce"
    headers[15] = "price_half_gram"
    headers[17] = "image_url"
    headers[20] = "category"
    headers[28] = "slug"
    headers[29] = "dispensary_name"

    rows = []

    # Helper to create a row
    def make_row(
            name,
            category,
            price_map,
            description="Test Description",
            dispensary="Test Dispensary"):
        row = [""] * 35
        row[1] = description
        row[2] = name
        row[17] = "https://via.placeholder.com/150"
        row[20] = category
        row[28] = "test-slug"
        row[29] = dispensary

        # Prices
        row[9] = price_map.get("gram", "")
        row[10] = price_map.get("2g", "")
        row[11] = price_map.get("eighth", "")
        row[12] = price_map.get("quarter", "")
        row[13] = price_map.get("half_ounce", "")
        row[14] = price_map.get("ounce", "")
        row[15] = price_map.get("half_gram", "")

        return row

    # 1. Blue Dream (Flower) - Targeted for Eighths
    rows.append(make_row(
        "Blue Dream",
        "Sativa",
        {"eighth": "35.00", "gram": "10.00"},
        description="Classic Sativa strain. THC: 22% CBD: 0.1%",
        dispensary="Wellness Center"
    ))

    # 2. Vape Cartridge - Targeted for Half Gram
    rows.append(make_row(
        "Gelato Vape Cart",
        "Concentrate",
        {"half_gram": "30.00"},
        description="High potency distillate. good_words: vape pen cart. THC: 88%",
        dispensary="The Vape Shop"
    ))

    # 3. Cheap Wax - Targeted for Concentrates
    rows.append(make_row(
        "Shatter Special",
        "Wax",
        {"gram": "15.00"},
        description="Budget shatter. THC: 75%",
        dispensary="Budget Buds"
    ))

    # 4. Bulk Flower - Targeted for Ounce
    rows.append(make_row(
        "OG Kush",
        "Indica",
        {"ounce": "120.00", "half_ounce": "65.00"},
        description="Heavy hitter. THC: 24%",
        dispensary="Bulk Barn"
    ))

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Created {filename} with {len(rows)} rows.")


if __name__ == "__main__":
    create_mock_csv()
