import React from 'react';

const AppFooter: React.FC = () => {
  return (
    <footer className="border-t bg-background">
      <div className="container py-6 md:py-8 mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center space-x-2">
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
            </div>
            <p className="text-sm text-muted-foreground mt-2">
              Effortlessly extract structured data from various file types with AI-powered analysis.
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-3">Product</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Features</a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">How It Works</a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Pricing</a>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-3">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Documentation</a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">API Reference</a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Support</a>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-3">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Privacy Policy</a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Terms of Service</a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground">Cookie Policy</a>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t mt-8 pt-6">
          <p className="text-xs text-muted-foreground text-center">
            © {new Date().getFullYear()} Universal Data Extractor. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default AppFooter;