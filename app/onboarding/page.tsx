'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, ArrowRight, Check, MapPin, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui';

const steps = [
  { title: 'Where are you in your journey?', options: ['After 10th', 'After 12th', 'Already in college'] },
  { title: 'What do you enjoy most?', options: ['Building & technology', 'Biology & health', 'Business & people', 'Design & creativity', 'Law, society & policy'] },
  { title: 'Where would you like to study?', options: ['Near home', 'Anywhere in India', 'US / UK / EU', 'Gulf countries', 'I am not sure yet'] },
  { title: 'What matters most right now?', options: ['Career fit', 'Affordable education', 'Top colleges', 'Scholarships', 'Fastest path to a career'] },
];

export default function OnboardingPage() {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const current = steps[step];
  const done = step === steps.length - 1 && answers[step];

  const pick = (value: string) => setAnswers((a) => ({ ...a, [step]: value }));
  const next = () => { if (!answers[step]) return; if (step < steps.length - 1) setStep(step + 1); else setStep(steps.length); };

  if (step >= steps.length) return <main className="min-h-screen bg-paper px-6 py-8"><div className="mx-auto max-w-2xl"><Link href="/" className="text-sm font-semibold"><ArrowLeft size={15} className="mr-1 inline"/> Home</Link><div className="mt-16 rounded-[2rem] border border-black/8 bg-white p-8 shadow-soft sm:p-12"><div className="grid size-14 place-items-center rounded-2xl bg-mint"><Sparkles size={22}/></div><h1 className="mt-7 text-4xl font-semibold tracking-tight">Your Vira journey is ready.</h1><p className="mt-4 text-base leading-7 text-black/52">We have enough signal to start building your first personalized roadmap. Next, we’ll refine it with your marks, subjects, goals and budget.</p><div className="mt-8 space-y-3">{Object.entries(answers).map(([i,v]) => <div key={i} className="flex items-center justify-between rounded-2xl border border-black/8 p-4"><span className="text-sm text-black/45">{steps[Number(i)].title}</span><span className="text-sm font-semibold">{v}</span></div>)}</div><Link href="/" className="mt-8 block"><Button className="w-full bg-ink text-white">Continue to Vira <ArrowRight size={16} className="ml-2"/></Button></Link></div></div></main>;

  return <main className="min-h-screen bg-paper px-6 py-8"><div className="mx-auto max-w-2xl"><div className="flex items-center justify-between"><Link href="/" className="text-sm font-semibold"><ArrowLeft size={15} className="mr-1 inline"/> Back</Link><div className="text-xs font-semibold text-black/40">{step + 1} / {steps.length}</div></div><div className="mt-6 h-1.5 overflow-hidden rounded-full bg-black/8"><div className="h-full rounded-full bg-accent transition-all" style={{width: `${((step + 1) / steps.length) * 100}%`}}/></div><div className="mt-16"><div className="text-sm font-semibold text-accent">Build your personal signal</div><h1 className="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">{current.title}</h1><div className="mt-9 space-y-3">{current.options.map((option) => <button key={option} onClick={() => pick(option)} className={`flex w-full items-center justify-between rounded-2xl border p-5 text-left transition ${answers[step] === option ? 'border-accent bg-lilac' : 'border-black/8 bg-white hover:-translate-y-0.5 hover:shadow-soft'}`}><span className="font-medium">{option}</span>{answers[step] === option && <Check size={18} className="text-accent"/>}</button>)}</div><div className="mt-7 flex justify-between text-xs text-black/40"><span className="flex items-center gap-1"><MapPin size={13}/> Your answers stay part of your profile</span>{done ? 'Almost there' : 'Takes about 60 seconds'}</div><Button disabled={!answers[step]} onClick={next} className="mt-8 w-full bg-ink text-white disabled:cursor-not-allowed disabled:opacity-30">{step === steps.length - 1 ? 'Build my roadmap' : 'Continue'} <ArrowRight size={16} className="ml-2"/></Button></div></div></main>;
}
