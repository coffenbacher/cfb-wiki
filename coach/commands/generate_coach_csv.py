from datetime.datetime import now
from coach.utils import *
import csv
import json

def generate_coach_csv(output_directory='./'):
    # Extract all current names from Wiki
    names = get_names_current_coaches_and_coordinators()
    
    # Extract the tenures for the names we have
    tenures = []
    for name in names[:5]:
        additional = extract_coach_tenures(name)
        tenures.extend(additional)
    
    # Write everything to disk
    with open('coach_tenure.csv', 'w') as csvfile:
        fieldnames = tenures[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in tenures:
             writer.writerow(t)
    
    with open('coach_tenure_meta.json', 'w') as metafile:
        d = {
                'created': now(),
                'rows': len(tenures),
                'headers': ','.join(fieldnames),
            }
        metafile.write(d)
        
        
if __name__ == '__main__':
    generate_coach_csv()