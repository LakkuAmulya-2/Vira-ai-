"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

type Message = { role: "user" | "assistant"; content: string; signals?: {title:string;rationale:string;confidence:number}[]; questions?: string[] };

export default function CareerPage() {
  const [messages, setMessages] = useState<Message[]>([{role:"assistant",content:"Tell me what you're curious about. You don't need to know your career yet — we'll explore it together."}]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;
    setMessages(prev=>[...prev,{role:"user",content:text}]);
    setInput(""); setLoading(true);
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(base + "/api/v1/chat/", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,profile:{}})});
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setMessages(prev=>[...prev,{role:"assistant",content:data.answer,signals:data.data?.signals,questions:data.follow_up_questions}]);
    } catch {
      setMessages(prev=>[...prev,{role:"assistant",content:"I couldn't reach the intelligence service. Please try again when the backend is available."}]);
    } finally {setLoading(false);}
  }

  return <main className="chat-shell">
    <aside className="chat-side"><Link href="/" className="brand">VIRA<span>AI</span></Link><div className="chat-label">CAREER EXPLORATION</div><p>Explore possibilities with evidence and questions, not deterministic predictions.</p><Link href="/dashboard">← Dashboard</Link></aside>
    <section className="chat-main">
      <header><span className="eyebrow">CONVERSATION WITH VIRA</span><h1>Let's explore what could fit.</h1></header>
      <div className="messages">
        {messages.map((m,i)=><div key={i} className={"message "+m.role}>
          <div className="message-role">{m.role==="assistant"?"VIRA":"YOU"}</div><p>{m.content}</p>
          {m.signals?.map(s=><article className="signal-card" key={s.title}><strong>{s.title}</strong><p>{s.rationale}</p><small>Exploration confidence: {Math.round(s.confidence*100)}%</small></article>)}
          {m.questions?.length ? <div className="questions">{m.questions.map(q=><button key={q} onClick={()=>setInput(q)}>{q}</button>)}</div> : null}
        </div>)}
        {loading && <div className="thinking">Vira is thinking…</div>}
      </div>
      <form onSubmit={send} className="composer"><textarea value={input} onChange={e=>setInput(e.target.value)} placeholder="For example: I enjoy technology, but I'm not sure which field is right for me..." /><button className="primary" disabled={loading}>Send →</button></form>
    </section>
  </main>;
}
