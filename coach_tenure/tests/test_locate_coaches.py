from coach.utils import get_names_current_coaches_and_coordinators

def test_current_coaches_and_coordinators():
    # http://en.wikipedia.org/wiki/List_of_current_NCAA_Division_I_FBS_football_coaches
    names = get_names_current_coaches_and_coordinators()
    
    # Subtract 10 to handle vacancies
    assert 128*3 - 10 < len(names)