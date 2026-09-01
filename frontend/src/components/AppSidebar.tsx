"use client";
import Link from "next/link";
import {usePathname} from "next/navigation";
const items=[["Overview","/dashboard"],["Career","/career"],["Courses","/courses"],["Colleges","/colleges"],["Scholarships","/scholarships"],["Exams","/exams"],["Action plan","/journey"]];
export function AppSidebar({label="STUDENT WORKSPACE"}:{label?:string}){const path=usePathname();return <aside className="app-sidebar"><Link href="/" className="brand">VIRA<span>AI</span></Link><div className="workspace">{label}</div><nav>{items.map(([name,href])=><Link key={href} className={path===href?"selected":""} href={href}>{name}</Link>)}</nav><div className="sidebar-bottom"><i/> AI intelligence online</div></aside>}