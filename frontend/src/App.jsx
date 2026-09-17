import { useState } from 'react';
import { LayoutDashboard, ListTree, ClipboardCheck, Leaf, Wifi, RotateCcw } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Events from './pages/Events';
import Validation from './pages/Validation';
import { api } from './lib/api';

export default function App(){
  const [page,setPage]=useState('dashboard');
  const [toast,setToast]=useState('');
  const nav=[['dashboard','Dashboard',LayoutDashboard],['events','Events',ListTree],['validation','Validation',ClipboardCheck]];
  const notify=(m)=>{setToast(m);setTimeout(()=>setToast(''),3000)};
  const reset=async()=>{await api.reset();notify('Demo data reset.');setPage('dashboard');};
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><Leaf size={22}/></div><div><b>AEGIS<span>FARM</span></b><small>Adaptive field intelligence</small></div></div>
      <div className="sidebar-badge"><Wifi size={15}/> EDGE NETWORK ONLINE</div>
      <nav>{nav.map(([id,label,Icon])=><button key={id} className={page===id?'nav-active':''} onClick={()=>setPage(id)}><Icon size={18}/>{label}</button>)}</nav>
      <div className="sidebar-bottom"><button onClick={reset}><RotateCcw size={16}/> Reset demo</button><div className="version">35% PROTOTYPE · v0.1</div></div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="breadcrumb">PROJECT BETTER TOMORROW / <b>AEGISFARM</b></div><div className="top-status"><span>●</span> Simulation mode</div></header>
      {page==='dashboard'&&<Dashboard onActivity={notify}/>} {page==='events'&&<Events/>} {page==='validation'&&<Validation/>}
      {toast&&<div className="toast">{toast}</div>}
    </main>
  </div>
}
