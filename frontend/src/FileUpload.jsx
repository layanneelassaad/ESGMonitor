import React, { useState } from 'react'
import axios from 'axios'


const API = 'http://127.0.0.1:8000/api/v1'


export default function FileUpload(){
const [file, setFile] = useState(null)
const [result, setResult] = useState(null)
const [loading, setLoading] = useState(false)


const onUpload = async () => {
if(!file) return alert('Select a file')
const form = new FormData(); form.append('file', file)
setLoading(true)
try{
const { data } = await axios.post(`${API}/analysis/upload`, form)
setResult(data.result)
} finally {
setLoading(false)
}
}


return (
<div>
<input type="file" onChange={e=>setFile(e.target.files[0])} />
<button onClick={onUpload} disabled={loading}>{loading? 'Processing…':'Upload & Analyze'}</button>
{result && (
<div style={{marginTop:20}}>
<h3>Total ESG Score: {result.total_score}</h3>
<p><b>E</b>: {result.e_score} · <b>S</b>: {result.s_score} · <b>G</b>: {result.g_score}</p>
<h4>Summary</h4>
<p>{result.summary}</p>
<h4>Top Topics</h4>
<ul>
{result.topics.overall.map((t,i)=> <li key={i}>{t.label} — {Math.round(t.score*100)}%</li>)}
</ul>
<h4>Branches</h4>
<ul>
{Object.entries(result.branches).map(([loc, sum])=> <li key={loc}><b>{loc}:</b> {sum}</li>)}
</ul>
</div>
)}
</div>
)
}