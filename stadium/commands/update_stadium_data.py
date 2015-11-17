from datetime import datetime
import shutil
import csv
import json
import logging
import os
from unidecode import unidecode

from stadium.utils import *
ROOT = 'stadium'
FIELDNAMES = ['stadium', 'team', 'image', 'city', 'state', 'conference', 'built_datetime', 'capacity', 'record', 'record_datetime']
FIELDNAMES = [unidecode(f) for f in FIELDNAMES]
FN = extract_stadiums
    
def generate_csv(output_directory='./'):
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
                    filename= root_filename + ROOT + '.log',
                    filemode='w')
    
    # Extract all current names from Wiki
    data = FN()
    
    # Write everything to csv
    with open(root_filename + ROOT + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, extrasaction='ignore')
        for d in data:
            asci = dict([(unidecode(k), unidecode(unicode(v))) for k, v in d.items()])
            writer.writerow(asci)
            # [unidecode(unicode(d.get(field))) for field in FIELDNAMES]
    
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