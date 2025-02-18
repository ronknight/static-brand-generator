import csv
import re

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def generate_popular_html():
    brands = []
    with open('brand-url-popular-rating.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include brands that have a Popular-Rating and Inv = TRUE
            if row['Popular-Rating'] and row['Inv'].upper() == 'TRUE':
                brands.append(row)
    
    # Sort brands by Popular-Rating (as integer)
    brands.sort(key=lambda x: int(x['Popular-Rating']))
    
    html = ['<div class="popular-characters">']
    
    for brand in brands:
        brand_slug = slugify(brand['BrandName'])
        # Retrieve and trim the LogoName field
        logo = brand.get('LogoName', '').strip()
        if logo != "":
            html.append(f'''    <a href="{brand['URL']}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link">
        <img src="https://www.4sgm.com/assets/Image/Category/{logo}" alt="{brand['BrandName']}" class="brand-logo">
    </a>''')
        else:
            html.append(f'''    <a href="{brand['URL']}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link">
        <span class="tag {brand_slug}">{brand['BrandName']}</span>
    </a>''')
    html.append('</div>')
    
    with open('popular.html', 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

generate_popular_html()