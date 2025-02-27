import re
import hashlib

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

    # Extract brand names from popular.html
    popular_brands = set(re.findall(r'<span class="tag ([^"]+)">.*?</span>', popular_html))

    # Extract existing brand names from base.html
    existing_item_brands = set(re.findall(r'\.item\.([a-z0-9-]+)', base_html))
    existing_tag_brands = set(re.findall(r'\.tag\.([a-z0-9-]+)', base_html))
    existing_brands = existing_item_brands.union(existing_tag_brands)

    # Identify new brands
    new_brands = popular_brands - existing_brands

    def is_light_color(hex_color):
        """Determine if a hex color is light or dark."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Calculate relative luminance (Y)
        Y = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        # Use a threshold to determine if the color is light
        return Y > 128

    def get_brand_color(brand_name):
        """Determine brand color based on the brand name."""
        if brand_name == "kodak":
            return "#FFD700"  # Yellow
        elif brand_name == "l-a-colors":
            return "#FF69B4"  # Pink
        elif brand_name == "cooking-basics":
            return "#87CEEB"  # Light Blue
        elif brand_name == "sanrio":
            return "#FA8072"  # Salmon
        else:
            # Use hashlib to generate a consistent color based on the brand name
            hash_object = hashlib.md5(brand_name.encode())
            hex_dig = hash_object.hexdigest()
            # Take the first 6 characters of the hash for the color
            color_hex = hex_dig[:6]
            return f"#{color_hex}"

    # Generate CSS rules
    css_rules = ""
    for brand in new_brands:
        color = get_brand_color(brand)
        text_color = "#000000" if is_light_color(color) else "#FFFFFF"

        css_rules += f"""
.tag.{brand} {{
  background-color: {color};
  color: {text_color};
}}

.item.{brand} {{
  border-left-color: {color};
}}
"""

    # Write CSS rules to popular.css
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

if __name__ == "__main__":
    generate_css()