import { useState, useEffect } from 'react';
import axios from 'axios';
import { FileUploader } from './components/FileUploader';
import { AnalysisResults } from './components/AnalysisResults';
import { HistoryTable } from './components/HistoryTable';

interface AnalysisData {
  prediction: string;
  latency: number;
  confidence: number;
  ram_mb: number;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [classificationResults, setClassificationResults] = useState<AnalysisData | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [history, setHistory] = useState<any[]>([]);

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_URL}/history`);
      setHistory(res.data);
    } catch (error) {
      console.error("Failed to fetch history", error);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleFileUpload = (file: File) => {
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadedImage(e.target?.result as string);
      setClassificationResults(null);
    };
    reader.readAsDataURL(file);
  };

  const handleClassify = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
    
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${API_URL}/classify`, formData);
      // This 'response.data' now contains exactly what your UI displays
      setClassificationResults(response.data); 
      await fetchHistory();
    } catch (error) {
      console.error("Classification failed", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0B10] text-gray-100">
      {/* Header */}
      <header className="border-b border-[rgba(164,216,49,0.1)] backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1">
              <span className="text-3xl font-bold tracking-tight text-white">MED</span>
              <span className="text-3xl font-bold tracking-tight text-[#A4D831]">CLASSIFY</span>
            </div>
            <div className="ml-4 flex items-center gap-2 text-xs text-gray-400 tracking-widest">
              <svg className="w-3 h-3 text-[#A4D831]" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13 2L3 14h8l-2 8 10-12h-8l2-8z"/>
              </svg>
              HEALTHCARE SIMPLIFIED
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid gap-8">
          {/* File Uploader */}
          <FileUploader
            onFileUpload={handleFileUpload}
            uploadedImage={uploadedImage}
          />

          {/* Action Button */}
          {uploadedImage && (
            <div className="flex justify-center">
              <button
                onClick={handleClassify}
                disabled={isAnalyzing}
                className="relative px-12 py-4 rounded-xl bg-gradient-to-r from-[#A4D831] to-[#7CB030] text-[#0A0B10] font-semibold tracking-wide transition-all duration-300 hover:shadow-[0_0_30px_rgba(164,216,49,0.5)] disabled:opacity-50 disabled:cursor-not-allowed"
                style={{
                  boxShadow: '0 8px 32px rgba(164, 216, 49, 0.3)'
                }}
              >
                {isAnalyzing ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                    </svg>
                    ANALYZING...
                  </span>
                ) : (
                  'CLASSIFY DOCUMENT'
                )}
              </button>
            </div>
          )}

          {/* Analysis Results */}
          {classificationResults && (
            <AnalysisResults data={classificationResults} />
          )}

          {/* History */}
          {history.length > 0 && (
            <HistoryTable history={history} />
          )}
        </div>
      </main>
    </div>
  );
}
