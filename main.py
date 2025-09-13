import argparse
import asyncio
import json
from reporter import Reporter
from agents.product_agent import get_product_agent
from agents.image_agent import get_image_agent
from agents.error_agent import get_error_agent

def parse_agent_result(agent_history):
    """
    Extract structured output from Browser-Use agent.
    Returns a list suitable for Reporter.merge_agent_results.
    """
    last_step = getattr(agent_history, "last_step", None)
    if not last_step:
        return [{
            "category": "Unknown",
            "success": False,
            "partial": False,
            "details": {"raw": "No steps completed"}
        }]

    output = getattr(last_step, "output", str(last_step))

    # If output is a JSON string, parse it
    if isinstance(output, str):
        try:
            output_data = json.loads(output)
        except json.JSONDecodeError:
            output_data = {"raw": output}
    elif isinstance(output, dict):
        output_data = output
    else:
        output_data = {"raw": str(output)}

    # Handle both dict and list outputs
    if isinstance(output_data, dict):
        return [{
            "category": output_data.get("category", "Unknown"),
            "success": output_data.get("success", False),
            "partial": output_data.get("partial", False),
            "details": output_data.get("details", {"raw": str(output_data)})
        }]
    elif isinstance(output_data, list):
        results = []
        for item in output_data:
            if isinstance(item, dict):
                results.append({
                    "category": item.get("category", "Unknown"),
                    "success": item.get("success", False),
                    "partial": item.get("partial", False),
                    "details": item.get("details", {"raw": str(item)})
                })
            else:
                results.append({
                    "category": "Unknown",
                    "success": False,
                    "partial": False,
                    "details": {"raw": str(item)}
                })
        return results
    else:
        return [{
            "category": "Unknown",
            "success": False,
            "partial": False,
            "details": {"raw": str(output_data)}
        }]


async def run_tests(base_url, products, timeout, out_file):
    reporter = Reporter()

    for product in products or [""]:
        url = f"{base_url}{product}"
        print(f"🔍 Testing {url}...")

        for agent_name, agent_getter, category_name, steps in [
            ("Product Page", get_product_agent, "Product Page Validation", 20),
            ("Image Validation", get_image_agent, "Image Validation", 40),
            ("Error Detection", get_error_agent, "Error Detection", 20)
        ]:
            try:
                agent = agent_getter(url)
                res = await asyncio.wait_for(agent.run_structured(max_steps=steps), timeout=timeout)
                step_results = parse_agent_result(res)
            except asyncio.TimeoutError:
                step_results = [{
                    "category": category_name,
                    "success": False,
                    "partial": False,
                    "details": {"raw": f"{agent_name} timed out"}
                }]
            reporter.merge_agent_results(step_results)

    reporter.save(out_file)
    print(f"✅ Report saved to {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ecommerce Agent CLI")
    parser.add_argument("--url", required=True, help="Base store URL")
    parser.add_argument("--products", nargs="*", help="Product paths (e.g., /products/demo-product)")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout per agent (seconds)")
    parser.add_argument("--out", default="report.json", help="Output JSON file")
    args = parser.parse_args()

    asyncio.run(run_tests(args.url, args.products, args.timeout, args.out))