<h1 align="center">🚀 <a href="https://github.com/ronknight/static-brand-html-generator">Static Brand HTML Generator</a></h1>

<h4 align="center">🔧 A Python-powered static site generator that organizes brand data and presents it in a structured HTML format.</h4>

<p align="center">
  <a href="https://twitter.com/PinoyITSolution"><img src="https://img.shields.io/twitter/follow/PinoyITSolution?style=social"></a>
  <a href="https://github.com/ronknight?tab=followers"><img src="https://img.shields.io/github/followers/ronknight?style=social"></a>
  <a href="https://github.com/ronknight/static-brand-html-generator/stargazers"><img src="https://img.shields.io/github/stars/BEPb/BEPb.svg?logo=github"></a>
  <a href="https://github.com/ronknight/static-brand-html-generator/network/members"><img src="https://img.shields.io/github/forks/BEPb/BEPb.svg?color=blue&logo=github"></a>
  <a href="https://youtube.com/@PinoyITSolution"><img src="https://img.shields.io/youtube/channel/subscribers/UCeoETAlg3skyMcQPqr97omg"></a>
  <a href="https://github.com/ronknight/static-brand-html-generator/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
  <a href="https://github.com/ronknight/static-brand-html-generator/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <a href="https://github.com/ronknight"><img src="https://img.shields.io/badge/Made%20with%20%F0%9F%A4%8D%20by%20-%20Ronknight%20-%20red"></a>
</p>

## 📌 Overview
The **Static Brand HTML Generator** is a Python-based tool that creates brand listing pages using data from CSV files and statistics. It categorizes brands alphabetically and by popularity, generating corresponding HTML files with logos and styling.

## 📂 Project Structure
```
static-brand-html-generator/
├── .env                      # Environment variables configuration
├── generate-brands.py        # Script to generate brands.html
├── generate_popular_new.py   # Script to generate popular.html
├── generate_popular_css.py   # Script to generate CSS for popular brands
├── brands.html              # Generated alphabetical list of brands
├── popular.html             # Generated list of popular brands
├── popular.css             # Generated CSS styles for popular brands
└── README.md               # Project documentation
```

## 🔧 Environment Variables
The `.env` file should contain:
```
DATA_FILE=path/to/brandlist.csv
STATISTICS_FILE=path/to/statistics.tsv
SKIP_BRANDS=brand1,brand2,brand3
```

## 📊 Data Structure
The data files should contain:

**BrandList CSV:**
- BrandName: Brand name
- URL: Brand URL
- Popular-Rating: Priority rating (1-n)
- Active: Status (TRUE/FALSE)
- LogoName: Logo filename
- Image_URL: Base URL for logos

**Statistics TSV:**
- Name: Brand name
- ItemCount: Number of items
- TotalQtyOnHand: Total inventory quantity

## 🚀 Features
- 📌 **Smart Brand Sorting**: Combines popularity ratings with inventory data
- 🎯 **Priority System**: Uses Popular-Rating to determine brand display order
- 📊 **Inventory Integration**: Considers TotalQtyOnHand for brand relevance
- 🖼️ **Logo Management**: Supports both local and remote logo URLs
- 🎨 **Dynamic CSS**: Generates brand-specific styling

## 🔧 Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/ronknight/static-brand-html-generator.git
   cd static-brand-html-generator
   ```
2. Create and configure `.env` file
3. Install dependencies:
   ```sh
   pip install python-dotenv
   ```

## 📌 Usage
Run the scripts in order:
```sh
python generate-brands.py
python generate_popular_new.py
python generate_popular_css.py
```

## 🔍 Brand Selection Logic
1. Brands with Popular-Rating are sorted first (ascending order)
2. Remaining brands are sorted by TotalQtyOnHand (descending)
3. Minimum inventory threshold of 100 items required
4. Limited to top 50 brands total

## ⚠️ Disclaimer
This project processes proprietary brand data. Ensure proper data handling and privacy compliance.

## 📜 License
MIT License - see [LICENSE](LICENSE)

---
<h4 align="center">💡 Made with ❤️ by <a href="https://github.com/ronknight">Ron Knight</a></h4>

