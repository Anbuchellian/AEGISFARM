import { useEffect, useState } from 'react';
import { Clock3, Crosshair } from 'lucide-react';
import { api } from '../lib/api';

export default function Events() {
  const [events, setEvents] = useState([]);
  const [interventions, setInterventions] = useState([]);
  useEffect(() => { Promise.all([api.detections(), api.interventions()]).then(([a,b])=>{setEvents(a);setInterventions(b)}); }, []);
  return <div className="page"><div className="section-head"><div><div className="eyebrow">EVENT INTELLIGENCE</div><h2>Detection → response timeline</h2></div></div>
    <div className="grid-two">
      <div className="panel"><div className="panel-title"><span><Crosshair size={18}/> DETECTIONS</span></div>{events.length===0?<div className="empty-state">Run a simulation first.</div>:events.map(e=><div className="timeline-row" key={e.id}><div className="timeline-dot"></div><div><b>{e.species}</b><span>{e.zone} · {Math.round(e.confidence*100)}% · {e.direction}</span></div><time>{new Date(e.detected_at).toLocaleTimeString()}</time></div>)}</div>
      <div className="panel"><div className="panel-title"><span><Clock3 size={18}/> INTERVENTIONS</span></div>{interventions.length===0?<div className="empty-state">No interventions yet.</div>:interventions.map(i=><div className="timeline-row" key={i.id}><div className={`timeline-dot ${i.outcome==='retreated'?'good-dot':''}`}></div><div><b>{i.strategy}</b><span>{i.outcome} · {i.response_time_ms} ms</span></div><time>{new Date(i.created_at).toLocaleTimeString()}</time></div>)}</div>
    </div>
  </div>
}
