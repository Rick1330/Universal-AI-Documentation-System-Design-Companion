# AI Agent: Data Analyzer
import json
from typing import Dict, Any, List, Union
import re
import statistics # For mean, median, stdev

# Placeholder for future LLM integration (e.g., LangChain, OpenAI client)
# from ....app.core.config import settings
# import openai
# openai.api_key = settings.OPENAI_API_KEY

def generate_text_summary(text: str, max_length: int = 150) -> str:
    """Generates a concise summary of the text. Placeholder for LLM-based summarization."""
    if not text or not isinstance(text, str):
        return ""
    # Simple placeholder: take the first N characters/words
    summary = text[:max_length]
    if len(text) > max_length:
        summary += "..."
    # A real LLM call would be: openai.Completion.create(engine="davinci", prompt=f"Summarize this: {text}", max_tokens=60)
    return summary

def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
    """Extracts relevant keywords from the text. Placeholder for NLP/LLM-based keyword extraction."""
    if not text or not isinstance(text, str):
        return []
    # Simple placeholder: split by space, count frequency, take top N (case-insensitive)
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return []
    word_counts = {}
    for word in words:
        if len(word) > 3: # Basic filter for very short words
            word_counts[word] = word_counts.get(word, 0) + 1
    sorted_keywords = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    return [kw[0] for kw in sorted_keywords[:num_keywords]]

def attempt_type_conversion(value: str) -> Union[int, float, str]:
    """Attempts to convert a string to an int or float."""
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value # Return original string if conversion fails

async def run_analysis_agent(cleaned_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for the Data Analyzer Agent.
    Processes cleaned JSON data to derive insights.
    """
    print(f"Analyzer Agent: Processing cleaned data.")
    analysis_output = {
        "text_analysis": {"summary": "", "keywords": []},
        "table_analysis": [],
        "key_field_summary": cleaned_data.get("key_fields", {}),
        "overall_insights": [],
        "visualization_data": {}
    }

    # 1. Textual Analysis
    full_text = cleaned_data.get("full_text_content", "")
    if isinstance(full_text, list):
        full_text = " \n".join(filter(None,full_text)) # Join if it was an array of strings
    
    if full_text:
        analysis_output["text_analysis"]["summary"] = generate_text_summary(full_text)
        analysis_output["text_analysis"]["keywords"] = extract_keywords(full_text)

    # 2. Tabular Data Analysis
    tables = cleaned_data.get("tables", [])
    first_suitable_table_for_viz = None

    for table_idx, table_item in enumerate(tables):
        if not (isinstance(table_item, dict) and "data" in table_item and isinstance(table_item["data"], list)):
            continue
        
        table_name = table_item.get("name", f"table_{table_idx + 1}")
        table_data = table_item["data"]
        if not table_data: continue

        current_table_analysis = {"table_name": table_name, "column_statistics": [], "row_count": len(table_data) -1 if len(table_data)>0 else 0}
        headers = table_data[0] if table_data else []
        column_data_typed: Dict[str, List[Any]] = {header: [] for header in headers}
        
        # Skip header row for data processing
        for row_idx, row in enumerate(table_data[1:] if len(table_data) > 1 else []):
            if len(row) == len(headers):
                for col_idx, cell_value in enumerate(row):
                    column_data_typed[headers[col_idx]].append(attempt_type_conversion(cell_value))
        
        for col_idx, header in enumerate(headers):
            col_stats = {"column_name": header, "inferred_type": "text"} # Default to text
            numeric_values: List[Union[int, float]] = [v for v in column_data_typed[header] if isinstance(v, (int, float))]
            string_values: List[str] = [str(v) for v in column_data_typed[header] if isinstance(v, str)]

            if numeric_values:
                col_stats["inferred_type"] = "numeric"
                col_stats["count"] = len(numeric_values)
                col_stats["sum"] = sum(numeric_values)
                col_stats["mean"] = round(statistics.mean(numeric_values), 2) if numeric_values else 0
                col_stats["median"] = round(statistics.median(numeric_values), 2) if numeric_values else 0
                col_stats["min"] = min(numeric_values) if numeric_values else 0
                col_stats["max"] = max(numeric_values) if numeric_values else 0
                col_stats["std_dev"] = round(statistics.stdev(numeric_values), 2) if len(numeric_values) > 1 else 0
                
                # For MVP viz: pick first numeric column of first table with string labels
                if not first_suitable_table_for_viz and col_idx > 0: # Ensure there's a label column
                    label_col_data = [str(v) for v in column_data_typed[headers[0]]]
                    if all(isinstance(v, str) for v in label_col_data):
                        first_suitable_table_for_viz = {
                            "title": f"{header} by {headers[0]} ({table_name})",
                            "labels": label_col_data[:10], # Limit to 10 for viz
                            "values": numeric_values[:10]
                        }
            elif string_values: # Categorical/Text
                freq_dist = {}
                for s_val in string_values:
                    freq_dist[s_val] = freq_dist.get(s_val, 0) + 1
                sorted_freq = sorted(freq_dist.items(), key=lambda item: item[1], reverse=True)
                col_stats["top_values_frequency"] = dict(sorted_freq[:5]) # Top 5 frequent
            
            current_table_analysis["column_statistics"].append(col_stats)
        analysis_output["table_analysis"].append(current_table_analysis)

    # 3. Key-Field Summary (already in analysis_output["key_field_summary"])

    # 4. Overall Insights (Placeholder)
    if analysis_output["text_analysis"]["summary"]:
        analysis_output["overall_insights"].append(f"Document Summary: {analysis_output['text_analysis']['summary'][:50]}...")
    if tables and analysis_output["table_analysis"]:
        analysis_output["overall_insights"].append(f"Analyzed {len(tables)} table(s). First table ('{analysis_output['table_analysis'][0]['table_name']}') has {analysis_output['table_analysis'][0]['row_count']} data rows.")
    if not analysis_output["overall_insights"]:
        analysis_output["overall_insights"].append("Basic analysis complete. No specific high-level insights generated by placeholder logic.")

    # 5. Visualization Data
    if first_suitable_table_for_viz:
        analysis_output["visualization_data"] = {"bar_chart_data": first_suitable_table_for_viz}
    
    print(f"Analyzer Agent: Analysis complete.")
    return analysis_output

# Example usage (for testing locally):
# if __name__ == "__main__":
#     import asyncio
#     sample_cleaned_data = {
#         "full_text_content": "This report details quarterly sales. Q1 saw strong growth, particularly in the Alpha product line. Q2 experienced a slight dip due to market seasonality but recovered by month end. Key takeaway: Alpha product is a consistent performer.",
#         "tables": [
#             {
#                 "name": "sales_q1",
#                 "data": [
#                     ["Product", "Units Sold", "Revenue"],
#                     ["Alpha", "150", "15000"],
#                     ["Beta", "90", "8100"],
#                     ["Gamma", "110", "9900"]
#                 ]
#             }
#         ],
#         "key_fields": {
#             "Report Version": "1.2",
#             "Generated Date": "2024-05-10"
#         }
#     }
#     analysis_result = asyncio.run(run_analysis_agent(sample_cleaned_data))
#     print("Analysis Result:", json.dumps(analysis_result, indent=2))

