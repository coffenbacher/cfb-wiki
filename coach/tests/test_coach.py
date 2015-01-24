from coach.utils import extract_coach_tenures

def test_extract_coach_urban_meyer():
    tenures = extract_coach_tenures("Urban Meyer")
    assert len(tenures) == 11
    assert tenures[-7]['name'] == "Urban Meyer"
    assert tenures[-7]['team'] == "Illinois State"
    assert tenures[-7]['position'] == "QB/WR"
    assert tenures[-7]['startyear'] == "1989"
    assert tenures[-7]['endyear'] == "1989"
    assert tenures[-5]['name'] == "Urban Meyer"
    assert tenures[-5]['team'] == "Notre Dame"
    assert tenures[-5]['position'] == "WR"
    assert tenures[-5]['startyear'] == "1996"
    assert tenures[-5]['endyear'] == "2000"
    assert tenures[-2]['name'] == "Urban Meyer"
    assert tenures[-2]['team'] == "Florida"
    assert tenures[-2]['position'] == "HC"
    assert tenures[-2]['startyear'] == "2005"
    assert tenures[-2]['endyear'] == "2010"
    assert tenures[-1]['name'] == "Urban Meyer"
    assert tenures[-1]['team'] == "Ohio State"
    assert tenures[-1]['position'] == "HC"
    assert tenures[-1]['startyear'] == "2012"
    assert tenures[-1]['endyear'] == "2015"
    
def test_extract_coach_mark_helfrich():
    tenures = extract_coach_tenures("Mark Helfrich")
    assert len(tenures) == 6
    assert tenures[-2]['name'] == "Mark Helfrich"
    assert tenures[-2]['team'] == "Oregon"
    assert tenures[-2]['position'] == "OC/QB"
    assert tenures[-2]['startyear'] == "2009"
    assert tenures[-2]['endyear'] == "2012"
    assert tenures[-1]['name'] == "Mark Helfrich"
    assert tenures[-1]['team'] == "Oregon"
    assert tenures[-1]['position'] == "HC"
    assert tenures[-1]['startyear'] == "2013"
    assert tenures[-1]['endyear'] == "2015"