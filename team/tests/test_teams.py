from team.utils import extract_teams


# This function tests basic functionality
def test_extract_teams():
    teams = extract_teams()
    assert len(teams) == 127
    print teams[0:5]