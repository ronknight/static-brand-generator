import csv
import re
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def load_data(data_file, stats_file):
    with open(data_file, 'r') as f:
        data = list(csv.DictReader(f))
    with open(stats_file, 'r') as f:
        stats = list(csv.DictReader(f, delimiter='\t'))
    return data, stats

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower())

def build_url(url, brand_slug):
    return f"{url}?brand={brand_slug}"

def generate_brands_html(data, stats):
    statistics_data = {row['Name']: row for row in stats}
    letter_groups = {chr(i): [] for i in range(65, 91)}
    letter_groups['#'] = []

    for row in data:
        brand_name = row['BrandName']
        if brand_name in statistics_data:
            row['Number_of_Items'] = statistics_data[brand_name]['ItemCount']
            total_qty_on_hand = statistics_data[brand_name]['TotalQtyOnHand'].replace(',', '')
            if int(float(total_qty_on_hand)) >= 100:
                row['Active'] = str(int(float(total_qty_on_hand) > 0))
                first_letter = brand_name[0].upper()
                if first_letter.isalpha():
                    letter_groups[first_letter].append(row)
                else:
                    letter_groups['#'].append(row)

    html = ['<div class="container"><div class="row" id="masonry-grid">']
    letters = sorted(letter_groups.keys())
    if '#' in letters:
        letters.remove('#')
        letters.insert(0, '#')

    for letter in letters:
        html.append(f'<div class="col-xs-12 col-sm-6 col-md-3 masonry-item" id="{letter}"><h4>{letter}</h4><div class="items-container">')
        brands_in_group = sorted(letter_groups[letter], key=lambda x: x['BrandName'])
        for brand in brands_in_group:
            brand_slug = slugify(brand['BrandName'])
            final_url = build_url(brand['URL'], brand_slug)
            class_attr = f'item {brand_slug}' if brand.get('Popular-Rating') else 'item'
            html.append(f'<a href="{final_url}" class="{class_attr}">{brand["BrandName"]}</a>')
        html.append('</div></div>')

    html.append('</div></div>')
    with open('brands.html', 'w') as f:
        f.write('\n'.join(html))

def generate_popular_html(data, stats):
    statistics_data = {row['Name']: row for row in stats}
    rated_brands = [(row['BrandName'], statistics_data[row['BrandName']]) for row in data if row['Popular-Rating'] and row['BrandName'] in statistics_data and 'Popular-Rating' in statistics_data[row['BrandName']]]
    non_rated_brands = [(row['BrandName'], statistics_data[row['BrandName']]) for row in data if not row['Popular-Rating'] and row['BrandName'] in statistics_data]
    sorted_brands = sorted(rated_brands, key=lambda x: int(x[1]['Popular-Rating']))
    sorted_brands += [(brand_name, brand_data) for brand_name, brand_data in non_rated_brands if int(float(brand_data['TotalQtyOnHand'].replace(',', ''))) >= 100]
    sorted_brands = sorted_brands[:50]
    html = ['<div class="popular-characters">']
    for brand_name, brand_data in sorted_brands:
        logo = brand_data.get('LogoName', '').strip()
        brand_slug = slugify(brand_name)
        final_url = build_url(brand_data['URL'], brand_slug)
        if logo:
            logo_url = f"{brand_data['Image_URL'].strip()}{logo}" if not logo.startswith("http") else logo
            html.append(f'<a href="{final_url}"><img src="{logo_url}" alt="Wholesale {brand_name}" class="brand-logo"><p class="brand-name">{brand_name}</p></a>')
        else:
            html.append(f'<a href="{final_url}"><span class="tag {brand_slug}">{brand_name}</span></a>')
    html.append('</div>')
    with open('popular.html', 'w') as f:
        f.write('\n'.join(html))

