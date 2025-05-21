import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import AppHeader from '../components/layout/AppHeader';
import AppFooter from '../components/layout/AppFooter';
import { FileUploader } from '../components/ui/file-uploader';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { uploadFile } from '../services/api';
import { FileType } from '../types';

const Upload = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState<string | undefined>(undefined);
  const navigate = useNavigate();

  // Simulated progress for demo purposes
  const simulateProgress = () => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.floor(Math.random() * 10) + 1;
      if (progress > 100) progress = 100;
      setUploadProgress(progress);
      if (progress === 100) clearInterval(interval);
    }, 200);
    return interval;
  };

  const handleFileSelected = async (file: File) => {
    setIsUploading(true);
    setUploadError(undefined);
    
    // Start simulated progress
    const progressInterval = simulateProgress();
    
    try {
      // Upload file to the API
      const response = await uploadFile({ file });
      
      // Clear progress simulation and set to 100%
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // Show success message
      toast.success('File uploaded successfully!', {
        description: 'Your file is now being processed.',
      });
      
      // Navigate to the results page after a short delay
      setTimeout(() => {
        navigate(`/results/${response.job_id}`);
      }, 1500);
    } catch (error: unknown) {
      clearInterval(progressInterval);
      setUploadProgress(0);
      setIsUploading(false);
      
      // Display error message
      const errorMessage = error instanceof Error ? error.message : 
                          typeof error === 'object' && error !== null && 'detail' in error 
                          ? String((error as {detail: string}).detail) 
                          : 'An unexpected error occurred. Please try again.';
      
      setUploadError(errorMessage);
      
      toast.error('Upload failed', {
        description: errorMessage,
      });
    }
  };

  // List of supported file types for display
  const supportedFileTypes: FileType[] = ['PDF', 'TXT', 'CSV'];

  return (
    <div className="min-h-screen flex flex-col">
      <AppHeader />
      
      <main className="flex-grow container py-8 md:py-16 max-w-3xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Upload Your File</CardTitle>
            <CardDescription>
              Upload a document to extract data and analyze its contents
            </CardDescription>
          </CardHeader>
          <CardContent>
            <FileUploader 
              onFileSelected={handleFileSelected}
              isUploading={isUploading}
              progress={uploadProgress}
              error={uploadError}
              supportedTypes={['application/pdf', 'text/plain', 'text/csv']}
              maxSizeMB={10}
            />
            
            {/* Supported file types info */}
            <div className="mt-6 border-t pt-4">
              <h3 className="text-sm font-medium mb-2">Supported File Types:</h3>
              <div className="flex flex-wrap gap-2">
                {supportedFileTypes.map((type) => (
                  <div 
                    key={type} 
                    className="px-3 py-1 bg-secondary text-secondary-foreground rounded-md text-sm"
                  >
                    {type}
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
      
      <AppFooter />
    </div>
  );
};

export default Upload;