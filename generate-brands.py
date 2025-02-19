import csv
import re
from collections import defaultdict

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

def generate_popular_html():
    # Read and sort brands by Popular-Rating
    popular_brands = []
    with open('BrandList.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include brands with rating AND Active = TRUE
            if row['Popular-Rating'] and row['Active'].upper() == 'TRUE':
                row['Popular-Rating'] = int(row['Popular-Rating'])
                popular_brands.append(row)
    
    # Sort by Popular-Rating
    popular_brands.sort(key=lambda x: x['Popular-Rating'])
    
    # Generate popular.html
    html = ['<div class="popular-characters">']
    
    for brand in popular_brands:
        brand_slug = slugify(brand['BrandName'])
        final_url = build_url(brand['URL'], brand_slug)
        html.append(f'''    <a href="{final_url}">
        <span class="tag {brand_slug}">{brand['BrandName']}</span>
    </a>''')
    
    html.append('</div>')
    
    with open('popular.html', 'w') as f:
        f.write('\n'.join(html))

def generate_brands_html():
    # Group brands by first letter
    letter_groups = defaultdict(list)
    
    with open('BrandList.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Active'].upper() == 'TRUE':
                first_letter = get_first_letter(row['BrandName'])
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