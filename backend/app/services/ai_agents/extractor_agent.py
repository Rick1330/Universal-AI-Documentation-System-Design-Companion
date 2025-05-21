# AI Agent: Data Extractor
import os
import csv
import json
import requests
from typing import Dict, Any, List

# Import settings for AI API integration
from ...core.config import settings

def extract_full_text_from_txt(file_path: str) -> str:
    """Extracts all text content from a TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file {file_path}: {e}")
        return ""

def extract_tables_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Parses a CSV file and returns its content as a list of tables (in this case, one table)."""
    tables = []
    table_data: List[List[str]] = []
    try:
        with open(file_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                table_data.append(row)
        if table_data:
            tables.append({
                "name": os.path.basename(file_path),
                "data": table_data
            })
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
    return tables

def extract_key_fields_with_gemini(text_content: str) -> Dict[str, Any]:
    """
    Uses Gemini API to extract key fields from text content.
    Returns a dictionary of key-value pairs.
    """
    # Check if we have a Gemini API key
    if not settings.GEMINI_API_KEY:
        print("Warning: No Gemini API key found. Using placeholder extraction.")
        # Fallback to basic extraction if no API key
        key_fields = {}
        if "Invoice Number:" in text_content:
            key_fields["Invoice Number"] = "INV-PLACEHOLDER"
        if "Date:" in text_content:
            key_fields["Date"] = "YYYY-MM-DD-PLACEHOLDER"
        return key_fields
    
    try:
        # Prepare the API request to Gemini
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
        
        # Create a prompt that instructs Gemini to extract key fields
        prompt = f"""
        Extract key fields from the following text content as JSON.
        Look for important information like dates, names, numbers, amounts, and other structured data.
        Format the response as a valid JSON object with key-value pairs.
        
        Text content:
        {text_content}
        
        Return ONLY a valid JSON object with the extracted key-value pairs, nothing else.
        """
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        # Make the API request
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the response
        result = response.json()
        
        # Extract the generated text from the response
        if "candidates" in result and len(result["candidates"]) > 0:
            if "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"]:
                generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
                
                # Try to parse the JSON response
                try:
                    # Find JSON object in the response (in case there's additional text)
                    import re
                    json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        extracted_fields = json.loads(json_str)
                        return extracted_fields
                    else:
                        print("Warning: No JSON object found in Gemini response")
                        return {}
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from Gemini response: {e}")
                    return {}
        
        print("Warning: Unexpected response format from Gemini API")
        return {}
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {}

async def run_extraction_agent(file_path: str, content_type: str, original_filename: str) -> Dict[str, Any]:
    """
    Main function for the Data Extractor Agent.
    Orchestrates extraction based on file type.
    """
    print(f"Extractor Agent: Processing file {original_filename} ({content_type}) from path {file_path}")
    
    output_json = {
        "full_text_content": "",
        "tables": [],
        "key_fields": {}
    }

    if content_type == "text/plain":
        output_json["full_text_content"] = extract_full_text_from_txt(file_path)
        print(f"Extractor Agent: TXT processing complete for {original_filename}")

    elif content_type == "text/csv":
        output_json["tables"] = extract_tables_from_csv(file_path)
        # CSVs are primarily tables; full_text_content might be less relevant or a concatenation.
        # For simplicity, we can join all rows to form a basic text representation if needed.
        if output_json["tables"] and output_json["tables"][0]["data"]:
            all_rows_text = []
            for row in output_json["tables"][0]["data"]:
                all_rows_text.append(",".join(row))
            output_json["full_text_content"] = "\n".join(all_rows_text)
        print(f"Extractor Agent: CSV processing complete for {original_filename}")

    elif content_type == "application/pdf":
        # Placeholder for PDF processing (Phase 3)
        output_json["full_text_content"] = f"PDF processing for {original_filename} is not yet implemented (Phase 3)."
        print(f"Extractor Agent: PDF processing placeholder for {original_filename}")
        
    # Add other file types here (e.g., DOCX, images with OCR - Stretch Goals)
    # elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    #     pass
    # elif content_type.startswith("image/"):
    #     pass

    else:
        output_json["full_text_content"] = f"Unsupported file type: {content_type} for file {original_filename}."
        print(f"Extractor Agent: Unsupported file type {content_type} for {original_filename}")

    # Use Gemini API for key field extraction from text content
    if output_json["full_text_content"] and not output_json["key_fields"]:
        output_json["key_fields"] = extract_key_fields_with_gemini(output_json["full_text_content"])

    return output_json

# Example usage (for testing locally):
# if __name__ == "__main__":
#     # Create dummy files for testing
#     with open("sample.txt", "w") as f:
#         f.write("This is a sample text file.\nIt contains multiple lines.\nInvoice Number: INV-123\nDate: 2024-01-15")
#     with open("sample.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["Header1", "Header2", "Header3"])
#         writer.writerow(["Data1A", "Data1B", "Data1C"])
#         writer.writerow(["Data2A", "Data2B", "Data2C"])

#     txt_result = asyncio.run(run_extraction_agent("sample.txt", "text/plain", "sample.txt"))
#     print("TXT Extraction Result:", json.dumps(txt_result, indent=2))

#     csv_result = asyncio.run(run_extraction_agent("sample.csv", "text/csv", "sample.csv"))
#     print("CSV Extraction Result:", json.dumps(csv_result, indent=2))

#     # Clean up dummy files
#     os.remove("sample.txt")
#     os.remove("sample.csv")
