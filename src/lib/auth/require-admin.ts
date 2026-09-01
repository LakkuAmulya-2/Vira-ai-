import { auth } from "@/auth";
import { NextResponse } from "next/server";

export async function requireAdmin() {
  const session = await auth();
  if (!session?.user?.id) return { error: NextResponse.json({ error: "UNAUTHORIZED" }, { status: 401 }) };
  const { prisma } = await import("@/lib/db/prisma");
  const user = await prisma.user.findUnique({ where: { id: session.user.id }, select: { role: true } });
  if (user?.role !== "ADMIN") return { error: NextResponse.json({ error: "FORBIDDEN" }, { status: 403 }) };
  return { userId: session.user.id };
}
