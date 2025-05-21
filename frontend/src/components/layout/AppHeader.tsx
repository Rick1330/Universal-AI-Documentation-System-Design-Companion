import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/button';

const AppHeader: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
      <div className="container flex h-16 items-center justify-between mx-auto">
        <Link to="/" className="flex items-center space-x-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="h-6 w-6"
          >
            <path d="M20 17.58A5 5 0 0 1 18.51 19L15 21.31 12 18l-3-3-4.5 4.5a5 5 0 0 1 0-7.08L7 10.13 8.5 9 12 13l7-8h3v3l-2 3z" />
            <path d="m5 2 5 5-5 5" />
          </svg>
          <span className="text-lg font-bold">Universal Data Extractor</span>
        </Link>
        <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
          <Link
            to="/"
            className="transition-colors hover:text-foreground/80 text-foreground/60"
          >
            Home
          </Link>
          <Link
            to="/upload"
            className="transition-colors hover:text-foreground/80 text-foreground/60"
          >
            Upload
          </Link>
        </nav>
        <div className="flex items-center space-x-2">
          <Link to="/upload">
            <Button variant="default" size="sm">
              Upload File
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
};

export default AppHeader;