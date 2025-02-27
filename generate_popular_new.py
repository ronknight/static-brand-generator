import csv
import re
import os
from dotenv import load_dotenv

load_dotenv()

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
        with open(os.getenv('STATISTICS_FILE'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            skip_brands = [brand.strip().lower() for brand in os.getenv('SKIP_BRANDS').split(',')]
            for row in reader:
                brand_name = row['Name']
                if brand_name.lower() in skip_brands:
                    continue
                try:
                    statistics_data[row['Name']] = {
                        'ItemCount': row['ItemCount'],
                        'TotalQtyOnHand': int(row['TotalQtyOnHand'].replace(',', ''))  # Convert to integer
                    }
                except KeyError as e:
                    print(f"Error reading statistics data: {e}")
                    print(f"Row contents: {row}")
    except Exception as e:
        print(f"Error opening STATISTICS_FILE: {e}")

    # Sort by TotalQtyOnHand and get top 50
    sorted_statistics = sorted(statistics_data.items(), key=lambda item: item[1]['TotalQtyOnHand'], reverse=True)[:50]
    top_50_brands = {brand_name: {'TotalQtyOnHand': data['TotalQtyOnHand'], 'URL': ''} for brand_name, data in sorted_statistics}

    # Read BrandList data and override with Popular-Rating
    try:
        with open(os.getenv('DATA_FILE'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            skip_brands = [brand.strip().lower() for brand in os.getenv('SKIP_BRANDS').split(',')]
            for row in reader:
                brand_name = row['BrandName']
                if brand_name.lower() in skip_brands:
                    continue

                if row.get('Popular-Rating', '').strip() and row.get('Active', '').upper() == 'TRUE':
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
                            'URL': '',
                            'LogoName': row.get('LogoName', '').strip(),
                            'Image_URL': row.get('Image_URL', '').strip()
                        }
    except KeyError as e:
        print(f"Error reading DATA_FILE: {e}")

    # Separate brands with and without Popular-Rating
    rated_brands = []
    non_rated_brands = []
    for brand_name, brand_data in top_50_brands.items():
        if 'Popular-Rating' in brand_data and brand_data['Popular-Rating'] > 0:  # Add check for positive rating
            rated_brands.append((brand_name, brand_data))
        else:
            non_rated_brands.append((brand_name, brand_data))

    # Sort the rated brands by Popular-Rating (ascending)
    rated_brands = sorted(rated_brands, key=lambda item: item[1]['Popular-Rating'])

    # Sort the non-rated brands by TotalQtyOnHand (descending)  
    non_rated_brands = sorted(non_rated_brands, key=lambda item: item[1]['TotalQtyOnHand'], reverse=True)

    # First add rated brands (if they meet minimum quantity)
    sorted_brands = [(brand_name, brand_data) for brand_name, brand_data in rated_brands if brand_data['TotalQtyOnHand'] >= 100]
    
    # Then add non-rated brands (if they meet minimum quantity)
    sorted_brands += [(brand_name, brand_data) for brand_name, brand_data in non_rated_brands if brand_data['TotalQtyOnHand'] >= 100]

    # Limit to top 50
    sorted_brands = sorted_brands[:50]

    html = ['<div class="popular-characters">']

    for brand_name, brand_data in sorted_brands:
        logo = brand_data.get('LogoName', '').strip()
        brand_slug = slugify(brand_name)
        final_url = build_url(brand_data['URL'], brand_slug)
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

    popular_html = '\n'.join(html)
    # Existing extraction for span-tag based brands
    popular_brands_spans = set(re.findall(r'<span class="tag ([^" ]+)"', popular_html, flags=re.IGNORECASE))
    # New extraction for brands with images: get brand names from <p class="brand-name">
    brand_names = re.findall(r'<p class="brand-name">(.*?)</p>', popular_html, flags=re.IGNORECASE)
    # Convert brand names to slugs using your slugify function
    popular_brands_images = {slugify(name.strip()) for name in brand_names if name.strip() != ""}
    # Combine both sets so all brands are included
    popular_brands = popular_brands_spans.union(popular_brands_images)

    with open('popular.html', 'w') as f:
        f.write(popular_html)

generate_popular_html()
