import datetime
from coach.utils import *
import shutil
import csv
import json
import logging
import os
                
def generate_coach_csv(output_directory='./'):
    # Set up root data dir
    root_filename = 'coach/cfb-data/automated/wiki/coach_tenure/'
    
    # Clone data repository for updates - continue if already exists
    from sh import git
    try:
        shutil.rmtree('coach/cfb-data/')
    except:
        pass
    git.clone('https://'+os.getenv('MACHINE_AUTH')+'@github.com/coffenbacher/cfb-data.git', 'coach/cfb-data/')
    
    # Set up logging
    logging.basicConfig(level='WARNING',
                    #format='%(asctime)s %(levelname)-8s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= root_filename + 'coach_tenure.log',
                    filemode='w')
    
    # Extract all current names from Wiki
    names = get_names_current_coaches_and_coordinators()
    
    # Extract the tenures for the names we have
    tenures = []
    for name in names:
        additional = extract_coach_tenures(name)
        tenures.extend(additional)
        
    # Filter out broken tenures
    tenures = filter_tenures_to_valid(tenures)
    tenures = sort_tenures(tenures)
    
    # Write everything to disk
    with open(root_filename + 'coach_tenure.csv', 'w') as csvfile:
        fieldnames = ['name', 'team', 'position', 'startyear', 'endyear']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for t in tenures:
            writer.writerow(t)
    
    with open(root_filename + 'coach_tenure_meta.json', 'w') as metafile:
        d = {
                'created': datetime.datetime.now().strftime('%x %X'),
                'rows': len(tenures),
                'headers': ','.join(fieldnames),
            }
        metafile.write(json.dumps(d))
        
    git = git.bake(**{'git-dir': 'coach/cfb-data/.git/', 'work-tree': 'coach/cfb-data'})
    git.commit(m='Auto updating coach_tenure data', a=True)
    git.push('origin', 'master')
    
    
if __name__ == '__main__':
    generate_coach_csv()