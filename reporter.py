import json

class Reporter:
    def __init__(self):
        self.results = []

    def add_result(self, category, success, details=None, partial=False):
        """
        Add a single test result.
        partial=True marks tests that are partially passed.
        """
        self.results.append({
            "category": category,
            "success": success or partial,
            "partial": partial,
            "details": details
        })

    def merge_agent_results(self, step_results):
        """
        Merge multiple structured step results into the reporter.
        Handles both list and dict inputs.
        """
        if isinstance(step_results, dict):
            self.results.append(step_results)
        elif isinstance(step_results, list):
            self.results.extend(step_results)
        else:
            # fallback: wrap in a dict
            self.results.append({
                "category": "Unknown",
                "success": False,
                "partial": False,
                "details": {"raw": str(step_results)}
            })

    def finalize(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("success"))
        failed = total - passed
        partial = sum(1 for r in self.results if r.get("partial") and not r.get("success"))
        issues_count = sum(len(r.get("details", {}).get("issues", [])) for r in self.results)
        return {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "partial": partial,
                "total_issues": issues_count
            },
            "results": self.results
        }

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.finalize(), f, indent=2)