import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { toast } from 'sonner';
import AppHeader from '../components/layout/AppHeader';
import AppFooter from '../components/layout/AppFooter';
import { ChartComponent } from '../components/ui/chart';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { DataTable } from '../components/ui/data-table';
import { ColumnDef } from '@tanstack/react-table';
import { getJobStatus } from '../services/api';
import { Job, Table } from '../types';
import { Download, AlertTriangle, FileText, Table as TableIcon, BarChart } from 'lucide-react';
import { Skeleton } from '../components/ui/skeleton';

// Function to create columns for data tables dynamically
const createTableColumns = (table: Table): ColumnDef<Record<string, unknown>>[] => {
  return table.header.map((header, index) => ({
    accessorKey: `col${index}`,
    header,
    cell: ({ row }) => row.original[`col${index}`],
  }));
};

// Function to format table data for DataTable component
const formatTableData = (table: Table): Record<string, unknown>[] => {
  return table.rows.map((row) => {
    const rowData: Record<string, unknown> = {};
    row.forEach((cell, index) => {
      rowData[`col${index}`] = cell;
    });
    return rowData;
  });
};

// Job status badge component
const StatusBadge: React.FC<{ status: Job['status'] }> = ({ status }) => {
  switch (status) {
    case 'pending':
      return <Badge variant="outline" className="bg-yellow-100 text-yellow-800 border-yellow-300">Pending</Badge>;
    case 'processing':
      return <Badge variant="outline" className="bg-blue-100 text-blue-800 border-blue-300">Processing</Badge>;
    case 'completed':
      return <Badge variant="outline" className="bg-green-100 text-green-800 border-green-300">Completed</Badge>;
    case 'failed':
      return <Badge variant="outline" className="bg-red-100 text-red-800 border-red-300">Failed</Badge>;
    default:
      return <Badge variant="outline">Unknown</Badge>;
  }
};

// KeyValue display component for metadata and fields
const KeyValue: React.FC<{ label: string; value: string | number }> = ({ label, value }) => (
  <div className="flex justify-between py-2 border-b last:border-b-0">
    <span className="text-muted-foreground">{label}</span>
    <span className="font-medium">{value}</span>
  </div>
);

