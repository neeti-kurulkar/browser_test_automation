import argparse
import asyncio
import json
from reporter import Reporter
from agents.product_agent import get_product_agent
from agents.image_agent import get_image_agent
from agents.error_agent import get_error_agent


def parse_agent_result(agent_history):
    """
    Extract structured output from a Browser-Use agent run.
    Normalizes agent output into a consistent schema so that Reporter can merge results.
    Handles cases where output may be a string, dict, list of dicts, or invalid JSON.
    """

    # Get the last step from the agent run
    last_step = getattr(agent_history, "last_step", None)
    if not last_step:
        # No steps completed → mark as failure
        return [{
            "category": "Unknown",
            "success": False,
            "partial": False,
            "details": {"raw": "No steps completed"}
        }]

    # Try to extract structured output
    output = getattr(last_step, "output", str(last_step))

    # Case 1: output is a JSON string → parse it
    if isinstance(output, str):
        try:
            output_data = json.loads(output)
        except json.JSONDecodeError:
            output_data = {"raw": output}

    # Case 2: already a dict
    elif isinstance(output, dict):
        output_data = output

    # Case 3: fallback → just stringify whatever we got
    else:
        output_data = {"raw": str(output)}

    # Normalize to a list of results
    if isinstance(output_data, dict):
        # Wrap a single dict into a standard schema
        return [{
            "category": output_data.get("category", "Unknown"),
            "success": output_data.get("success", False),
            "partial": output_data.get("partial", False),
            "details": output_data.get("details", {"raw": str(output_data)})
        }]

    elif isinstance(output_data, list):
        # If the agent returned multiple dicts, normalize each
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
                # Unexpected type → treat as raw output
                results.append({
                    "category": "Unknown",
                    "success": False,
                    "partial": False,
                    "details": {"raw": str(item)}
                })
        return results

    # Default fallback
    else:
        return [{
            "category": "Unknown",
            "success": False,
            "partial": False,
            "details": {"raw": str(output_data)}
        }]


async def run_tests(base_url, products, timeout, out_file):
    """
    Main test runner.
    Iterates over all products and agents, collects results, and saves a final report.
    """

    reporter = Reporter()  # Consolidates results across all agents/products

    # If no products given, run on the base URL
    for product in products or [""]:
        url = f"{base_url}{product}"
        print(f"🔍 Testing {url}...")

        # Run each agent with its settings
        for agent_name, agent_getter, category_name, steps in [
            ("Product Page", get_product_agent, "Product Page Validation", 20),
            ("Image Validation", get_image_agent, "Image Validation", 40),
            ("Error Detection", get_error_agent, "Error Detection", 20)
        ]:
            try:
                # Build agent
                agent = agent_getter(url)

                # Run agent with step limit + timeout
                res = await asyncio.wait_for(
                    agent.run_structured(max_steps=steps),
                    timeout=timeout
                )

                # Normalize agent output
                step_results = parse_agent_result(res)

            except asyncio.TimeoutError:
                # Handle agent timeout → mark as failure
                step_results = [{
                    "category": category_name,
                    "success": False,
                    "partial": False,
                    "details": {"raw": f"{agent_name} timed out"}
                }]

            # Merge results into reporter
            reporter.merge_agent_results(step_results)

    # Save final report to JSON
    reporter.save(out_file)
    print(f"✅ Report saved to {out_file}")


if __name__ == "__main__":
    # CLI argument parser
    parser = argparse.ArgumentParser(description="Ecommerce Agent CLI")
    parser.add_argument("--url", required=True, help="Base store URL")
    parser.add_argument("--products", nargs="*", help="Product paths (e.g., /products/demo-product)")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout per agent (seconds)")
    parser.add_argument("--out", default="report.json", help="Output JSON file")
    args = parser.parse_args()

    # Run the test suite with provided arguments
    asyncio.run(run_tests(args.url, args.products, args.timeout, args.out))