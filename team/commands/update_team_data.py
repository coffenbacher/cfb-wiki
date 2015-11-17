from datetime import datetime
from team.utils import *
import shutil
import csv
import json
import logging
import os
from unidecode import unidecode


ROOT = 'team'
FIELDNAMES = ['team', 'name', 'city', 'state', 'conference', 'first_played', 'joined_fbs']
FIELDNAMES = [unidecode(f) for f in FIELDNAMES]
FN = extract_teams

def generate_csv(output_directory='./'):
    # Set up root data dir
    root_filename = ROOT + '/cfb-data/automated/wiki/team/'

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
                    filename= root_filename + 'team.log',
                    filemode='w')
    
    # Extract all current names from Wiki
    data = FN()
    
    # Write everything to disk
    with open(root_filename + ROOT + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, extrasaction='ignore')
        for d in data:
            asci = dict([(unidecode(k), unidecode(unicode(v))) for k, v in d.items()])
            writer.writerow(asci)
            
    # Write everything to json
    with open(root_filename + ROOT + '.json', 'w') as jsonfile:
        relevant = [{f: d.get(f, None) for f in FIELDNAMES} for d in data]
        jsonfile.write(json.dumps(relevant))
        
    with open(root_filename + ROOT + '_meta.json', 'w') as metafile:
        d = {
                'created': datetime.now().strftime('%x %X'),
                'rows': len(data),
                'headers': ','.join(FIELDNAMES),
            }
        metafile.write(json.dumps(d))
        
    git = git.bake(**{'git-dir': ROOT + '/cfb-data/.git/', 'work-tree': ROOT + '/cfb-data'})
    git.commit(m='Auto updating %s data' % ROOT, a=True)
    git.push('origin', 'master')
    
    
if __name__ == '__main__':
    generate_csv()