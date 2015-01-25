from coach.utils import *
import logging
log = logging.getLogger()


def test_full_extraction():
    names = get_names_current_coaches_and_coordinators()
    tenures = []
    for name in names:
        additional = extract_coach_tenures(name)
        tenures.extend(additional)
        
    assert len(tenures) > 1000
    
    for t in tenures:
        log.debug('Testing %s' % t)
        assert int(t['startyear'])
        assert int(t['endyear'])
        assert len(t['name']) > 0
        assert len(t['position']) > 0
        assert len(t['team']) > 0
    