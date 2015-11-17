import datetime
from coach_tenure.utils import *
import shutil
import csv
import json
import logging
import os
from unidecode import unidecode

ROOT = 'coach_tenure'
FIELDNAMES = ['name', 'team', 'position', 'startyear', 'endyear']
FIELDNAMES = [unidecode(f) for f in FIELDNAMES]

def generate_coach_csv(output_directory='./'):
    # Set up root data dir
    root_filename = ROOT + '/cfb-data/automated/wiki/' + ROOT + '/'

    # Clone data repository for updates - continue if already exists
    from sh import git
    try:
        shutil.rmtree(ROOT + '/cfb-data/')
    except:
        pass
    git.clone('https://'+os.getenv('MACHINE_AUTH')+'@github.com/coffenbacher/cfb-data.git', ROOT + '/cfb-data/')
    
    # Create our root if required
    if not os.path.exists(root_filename):
        os.makedirs(root_filename)
    
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
    data = sort_tenures(tenures)
    
    # Write everything to csv
    with open(root_filename + ROOT + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        for d in data:
            asci = dict([(unidecode(k), unidecode(unicode(v))) for k, v in d.items()])
            writer.writerow(asci)
            
    # Write everything to json
    with open(root_filename + ROOT + '.json', 'w') as jsonfile:
        relevant = [{f: d.get(f, None) for f in FIELDNAMES} for d in data]
        jsonfile.write(json.dumps(relevant))
    
    with open(root_filename + ROOT + '_meta.json', 'w') as metafile:
        d = {
                'created': datetime.datetime.now().strftime('%x %X'),
                'rows': len(data),
                'headers': ','.join(FIELDNAMES),
            }
        metafile.write(json.dumps(d))
        
    git = git.bake(**{'git-dir': ROOT + '/cfb-data/.git/', 'work-tree': ROOT + '/cfb-data'})
    git.commit(m='Auto updating %s data' % ROOT, a=True)
    git.push('origin', 'master')
    
    
if __name__ == '__main__':
    generate_coach_csv()