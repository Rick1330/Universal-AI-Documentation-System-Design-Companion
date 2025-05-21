import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'sonner';
import { Toast } from './components/ui/toast';
import Landing from './pages/Landing';
import Upload from './pages/Upload';
import Results from './pages/Results';
import Error from './pages/Error';
import './App.css';

function App() {
  return (
    <Router>
      {/* Global toast notifications */}
      <Toaster />
      <Toast />
      
      <Routes>
        {/* Main routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/results/:jobId" element={<Results />} />
        
        {/* Error routes */}
        <Route path="/404" element={<Error code="404" title="Page Not Found" message="The page you are looking for doesn't exist or has been moved." />} />
        <Route path="/error" element={<Error code="500" title="Server Error" message="An unexpected error occurred. Please try again later." />} />
        
        {/* Redirect any unmatched routes to 404 */}
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Routes>
    </Router>
  );
}

export default App;