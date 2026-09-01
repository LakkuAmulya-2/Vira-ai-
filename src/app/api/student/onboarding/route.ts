import { auth } from "@/auth";
import { onboardingSchema } from "@/modules/students/application/student.schemas";
import { upsertStudentProfile } from "@/modules/students/application/student.service";
import { NextResponse } from "next/server";

export async function PUT(request: Request) {
  const session = await auth();
  if (!session?.user?.id) return NextResponse.json({ error: "UNAUTHORIZED" }, { status: 401 });
  const body = await request.json();
  const parsed = onboardingSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: "VALIDATION_ERROR", details: parsed.error.flatten() }, { status: 422 });
  const profile = await upsertStudentProfile(session.user.id, parsed.data);
  return NextResponse.json({ id: profile.id, updatedAt: profile.updatedAt.toISOString() });
}
