from .base_agent import make_base_agent

def get_error_agent(url: str):
    task = f"""
You are a QA agent detecting errors on an ecommerce page.

Steps:
1. Capture JavaScript console errors and uncaught exceptions.
2. Capture network failures (4xx, 5xx).
3. Detect resource loading failures (CSS, JS, images).
4. Identify CORS errors.
5. Report third-party script failures (analytics, payments).
6. Check for performance warnings and security issues.
7. Always output results in structured JSON format with keys: 
   "category", "success", "partial", "details"

Details should include:
- all detected errors with type, code, message
- partial success if some errors could not be checked

Target URL: {url}
"""
    return make_base_agent(task)
