import mwparserfromhell
import wikipedia
from pywikibot import Page, Site
import re
import datetime
import logging; logging.basicConfig(); log = logging.getLogger(); log.setLevel('DEBUG')


def extract_coach_tenures(name):
    page_name = get_page_name_from_coach_name_wiki(name)
    log.debug('Looking up %s as http://en.wikipedia.org/wiki/%s' % (name, page_name))
    
    p = Page(Site('en', 'wikipedia'), page_name).get()
    parsed = mwparserfromhell.parse(p)
    templates = parsed.filter_templates()
    for t in templates:
        for p in t.params:
            if "coach_teams" in p.name:
                teams = parse_coach_teams_and_positions_from_wiki(p)
            if "coach_years" in p.name:
                years = parse_coach_years_from_wiki(p)
    tenures = [dict(t[0].items() + t[1].items()) for t in zip(teams, years)]
    [d.update({'name': name}) for d in tenures]
    return tenures
    
def parse_coach_teams_and_positions_from_wiki(teams_section):
    results = []
    sections = re.split('<br.?>', unicode(teams_section.value))
    for wikicode in sections:
        d = {}
        wikicode = mwparserfromhell.parse(wikicode).strip_code().strip()
        
        # Get the team name
        p = '('.join(wikicode.split('(')[:-1]).strip()
        d['team'] = p if p else wikicode
        
        # Get the position coach name
        p = re.findall('\(([\w/]+)\)(?=$)', wikicode)
        d['position'] = p[0] if p else 'HC'
        results.append(d)
    return results
    
def parse_coach_years_from_wiki(years_section):
    results = []
    for wikicode in years_section.value.split('<br>'):
        d = {}
        s = wikicode.strip().split(u'\u2013')
        d['startyear'] = s[0]
        d['endyear'] = s[0] if len(s) == 1 else s[1]
        d['endyear'] = d['endyear'] if d['endyear'] != 'present' else str(datetime.datetime.now().year)
        results.append(d)
    return results

def get_page_name_from_coach_name_wiki(name):
    try:
        return wikipedia.page(name).title.replace(' ', '_')
    except wikipedia.DisambiguationError as e:
        football_specific = filter(lambda x: 'football' in x.lower(), e.options)
        if len(football_specific) > 1:
            log.warning('Too many wikipedia pages found for %s' % name)
        return football_specific[0].replace(' ', '_')