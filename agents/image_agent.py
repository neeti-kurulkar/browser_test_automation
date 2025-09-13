from .base_agent import make_base_agent

def get_image_agent(url: str):
    task = f"""
You are a QA agent testing an ecommerce product page for images.

Steps:
1. Verify all images on the page load successfully.
2. Check primary product images, gallery images, category images, brand logos, promotional banners.
3. Validate alt text for accessibility.
4. Check image dimensions.
5. Detect broken images (404 errors).
6. Trigger lazy-loaded images by scrolling and waiting.
7. Always output results in structured JSON format with keys: 
   "category", "success", "partial", "details"

Details should include:
- all visible images with src, alt, width/height
- any broken or missing images
- partial success if some images cannot be extracted

Target URL: {url}
"""
    return make_base_agent(task)
