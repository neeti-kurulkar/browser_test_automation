# Ecommerce QA Automation with Browser-Use

## Overview

This project is a browser-based QA automation system for ecommerce stores. It uses agentic QA models to validate product pages, images, and errors, generating a structured JSON report for analysis.

### Key Capabilities

- **Product Page QA**: Check product title, price, description, add-to-cart button, variants, and SEO metadata
- **Image QA**: Validate all images (primary, gallery, category, banners) including lazy-loaded images and alt text
- **Error Detection QA**: Detect JavaScript errors, network issues, resource loading failures, and other visible page errors

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repo_url>
cd browser_test_automation
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note**: The project uses Browser-Use for browser automation. Please ensure you have the correct Python version and dependencies installed.

## Running the QA Agents

```bash
python main.py --url <base_store_url> --products <product_paths> --timeout 180 --out report.json
```

### Arguments

- `--url`: Base URL of the ecommerce store (required)
- `--products`: List of product paths relative to the base URL (e.g., `/products/demo-product`)
- `--timeout`: Maximum time (seconds) per agent (default: 180)
- `--out`: Output file path for the report (default: `report.json`)

### Example

```bash
python main.py --url https://shella-demo.myshopify.com/ --products products/blend-field-jacket --timeout 180 --out report.json
```

## Output

The tool generates a structured JSON report like:

```json
{
  "summary": {
    "total_tests": 3,
    "passed": 0,
    "failed": 3
  },
  "results": [
    {
      "category": "Product Page Validation",
      "success": false,
      "partial": false,
      "details": { ... }
    }
  ]
}
```

The report captures success/failure, partial completions, and detailed information for each agent.

## Current Working Features

✅ **Product Page QA**: Extracts title, price, description, add-to-cart button, product variants  
✅ **Image QA**: Detects visible images; identifies primary/gallery/other categories  
✅ **Error Detection QA**: Reports visible page errors, missing resources  
✅ **Structured JSON output** via Reporter class  
✅ **Handles multiple products** in one run  

## Known Limitations / Issues

⚠️ **SEO Metadata Detection**: `<title>` and `<meta description>` sometimes not detected due to dynamic rendering  
⚠️ **Image Extraction**: Some images (lazy-loaded, CSS backgrounds, `<picture>` elements) may not be fully captured  
⚠️ **Error Detection**: Cannot fully detect console errors, network failures, or CORS issues that are not visible on the page  
⚠️ **Partial success reporting**: Some results marked as partial when exact extraction is not possible, e.g., alt text or exact image URLs  
⚠️ **Timeouts**: Long product pages or pages with many images may require increased `--timeout`  

## Next Steps / Improvements

- Integrate console/network capture for more accurate error reporting
- Improve lazy-loaded and CSS background image detection
- Refine SEO metadata extraction using JS evaluation
- Better partial vs full success classification in reports