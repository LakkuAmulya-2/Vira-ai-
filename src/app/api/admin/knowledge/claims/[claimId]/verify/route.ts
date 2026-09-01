import { NextResponse } from "next/server";
import { requireAdmin } from "@/lib/auth/require-admin";
import { verifyKnowledgeClaim } from "@/modules/knowledge/application/knowledge.service";

export async function POST(_: Request, context: { params: Promise<{ claimId: string }> }) {
  const guard = await requireAdmin();
  if ("error" in guard) return guard.error;
  const { claimId } = await context.params;
  const claim = await verifyKnowledgeClaim(claimId, guard.userId);
  return NextResponse.json(claim);
}
