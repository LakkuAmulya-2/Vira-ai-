"use client";

import Link from "next/link";
import { useState } from "react";

type Action = { id:string; title:string; category:string; status:"READY"|"BLOCKED"|"NEEDS_REVIEW"; depends_on:string[]; reasons:string[]; missing_information:string[] };

const fallback: Action[] = [
  {id:"profile",title:"Complete student intelligence profile",category:"PROFILE",status:"READY",depends_on:[],reasons:["Start by giving Vira enough context."],missing_information:[]},
  {id:"career",title:"Validate career direction",category:"CAREER",status:"BLOCKED",depends_on:["profile"],reasons:["Profile context is required first."],missing_information:["interests"]},
  {id:"course",title:"Select course pathways",category:"COURSE",status:"BLOCKED",depends_on:["career"],reasons:["Career direction should be explored first."],missing_information:["intended_program"]},
  {id:"college",title:"Build verified college shortlist",category:"COLLEGE",status:"BLOCKED",depends_on:["course"],reasons:["Matching needs verified academic and budget context."],missing_information:["target_country","academics","budget"]},
  {id:"scholarship",title:"Check scholarship eligibility",category:"FUNDING",status:"BLOCKED",depends_on:["college"],reasons:["Eligibility depends on destination and student context."],missing_information:["household_income"]},
  {id:"exams",title:"Check entrance and language requirements",category:"EXAM",status:"BLOCKED",depends_on:["college"],reasons:["Requirements depend on program and destination."],missing_information:["target_country"]},
  {id:"documents",title:"Prepare application documents",category:"DOCUMENTS",status:"BLOCKED",depends_on:["college"],reasons:["Document requirements should be verified per application."],missing_information:["full_name"]},
  {id:"timeline",title:"Generate deadline timeline",category:"TIMELINE",status:"BLOCKED",depends_on:["documents"],reasons:["Timeline is generated from verified opportunities."],missing_information:["target_intake","target_country"]}
];

export default function JourneyPage() {
  const [actions,setActions]=useState<Action[]>(fallback);
  const [loading,setLoading]=useState(false);

  async function generatePlan(){
    setLoading(true);
    try{
      const base=process.env.NEXT_PUBLIC_API_URL||"";
      const res=await fetch(base+"/api/v1/admissions/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({profile:{},goal:{}})});
      if(!res.ok) throw new Error();
      const data=await res.json();
      if(Array.isArray(data.actions)) setActions(data.actions);
    }catch{} finally{setLoading(false);}
  }

  const next=actions.find(a=>a.status==="READY")||actions[0];
  return <main className="journey-shell">
    <aside className="journey-sidebar"><Link href="/" className="brand">VIRA<span>AI</span></Link><div className="workspace">ADMISSION JOURNEY</div><Link href="/dashboard">Overview</Link><Link href="/career">Talk to Vira</Link><Link className="side-active" href="/journey">Action center</Link><div className="journey-note">Autonomous planning never submits an application without your approval.</div></aside>
    <section className="journey-main">
      <header className="journey-header"><div><span className="eyebrow">YOUR ACTION CENTER</span><h1>Turn decisions into momentum.</h1><p>Vira organizes your admission journey into explainable, dependency-aware actions.</p></div><button className="primary" onClick={generatePlan} disabled={loading}>{loading?"Generating…":"Refresh my plan →"}</button></header>
      <section className="journey-next"><div><span className="eyebrow">NEXT BEST ACTION</span><h2>{next?.title}</h2><p>{next?.reasons?.[0]||"Complete this step to unlock more of your journey."}</p>{next?.missing_information?.length?<div className="missing">{next.missing_information.map(x=><span key={x}>Needs: {x.replaceAll("_"," ")}</span>)}</div>:null}</div><Link className="dark-button" href={next?.id==="career"?"/career":"/onboarding"}>Take action →</Link></section>
      <section className="journey-list">
        <div className="list-head"><span className="eyebrow">JOURNEY MAP</span><span>{actions.filter(a=>a.status==="READY").length} ready · {actions.length} total</span></div>
        {actions.map((a,i)=><article className={"action-row "+a.status.toLowerCase()} key={a.id}><div className="action-index">{String(i+1).padStart(2,"0")}</div><div className="action-title"><h3>{a.title}</h3><p>{a.reasons?.[0]}</p>{a.depends_on.length>0&&<small>Depends on: {a.depends_on.join(", ")}</small>}</div><div className="action-status"><span>{a.status.replace("_"," ")}</span>{a.missing_information.length>0&&<small>{a.missing_information.length} details needed</small>}</div><Link href={a.id==="career"?"/career":"/onboarding"}>Open →</Link></article>)}
      </section>
      <section className="journey-safety"><span className="eyebrow">AUTONOMY WITH CONTROL</span><h2>Vira can plan, track and prepare. You approve important actions.</h2><div><article><b>01</b><p>Verified information before recommendations</p></article><article><b>02</b><p>Visible uncertainty when information is missing</p></article><article><b>03</b><p>Explicit approval before external actions</p></article></div></section>
    </section>
  </main>;
}
