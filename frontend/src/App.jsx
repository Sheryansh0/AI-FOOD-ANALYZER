import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import FoodAnalyzerForm from "./components/FoodAnalyzerForm";
import ResultsDisplay from "./components/ResultsDisplay";
import Header from "./components/Header";
import Background from "./components/Background";

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (data) => {
    setResults(data);
    setLoading(false);
  };

  const handleReset = () => {
    setResults(null);
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      <Background />

      <div className="relative z-10">
        <Header />

        <main className="container mx-auto px-4 py-8">
          <AnimatePresence mode="wait">
            {!results ? (
              <motion.div
                key="form"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
              >
                <FoodAnalyzerForm
                  onAnalysisComplete={handleAnalysisComplete}
                  loading={loading}
                  setLoading={setLoading}
                />
              </motion.div>
            ) : (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
              >
                <ResultsDisplay results={results} onReset={handleReset} />
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

export default App;