const Results = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);

  // Fetch job status and handle polling for processing jobs
  useEffect(() => {
    if (!jobId) {
      setError('Job ID is missing');
      setLoading(false);
      return;
    }

    const fetchJob = async () => {
      try {
        const data = await getJobStatus(jobId);
        setJob(data);
        
        // Clear any existing error
        setError(null);

        // If job is still processing, continue polling
        if (data.status === 'pending' || data.status === 'processing') {
          // Already have an interval running, let it continue
          if (!pollingInterval) {
            const interval = setInterval(fetchJob, 3000);
            setPollingInterval(interval);
          }
        } else {
          // Job completed or failed, stop polling
          if (pollingInterval) {
            clearInterval(pollingInterval);
            setPollingInterval(null);
          }
          
          if (data.status === 'completed') {
            toast.success('Processing completed!', {
              description: 'Your data has been successfully processed.',
            });
          } else if (data.status === 'failed') {
            toast.error('Processing failed', {
              description: data.message,
            });
          }
        }

        setLoading(false);
      } catch (error) {
        if (pollingInterval) {
          clearInterval(pollingInterval);
          setPollingInterval(null);
        }
        setError('Failed to load job details. Please try again later.');
        setLoading(false);
        toast.error('Error loading job', {
          description: 'Could not retrieve job status. Please try again.',
        });
      }
    };

    fetchJob();

    // Clean up interval on unmount
    return () => {
      if (pollingInterval) clearInterval(pollingInterval);
    };
  }, [jobId, pollingInterval]);

  return (
    <div className="min-h-screen flex flex-col">
      <AppHeader />
      
      <main className="flex-grow container py-8">
        {/* Job Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">
                {loading ? (
                  <Skeleton className="h-9 w-64" />
                ) : (
                  <>Processing: {job?.file_name || 'Unknown File'}</>
                )}
              </h1>
              <div className="flex items-center gap-2 text-muted-foreground">
                {loading ? (
                  <Skeleton className="h-5 w-32" />
                ) : (
                  <>
                    <span>Job ID: {jobId}</span>
                    {job && <StatusBadge status={job.status} />}
                  </>
                )}
              </div>
            </div>
            {job?.status === 'completed' && job.download_urls && (
              <div className="flex flex-wrap gap-2">
                <Button variant="outline" size="sm" asChild>
                  <a href={job.download_urls.csv} download>
                    <Download className="h-4 w-4 mr-2" />
                    Download CSV
                  </a>
                </Button>
                <Button variant="outline" size="sm" asChild>
                  <a href={job.download_urls.json} download>
                    <Download className="h-4 w-4 mr-2" />
                    Download JSON
                  </a>
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <Card className="mb-8">
            <CardHeader>
              <Skeleton className="h-6 w-32 mb-2" />
              <Skeleton className="h-4 w-48" />
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-3/4" />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error State */}
        {error && (
          <Card className="border-red-200 mb-8">
            <CardHeader className="text-red-700">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                <CardTitle>Error</CardTitle>
              </div>
              <CardDescription className="text-red-600">
                {error}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="mb-4">There was a problem retrieving the job details. Please try again or start a new job.</p>
              <Button asChild>
                <Link to="/upload">Go to Upload</Link>
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Processing State */}
        {!loading && !error && job?.status === 'processing' && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="inline-block h-3 w-3 rounded-full bg-blue-500 animate-pulse"></span>
                Processing Your File
              </CardTitle>
              <CardDescription>
                Your file is currently being analyzed. This may take a few moments.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium">Processing Progress</span>
                  <span className="text-xs text-muted-foreground">{job.progress || 0}%</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary transition-all duration-300" 
                    style={{ width: `${job.progress || 0}%` }}
                  ></div>
                </div>
              </div>
              <p className="text-sm text-muted-foreground">
                We're currently extracting data from your file. Please wait while the system analyzes the content.
              </p>
            </CardContent>
          </Card>
        )}

        {/* Failed State */}
        {!loading && !error && job?.status === 'failed' && (
          <Card className="border-red-200 mb-8">
            <CardHeader className="text-red-700">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                <CardTitle>Processing Failed</CardTitle>
              </div>
              <CardDescription className="text-red-600">
                An error occurred while processing your file
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="mb-4">{job.message}</p>
              <p className="mb-6 text-sm text-muted-foreground">
                This could be due to an unsupported file format, file corruption, or server issues.
                Please try uploading your file again or try with a different file.
              </p>
              <Button asChild>
                <Link to="/upload">Try Again</Link>
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Completed State - Results */}
        {!loading && !error && job?.status === 'completed' && job.results && (
          <Tabs defaultValue="cleaned" className="mb-8">
            <TabsList className="grid grid-cols-3 mb-8">
              <TabsTrigger value="extracted" className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                <span className="hidden sm:inline">Raw Extracted Data</span>
                <span className="sm:hidden">Raw Data</span>
              </TabsTrigger>
              <TabsTrigger value="cleaned" className="flex items-center gap-2">
                <TableIcon className="h-4 w-4" />
                <span className="hidden sm:inline">Cleaned & Structured Data</span>
                <span className="sm:hidden">Structured</span>
              </TabsTrigger>
              <TabsTrigger value="analysis" className="flex items-center gap-2">
                <BarChart className="h-4 w-4" />
                <span className="hidden sm:inline">Analysis & Insights</span>
                <span className="sm:hidden">Analysis</span>
              </TabsTrigger>
            </TabsList>
            
            {/* Raw Extracted Data Tab */}
            <TabsContent value="extracted">
              <div className="grid gap-6">
                {/* Raw Text Content */}
                <Card>
                  <CardHeader>
                    <CardTitle>Extracted Text Content</CardTitle>
                    <CardDescription>
                      Raw text extracted from the document
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="bg-muted p-4 rounded-md whitespace-pre-wrap font-mono text-sm">
                      {job.results.extracted_data.text_content}
                    </div>
                  </CardContent>
                </Card>
                
                {/* Key Fields */}
                <Card>
                  <CardHeader>
                    <CardTitle>Extracted Key Fields</CardTitle>
                    <CardDescription>
                      Important fields identified in the document
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-1">
                      {Object.entries(job.results.extracted_data.key_fields).map(([key, value]) => (
                        <KeyValue key={key} label={key} value={value.toString()} />
                      ))}
                    </div>
                  </CardContent>
                </Card>
                
                {/* Tables */}
                {job.results.extracted_data.tables.map((table, tableIndex) => {
                  const columns = createTableColumns(table);
                  const data = formatTableData(table);
                  
                  return (
                    <DataTable 
                      key={`extracted-table-${tableIndex}`}
                      columns={columns}
                      data={data}
                      title={table.title || `Table ${tableIndex + 1}`}
                    />
                  );
                })}
              </div>
            </TabsContent>
            
            {/* Cleaned & Structured Data Tab */}
            <TabsContent value="cleaned">
              <div className="grid gap-6">
                {/* Cleaned Text Content */}
                <Card>
                  <CardHeader>
                    <CardTitle>Cleaned Text Content</CardTitle>
                    <CardDescription>
                      Processed and normalized text content
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="bg-muted p-4 rounded-md whitespace-pre-wrap font-mono text-sm">
                      {job.results.cleaned_data.text_content}
                    </div>
                  </CardContent>
                </Card>
                
                {/* Key Fields */}
                <Card>
                  <CardHeader>
                    <CardTitle>Structured Key Fields</CardTitle>
                    <CardDescription>
                      Normalized and typed key fields from the document
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-1">
                      {Object.entries(job.results.cleaned_data.key_fields).map(([key, value]) => (
                        <KeyValue key={key} label={key} value={value.toString()} />
                      ))}
                    </div>
                  </CardContent>
                </Card>
                
                {/* Tables */}
                {job.results.cleaned_data.tables.map((table, tableIndex) => {
                  const columns = createTableColumns(table);
                  const data = formatTableData(table);
                  
                  return (
                    <DataTable 
                      key={`cleaned-table-${tableIndex}`}
                      columns={columns}
                      data={data}
                      title={table.title || `Table ${tableIndex + 1}`}
                    />
                  );
                })}
              </div>
            </TabsContent>
            
            {/* Analysis & Insights Tab */}
            <TabsContent value="analysis">
              <div className="grid gap-6">
                {/* Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle>Document Summary</CardTitle>
                    <CardDescription>
                      AI-generated summary of the document contents
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p>{job.results.analysis.summary}</p>
                  </CardContent>
                </Card>
                
                {/* Keywords and Sentiment */}
                <div className="grid md:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Key Concepts</CardTitle>
                      <CardDescription>
                        Important keywords identified in the document
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2">
                        {job.results.analysis.keywords.map((keyword, index) => (
                          <Badge key={index} variant="secondary">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardHeader>
                      <CardTitle>Document Sentiment</CardTitle>
                      <CardDescription>
                        Overall tone analysis of the document
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center gap-2">
                        {job.results.analysis.sentiment === 'positive' && (
                          <>
                            <span className="inline-block h-4 w-4 rounded-full bg-green-500"></span>
                            <span className="capitalize">Positive</span>
                          </>
                        )}
                        {job.results.analysis.sentiment === 'negative' && (
                          <>
                            <span className="inline-block h-4 w-4 rounded-full bg-red-500"></span>
                            <span className="capitalize">Negative</span>
                          </>
                        )}
                        {job.results.analysis.sentiment === 'neutral' && (
                          <>
                            <span className="inline-block h-4 w-4 rounded-full bg-blue-500"></span>
                            <span className="capitalize">Neutral</span>
                          </>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </div>
                
                {/* Charts */}
                <div className="grid md:grid-cols-2 gap-6">
                  {job.results.charts_data.filter(chart => chart.type === 'bar' || chart.type === 'pie').map((chart, index) => (
                    <ChartComponent
                      key={`chart-${index}`}
                      type={chart.type as 'bar' | 'pie'} // Cast type after filtering
                      title={chart.title}
                      data={chart.data}
                    />
                  ))}
                </div>
              </div>
            </TabsContent>
          </Tabs>
        )}
      </main>
      
      <AppFooter />
    </div>
  );
};

export default Results;