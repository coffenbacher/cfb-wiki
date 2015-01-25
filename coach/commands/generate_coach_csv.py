import datetime
from coach.utils import *
import csv
import json
from sh import git
import logging

                
def generate_coach_csv(output_directory='./'):
    # Clone data repository for updates - continue if already exists
    try:
        git.clone('https://cfb-data-machine-user:y5^%WSk7DjfR@github.com/coffenbacher/cfb-data.git')
    except:
        pass 
    
    # Set up logging
    logging.basicConfig(level='WARNING',
                    #format='%(asctime)s %(levelname)-8s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='cfb-data/automated/wiki/coach_tenure/coach_tenure.log',
                    filemode='w')
    
    # Extract all current names from Wiki
    names = get_names_current_coaches_and_coordinators()
    
    # Extract the tenures for the names we have
    tenures = []
    for name in names[:10]:
        additional = extract_coach_tenures(name)
        tenures.extend(additional)
        
    # Filter out broken tenures
    tenures = filter_tenures_to_valid(tenures)
    
    # Write everything to disk
    with open('cfb-data/automated/wiki/coach_tenure/coach_tenure.csv', 'w') as csvfile:
        fieldnames = ['name', 'team', 'position', 'startyear', 'endyear']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for t in tenures:
            writer.writerow(t)
    
    with open('cfb-data/automated/wiki/coach_tenure/coach_tenure_meta.json', 'w') as metafile:
        d = {
                'created': datetime.datetime.now().strftime('%x %X'),
                'rows': len(tenures),
                'headers': ','.join(fieldnames),
            }
        metafile.write(json.dumps(d))
        
    git.bake(_cwd='cfb-data/')
    git.add('.')
    git.commit(m='Auto updating coach_tenure data')
    
    
if __name__ == '__main__':
    generate_coach_csv()