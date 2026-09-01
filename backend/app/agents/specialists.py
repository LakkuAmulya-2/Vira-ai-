from app.agents.contracts import AgentName, AgentResult


class SpecialistAgent:
    name: AgentName

    async def run(self, message: str, user_id: str) -> AgentResult:
        raise NotImplementedError


class CareerAgent(SpecialistAgent):
    name = AgentName.CAREER

    async def run(self, message: str, user_id: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            answer="Career analysis requires verified knowledge and deterministic ranking.",
            actions=["load_student_profile", "retrieve_verified_careers", "rank_candidates"],
        )


class AdmissionsAgent(SpecialistAgent):
    name = AgentName.ADMISSIONS

    async def run(self, message: str, user_id: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            answer="Admissions planning is grounded in verified eligibility, deadlines and institution data.",
            actions=["check_eligibility", "retrieve_requirements", "build_action_plan"],
        )


class ScholarshipAgent(SpecialistAgent):
    name = AgentName.SCHOLARSHIP

    async def run(self, message: str, user_id: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            answer="Scholarship matching must use verified eligibility and current deadlines.",
            actions=["load_profile", "filter_eligibility", "rank_scholarships"],
        )


class ExamAgent(SpecialistAgent):
    name = AgentName.EXAM

    async def run(self, message: str, user_id: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            answer="Exam planning uses verified exam requirements and date data.",
            actions=["retrieve_exam_requirements", "create_preparation_plan"],
        )


class ResearchAgent(SpecialistAgent):
    name = AgentName.RESEARCH

    async def run(self, message: str, user_id: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            answer="Research results are candidates until provenance verification is complete.",
            actions=["discover_sources", "collect_documents", "submit_for_verification"],
            requires_human_review=True,
        )


class RecommendationAgent(SpecialistAgent):
    name = AgentName.RECOMMENDATION

    async def run(self, message: str, user_id: str) -> AgentResult:
        return AgentResult(
            agent=self.name,
            answer="Recommendations are generated from profile constraints and verified evidence.",
            actions=["hard_filter", "deterministic_score", "attach_evidence", "explain"],
        )
