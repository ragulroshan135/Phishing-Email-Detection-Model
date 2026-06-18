import React, {useState, useEffect} from 'react'
import AnalyzeForm from './components/AnalyzeForm'
import ConfusionMatrixChart from './components/ConfusionMatrixChart'
import axios from 'axios'

export default function App(){
  const [metrics, setMetrics] = useState(null)

  useEffect(()=>{
    axios.get('http://localhost:8000/metrics').then(r=>setMetrics(r.data)).catch(()=>{})
  },[])

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      <div className="max-w-5xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold">Phishing Email Detection Model</h1>
          <p className="text-sm text-gray-400">Paste an email to analyze for phishing indicators.</p>
        </header>
        <main className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <AnalyzeForm />
          </div>
          <aside className="p-4 bg-gray-800 rounded-md">
            <h3 className="font-semibold mb-3">Model Metrics</h3>
            {metrics ? (
              <div className="space-y-2 text-sm">
                <div>Accuracy: {metrics.accuracy}</div>
                <div>Precision: {metrics.precision}</div>
                <div>Recall: {metrics.recall}</div>
                <div>F1: {metrics.f1}</div>
                {metrics.confusion_matrix && <ConfusionMatrixChart matrix={metrics.confusion_matrix} />}
              </div>
            ) : (
              <div className="text-gray-400">No metrics yet. Train model first.</div>
            )}
          </aside>
        </main>
      </div>
    </div>
  )
}
