# AI Agent: Data Extractor
import os
import csv
import json
from typing import Dict, Any, List

# Placeholder for future LLM integration (e.g., LangChain, OpenAI client)
# from ....app.core.config import settings
# import openai
# openai.api_key = settings.OPENAI_API_KEY

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
        # Placeholder for LLM-based key-field extraction from TXT for MVP
        # For example, if it's a simple structured TXT, an LLM could find key-value pairs.
        # output_json["key_fields"] = {"extracted_from_txt_by_llm_placeholder": "value"}
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
        # output_json["tables"] = [] # Placeholder for PDF table extraction
        # output_json["key_fields"] = {} # Placeholder for PDF key-field extraction
        print(f"Extractor Agent: PDF processing placeholder for {original_filename}")
        
    # Add other file types here (e.g., DOCX, images with OCR - Stretch Goals)
    # elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    #     pass
    # elif content_type.startswith("image/"):
    #     pass

    else:
        output_json["full_text_content"] = f"Unsupported file type: {content_type} for file {original_filename}."
        print(f"Extractor Agent: Unsupported file type {content_type} for {original_filename}")

    # Simulate LLM key field extraction for any text content if no specific logic applied
    # This is a very basic placeholder for a more sophisticated LLM call
    if output_json["full_text_content"] and not output_json["key_fields"]:
        # In a real scenario, this would involve a prompt to an LLM
        # e.g., find_key_value_pairs(output_json["full_text_content"])
        # For now, a simple placeholder:
        if "Invoice Number:" in output_json["full_text_content"]:
             output_json["key_fields"]["Invoice Number"] = "INV-LLM-PLACEHOLDER"
        if "Date:" in output_json["full_text_content"]:
            output_json["key_fields"]["Date"] = "YYYY-MM-DD-LLM-PLACEHOLDER"

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

