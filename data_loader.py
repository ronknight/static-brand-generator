import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Brand:
    def __init__(self, data: Dict):
        self.brand_name: str = data['brandName']
        self.url: str = data['url']
        self.popular_rating: Optional[int] = data.get('popularRating')
        self.logo_name: Optional[str] = data.get('logoName')
        self.image_url: Optional[str] = data.get('imageUrl')
        self.item_count: int = data['itemCount']
        self.total_qty_on_hand: int = data['totalQtyOnHand']
    
    @property
    def is_active(self) -> bool:
        return self.total_qty_on_hand >= 100
    
    @property
    def full_logo_url(self) -> Optional[str]:
        if not self.logo_name:
            return None
        if self.logo_name.startswith('http'):
            return self.logo_name
        return f"{self.image_url}{self.logo_name}" if self.image_url else None
    
    def build_url(self, brand_slug: str) -> str:
        base_url = self.url
        if "utm_source=" in base_url:
            return base_url
        return f"{base_url}&utm_source=webjaguar&utm_medium=website&utm_campaign=brands-page&utm_content={brand_slug}-link"

class BrandCatalog:
    def __init__(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.brands: List[Brand] = [Brand(b) for b in data['brands']]
        self.metadata = data['metadata']
        self.skip_brands = set(brand.lower() for brand in self.metadata['skipBrands'])
    
    def get_active_brands(self) -> List[Brand]:
        """Returns brands that are active (TotalQtyOnHand >= 100)"""
        return [brand for brand in self.brands 
                if brand.is_active and brand.brand_name.lower() not in self.skip_brands]
    
    def get_popular_brands(self, limit: int = 50) -> List[Brand]:
        """Returns top brands sorted by popular rating and quantity"""
        active_brands = self.get_active_brands()
        
        # Separate rated and non-rated brands
        rated = [(b, b.popular_rating) for b in active_brands if b.popular_rating]
        non_rated = [b for b in active_brands if not b.popular_rating]
        
        # Sort rated brands by rating, non-rated by quantity
        sorted_rated = sorted(rated, key=lambda x: x[1])
        sorted_non_rated = sorted(non_rated, key=lambda x: x.total_qty_on_hand, reverse=True)
        
        # Combine lists
        result = [b[0] for b in sorted_rated] + sorted_non_rated
        return result[:limit]

def convert_csv_to_json(data_file: str, stats_file: str, output_file: str):
    """Converts existing CSV/TSV files to the new JSON format"""
    import csv
    
    # Read statistics data
    statistics = {}
    with open(stats_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            statistics[row['Name']] = {
                'itemCount': row['ItemCount'],
                'totalQtyOnHand': int(row['TotalQtyOnHand'].replace(',', ''))
            }
    
    # Read brand data and combine with statistics
    brands = []
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand_name = row['BrandName']
            if brand_name in statistics:
                brand = {
                    "brandName": brand_name,
                    "url": row['URL'],
                    "popularRating": int(row['Popular-Rating']) if row.get('Popular-Rating') else None,
                    "logoName": row.get('LogoName', '').strip() or None,
                    "imageUrl": row.get('Image_URL', '').strip() or None,
                    "itemCount": statistics[brand_name]['itemCount'],
                    "totalQtyOnHand": statistics[brand_name]['totalQtyOnHand']
                }
                brands.append(brand)
    
    # Create JSON structure
    data = {
        "brands": brands,
        "metadata": {
            "lastUpdated": datetime.now().isoformat(),
            "totalBrands": len(brands),
            "skipBrands": os.getenv('SKIP_BRANDS', '').split(',')
        }
    }
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Example usage to convert existing files
    if os.getenv('DATA_FILE') and os.getenv('STATISTICS_FILE'):
        convert_csv_to_json(
            os.getenv('DATA_FILE'),
            os.getenv('STATISTICS_FILE'),
            'brands_data.json'
        )