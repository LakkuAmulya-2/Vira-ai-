'use client';

import Link from 'next/link';
import { ArrowRight, Brain, CheckCircle2, Compass, GraduationCap, Search, Sparkles, WalletCards } from 'lucide-react';
import { Button, Pill } from '@/components/ui';
import { careerCards, hiddenGems } from '@/lib/demo-data';

const stats = [
  ['10th → Career', 'Start with clarity'],
  ['12th → College', 'Know your next move'],
  ['Scholarships', 'Never miss an opportunity'],
  ['Admissions', 'One guided journey'],
];

export default function Home() {
  return (
    <main className="noise min-h-screen">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5 lg:px-8">
        <div className="flex items-center gap-2 text-lg font-bold tracking-tight"><div className="grid size-8 place-items-center rounded-xl bg-ink text-white"><Sparkles size={15}/></div>Vira AI</div>
        <div className="hidden items-center gap-7 text-sm text-black/55 md:flex">
          <a href="#how">How it works</a><a href="#discover">Discover</a><a href="#scholarships">Scholarships</a>
        </div>
        <Link href="/onboarding"><Button className="bg-ink text-white">Build my roadmap <ArrowRight size={16} className="ml-2"/></Button></Link>
      </nav>

      <section className="mx-auto grid max-w-7xl gap-10 px-6 pb-20 pt-14 lg:grid-cols-[1.06fr_.94fr] lg:px-8 lg:pt-24">
        <div className="flex flex-col justify-center">
          <Pill className="w-fit bg-white">AI-native guidance for the decisions that matter</Pill>
          <h1 className="mt-6 max-w-4xl text-5xl font-semibold leading-[.98] tracking-[-.055em] sm:text-6xl lg:text-7xl">Your next step in education, made <span className="text-accent">clear.</span></h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-black/58 sm:text-xl">Vira turns marks, interests, budget and ambitions into a personalized path across careers, courses, colleges, scholarships and admissions.</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/onboarding"><Button className="bg-accent px-6 text-white shadow-soft">Get my personalized plan <ArrowRight size={17} className="ml-2"/></Button></Link>
            <Link href="#discover"><Button className="border border-black/10 bg-white">Explore hidden paths</Button></Link>
          </div>
          <div className="mt-10 grid max-w-2xl grid-cols-2 gap-3 sm:grid-cols-4">
            {stats.map(([big, small]) => <div key={big} className="rounded-2xl border border-black/8 bg-white/70 p-4"><div className="text-sm font-semibold">{big}</div><div className="mt-1 text-xs text-black/45">{small}</div></div>)}
          </div>
        </div>

        <div className="relative min-h-[560px] rounded-[2rem] border border-black/8 bg-white p-5 shadow-soft sm:p-7">
          <div className="absolute -right-8 -top-8 size-28 rounded-full bg-lilac gradient-orb" />
          <div className="relative rounded-[1.6rem] bg-ink p-6 text-white sm:p-8">
            <div className="flex items-center justify-between"><div><div className="text-sm text-white/45">Vira AI · Career Copilot</div><div className="mt-2 text-2xl font-semibold tracking-tight">Let’s find your best next move.</div></div><div className="grid size-11 place-items-center rounded-2xl bg-white/10"><Brain size={19}/></div></div>
            <div className="mt-8 space-y-3">
              {['What do you enjoy learning?', 'Where do you want to study?', 'What matters most: impact, income, creativity?'].map((q, i) => <div key={q} className="rounded-2xl border border-white/10 bg-white/5 p-4"><div className="text-xs text-white/35">0{i+1}</div><div className="mt-1 text-sm font-medium">{q}</div><div className="mt-3 h-2 rounded-full bg-white/10"><div className="h-2 rounded-full bg-white/70" style={{width: `${[78,58,42][i]}%`}} /></div></div>)}
            </div>
            <div className="mt-6 rounded-2xl bg-white p-4 text-ink"><div className="flex items-center gap-2 text-sm font-semibold"><Sparkles size={15} className="text-accent"/> Early signal</div><div className="mt-2 text-sm text-black/60">You may have stronger-fit paths beyond the obvious choices.</div></div>
          </div>
          <div className="mt-5 grid grid-cols-2 gap-3">
            <div className="rounded-2xl bg-paper p-5"><Compass className="text-accent" size={19}/><div className="mt-3 font-semibold">Career fit</div><div className="mt-1 text-xs text-black/45">Evidence-backed matches</div></div>
            <div className="rounded-2xl bg-mint p-5"><WalletCards size={19}/><div className="mt-3 font-semibold">Funding</div><div className="mt-1 text-xs text-black/45">Scholarships + affordability</div></div>
          </div>
        </div>
      </section>

      <section id="how" className="border-y border-black/8 bg-white/55">
        <div className="mx-auto max-w-7xl px-6 py-20 lg:px-8">
          <div className="max-w-3xl"><Pill>One profile. One intelligent journey.</Pill><h2 className="mt-5 text-4xl font-semibold tracking-tight sm:text-5xl">From “I don’t know” to “I know what to do next.”</h2></div>
          <div className="mt-12 grid gap-4 md:grid-cols-4">
            {[['01','Discover','Understand your strengths, interests and constraints.'],['02','Decide','Compare careers, courses and colleges that fit you.'],['03','Prepare','Track exams, scholarships, documents and deadlines.'],['04','Act','Move through applications with guided next-best actions.']].map(([n,t,d]) => <div key={n} className="rounded-[1.5rem] border border-black/8 bg-white p-6"><div className="text-xs font-bold text-accent">{n}</div><div className="mt-12 text-xl font-semibold">{t}</div><p className="mt-2 text-sm leading-6 text-black/50">{d}</p></div>)}
          </div>
        </div>
      </section>

      <section id="discover" className="mx-auto max-w-7xl px-6 py-20 lg:px-8">
        <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-end"><div><Pill>Personalized discovery</Pill><h2 className="mt-5 text-4xl font-semibold tracking-tight sm:text-5xl">See the paths most people miss.</h2><p className="mt-4 max-w-2xl text-base leading-7 text-black/52">Vira looks beyond the default choices and explains why a path may fit you.</p></div><Link href="/onboarding" className="text-sm font-semibold">Get your matches <ArrowRight size={15} className="ml-1 inline"/></Link></div>
        <div className="mt-10 grid gap-4 lg:grid-cols-3">
          {careerCards.map((card) => <article key={card.title} className="rounded-[1.5rem] border border-black/8 bg-white p-6 shadow-[0_14px_45px_rgba(17,17,17,.05)]"><div className="flex items-center justify-between"><div className="grid size-11 place-items-center rounded-2xl bg-lilac"><GraduationCap size={19}/></div><span className="text-sm font-bold text-accent">{card.match}% fit</span></div><h3 className="mt-7 text-xl font-semibold">{card.title}</h3><p className="mt-2 text-sm leading-6 text-black/52">{card.note}</p><div className="mt-6 flex items-center gap-2 text-xs font-semibold text-black/45"><CheckCircle2 size={15} className="text-accent"/> Why it fits you</div></article>)}
        </div>
        <div className="mt-5 rounded-[1.5rem] border border-black/8 bg-ink p-7 text-white"><div className="flex flex-col justify-between gap-5 md:flex-row md:items-center"><div><div className="text-sm text-white/45">Hidden gems</div><div className="mt-2 text-2xl font-semibold tracking-tight">Opportunities you didn’t know existed.</div></div><div className="flex flex-wrap gap-2">{hiddenGems.map((g) => <span key={g} className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs text-white/75">{g}</span>)}</div></div></div>
      </section>

      <section id="scholarships" className="bg-[#EEEAFE]">
        <div className="mx-auto grid max-w-7xl gap-10 px-6 py-20 lg:grid-cols-[.85fr_1.15fr] lg:px-8">
          <div><Pill className="bg-white/70">Scholarship intelligence</Pill><h2 className="mt-5 text-4xl font-semibold tracking-tight sm:text-5xl">Don’t let money hide the opportunity.</h2><p className="mt-5 max-w-xl text-base leading-7 text-black/55">Build one student profile. See scholarships you may qualify for, what documents you need, and which deadlines matter next.</p><Link href="/onboarding"><Button className="mt-7 bg-ink text-white">Find my opportunities <Search size={16} className="ml-2"/></Button></Link></div>
          <div className="rounded-[2rem] border border-black/8 bg-white p-6 shadow-soft"><div className="flex items-center justify-between"><div className="font-semibold">Your opportunity board</div><div className="text-xs text-black/40">Vira intelligence</div></div><div className="mt-5 space-y-3">{[['Merit scholarship','High match','Apply by Oct 14'],['University grant','Strong match','Documents ready'],['Need-based support','Review needed','Income proof required']].map(([a,b,c]) => <div key={a} className="grid grid-cols-[1fr_auto] gap-4 rounded-2xl border border-black/8 p-4"><div><div className="text-sm font-semibold">{a}</div><div className="mt-1 text-xs text-black/45">{c}</div></div><div className="self-center rounded-full bg-mint px-3 py-1 text-xs font-semibold">{b}</div></div>)}</div></div>
        </div>
      </section>

      <footer className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-10 text-sm text-black/45 sm:flex-row sm:items-center sm:justify-between lg:px-8"><div className="font-semibold text-black">Vira AI</div><div>Built for better student decisions.</div></footer>
    </main>
  );
}
