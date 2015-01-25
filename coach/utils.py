import mwparserfromhell
import wikipedia
from pywikibot import Page, Site, NoPage, IsRedirectPage
import re
import datetime
import logging;


def extract_coach_tenures(name):
    """
    Extract a coaches tenures from Wikipedia.
    
    Arguments:
    - name (name of coach)
    
    Returns:
    - list(dict)
    """
    logging.info('Looking for coach %s' % name)
    page_name = get_page_name_from_coach_name_wiki(name)
    
    # If we can't find a wikipedia page, return immediately
    if not page_name:
        return []
    else:
        logging.debug('Looking up %s as http://en.wikipedia.org/wiki/%s' % (name, page_name))
    
    # Extract page content from wikipedia and narrow it down to the templates
    p = Page(Site('en', 'wikipedia'), page_name)
    if p.isRedirectPage():
        p = p.getRedirectTarget()
    content = p.get()

    parsed = mwparserfromhell.parse(content)
    templates = parsed.filter_templates()
    
    # Extract teams and years from the template
    teams, years = None, None
    for t in templates:
        for p in t.params:
            if "coach_teams" in p.name:
                teams = parse_coach_teams_and_positions_from_wiki(p)
            if "coach_years" in p.name:
                years = parse_coach_years_from_wiki(p)
                
    # If we were not able to extract information from the page, log & return empty
    if not teams or not years:
        logging.warning('ISSUE DETECTED: %s is valid page but no information extracted' % name)
        return []
    
    tenures = [dict(t[0].items() + t[1].items()) for t in zip(teams, years)]
    [d.update({'name': name}) for d in tenures]
    return tenures
    
def parse_coach_teams_and_positions_from_wiki(teams_section):
    logging.debug('Parsing teams_section: %s' % unicode(teams_section))
    
    results = []
    sections = re.split('<br.?.?>', unicode(teams_section.value))
    for wikicode in sections:
        d = {}
        wikicode = mwparserfromhell.parse(wikicode).strip_code().strip()
        
        # Get the team name
        p = '('.join(wikicode.split('(')[:-1]).strip()
        d['team'] = (p if p else wikicode).replace(u'\u2013', '-')
        
        # Get the position coach name
        p = re.findall('\(([\w/]+)\)(?=$)', wikicode)
        d['position'] = standardize_position_title(p[0] if p else 'HC')
        results.append(d)
    return results
    
def parse_coach_years_from_wiki(years_section):
    logging.debug('Parsing years_section: %s' % unicode(years_section))
    
    results = []
    sections = re.split('<br.?.?>', unicode(years_section.value).lower())
    for wikicode in sections:
        d = {}
        s = wikicode.strip().split(u'\u2013')
        if u'&ndash;' in s[0]:
            s = s[0].split(u'&ndash;')
        if u'-' in s[0]:
            s = s[0].split('-')
        d['startyear'] = s[0]
        d['endyear'] = s[0] if len(s) == 1 else s[1]
        d['endyear'] = d['endyear'] if d['endyear'].lower() != 'present' else str(datetime.datetime.now().year)
        results.append(d)
    return results

def get_page_name_from_coach_name_wiki(name):
    try:
        page = wikipedia.page(name).title.replace(' ', '_')
        if is_football_coach_wiki(page):
            return page
        else:
            logging.warning('''ISSUE DETECTED: %s is not about a football coach and there is no disambiguation page''' % name)
    
    except wikipedia.DisambiguationError as e:
        # Need to disambiguate to the coach
        valid = ['(American football)', '(linebacker)', 
                '(American football coach)', '(coach)']
        for option in e.options:
            if any([any([v in option]) for v in valid]):
                page = option.replace(' ', '_')
                if is_football_coach_wiki(option):
                    return page
                logging.warning('ISSUE DETECTED: %s is a football page but no mention of coach' % name)
        logging.warning('ISSUE DETECTED: %s could not be found in disambiguation page' % name)
        return None
    
    except wikipedia.PageError:
        # Cannot find a page
        return None

def is_football_coach_wiki(page):
    try:
        p = Page(Site('en', 'wikipedia'), page).get(get_redirect=True)
        return 'football' in p.lower() and 'coach' in p.lower()
    except NoPage:
        return False

def standardize_position_title(position):
    if 'assistant' in position:
        return 'GA'
    if 'ASST' in position:
        return 'GA'
    return position


def get_names_current_coaches_and_coordinators():
    """
    Gets the names of the current D1 coaches and coordinators.
    
    Params:
    - None
    
    Returns:
    - list[str(), str()]
    """
    
    p = Page(Site('en', 'wikipedia'), 'List_of_current_NCAA_Division_I_FBS_football_coaches').get()
    parsed = mwparserfromhell.parse(p)
    nameps = filter(lambda x: 'sortname' == x.name, parsed.filter_templates())
    results = []
    for n in nameps:
        results.append(' '.join([unicode(p.value) for p in n.params[:2]]))
    return results
    
def filter_tenures_to_valid(tenures):
    filtered = []
    for t in tenures:
        if is_valid_tenure(t):
            filtered.append(t)
        else:
            logging.warning('ISSUE DETECTED: %s' % t)
    
    return filtered

def is_valid_tenure(tenure):
    try:
        if int(tenure['startyear']) < 1800:
            return False
            
        if int(tenure['endyear']) < 1800:
            return False
        
        if int(tenure['endyear']) < int(tenure['startyear']):
            return False
            
        if len(str(tenure['team'])) < 2 or len(str(tenure['team'])) > 30:
            return False
            
        if len(str(tenure['position'])) < 1 or len(str(tenure['position'])) > 20:
            return False
            
        if len(str(tenure['name'])) < 2 or len(str(tenure['name'])) > 20:
            return False

        return True
    except:
        return False
    
    
    