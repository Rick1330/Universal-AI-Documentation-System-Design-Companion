import React from 'react';
import { Link } from 'react-router-dom';
import AppHeader from '../components/layout/AppHeader';
import AppFooter from '../components/layout/AppFooter';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { AlertOctagon } from 'lucide-react';

interface ErrorProps {
  title?: string;
  message?: string;
  code?: string | number;
}

const Error: React.FC<ErrorProps> = ({
  title = "Something went wrong",
  message = "We couldn't load the page you requested. Please try again or return to the home page.",
  code = "404"
}) => {
  return (
    <div className="min-h-screen flex flex-col">
      <AppHeader />
      
      <main className="flex-grow container py-16 flex items-center justify-center">
        <Card className="w-full max-w-lg mx-auto">
          <CardHeader>
            <div className="flex justify-center mb-6">
              <div className="h-20 w-20 rounded-full bg-red-100 flex items-center justify-center">
                <AlertOctagon className="h-10 w-10 text-red-600" />
              </div>
            </div>
            <CardTitle className="text-2xl text-center">
              {title}
            </CardTitle>
            <CardDescription className="text-center text-base">
              Error {code}
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <p className="mb-6">{message}</p>
            <div className="flex justify-center space-x-4">
              <Button asChild>
                <Link to="/">
                  Go to Home Page
                </Link>
              </Button>
              <Button variant="outline" asChild>
                <Link to="/upload">
                  Upload a File
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
      
      <AppFooter />
    </div>
  );
};

export default Error;