def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def generate_css():
    try:
        with open("popular.html", "r") as f:
            popular_html = f.read()
    except FileNotFoundError:
        print("Error: popular.html not found.")
        return

    try:
        with open("base.html", "r") as f:
            base_html = f.read()
    except FileNotFoundError:
        print("Error: base.html not found.")
        return

    popular_brands_spans = set(re.findall(r'<span class="tag ([^"]+)">.*?</span>', popular_html))
    popular_brands_images = set(re.findall(r'<p class="brand-name">(.*?)</p>', popular_html))
    popular_brands = popular_brands_spans.union(popular_brands_images)

    css_rules = ""
    for brand in popular_brands:
        color = "#ff0000"  # Placeholder for actual color logic
        text_color = "#000000" if int(color[1:], 16) > 0x888888 else "#FFFFFF"
        background = hex_to_rgba(color, 0.2)
        css_rules += f"""
.tag.{brand} {{
  background-color: {color};
  color: {text_color};
  font-weight: bold;
}}

.item.{brand} {{
  border-left: 4px solid {color} !important;
  background: {background} !important;
  color: #000 !important;
  font-weight: bold !important;
}}
"""

    try:
        with open("popular.css", "w") as f:
            f.write(f"""/* popular.css */

.popular-brands-tag {{
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}}

.popular-brands-item {{
  margin-bottom: 5px;
}}

{css_rules}""")
        print("popular.css generated successfully.")
    except Exception as e:
        print(f"Error writing to popular.css: {e}")

    dynamic_css_start = "<!-- Dynamic CSS Start -->"
    dynamic_css_end = "<!-- Dynamic CSS End -->"

    if dynamic_css_start in base_html and dynamic_css_end in base_html:
        new_css_block = f"{dynamic_css_start}\n<style>\n{css_rules}\n</style>\n{dynamic_css_end}"
        updated_base_html = re.sub(
            f"{re.escape(dynamic_css_start)}.*?{re.escape(dynamic_css_end)}",
            new_css_block,
            base_html,
            flags=re.DOTALL
        )
        try:
            with open("base.html", "w") as f:
                f.write(updated_base_html)
            print("base.html updated with dynamic CSS.")
        except Exception as e:
            print(f"Error updating base.html: {e}")
    else:
        print("Dynamic CSS placeholders not found in base.html. Please add them.")

def finalize_sort():
    brands_file = "brands.html"
    if not os.path.exists(brands_file):
        print(f"Error: {brands_file} not found.")
        return

    with open(brands_file, "r", encoding="utf-8") as f:
        content = f.read()

    # For each items-container block, find all brand links and sort by visible text
    container_pattern = r'(<div class="items-container">)(.*?)(</div>)'
    blocks = re.findall(container_pattern, content, flags=re.DOTALL)

    for container_open, container_content, container_close in blocks:
        link_pattern = r'(<a[^>]+class="[^"]*item[^"]*"[^>]*>)(.*?)(</a>)'
        matches = re.findall(link_pattern, container_content, flags=re.DOTALL)

        sorted_matches = sorted(matches, key=lambda x: x[1].strip().lower())
        sorted_container = "".join(f"{m[0]}{m[1]}{m[2]}" for m in sorted_matches)

        new_block = f"{container_open}{sorted_container}{container_close}"
        content = content.replace(
            f"{container_open}{container_content}{container_close}",
            new_block,
            1
        )

    with open(brands_file, "w", encoding="utf-8") as f:
        f.write(content)

def run_scripts():
    # Ensure required environment variables are set
    required_vars = [
        'DATA_FILE',
        'STATISTICS_FILE',
        'SKIP_BRANDS',
        'BASE_URL',
        'CDN_URL',
        'IMAGE_URL',
        'DOMAIN_NAME'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return

    # Run scripts in order
    scripts = [
        'generate-brands.py',
        'generate_popular_new.py',
        'generate_popular_css.py'
    ]
    
    for script in scripts:
        print(f"Running {script}...")
        subprocess.run(['python', script], check=True)
        print(f"Finished {script}")

if __name__ == "__main__":
    run_scripts()
    finalize_sort()