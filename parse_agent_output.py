import json

def parse_agent_output(output_text: str, agent_type: str) -> dict:
    """
    Converts agent output JSON string into structured dict.
    Handles 'product', 'image', 'error' types.
    Falls back to raw text if JSON parsing fails.
    """
    try:
        data = json.loads(output_text)
        # Ensure essential keys exist
        if "category" not in data:
            data["category"] = agent_type.capitalize()
        if "success" not in data:
            data["success"] = False
        if "partial" not in data:
            data["partial"] = False
        if "details" not in data:
            data["details"] = {}
        return data
    except json.JSONDecodeError:
        # fallback for non-JSON output
        return {
            "category": agent_type.capitalize(),
            "success": False,
            "partial": False,
            "details": {"raw": output_text}
        }
