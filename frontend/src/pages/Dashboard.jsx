import { useEffect, useState } from 'react';
import { ShieldCheck, RadioTower, Radar, Activity, BellRing, Zap, RefreshCcw } from 'lucide-react';
import MetricCard from '../components/MetricCard';
import FlowStrip from '../components/FlowStrip';
import FarmMap from '../components/FarmMap';
import { api } from '../lib/api';

export default function Dashboard({onActivity}) {
  const [data, setData] = useState(null);
  const [busy, setBusy] = useState(false);
  const [mode, setMode] = useState('normal');

  const load = async () => setData(await api.dashboard());
  useEffect(() => { load(); }, []);

  const simulate = async (noResponse=false) => {
    setBusy(true);
    try {
      await api.simulate({species:'wild_boar', confidence:0.94, zone:'North-West', direction:'South-East', threat_state:'Approaching Crop', simulate_no_response:noResponse});
      await load();
      onActivity?.(noResponse ? 'Adaptive retry completed — retreat verified.' : 'Intrusion simulated — deterrence verified.');
    } finally { setBusy(false); }
  };

  if (!data) return <div className="loading">Booting AEGISFARM…</div>;
  const latest = data.latest_detection;
  return <div className="page">
    <div className="hero-row">
      <div>
        <div className="eyebrow"><span className="pulse"></span> EDGE-AI PROTECTION NETWORK</div>
        <h1>One farm.<br/><span>One intelligent boundary.</span></h1>
        <p className="hero-copy">AEGISFARM closes the loop between animal intrusion and verified retreat.</p>
      </div>
      <div className="hero-actions">
        <button className="btn primary" onClick={() => simulate(false)} disabled={busy}><Zap size={17}/>{busy ? 'Running…' : 'Simulate Intrusion'}</button>
        <button className="btn secondary" onClick={() => simulate(true)} disabled={busy}><RefreshCcw size={17}/>Simulate No Response</button>
      </div>
    </div>

    <FlowStrip active={latest ? 7 : 1}/>

    <div className="metrics">
      <MetricCard label="FARM STATUS" value={data.farm.status} hint={`${data.farm.nodes_online} edge nodes online`} tone="success" />
      <MetricCard label="INTRUSIONS" value={data.stats.total_intrusions} hint="events recorded" />
      <MetricCard label="VERIFIED RETREATS" value={data.stats.verified_retreats} hint="closed-loop outcomes" tone="success" />
      <MetricCard label="RESPONSE MEMORY" value={data.stats.response_memory_entries} hint="learned strategy records" tone="accent" />
    </div>

    <div className="grid-two">
      <FarmMap latest={latest}/>
      <div className="panel incident-panel">
        <div className="panel-title"><span><Radar size={18}/> LATEST EVENT</span><span className="tag">PROTOTYPE</span></div>
        {latest ? <>
          <div className="incident-main">
            <div className="animal-symbol">🐗</div>
            <div><div className="incident-name">{latest.species}</div><div className="muted">{latest.confidence*100}% confidence · {latest.zone}</div></div>
          </div>
          <div className="event-grid">
            <div><span>Threat state</span><b>{latest.threat_state}</b></div>
            <div><span>Direction</span><b>{latest.direction}</b></div>
            <div><span>Action</span><b>Deterrence Active</b></div>
            <div><span>Status</span><b className="good">Retreat Confirmed ✓</b></div>
          </div>
          <div className="response-card"><ShieldCheck size={24}/><div><b>Closed loop complete</b><p>System observed the response and updated farm memory.</p></div></div>
        </> : <div className="empty-state">No intrusion event yet. Start the simulation.</div>}
      </div>
    </div>

    <div className="grid-three">
      <div className="panel"><div className="panel-title"><span><RadioTower size={18}/> SENSOR NETWORK</span></div>
        {['AI camera node 01','PIR sensor node 02','Audio node 03'].map((x)=><div className="list-row" key={x}><span>{x}</span><span className="online">ONLINE</span></div>)}
      </div>
      <div className="panel"><div className="panel-title"><span><BellRing size={18}/> FARMER ALERT</span></div>
        <div className="alert-box"><b>Wild Boar detected</b><span>North-West · Action active</span><em>Retreat confirmed</em></div>
      </div>
      <div className="panel"><div className="panel-title"><span><Activity size={18}/> RESPONSE MODE</span></div>
        <div className="mode-buttons">{['normal','adaptive'].map(m=><button key={m} className={mode===m?'selected':''} onClick={()=>setMode(m)}>{m}</button>)}</div>
        <p className="small-copy">{mode==='adaptive' ? 'Adaptive retry is enabled: if the first permitted response is ineffective, the engine selects the next approved strategy.' : 'First-line strategy is selected from safety rules and farm response memory.'}</p>
      </div>
    </div>
  </div>
}
