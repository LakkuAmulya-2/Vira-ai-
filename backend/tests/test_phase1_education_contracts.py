from app.education.schemas import CountryCreate, InstitutionCreate, ProgramCreate
def test_country_normal_contract():
    assert CountryCreate(iso_code="IN",name="India",region="South Asia").iso_code=="IN"
def test_institution_contract():
    assert InstitutionCreate(canonical_name="X University",country_code="US",institution_type="UNIVERSITY").country_code=="US"
def test_program_duration_positive():
    assert ProgramCreate(institution_id="a",course_id="b",official_name="CS",duration_months=48).duration_months==48
