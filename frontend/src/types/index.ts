// Types definitions for the application
export interface Job {
  job_id: string;
  file_name: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  message: string;
  results?: JobResults;
  download_urls?: DownloadUrls;
  created_at: string;
  updated_at: string;
}

export interface ExtractedData {
  text_content: string;
  tables: Table[];
  key_fields: Record<string, string>;
}

export interface CleanedData {
  text_content: string;
  tables: Table[];
  key_fields: Record<string, string | number>;
}

export interface Analysis {
  summary: string;
  keywords: string[];
  sentiment: 'positive' | 'negative' | 'neutral';
}

export interface ChartData {
  type: 'bar' | 'pie' | 'line';
  title: string;
  data: Record<string, unknown>[];
}

export interface Table {
  title: string;
  header: string[];
  rows: (string | number)[][];
}

export interface JobResults {
  extracted_data: ExtractedData;
  cleaned_data: CleanedData;
  analysis: Analysis;
  charts_data: ChartData[];
}

export interface DownloadUrls {
  csv: string;
  json: string;
}

export interface ApiError {
  detail: string;
}

export type FileType = 'PDF' | 'TXT' | 'CSV';

export interface FileUploadResponse {
  job_id: string;
  file_name: string;
  status: 'pending';
  message: string;
  created_at: string;
  updated_at: string;
}

export interface FileUploadRequest {
  file: File;
}