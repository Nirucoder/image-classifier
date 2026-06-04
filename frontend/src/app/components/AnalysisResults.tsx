interface AnalysisResultsProps {
  data: {
    prediction: string;
    latency: number;
    confidence: number;
    ram_mb: number;
  };
}

export function AnalysisResults({ data }: AnalysisResultsProps) {
  return (
    <div
      className="rounded-2xl p-8 backdrop-blur-xl animate-[fadeIn_0.5s_ease-in]"
      style={{
        background: 'rgba(31, 41, 55, 0.3)',
        border: '1px solid rgba(164, 216, 49, 0.2)',
        boxShadow: 'inset 0 0 20px rgba(164, 216, 49, 0.05), 0 0 40px rgba(164, 216, 49, 0.1)'
      }}
    >
      <h2 className="text-xl mb-6 text-[#A4D831] font-mono tracking-wide flex items-center gap-2">
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        CLASSIFICATION RESULTS
      </h2>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Document Category */}
        <div
          className="rounded-xl p-6 backdrop-blur-sm"
          style={{
            background: 'rgba(10, 11, 16, 0.6)',
            border: '1px solid rgba(164, 216, 49, 0.15)',
            boxShadow: 'inset 0 0 15px rgba(164, 216, 49, 0.03)'
          }}
        >
          <p className="text-xs text-gray-400 font-mono mb-3 tracking-wider">DOCUMENT TYPE</p>
          <div
            className="inline-flex px-4 py-2 rounded-lg font-mono"
            style={{
              background: 'linear-gradient(135deg, rgba(164, 216, 49, 0.15), rgba(124, 176, 48, 0.15))',
              border: '1px solid #A4D831',
              boxShadow: '0 0 20px rgba(164, 216, 49, 0.3)',
              color: '#A4D831'
            }}
          >
            {data.prediction}
          </div>
          {data.confidence < 0.6 && data.confidence >= 0.3 && (
            <div className="mt-2 text-[10px] text-yellow-500 font-mono animate-pulse flex items-center gap-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              LOW CONFIDENCE WARNING
            </div>
          )}
        </div>

        {/* Inference Time */}
        <div
          className="rounded-xl p-6 backdrop-blur-sm"
          style={{
            background: 'rgba(10, 11, 16, 0.6)',
            border: '1px solid rgba(164, 216, 49, 0.15)',
            boxShadow: 'inset 0 0 15px rgba(164, 216, 49, 0.03)'
          }}
        >
          <p className="text-xs text-gray-400 font-mono mb-3 tracking-wider">INFERENCE TIME</p>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-mono text-[#A4D831]">
              {data.latency}
            </span>
            <span className="text-sm text-gray-400 font-mono">ms</span>
          </div>
          <div className="mt-3 h-1.5 bg-[rgba(164,216,49,0.1)] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#A4D831] to-[#7CB030] rounded-full transition-all duration-1000"
              style={{
                width: `${Math.min((data.latency / 500) * 100, 100)}%`,
                boxShadow: '0 0 10px rgba(164, 216, 49, 0.5)'
              }}
            />
          </div>
        </div>

        {/* Confidence Score */}
        <div
          className="rounded-xl p-6 backdrop-blur-sm"
          style={{
            background: 'rgba(10, 11, 16, 0.6)',
            border: '1px solid rgba(164, 216, 49, 0.15)',
            boxShadow: 'inset 0 0 15px rgba(164, 216, 49, 0.03)'
          }}
        >
          <p className="text-xs text-gray-400 font-mono mb-3 tracking-wider">CONFIDENCE SCORE</p>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-mono text-[#A4D831]">
              {(data.confidence * 100).toFixed(1)}
            </span>
            <span className="text-sm text-gray-400 font-mono">%</span>
          </div>
          <div className="mt-3 h-1.5 bg-[rgba(164,216,49,0.1)] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#A4D831] to-[#7CB030] rounded-full transition-all duration-1000"
              style={{
                width: `${data.confidence * 100}%`,
                boxShadow: '0 0 10px rgba(164, 216, 49, 0.5)'
              }}
            />
          </div>
        </div>

        {/* RAM Usage */}
        <div
          className="rounded-xl p-6 backdrop-blur-sm"
          style={{
            background: 'rgba(10, 11, 16, 0.6)',
            border: '1px solid rgba(164, 216, 49, 0.15)',
            boxShadow: 'inset 0 0 15px rgba(164, 216, 49, 0.03)'
          }}
        >
          <p className="text-xs text-gray-400 font-mono mb-3 tracking-wider">MEMORY FOOTPRINT</p>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-mono text-[#A4D831]">
              {data.ram_mb.toFixed(1)}
            </span>
            <span className="text-sm text-gray-400 font-mono">MB</span>
          </div>
          <div className="mt-3 h-1.5 bg-[rgba(164,216,49,0.1)] rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#A4D831] to-[#7CB030] rounded-full transition-all duration-1000"
              style={{
                width: `${Math.min((data.ram_mb / 1024) * 100, 100)}%`,
                boxShadow: '0 0 10px rgba(164, 216, 49, 0.5)'
              }}
            />
          </div>
        </div>
      </div>

      {/* Additional Info */}
      <div
        className="mt-6 rounded-xl p-4 backdrop-blur-sm"
        style={{
          background: 'rgba(10, 11, 16, 0.4)',
          border: '1px solid rgba(164, 216, 49, 0.1)'
        }}
      >
        <p className="text-xs text-gray-400 font-mono flex items-center gap-2">
          <svg className="w-4 h-4 text-[#A4D831]" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          Model: MEDCLASSIFY-Classifier-v2.1 | Processing complete
        </p>
      </div>
    </div>
  );
}
