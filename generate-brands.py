import csv
import re
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

def slugify(text):
    # Convert to lowercase and replace special chars with hyphens
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def get_first_letter(brand):
    # Get first letter, handle numbers/special cases
    first = brand[0].upper()
    return '#' if first.isdigit() or not first.isalpha() else first

def build_url(url, brand_slug):
    if "utm_source=" in url:
        return url
    else:
        return f"{url}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link"


def generate_brands_html():
    # Group brands by first letter
    letter_groups = defaultdict(list)

    # Read statistics data
    statistics_data = {}
    with open(os.getenv('STATISTICS_FILE'), 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            try:
                statistics_data[row['Name']] = {
                    'ItemCount': row['ItemCount'],
                    'TotalQtyOnHand': row['TotalQtyOnHand']
                }
            except KeyError as e:
                print(f"Error reading statistics data: {e}")
                print(f"Row contents: {row}")
    
    with open(os.getenv('DATA_FILE'), 'r') as f:
        reader = csv.DictReader(f)
        skip_brands = [brand.strip().lower() for brand in os.getenv('SKIP_BRANDS').split(',')]
        for row in reader:
            brand_name = row['BrandName']
            if brand_name.lower() in skip_brands:
                continue

            if row['Active'].upper() == 'TRUE':
                # Update Active and TotalQtyOnHand from statistics data
                if brand_name in statistics_data:
                    row['Number_of_Items'] = statistics_data[brand_name]['ItemCount']
                    total_qty_on_hand = statistics_data[brand_name]['TotalQtyOnHand'].replace(',', '')
                    if int(float(total_qty_on_hand)) >= 100:
                        row['Active'] = str(int(float(total_qty_on_hand) > 0))  # Convert to "0" or "1" string
                        first_letter = get_first_letter(brand_name)
                        letter_groups[first_letter].append(row)
    
    html = ['''<div class="container">
    <!-- Masonry Grid -->
    <div class="row" id="masonry-grid">''']
    
    letters = sorted(letter_groups.keys())
    if '#' in letters:
        letters.remove('#')
        letters.insert(0, '#')
        
    for letter in letters:
        # Match exact format from base copy.html
        html.append(f'''        <!-- Example Card -->
        <div class="col-xs-12 col-sm-6 col-md-3 masonry-item" id="{letter}">
            <h4>{letter}</h4>
            <div class="items-container">''')
        
        brands_in_group = sorted(letter_groups[letter], key=lambda x: x['BrandName'])
        for brand in brands_in_group:
            brand_slug = slugify(brand['BrandName'])
            final_url = build_url(brand['URL'], brand_slug)
            class_attr = f'item {brand_slug}' if brand.get('Popular-Rating') else 'item'
            
            html.append(f'''                <a href="{final_url}"
                    class="{class_attr}">{brand['BrandName']}</a>''')
        
        html.append('''            </div>
        </div>''')
    
    html.append('''    </div>
</div>''')
    
    with open('brands.html', 'w') as f:
        f.write('\n'.join(html))

generate_brands_html()