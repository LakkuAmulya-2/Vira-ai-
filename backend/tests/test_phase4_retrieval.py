from app.retrieval.embedding import cosine_similarity,deterministic_embedding
from app.retrieval.contracts import RetrievalRequest
def test_embedding_is_deterministic():
    assert deterministic_embedding("scholarship eligibility")==deterministic_embedding("scholarship eligibility")
def test_embedding_similarity():
    a=deterministic_embedding("computer science admissions")
    b=deterministic_embedding("computer science admissions requirements")
    assert cosine_similarity(a,b)>0
def test_retrieval_weights_are_valid():
    request=RetrievalRequest(query="college scholarship",lexical_weight=.4,vector_weight=.6)
    assert request.limit==12
