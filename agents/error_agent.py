from .base_agent import make_base_agent

def get_error_agent(url: str):
    task = f"""
You are a QA agent detecting runtime errors on an ecommerce page.

Your task is to capture all errors including console exceptions, network failures, resource load issues, CORS issues, performance warnings, and security warnings.

⚠️ OUTPUT REQUIREMENTS:
- Return only a single valid JSON object.
- No explanations, markdown, or text outside JSON.
- Follow the exact schema below.
- If some errors are detected but not all checks can be performed, set "partial": true.

JSON schema:
{{
  "category": "Error Detection",
  "success": true | false,
  "partial": true | false,
  "details": {{
    "errors": [
      {{
        "type": "console | network | resource | CORS | performance | security",
        "code": "string or null",
        "message": "string"
      }}
    ],
    "issues": ["list of error summaries"]
  }}
}}

✅ Example 1: page has no errors
{{
  "category": "Error Detection",
  "success": true,
  "partial": false,
  "details": {{
    "errors": [],
    "issues": []
  }}
}}

✅ Example 2: runtime errors detected
{{
  "category": "Error Detection",
  "success": false,
  "partial": true,
  "details": {{
    "errors": [
      {{"type": "network", "code": "404", "message": "GET /favicon.ico not found"}},
      {{"type": "console", "code": null, "message": "Uncaught TypeError: Cannot read property 'x' of undefined"}}
    ],
    "issues": ["Missing favicon", "JavaScript runtime error on product page"]
  }}
}}

Additional instructions:
- Wait and observe for dynamically loaded content that might trigger errors.
- Capture all network and console errors.
- Include partial=true if any checks could not be completed.
- Ensure JSON strictly matches the schema above.

Target URL: {url}
"""
    return make_base_agent(task)
