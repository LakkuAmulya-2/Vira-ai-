import { NextResponse } from "next/server";
import { requireAdmin } from "@/lib/auth/require-admin";
import { dataSourceSchema } from "@/modules/knowledge/application/knowledge.schemas";
import { createDataSource } from "@/modules/knowledge/application/knowledge.service";

export async function POST(request: Request) {
  const guard = await requireAdmin();
  if ("error" in guard) return guard.error;
  const parsed = dataSourceSchema.safeParse(await request.json());
  if (!parsed.success) return NextResponse.json({ error: "VALIDATION_ERROR", details: parsed.error.flatten() }, { status: 422 });
  const source = await createDataSource(parsed.data, guard.userId);
  return NextResponse.json(source, { status: 201 });
}
