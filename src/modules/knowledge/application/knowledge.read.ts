import { KnowledgeEntityType, VerificationStatus } from "@prisma/client";
import { prisma } from "@/lib/db/prisma";

export async function findCurrentVerifiedClaims(entityType: KnowledgeEntityType, entityKey: string) {
  const now = new Date();
  return prisma.knowledgeClaim.findMany({
    where: {
      entityType,
      entityKey,
      status: VerificationStatus.VERIFIED,
      OR: [{ effectiveUntil: null }, { effectiveUntil: { gt: now } }],
    },
    include: { source: true, document: true },
    orderBy: [{ verifiedAt: "desc" }, { updatedAt: "desc" }],
  });
}
