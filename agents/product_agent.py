from .base_agent import make_base_agent

def get_product_agent(url: str):
    task = f"""
You are a QA agent testing an ecommerce product page.

Steps:
1. Navigate to the target URL.
2. Confirm the page loads within the timeout.
3. Validate presence of:
   - Product title
   - Product price
   - Product description
   - Add-to-cart button
   - Product variants (if any)
4. Check page title & meta description exist.
5. Report missing or broken elements clearly.
6. Always output results in structured JSON format with keys: 
   "category", "success", "partial", "details"

Details should include:
- product_elements with all extracted info
- SEO metadata status
- any issues or missing elements

Target URL: {url}
"""
    return make_base_agent(task)
