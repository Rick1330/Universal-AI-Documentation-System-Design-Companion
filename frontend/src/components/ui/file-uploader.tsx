import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { Button } from './button';
import { Progress } from './progress';
import { X, Upload, FileText, AlertCircle } from 'lucide-react';
import { Card } from './card';

interface FileUploaderProps {
  onFileSelected: (file: File) => void;
  isUploading: boolean;
  progress?: number;
  error?: string;
  supportedTypes?: string[];
  maxSizeMB?: number;
}

const FileUploader = ({
  onFileSelected,
  isUploading,
  progress = 0,
  error,
  supportedTypes = ['application/pdf', 'text/plain', 'text/csv'],
  maxSizeMB = 10
}: FileUploaderProps) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Helper function to display readable file extensions
  const getReadableFileTypes = () => {
    const typeMap: Record<string, string> = {
      'application/pdf': 'PDF',
      'text/plain': 'TXT',
      'text/csv': 'CSV'
    };
    
    return supportedTypes
      .map(type => typeMap[type] || type.split('/')[1].toUpperCase())
      .join(', ');
  };

  const handleDrag = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFile = (file: File): boolean => {
    // Check file type
    if (!supportedTypes.includes(file.type)) {
      setFileError(`Invalid file type. Supported types: ${getReadableFileTypes()}`);
      return false;
    }
    
    // Check file size
    const fileSizeMB = file.size / (1024 * 1024);
    if (fileSizeMB > maxSizeMB) {
      setFileError(`File is too large. Maximum size: ${maxSizeMB}MB`);
      return false;
    }
    
    setFileError(null);
    return true;
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
        onFileSelected(file);
      }
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
        onFileSelected(file);
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const removeFile = () => {
    setSelectedFile(null);
    setFileError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <Card className="p-6">
      {/* File input (hidden) */}
      <input 
        ref={fileInputRef}
        type="file"
        multiple={false}
        onChange={handleChange}
        accept={supportedTypes.join(',')}
        className="hidden"
      />
      
      {/* Error display */}
      {(fileError || error) && (
        <div className="mb-4 bg-destructive/10 text-destructive p-3 rounded-md flex items-start gap-2">
          <AlertCircle className="h-5 w-5 mt-0.5" />
          <p>{fileError || error}</p>
        </div>
      )}
      
      {/* Selected file display */}
      {selectedFile && !isUploading ? (
        <div className="mb-4 p-3 border rounded-md bg-secondary/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">{selectedFile.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={removeFile} 
              className="h-8 w-8 p-0"
            >
              <X className="h-4 w-4" />
              <span className="sr-only">Remove file</span>
            </Button>
          </div>
        </div>
      ) : null}
      
      {/* Upload progress display */}
      {isUploading && (
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <p className="text-sm font-medium">Uploading...</p>
            <span className="text-xs text-muted-foreground">{progress}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>
      )}
      
      {/* Drop area */}
      {!selectedFile || (selectedFile && !isUploading) ? (
        <div 
          className={`border-2 border-dashed rounded-md ${dragActive ? 'border-primary bg-primary/5' : 'border-muted-foreground/25'}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center py-8 px-4 text-center">
            <Upload className="h-10 w-10 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-1">
              {dragActive ? 'Drop your file here' : 'Drag & drop your file here'}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              or click to browse (Supported formats: {getReadableFileTypes()})
            </p>
            <Button 
              type="button"
              onClick={handleButtonClick}
              disabled={isUploading}
            >
              Browse Files
            </Button>
          </div>
        </div>
      ) : null}
    </Card>
  );
};

export { FileUploader };