import re
import hashlib

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

    # Extract brand names from popular.html
    popular_brands = set(re.findall(r'<span class="tag ([^"]+)">.*?</span>', popular_html))
    
    # Instead of subtracting existing brands, update CSS for all reported brands
    new_brands = popular_brands

    def is_light_color(hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        Y = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        return Y > 128

    def get_brand_color(brand_name):
        if brand_name == "kodak":
            return "#FFD700"  # Yellow
        elif brand_name == "l-a-colors":
            return "#FF69B4"  # Pink
        elif brand_name == "cooking-basics":
            return "#87CEEB"  # Light Blue
        elif brand_name == "sanrio":
            return "#FA8072"  # Salmon
        else:
            hash_object = hashlib.md5(brand_name.encode())
            hex_dig = hash_object.hexdigest()
            color_hex = hex_dig[:6]
            return f"#{color_hex}"

    css_rules = ""
    for brand in new_brands:
        color = get_brand_color(brand)
        text_color = "#000000" if is_light_color(color) else "#FFFFFF"
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

    # Write to popular.css (ensure popular.css is loaded after any static styles)
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

    # --- Update dynamic CSS in base.html ---
    # Expect base.html to contain these placeholder markers:
    # <!-- Dynamic CSS Start -->
    # <!-- Dynamic CSS End -->
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

if __name__ == "__main__":
    generate_css()