const zones = [
  {id:'Z1', name:'North-West', risk:78, cls:'high'},
  {id:'Z2', name:'North-East', risk:36, cls:'medium'},
  {id:'Z3', name:'South-West', risk:58, cls:'medium'},
  {id:'Z4', name:'South-East', risk:24, cls:'low'},
];
export default function FarmMap({latest}) {
  return <div className="farm-map">
    <div className="map-header"><span>LIVE FARM ZONES</span><span className="map-live">● SIMULATION LIVE</span></div>
    <div className="field-grid">
      {zones.map((z, idx) => <div key={z.id} className={`field-zone ${z.cls} ${latest?.zone === z.name ? 'selected' : ''}`}>
        <div className="zone-id">{z.id}</div>
        <div className="zone-name">{z.name}</div>
        <div className="zone-risk">{z.risk}% risk</div>
        {latest?.zone === z.name && <div className="animal-marker">◉</div>}
      </div>)}
    </div>
    <div className="map-legend"><span><i className="dot high"></i> High risk</span><span><i className="dot medium"></i> Medium</span><span><i className="dot low"></i> Low</span></div>
  </div>
}
