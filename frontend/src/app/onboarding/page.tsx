"use client";

import { FormEvent, useMemo, useState } from "react";

const questions = [
  { key: "education_stage", label: "Where are you right now?", placeholder: "After 10th, After 12th, Undergraduate..." },
  { key: "interests", label: "What genuinely interests you?", placeholder: "Technology, design, biology..." },
  { key: "career_goals", label: "What would you like to explore?", placeholder: "Building products, research, helping people..." },
  { key: "preferred_countries", label: "Where are you open to studying?", placeholder: "India, Germany, UK..." },
  { key: "budget", label: "What annual budget should we respect?", placeholder: "Enter amount in your local currency" },
];

export default function OnboardingPage() {
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string,string>>({});
  const [loading, setLoading] = useState(false);
  const current = questions[index];
  const progress = useMemo(()=>((index+1)/questions.length)*100,[index]);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (index < questions.length-1) return setIndex(index+1);
    setLoading(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "";
      const payload = {
        education_stage: answers.education_stage || "UNKNOWN",
        country_code: "IN",
        interests: (answers.interests || "").split(",").map(x=>x.trim()).filter(Boolean),
        career_goals: (answers.career_goals || "").split(",").map(x=>x.trim()).filter(Boolean),
        preferred_countries: (answers.preferred_countries || "").split(",").map(x=>x.trim()).filter(Boolean),
        annual_budget_minor: Number(answers.budget || 0) || undefined,
      };
      await fetch(base + "/api/v1/student-intelligence/profile", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
    } finally { setLoading(false); }
  }

  return <main className="onboarding">
    <div className="top"><a href="/">← VIRA</a><span>{index+1} / {questions.length}</span></div>
    <div className="progress"><i style={{width: progress+"%"}} /></div>
    <form onSubmit={submit} className="question">
      <div className="eyebrow">STUDENT INTELLIGENCE</div>
      <h1>{current.label}</h1>
      <p>There are no right answers. Vira uses your context to make better decisions with you.</p>
      <textarea autoFocus value={answers[current.key] || ""} placeholder={current.placeholder} onChange={e=>setAnswers({...answers,[current.key]:e.target.value})} />
      <div className="form-actions">
        <button type="button" disabled={index===0} onClick={()=>setIndex(index-1)}>Back</button>
        <button className="primary" disabled={loading}>{loading ? "Building profile..." : index===questions.length-1 ? "Build my profile →" : "Continue →"}</button>
      </div>
    </form>
  </main>;
}
