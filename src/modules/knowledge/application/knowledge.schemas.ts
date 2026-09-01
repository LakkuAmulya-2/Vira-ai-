import { z } from "zod";

const country = z.string().regex(/^[A-Z]{2}$/).optional();

export const dataSourceSchema = z.object({
  name: z.string().trim().min(2).max(200),
  baseUrl: z.string().url(),
  sourceType: z.enum(["GOVERNMENT","UNIVERSITY","INSTITUTION","EXAM_BODY","SCHOLARSHIP_PROVIDER","REGULATOR","OTHER"]),
  countryCode: country,
  jurisdiction: z.string().trim().min(2).max(160).optional(),
});

export const sourceDocumentSchema = z.object({
  sourceId: z.string().cuid(),
  url: z.string().url(),
  title: z.string().trim().max(500).optional(),
  contentHash: z.string().trim().min(16).max(256).optional(),
  fetchedAt: z.string().datetime().optional(),
  publishedAt: z.string().datetime().optional(),
  effectiveFrom: z.string().datetime().optional(),
  effectiveUntil: z.string().datetime().optional(),
});

export const knowledgeClaimSchema = z.object({
  entityType: z.enum(["CAREER","COURSE","COLLEGE","PROGRAM","EXAM","SCHOLARSHIP","ELIGIBILITY_RULE","DEADLINE"]),
  entityKey: z.string().trim().min(1).max(240),
  field: z.string().trim().min(1).max(160),
  value: z.unknown(),
  sourceId: z.string().cuid(),
  documentId: z.string().cuid().optional(),
  jurisdiction: z.string().trim().max(160).optional(),
  countryCode: country,
  effectiveFrom: z.string().datetime().optional(),
  effectiveUntil: z.string().datetime().optional(),
});

export type DataSourceInput = z.infer<typeof dataSourceSchema>;
export type SourceDocumentInput = z.infer<typeof sourceDocumentSchema>;
export type KnowledgeClaimInput = z.infer<typeof knowledgeClaimSchema>;
