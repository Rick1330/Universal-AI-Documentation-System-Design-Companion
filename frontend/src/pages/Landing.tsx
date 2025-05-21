import React from 'react';
import { Link } from 'react-router-dom';
import AppHeader from '../components/layout/AppHeader';
import AppFooter from '../components/layout/AppFooter';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';

// Feature component for the landing page
const FeatureCard = ({ 
  icon, 
  title, 
  description 
}: { 
  icon: React.ReactNode; 
  title: string; 
  description: string 
}) => {
  return (
    <Card className="border-0 shadow-sm">
      <CardContent className="flex flex-col items-center text-center p-6">
        <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
          {icon}
        </div>
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        <p className="text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  );
};

// Step component for How It Works section
const Step = ({ 
  number, 
  title, 
  description 
}: { 
  number: number; 
  title: string; 
  description: string 
}) => {
  return (
    <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
      <div className="flex-shrink-0 h-12 w-12 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold text-lg">
        {number}
      </div>
      <div>
        <h3 className="text-lg font-semibold mb-1">{title}</h3>
        <p className="text-muted-foreground">{description}</p>
      </div>
    </div>
  );
};

const Landing = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <AppHeader />
      
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-gradient-to-b from-background to-secondary/20">
          <div className="container py-20 md:py-32">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
                Extract Data from Any File with AI
              </h1>
              <p className="text-xl md:text-2xl text-muted-foreground mb-8">
                Universal Data Extractor processes your files and identifies structured data, tables, and key insights automatically.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Link to="/upload">
                  <Button size="lg" className="h-12 px-6">
                    Upload Your File
                  </Button>
                </Link>
                <Button size="lg" variant="outline" className="h-12 px-6">
                  Learn More
                </Button>
              </div>
            </div>
          </div>
        </section>
        
        {/* Features Section */}
        <section className="py-16 md:py-24 bg-background">
          <div className="container">
            <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <FeatureCard
                icon={<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>}
                title="Any File Type"
                description="Process PDFs, text files, CSVs and more. Our system adapts to your content automatically."
              />
              <FeatureCard
                icon={<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary"><path d="M20 17.58A5 5 0 0 1 18.51 19L15 21.31 12 18l-3-3-4.5 4.5a5 5 0 0 1 0-7.08L7 10.13 8.5 9 12 13l7-8h3v3l-2 3z"/><path d="m5 2 5 5-5 5"/></svg>}
                title="AI-Powered Extraction"
                description="Advanced AI algorithms identify tables, structured data, and key information automatically."
              />
              <FeatureCard
                icon={<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary"><circle cx="12" cy="12" r="10"/><circle cx="10" cy="10" r="3"/><path d="m21 21-9-9"/></svg>}
                title="Instant Insights"
                description="Get immediate analysis, visualizations, and summaries from your extracted data."
              />
            </div>
          </div>
        </section>
        
        {/* How It Works Section */}
        <section className="py-16 md:py-24 bg-secondary/20">
          <div className="container">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            <div className="max-w-3xl mx-auto flex flex-col gap-8">
              <Step
                number={1}
                title="Upload Your File"
                description="Simply drag and drop or select your PDF, TXT, or CSV file. The system accepts files up to 10MB."
              />
              <Step
                number={2}
                title="AI Processing"
                description="Our AI analyzes your content, identifies structure, tables, and key information automatically."
              />
              <Step
                number={3}
                title="Review & Download Results"
                description="View the extracted data, analysis, and download in your preferred format for further use."
              />
            </div>
          </div>
        </section>
      </main>
      
      <AppFooter />
    </div>
  );
};

export default Landing;