# AI Agent: Data Cleaner
import re
from typing import Dict, Any, List, Union

# Placeholder for future LLM integration for contextual cleaning
# from ....app.core.config import settings
# import openai
# openai.api_key = settings.OPENAI_API_KEY

def trim_whitespace(value: str) -> str:
    """Trims leading/trailing whitespace and normalizes internal whitespace."""
    if not isinstance(value, str):
        return value
    value = value.strip()
    value = re.sub(r'\s+', ' ', value) # Replace multiple spaces with a single space
    return value

def clean_numeric_string(value: str) -> str:
    """Removes common currency symbols and thousand separators from a string intended to be numeric."""
    if not isinstance(value, str):
        return value
    # Remove currency symbols (add more as needed: €, £, ¥, etc.)
    cleaned_value = value.replace("$", "").replace(",", "")
    # Add more currency symbols if necessary
    # cleaned_value = re.sub(r"[$,€£¥]", "", value)
    # cleaned_value = cleaned_value.replace(",", "") # Remove thousand separators
    # Be careful not to remove decimal points or negative signs if they are valid
    # This basic version just removes $ and ,
    return cleaned_value

def standardize_date_string(value: str) -> str:
    """Attempts to standardize common date formats to YYYY-MM-DD. Placeholder for robust date parsing."""
    if not isinstance(value, str):
        return value
    # This is a very basic placeholder. A library like `dateutil.parser` would be needed for robust parsing.
    # Example: 'May 10, 2024' -> '2024-05-10'
    # Example: '10/05/2024' (assuming MM/DD/YYYY) -> '2024-10-05' or (DD/MM/YYYY) -> '2024-05-10'
    # For MVP, we might just trim whitespace and leave complex parsing to analyzer or later stages.
    # For now, just return the trimmed string, as robust date parsing is complex.
    return value # Placeholder - actual implementation would use dateutil.parser.parse(value).strftime('%Y-%m-%d')

def clean_value(value: Any) -> Any:
    """Applies a series of cleaning operations to a single value."""
    if isinstance(value, str):
        value = trim_whitespace(value)
        # Attempt to clean as numeric first, then standardize date if it's not primarily numeric looking
        # This order might need adjustment based on typical data
        cleaned_numeric_candidate = clean_numeric_string(value)
        # A simple heuristic: if it changed significantly and now looks like a number, it might be numeric
        # A more robust check would involve trying to parse as float/int
        if cleaned_numeric_candidate != value and re.match(r"^-?\d*\.?\d+$", cleaned_numeric_candidate):
            value = cleaned_numeric_candidate
        else:
            # If not obviously numeric after cleaning, try date standardization
            value = standardize_date_string(value) # Placeholder for now
    return value

async def run_cleaning_agent(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for the Data Cleaner Agent.
    Takes raw extracted JSON and applies cleaning rules.
    """
    print(f"Cleaner Agent: Processing extracted data.")
    cleaned_data = extracted_data.copy() # Work on a copy

    # Clean full_text_content
    if "full_text_content" in cleaned_data:
        if isinstance(cleaned_data["full_text_content"], str):
            cleaned_data["full_text_content"] = clean_value(cleaned_data["full_text_content"])
        elif isinstance(cleaned_data["full_text_content"], list):
            cleaned_data["full_text_content"] = [clean_value(item) for item in cleaned_data["full_text_content"] if isinstance(item, str)]

    # Clean tables
    if "tables" in cleaned_data and isinstance(cleaned_data["tables"], list):
        cleaned_tables = []
        for table in cleaned_data["tables"]:
            if isinstance(table, dict) and "data" in table and isinstance(table["data"], list):
                cleaned_table_data = []
                for row in table["data"]:
                    if isinstance(row, list):
                        cleaned_row = [clean_value(cell) for cell in row]
                        cleaned_table_data.append(cleaned_row)
                cleaned_tables.append({"name": table.get("name", "unknown_table"), "data": cleaned_table_data})
            else:
                 cleaned_tables.append(table) # Append as is if structure is not as expected
        cleaned_data["tables"] = cleaned_tables

    # Clean key_fields
    if "key_fields" in cleaned_data and isinstance(cleaned_data["key_fields"], dict):
        cleaned_key_fields = {}
        for key, value in cleaned_data["key_fields"].items():
            cleaned_key_fields[clean_value(key)] = clean_value(value) # Clean keys as well
        cleaned_data["key_fields"] = cleaned_key_fields
    
    print(f"Cleaner Agent: Cleaning complete.")
    return cleaned_data

# Example usage (for testing locally):
# if __name__ == "__main__":
#     import asyncio
#     import json
#     sample_extracted_data = {
#         "full_text_content": "  Invoice for services rendered. \nTotal Amount Due: $ 1,250.00 USD. Date: Oct 05, 2023  ",
#         "tables": [
#             {
#                 "name": "items_table",
#                 "data": [
#                     [" Item Description ", " Quantity ", " Unit Price ", " Line Total   "],
#                     ["Service A       ", "  2 ", " $100.00  ", "  $200.00 "],
#                     ["Service B       ", "  1 ", " $1050.00 ", " $1050.00   "]
#                 ]
#             }
#         ],
#         "key_fields": {
#             "Invoice Number": " INV-001  ",
#             "Payment Terms ": "Net 30 days",
#             "Ship Date": " N/A "
#         }
#     }
#     cleaned_result = asyncio.run(run_cleaning_agent(sample_extracted_data))
#     print("Cleaned Result:", json.dumps(cleaned_result, indent=2))

