from coach.utils import extract_coach_tenures


# This function tests basic functionality
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

#This function tests disambiguation
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
    
#This function tests a different brand of disambiguation
def test_extract_coach_mike_leach():
    tenures = extract_coach_tenures("Mike Leach")
    assert len(tenures) == 9
    assert tenures[-5]['name'] == "Mike Leach"
    assert tenures[-5]['team'] == "Valdosta State"
    assert tenures[-5]['position'] == "OC"
    assert tenures[-5]['startyear'] == "1992"
    assert tenures[-5]['endyear'] == "1996"

# This function tests a different breaking of lines
def test_extract_coach_bobby_bowden():
    tenures = extract_coach_tenures("Bobby Bowden")
    assert len(tenures) == 7
    
# This function tests a different breaking of lines
def test_extract_coach_tommy_tuberville():
    tenures = extract_coach_tenures("Tommy Tuberville")
    assert len(tenures) == 7
    assert int(tenures[0]['endyear'])
    assert int(tenures[0]['startyear'])