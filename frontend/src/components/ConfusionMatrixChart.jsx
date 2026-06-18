import React from 'react'

export default function ConfusionMatrixChart({matrix}){
  if(!matrix || matrix.length !== 2) return null
  const [[tn, fp],[fn, tp]] = matrix

  return (
    <div className="mt-4 p-3 bg-gray-800 rounded">
      <h4 className="font-semibold mb-2">Confusion Matrix</h4>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-400"><th></th><th>Pred: Safe</th><th>Pred: Phishing</th></tr>
        </thead>
        <tbody>
          <tr>
            <td className="font-semibold">Actual: Safe</td>
            <td className="p-2">{tn}</td>
            <td className="p-2">{fp}</td>
          </tr>
          <tr>
            <td className="font-semibold">Actual: Phishing</td>
            <td className="p-2">{fn}</td>
            <td className="p-2">{tp}</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
