const steps = ['DETECT','IDENTIFY','PREDICT','DETER','OBSERVE','ADAPT','VERIFY','LEARN'];
export default function FlowStrip({active=0}) {
  return <div className="flow-strip">
    {steps.map((step, i) => <div key={step} className={`flow-step ${i <= active ? 'active' : ''}`}>
      <span>{String(i+1).padStart(2,'0')}</span>{step}
    </div>)}
  </div>;
}
