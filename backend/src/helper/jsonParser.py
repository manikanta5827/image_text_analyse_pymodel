import json
import re
def is_json(data):
    try:
        json.loads(data)
        return True
    except (ValueError, TypeError):
        return False

def sanitize_json_string(data):
    return re.sub(r'[\x00-\x1F\x7F]+', '', data)


def jsonParser(structured_data):
    # Handle AI response
        if isinstance(structured_data, str):
            # Clean up the structured data before parsing as JSON
            structured_data = structured_data.replace("```json", "").replace("```", "").strip()
            sanitized_data = sanitize_json_string(structured_data)
            if not is_json(sanitized_data):
                sanitized_data += '""'  
            return json.loads(sanitized_data)
        elif isinstance(structured_data, dict):
            return structured_data
        else:
            raise ValueError("Unexpected AI response format")