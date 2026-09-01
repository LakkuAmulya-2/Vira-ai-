"use client";

import { useState } from "react";
import Link from "next/link";

const steps = ["Discover", "Profile", "Explore", "Plan"];

export default function HomePage() {
  const [active, setActive] = useState(0);
  return (
    <main className="shell">
      <nav className="nav">
        <div className="brand">VIRA<span>AI</span></div>
        <div className="navlinks"><a href="#journey">Journey</a><a href="#intelligence">Intelligence</a><Link href="/onboarding">Get started</Link></div>
      </nav>
      <section className="hero">
        <div className="eyebrow">AI-NATIVE STUDENT DECISION OS</div>
        <h1>From confusion to your next <em>best decision.</em></h1>
        <p>Career, courses, colleges, scholarships, exams and deadlines — connected into one intelligent journey.</p>
        <div className="actions"><Link className="primary" href="/onboarding">Build my path →</Link><a className="secondary" href="#journey">See how it works</a></div>
        <div className="signal"><span></span> Built for decisions after 10th & 12th — and beyond</div>
      </section>
      <section id="journey" className="journey">
        <div className="section-head"><div><div className="eyebrow">ONE CONNECTED JOURNEY</div><h2>Every question. One system.</h2></div><p>Vira does not stop at recommendations. It turns decisions into an actionable plan.</p></div>
        <div className="stepper">{steps.map((step, i)=><button key={step} onClick={()=>setActive(i)} className={active===i?"active":""}><b>0{i+1}</b>{step}</button>)}</div>
        <div className="journey-card">
          <div><span>STEP 0{active+1}</span><h3>{["Understand the student","Build decision context","Match verified opportunities","Create the action plan"][active]}</h3><p>{["Start with your academic stage, interests and constraints.","Identify missing information with adaptive questions.","Explore careers, courses, colleges and scholarships using verified knowledge.","Prioritize deadlines and next actions in one timeline."][active]}</p></div>
          <div className="orb"><div className="orb-core">V</div><i></i><i></i><i></i></div>
        </div>
      </section>
      <section id="intelligence" className="grid">
        {[
          ["Student Intelligence","A living profile built from academics, interests, strengths, budget and constraints."],
          ["Verified Knowledge","Recommendations are grounded in source-backed education data, not random AI output."],
          ["Agentic Guidance","Specialist agents coordinate complex decisions across careers, admissions and funding."],
          ["Autonomous Plan","Deadlines, next steps and changing opportunities become a personalized action system."]
        ].map(([title, text], i)=><article key={title}><span>0{i+1}</span><h3>{title}</h3><p>{text}</p></article>)}
      </section>
      <section className="cta"><div><div className="eyebrow">START WITH CLARITY</div><h2>You don't need to know the answer yet.</h2><p>Tell Vira where you are. We'll help you discover what comes next.</p></div><Link className="primary" href="/onboarding">Start my journey →</Link></section>
    </main>
  );
}
