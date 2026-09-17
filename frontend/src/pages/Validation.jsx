import { useEffect, useState } from 'react';
import { FileCheck2, Plus } from 'lucide-react';
import { api } from '../lib/api';

export default function Validation() {
  const [rows, setRows] = useState([]);
  const [form, setForm] = useState({tester:'', role:'', task:'', feedback:'', change_made:''});
  const load=()=>api.validation().then(setRows);
  useEffect(load,[]);
  const submit=async e=>{e.preventDefault(); if(!form.tester||!form.feedback) return; await api.addValidation(form); setForm({tester:'',role:'',task:'',feedback:'',change_made:''}); load();};
  return <div className="page"><div className="section-head"><div><div className="eyebrow">REAL USER VALIDATION</div><h2>Tester evidence</h2><p>Enter actual tester feedback here. Never invent user evidence for the submission.</p></div></div>
    <div className="grid-two">
      <form className="panel form-panel" onSubmit={submit}><div className="panel-title"><span><Plus size={18}/> ADD TESTER RECORD</span></div>{[['tester','Tester name / ID'],['role','Role'],['task','Task performed'],['feedback','Observed feedback'],['change_made','Design change made']].map(([k,l])=><label key={k}>{l}<textarea rows={k.includes('feedback')||k.includes('change')?3:1} value={form[k]} onChange={e=>setForm({...form,[k]:e.target.value})}/></label>)}<button className="btn primary" type="submit">Save validation record</button></form>
      <div className="panel"><div className="panel-title"><span><FileCheck2 size={18}/> RECORDS</span></div>{rows.length===0?<div className="empty-state">No tester records yet.</div>:rows.map(r=><div className="validation-card" key={r.id}><div className="validation-top"><b>{r.tester}</b><span>{r.role}</span></div><div><strong>Task:</strong> {r.task}</div><div><strong>Feedback:</strong> {r.feedback}</div><div><strong>Change:</strong> {r.change_made||'Not entered'}</div></div>)}</div>
    </div>
  </div>
}
