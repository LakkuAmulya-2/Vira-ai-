import { NextResponse } from "next/server";
import { requireAdmin } from "@/lib/auth/require-admin";
import { knowledgeClaimSchema } from "@/modules/knowledge/application/knowledge.schemas";
import { createKnowledgeClaim } from "@/modules/knowledge/application/knowledge.service";

export async function POST(request: Request) {
  const guard = await requireAdmin();
  if ("error" in guard) return guard.error;
  const parsed = knowledgeClaimSchema.safeParse(await request.json());
  if (!parsed.success) return NextResponse.json({ error: "VALIDATION_ERROR", details: parsed.error.flatten() }, { status: 422 });
  const claim = await createKnowledgeClaim(parsed.data, guard.userId);
  return NextResponse.json(claim, { status: 201 });
}
