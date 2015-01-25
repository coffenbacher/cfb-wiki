from coach.utils import *

def test_is_football_coach_wiki():
    assert not is_football_coach_wiki("Dave Nichol")
    assert not is_football_coach_wiki("Mark Helfrich (film editor)")
    assert is_football_coach_wiki("Urban Meyer")