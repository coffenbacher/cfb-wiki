from datetime import datetime
from team.utils import *
import shutil
import csv
import json
import logging
import os

ROOT = 'team'
                
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
    teams = extract_teams()
    
    # Write everything to disk
    with open(root_filename + 'team.csv', 'w') as csvfile:
        fieldnames = ['team', 'name', 'city', 'state', 'conference', 'first_played', 'joined_fbs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        for t in teams:
            writer.writerow(t)
    
    with open(root_filename + 'team_meta.json', 'w') as metafile:
        d = {
                'created': datetime.now().strftime('%x %X'),
                'rows': len(teams),
                'headers': ','.join(fieldnames),
            }
        metafile.write(json.dumps(d))
        
    git = git.bake(**{'git-dir': ROOT + '/cfb-data/.git/', 'work-tree': ROOT + '/cfb-data'})
    git.commit(m='Auto updating team data', a=True)
    git.push('origin', 'master')
    
    
if __name__ == '__main__':
    generate_csv()