import json

class Reporter:
    def __init__(self):
        self.results = []

    def add_result(self, category, success, details=None, partial=False):
        """
        Add a single test result.
        partial=True allows marking tests that are partially passed.
        """
        self.results.append({
            "category": category,
            "success": success or partial,
            "partial": partial,
            "details": details
        })

    def merge_agent_results(self, step_results):
        """
        Merge multiple step results (already structured) into reporter.
        """
        self.results.extend(step_results)

    def finalize(self):
        total = len(self.results)
        passed = sum(r["success"] for r in self.results)
        failed = total - passed
        return {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed
            },
            "results": self.results
        }

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.finalize(), f, indent=2)
