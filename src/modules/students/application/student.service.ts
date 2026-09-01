import { prisma } from "@/lib/db/prisma";
import type { OnboardingInput } from "./student.schemas";

export async function upsertStudentProfile(userId: string, input: OnboardingInput) {
  const budget = input.annualBudgetMinor ? BigInt(input.annualBudgetMinor) : null;
  return prisma.$transaction(async (tx) => {
    const profile = await tx.studentProfile.upsert({
      where: { userId },
      create: {
        userId,
        dateOfBirth: input.dateOfBirth ? new Date(input.dateOfBirth) : null,
        gender: input.gender,
        countryCode: input.countryCode,
        state: input.state,
        city: input.city,
        educationStage: input.educationStage,
        preferredCountries: input.preferredCountries,
        preferredLanguages: input.preferredLanguages,
        budgetCurrency: input.budgetCurrency,
        annualBudgetMinor: budget,
        onboardingCompletedAt: new Date(),
      },
      update: {
        dateOfBirth: input.dateOfBirth ? new Date(input.dateOfBirth) : null,
        gender: input.gender,
        countryCode: input.countryCode,
        state: input.state,
        city: input.city,
        educationStage: input.educationStage,
        preferredCountries: input.preferredCountries,
        preferredLanguages: input.preferredLanguages,
        budgetCurrency: input.budgetCurrency,
        annualBudgetMinor: budget,
        onboardingCompletedAt: new Date(),
      },
    });
    await Promise.all([
      tx.studentInterest.deleteMany({ where: { studentId: profile.id } }),
      tx.studentSkill.deleteMany({ where: { studentId: profile.id } }),
      tx.careerGoal.deleteMany({ where: { studentId: profile.id } }),
    ]);
    if (input.interests.length) await tx.studentInterest.createMany({ data: input.interests.map((x) => ({ studentId: profile.id, ...x })) });
    if (input.skills.length) await tx.studentSkill.createMany({ data: input.skills.map((x) => ({ studentId: profile.id, ...x })) });
    if (input.goals.length) await tx.careerGoal.createMany({ data: input.goals.map((x) => ({ studentId: profile.id, ...x })) });
    return profile;
  });
}
