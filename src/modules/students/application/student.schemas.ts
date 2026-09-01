import { z } from "zod";

const isoCountry = z.string().regex(/^[A-Z]{2}$/, "Use ISO 3166-1 alpha-2 country code");
const currency = z.string().regex(/^[A-Z]{3}$/, "Use ISO 4217 currency code");

export const onboardingSchema = z.object({
  dateOfBirth: z.string().date().optional(),
  gender: z.enum(["FEMALE", "MALE", "NON_BINARY", "PREFER_NOT_TO_SAY"]).optional(),
  countryCode: isoCountry,
  state: z.string().trim().min(1).max(120).optional(),
  city: z.string().trim().min(1).max(120).optional(),
  educationStage: z.enum(["AFTER_10", "AFTER_12", "UNDERGRADUATE", "OTHER"]),
  preferredCountries: z.array(isoCountry).max(20).default([]),
  preferredLanguages: z.array(z.string().trim().min(1).max(80)).max(20).default([]),
  budgetCurrency: currency.optional(),
  annualBudgetMinor: z.string().regex(/^\d+$/).optional(),
  interests: z.array(z.object({ name: z.string().trim().min(1).max(120), weight: z.number().int().min(1).max(10).default(1) })).max(50).default([]),
  skills: z.array(z.object({ name: z.string().trim().min(1).max(120), proficiency: z.number().int().min(1).max(5).optional() })).max(50).default([]),
  goals: z.array(z.object({ title: z.string().trim().min(1).max(160), priority: z.number().int().min(1).max(10).default(1) })).max(20).default([]),
});
export type OnboardingInput = z.infer<typeof onboardingSchema>;
