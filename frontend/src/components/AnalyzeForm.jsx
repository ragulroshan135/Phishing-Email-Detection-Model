import React, {useState} from 'react'
import axios from 'axios'

export default function AnalyzeForm(){
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyze = async () => {
    setLoading(true)
    try{
      const res = await axios.post('http://localhost:8000/analyze',{email: text})
      setResult(res.data)
    }catch(e){
      setResult({error: 'Unable to analyze. Is the backend running and the model trained?'})
    }
    setLoading(false)
  }

  const downloadReport = async () => {
    if(!text) return
    setLoading(true)
    try{
      const res = await axios.post('http://localhost:8000/report',{email: text}, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'phishing_report.pdf')
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
    }catch(e){
      alert('Unable to download report.')
    }
    setLoading(false)
  }

  return (
    <div className="p-4 bg-gray-800 rounded-md">
      <h2 className="font-semibold mb-2">Email Input</h2>
      <textarea value={text} onChange={e=>setText(e.target.value)} rows={12} className="w-full p-2 bg-gray-900 border border-gray-700 rounded text-sm" placeholder="Paste full email content here"></textarea>
      <div className="flex items-center gap-2 mt-3">
        <button onClick={analyze} disabled={loading} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded">{loading? 'Analyzing...':'Analyze'}</button>
        <button onClick={()=>{setText('')}} className="px-3 py-2 bg-gray-700 rounded">Clear</button>
        <button onClick={downloadReport} disabled={loading} className="px-3 py-2 bg-green-600 hover:bg-green-700 rounded">Download PDF</button>
      </div>

      {result && (
        <div className="mt-4 p-3 bg-gray-900 rounded text-sm">
          {result.error ? (
            <div className="text-red-400">{result.error}</div>
          ) : (
            <div>
              <div className="mb-2">Prediction: <strong className={result.prediction==='phishing'? 'text-red-400':'text-green-400'}>{result.prediction}</strong></div>
              <div>Confidence: {result.confidence}%</div>
              <div>Threat Score: {result.threat_score} / 100</div>
              <div className="mt-2">Indicators:</div>
              <ul className="list-disc ml-5">
                {result.indicators.keywords && result.indicators.keywords.map((k,i)=>(<li key={i}>{k}</li>))}
                {result.indicators.urls && result.indicators.urls.map((u,i)=>(<li key={i}>{u.url} - {u.flags.join(', ')}</li>))}
              </ul>
              <div className="mt-2">Recommendations:</div>
              <ul className="list-disc ml-5">
                <li>Do not click suspicious links</li>
                <li>Verify sender identity</li>
                <li>Avoid sharing credentials</li>
                <li>Report the email</li>
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
