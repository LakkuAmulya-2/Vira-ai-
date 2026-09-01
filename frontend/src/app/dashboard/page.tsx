"use client";

import Link from "next/link";
import { useState } from "react";

const modules = [
  ["Career paths", "Explore directions after your profile is analyzed."],
  ["Courses", "Compare established and emerging programs."],
  ["Colleges", "Match institutions using eligibility and verified data."],
  ["Scholarships", "Track funding opportunities relevant to you."],
];

export default function DashboardPage() {
  const [complete, setComplete] = useState(false);
  const progress = complete ? 78 : 64;
  return <main className="dashboard-shell">
    <aside className="sidebar">
      <Link href="/" className="brand">VIRA<span>AI</span></Link>
      <div className="workspace">STUDENT WORKSPACE</div>
      {["Overview","Career paths","Courses","Colleges","Funding","Timeline"].map((item,i)=><button key={item} className={i===0?"selected":""}>{item}</button>)}
      <div className="sidebar-bottom"><i/> Intelligence system online</div>
    </aside>
    <section className="dashboard">
      <header className="dashboard-header"><div><span className="eyebrow">YOUR DECISION SYSTEM</span><h1>Good to see you.</h1></div><Link href="/onboarding" className="profile-link">Update profile ↗</Link></header>
      <section className="hero-panel">
        <div className="profile-ring" style={{"--p":progress} as React.CSSProperties}><strong>{progress}%</strong></div>
        <div><span className="eyebrow">STUDENT INTELLIGENCE</span><h2>Your context is getting clearer.</h2><p>Complete remaining details to improve eligibility, affordability and recommendation quality.</p></div>
        <button className="dark-button" onClick={()=>setComplete(!complete)}>{complete?"Profile updated ✓":"Complete profile →"}</button>
      </section>
      <section className="metrics">{modules.map(([title,text])=><article key={title}><strong>—</strong><h3>{title}</h3><p>{text}</p></article>)}</section>
      <section className="next-action"><div><span className="eyebrow">NEXT BEST ACTION</span><h2>{complete?"Start exploring career directions.":"Add your academic history."}</h2><p>{complete?"Vira has enough context to begin structured exploration.":"Your latest qualification and score help evaluate realistic pathways."}</p></div><Link href="/onboarding" className="primary">{complete?"Explore paths →":"Continue onboarding →"}</Link></section>
      <section className="dashboard-grid">
        <article className="activity"><span className="eyebrow">JOURNEY STATUS</span>{["Student intelligence","Career discovery","Course discovery","College matching","Funding & scholarships","Action timeline"].map((x,i)=><div className="journey-row" key={x}><div><i className={i===0?"active-dot":""}/>{x}</div><span>{i===0?"In progress":"Not started"}</span></div>)}</article>
        <article className="deadlines"><span className="eyebrow">UPCOMING DEADLINES</span><h3>Your personalized timeline will appear here.</h3><p>Deadlines are shown only when Vira has verified opportunities relevant to your profile.</p></article>
      </section>
    </section>
  </main>;
}