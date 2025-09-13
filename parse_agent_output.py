# parse_agent_output.py
import re

def parse_agent_output(output_text: str, agent_type: str) -> dict:
    """
    Converts agent CLI output into structured data for the reporter.
    Returns a dict depending on agent_type: 'product', 'image', 'error'.
    """
    if agent_type == "product":
        data = {"title": None, "price": None, "description": None}
        title = re.search(r"Product title: PRESENT \('(.+?)'\)", output_text)
        price = re.search(r"Product price: PRESENT \('(.+?)'\)", output_text)
        desc = re.search(r"Product description: (?:PRESENT|PARTIALLY PRESENT|MISSING).*?'?(.+?)'?\n", output_text, re.DOTALL)
        if title:
            data["title"] = title.group(1)
        if price:
            data["price"] = price.group(1)
        if desc:
            data["description"] = desc.group(1).strip()
        return data

    elif agent_type == "image":
        # fallback: just return the raw output if extraction fails
        return {"raw": output_text}

    elif agent_type == "error":
        return {"raw": output_text}

    return {"raw": output_text}
