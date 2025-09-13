from .base_agent import make_base_agent

def get_product_agent(url: str):
    task = f"""
You are a QA agent testing an ecommerce product page.

Your task is to check whether the product page meets certain requirements, including product details, add-to-cart functionality, variants, and SEO metadata.

⚠️ OUTPUT REQUIREMENTS:
- You MUST return only a single valid JSON object.
- No explanations, no markdown, no text outside the JSON.
- Follow the exact schema shown below.
- If some elements are missing, set "partial": true and list them in "issues".
- If all required elements are present, "success": true and "partial": false.

JSON schema:
{{
  "category": "Product Page Validation",
  "success": true | false,
  "partial": true | false,
  "details": {{
    "product_elements": {{
      "title": "string or null",
      "price": "string or null",
      "description": "string or null",
      "add_to_cart": true | false,
      "variants": ["list of variants"] | []
    }},
    "seo_metadata": {{
      "title_tag": "string or null",
      "meta_description": "string or null"
    }},
    "issues": ["list of strings describing missing/broken elements"]
  }}
}}

✅ Example 1: all elements present
{{
  "category": "Product Page Validation",
  "success": true,
  "partial": false,
  "details": {{
    "product_elements": {{
      "title": "Floating Birthstone Locket Necklace",
      "price": "£79.00",
      "description": "A customizable locket with birthstones.",
      "add_to_cart": true,
      "variants": ["Silver", "Gold"]
    }},
    "seo_metadata": {{
      "title_tag": "Floating Birthstone Locket Necklace | Abbott Lyon",
      "meta_description": "Create your personalized locket with birthstones."
    }},
    "issues": []
  }}
}}

✅ Example 2: missing SEO metadata
{{
  "category": "Product Page Validation",
  "success": false,
  "partial": true,
  "details": {{
    "product_elements": {{
      "title": "Floating Birthstone Locket Necklace",
      "price": "£79.00",
      "description": "A customizable locket with birthstones.",
      "add_to_cart": true,
      "variants": ["Silver", "Gold"]
    }},
    "seo_metadata": {{
      "title_tag": null,
      "meta_description": null
    }},
    "issues": ["SEO title tag is missing", "Meta description is missing"]
  }}
}}

Additional instructions:
- Scroll the page and wait for lazy-loaded content if necessary to extract all product elements.
- Extract the page <title> and <meta name='description'> from the <head> section.
- Capture all variants and optional product configurations.
- If any element cannot be extracted, mark as partial and document in "issues".

Target URL: {url}
"""
    return make_base_agent(task)
