<h1 align="center">🚀 <a href="https://github.com/ronknight/static-brand-html-generator">Static Brand HTML Generator</a></h1>

<h4 align="center">🔧 A Python-powered static site generator for brand catalogs</h4>

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
Generates static HTML pages for brand catalogs with automated sorting and styling.

## 📂 Project Structure
```
static-brand-html-generator/
├── .env                      # Configuration
├── generate-brands.py        # Main generator
├── generate_popular_new.py   # Popular brands generator
├── generate_popular_css.py   # CSS generator
├── brands.html              # Output file
├── popular.html             # Output file
├── popular.css             # Output file
└── README.md               # Documentation
```

## 🔧 Environment Variables
```ini
DATA_FILE=path/to/source.csv
STATISTICS_FILE=path/to/stats.tsv
SKIP_BRANDS=brand1,brand2,brand3
```

## 📊 Data Structure

**Source CSV:**
- BrandName
- URL
- Popular-Rating (1-n)
- Active (TRUE/FALSE)
- LogoName
- Image_URL

**Stats TSV:**
- Name
- ItemCount
- TotalQtyOnHand

## 🚀 Features
- 📌 Smart brand sorting
- 🎯 Priority rating system
- 📊 Inventory integration
- 🖼️ Logo management
- 🎨 Dynamic CSS generation

## 🔧 Installation
```sh
git clone https://github.com/ronknight/static-brand-html-generator.git
cd static-brand-html-generator
pip install python-dotenv
```

## 📌 Usage
```sh
python generate-brands.py
python generate_popular_new.py
python generate_popular_css.py
```

## 🔍 Brand Selection Logic
1. Popular-Rating sorting (ascending)
2. Inventory quantity sorting (descending)
3. Minimum threshold: 100 items
4. Maximum brands: 50

## ⚠️ Disclaimer
Handles proprietary data - follow data protection guidelines.

## 📜 License
MIT License

---
<h4 align="center">💡 Made with ❤️ by <a href="https://github.com/ronknight">Ron Knight</a></h4>
````

