from .base_agent import make_base_agent

def get_image_agent(url: str):
    task = f"""
You are a QA agent testing an ecommerce product page for image quality.

Your task is to verify that all visible images load correctly, have proper dimensions, and contain accessibility attributes (alt text).

⚠️ OUTPUT REQUIREMENTS:
- Return only a single valid JSON object.
- No explanations, markdown, or text outside JSON.
- Follow the exact schema below.
- If some images are missing or broken, set "partial": true and list them in "issues".

JSON schema:
{{
  "category": "Image Validation",
  "success": true | false,
  "partial": true | false,
  "details": {{
    "images": [
      {{
        "src": "string (image URL)",
        "alt": "string or empty",
        "width": number | null,
        "height": number | null,
        "status": "ok | broken | missing alt"
      }}
    ],
    "issues": ["list of strings describing missing/broken images"]
  }}
}}

✅ Example 1: all images valid
{{
  "category": "Image Validation",
  "success": true,
  "partial": false,
  "details": {{
    "images": [
      {{"src": "https://example.com/img1.jpg", "alt": "Front view", "width": 800, "height": 800, "status": "ok"}},
      {{"src": "https://example.com/img2.jpg", "alt": "Side view", "width": 800, "height": 800, "status": "ok"}}
    ],
    "issues": []
  }}
}}

✅ Example 2: missing alt text and broken image
{{
  "category": "Image Validation",
  "success": false,
  "partial": true,
  "details": {{
    "images": [
      {{"src": "https://example.com/img1.jpg", "alt": "", "width": 800, "height": 800, "status": "missing alt"}},
      {{"src": "https://example.com/img2.jpg", "alt": "Side view", "width": null, "height": null, "status": "broken"}}
    ],
    "issues": ["Image img1.jpg missing alt text", "Image img2.jpg failed to load"]
  }}
}}

Additional instructions:
- Scroll and wait for lazy-loaded images.
- Capture dimensions for all visible images.
- Include all images: primary, gallery, banners, logos.
- Mark missing/broken images in "issues" and set partial=true if any problems occur.

Target URL: {url}
"""
    return make_base_agent(task)
