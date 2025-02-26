import csv
import re
import os
from dotenv import load_dotenv

load_dotenv()
print(f"DATA_FILE: {os.getenv('DATA_FILE')}")
print(f"STATISTICS_FILE: {os.getenv('STATISTICS_FILE')}")

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def build_url(url, brand_slug):
    if "utm_source=" in url:
        return url
    else:
        return f"{url}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link"

def generate_popular_html():
    # Read statistics data and get top 50 by TotalQtyOnHand
    statistics_data = {}
    try:
        with open("c:/Users/rona/PycharmProjects/static-brand-html-generator/Brands-Statistics-2025-02-25-16-54-04.csv", 'r', encoding='utf-8') as f:
            try:
                reader = csv.DictReader(f, delimiter=os.getenv('DELIMITER'))
                for row in reader:
                    try:
                        statistics_data[row['Name']] = {
                            'ItemCount': row['ItemCount'],
                            'TotalQtyOnHand': int(row['TotalQtyOnHand'].replace(',', ''))  # Convert to integer
                        }
                        print(f"Read row: {row['Name']}, TotalQtyOnHand={row['TotalQtyOnHand']}")
                    except KeyError as e:
                        print(f"Error reading statistics data: {e}")
                        print(f"Row contents: {row}")
            except Exception as e:
                print(f"Error creating csv.DictReader: {e}")
    except Exception as e:
        print(f"Error opening STATISTICS_FILE: {e}")

    # Sort by TotalQtyOnHand and get top 50
    sorted_statistics = sorted(statistics_data.items(), key=lambda item: item[1]['TotalQtyOnHand'], reverse=True)[:50]
    top_50_brands = {brand_name: {'TotalQtyOnHand': data['TotalQtyOnHand']} for brand_name, data in sorted_statistics}

    # Read BrandList data and override with Popular-Rating
    print("About to read DATA_FILE")
    try:
        with open(os.getenv('DATA_FILE'), 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                brand_name = row['BrandName']
                if row.get('Popular-Rating', '').strip() and row.get('Active', '').upper() == 'TRUE':
                    # If brand is in top 50 or has a Popular-Rating, add/update it
                    if brand_name in top_50_brands:
                        top_50_brands[brand_name].update({
                            'Popular-Rating': int(row['Popular-Rating']),
                            'URL': row['URL'],
                            'LogoName': row.get('LogoName', '').strip(),
                            'Image_URL': row.get('Image_URL', '').strip()
                        })
                    else:
                        # Add brand with Popular-Rating
                        top_50_brands[brand_name] = {
                            'TotalQtyOnHand': 0,  # Default value
                            'Popular-Rating': int(row['Popular-Rating']),
                            'URL': row['URL'],
                            'LogoName': row.get('LogoName', '').strip(),
                            'Image_URL': row.get('Image_URL', '').strip()
                        }
    except KeyError as e:
        print(f"Error reading DATA_FILE: {e}")

    print(f"Number of brands from STATISTICS_FILE: {len(statistics_data)}")
    print(f"Top 50 brands by TotalQtyOnHand: {list(top_50_brands.keys())}")

    # Sort top_50_brands by Popular-Rating (descending) then TotalQtyOnHand (descending)
    sorted_brands = sorted(top_50_brands.items(),
                             key=lambda item: (item[1].get('Popular-Rating', 0) * -1, item[1]['TotalQtyOnHand']),
                             reverse=True)

    print(f"Number of brands from DATA_FILE: {len(top_50_brands)}")
    print("Brands with Popular-Rating:")
    for brand_name, brand_data in top_50_brands.items():
        if 'Popular-Rating' in brand_data:
            print(f"  {brand_name}: Popular-Rating={brand_data['Popular-Rating']}, TotalQtyOnHand={brand_data['TotalQtyOnHand']}")

    sorted_brands = sorted_brands[:50]

    print("Final sorted brands:")
    for brand_name, brand_data in sorted_brands:
        print(f"  {brand_name}: Popular-Rating={brand_data.get('Popular-Rating', 0)}, TotalQtyOnHand={brand_data['TotalQtyOnHand']}")

    html = ['<div class="popular-characters">']

    for brand_name, brand_data in sorted_brands:
        brand_slug = slugify(brand_name)
        final_url = build_url(brand_data['URL'], brand_slug)
        logo = brand_data.get('LogoName', '').strip()
        if logo:
            if logo.startswith("http"):
                logo_url = logo
            else:
                image_url = brand_data.get('Image_URL', '').strip()
                logo_url = f"{image_url}{logo}"
            html.append(f'''    <a href="{final_url}">
    <img src="{logo_url}" alt="Wholesale {brand_name}" class="brand-logo">
        <p class="brand-name">{brand_name}</p>
</a>''')
        else:
            html.append(f'''    <a href="{final_url}">
    <span class="tag {brand_slug}">{brand_name}</span>
</a>''')
    html.append('</div>')

    with open('popular.html', 'w') as f:
        f.write('\n'.join(html))