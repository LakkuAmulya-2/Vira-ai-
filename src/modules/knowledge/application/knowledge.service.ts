import { VerificationStatus } from "@prisma/client";
import { prisma } from "@/lib/db/prisma";
import type { DataSourceInput, SourceDocumentInput, KnowledgeClaimInput } from "./knowledge.schemas";

export async function createDataSource(input: DataSourceInput, actorId: string) {
  const source = await prisma.dataSource.create({ data: { ...input, verificationStatus: VerificationStatus.PENDING } });
  await prisma.auditLog.create({ data: { actorId, action: "KNOWLEDGE_SOURCE_CREATED", resource: source.id } });
  return source;
}

export async function registerSourceDocument(input: SourceDocumentInput, actorId: string) {
  const document = await prisma.sourceDocument.create({
    data: {
      ...input,
      fetchedAt: input.fetchedAt ? new Date(input.fetchedAt) : undefined,
      publishedAt: input.publishedAt ? new Date(input.publishedAt) : undefined,
      effectiveFrom: input.effectiveFrom ? new Date(input.effectiveFrom) : undefined,
      effectiveUntil: input.effectiveUntil ? new Date(input.effectiveUntil) : undefined,
      status: VerificationStatus.PENDING,
    },
  });
  await prisma.auditLog.create({ data: { actorId, action: "SOURCE_DOCUMENT_REGISTERED", resource: document.id } });
  return document;
}

export async function createKnowledgeClaim(input: KnowledgeClaimInput, actorId: string) {
  const claim = await prisma.knowledgeClaim.create({
    data: {
      ...input,
      effectiveFrom: input.effectiveFrom ? new Date(input.effectiveFrom) : undefined,
      effectiveUntil: input.effectiveUntil ? new Date(input.effectiveUntil) : undefined,
      status: VerificationStatus.PENDING,
    },
  });
  await prisma.auditLog.create({ data: { actorId, action: "KNOWLEDGE_CLAIM_CREATED", resource: claim.id } });
  return claim;
}

export async function verifyKnowledgeClaim(claimId: string, actorId: string) {
  return prisma.$transaction(async (tx) => {
    const claim = await tx.knowledgeClaim.update({
      where: { id: claimId },
      data: { status: VerificationStatus.VERIFIED, verifiedAt: new Date() },
    });
    await tx.auditLog.create({ data: { actorId, action: "KNOWLEDGE_CLAIM_VERIFIED", resource: claimId } });
    return claim;
  });
}
