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

def generate_popular_html():
    # Read and sort brands by Popular-Rating
    popular_brands = []
    with open('brand-url-popular-rating.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include brands with rating AND Inv = TRUE
            if row['Popular-Rating'] and row['Inv'].upper() == 'TRUE':
                row['Popular-Rating'] = int(row['Popular-Rating'])
                popular_brands.append(row)
    
    # Sort by Popular-Rating
    popular_brands.sort(key=lambda x: x['Popular-Rating'])
    
    # Generate popular.html
    html = ['<div class="popular-characters">']
    
    for brand in popular_brands:
        brand_slug = slugify(brand['BrandName'])
        html.append(f'''    <a href="{brand['URL']}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link">
        <span class="tag {brand_slug}">{brand['BrandName']}</span>
    </a>''')
    
    html.append('</div>')
    
    with open('popular.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

def generate_brands_html():
    # Group brands by first letter
    letter_groups = defaultdict(list)
    
    with open('brand-url-popular-rating.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Inv'].upper() == 'TRUE':
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
            class_attr = f'item {brand_slug}' if brand.get('Popular-Rating') else 'item'
            
            html.append(f'''                <a href="{brand['URL']}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link"
                    class="{class_attr}">{brand['BrandName']}</a>''')
        
        html.append('''            </div>
        </div>''')
    
    html.append('''    </div>
</div>''')
    
    with open('brands.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

# Generate both files
generate_popular_html()
generate_brands_html()