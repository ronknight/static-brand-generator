import csv
import re

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def build_url(url, brand_slug):
    if "utm_source=" in url:
        return url
    else:
        return f"{url}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link"

def generate_popular_html():
    brands = []
    with open('BrandList.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include brands that have a Popular-Rating and are Active
            if row['Popular-Rating'] and row['Active'].upper() == 'TRUE':
                brands.append(row)
    
    brands.sort(key=lambda x: int(x['Popular-Rating']))
    html = ['<div class="popular-characters">']
    
    for brand in brands:
        brand_slug = slugify(brand['BrandName'])
        final_url = build_url(brand['URL'], brand_slug)
        logo = brand.get('LogoName', '').strip()
        # Debug output:
        print(f"DEBUG: {brand['BrandName']} logo: '{logo}'")
        if logo:
            if logo.startswith("http"):
                logo_url = logo
            else:
                logo_url = f"https://www.4sgm.com/assets/Image/Category/{logo}"
            html.append(f'''    <a href="{final_url}">
    <img src="{logo_url}" alt="Wholesale {brand['BrandName']}" class="brand-logo">
</a>''')
        else:
            html.append(f'''    <a href="{final_url}">
    <span class="tag {brand_slug}">{brand['BrandName']}</span>
</a>''')
    html.append('</div>')
    
    with open('popular.html', 'w') as f:
        f.write('\n'.join(html))

generate_popular_html()