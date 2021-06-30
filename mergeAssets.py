#!/usr/bin/env python3

import csv
import getopt
import sys

import_headers="Name,ID,Owner,Hostnames,IP Addresses,MAC Addresses,Importance,Labels,Description".split(',')

assets_file = None
onboarding_file = None

def usage():
    print('\n')
    print("Usage: -a <Assets Download> -o <Onboarding CSV>")
    print('\n')
    sys.exit()

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ha:o:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-a"):
            assets_file = arg
        elif opt in ("-o"):
            onboarding_file = arg

if assets_file == None or onboarding_file == None:
    usage()

with open(assets_file) as fin:
    assets = [{k: v for k, v in row.items()}
        for row in csv.DictReader(fin, quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',', skipinitialspace=True)]

with open(onboarding_file) as fin:
    onboarding = [{k: v for k, v in row.items()}
        for row in csv.DictReader(fin, quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',',skipinitialspace=True)]

update_entries = []
insert_entries = []

for ob_entry in onboarding:
    found = False
    for asset in assets:
        if asset['MAC Addresses'].lower() == ob_entry['MAC Addresses'].lower():
            found = True
            updated = asset.copy()
            if updated['Importance'] == "none":
                updated['Importance'] = ob_entry['Importance']
            if updated['Labels'] == "":
                updated['Labels'] = ob_entry['Labels']
            else:
                updated['Labels'] = updated['Labels'] + ',' + ob_entry['Labels']
            if updated['Description'] == "":
                updated['Description'] = ob_entry['Description']
            if updated['IP Addresses'].lower() != ob_entry['IP Addresses'].lower():
                if updated['IP Addresses'] == 'null':
                    updated['IP Addresses'] = ob_entry['IP Addresses']
            '''
            print("  Importance: " + str(asset['Importance']))
            print("  Importance: " + str(ob_entry['Importance']))
            print("  Importance: " + str(updated['Importance']))
            print("  Labels: " + str(asset['Labels']))
            print("  Labels: " + str(ob_entry['Labels']))
            print("  Labels: " + str(updated['Labels']))
            print("  Description: " + str(asset['Description']))
            print("  Description: " + str(ob_entry['Description']))
            print("  Description: " + str(updated['Description']))
            '''
            if 'Hostnames' in ob_entry.keys():
                if ob_entry['Hostnames'].lower() != updated['Hostnames'].lower():
                    updated['Hostnames'] = updated['Hostnames'] + "," + ob_entry['Hostnames']
                    #print("  Hostnames: " + str(ob_entry['Hostnames']))
                    #print("  Hostnames: " + str(updated['Hostnames']))
            '''
            if 'Name' in ob_entry.keys():
                if ob_entry['Name'].lower() != updated['Name'].lower():
                    print("  Name: " + str(ob_entry['Name']))
                    print("  Name: " + str(updated['Name']))
            #print("Found MAC: " + str(asset))
            #print("Match MAC: " + str(ob_entry))
            '''
            update_entries.append(updated)
        elif asset['IP Addresses'].lower() == ob_entry['IP Addresses'].lower():
            found = True
            print("Found IP but no or mismatched MAC: " + str(asset['IP Addresses']))
            '''
            print("  MAC Addresses: " + str(asset['MAC Addresses']))
            print("  MAC Addresses: " + str(ob_entry['MAC Addresses']))
            print("  Hostnames: " + str(asset['Hostnames']))
            print("  Hostnames: " + str(ob_entry['Hostnames']))
            print("  Importance: " + str(asset['Importance']))
            print("  Importance: " + str(ob_entry['Importance']))
            print("  Labels: " + str(asset['Labels']))
            print("  Labels: " + str(ob_entry['Labels']))
            print("  Description: " + str(asset['Description']))
            print("  Description: " + str(ob_entry['Description']))
            '''
    if not found:
        new_entry = ob_entry.copy()
        if 'Hostname' in new_entry:
            new_entry['Name'] = new_entry['Hostname']
        else:
            new_entry['Name'] = new_entry['IP Addresses']
        insert_entries.append(new_entry)

print('Num to update: %d' %len(update_entries))
print('Num to insert: %d' %len(insert_entries))

'''
for entry in update_entries:
    for key in entry.keys():
        if '\n' in entry[key]:
            print(entry[key])
'''

s = set()
for i in insert_entries:
    s.update(i)
header = list(s)

new_header = header.copy()

for item in header:
    found = False
    for key in import_headers:
        if key == item:
            found = True
            break
    if not found:
        new_header.remove(item)

header = new_header.copy()

for item in import_headers:
    found = False
    for key in new_header:
        if key == item:
            found = True
            break
    if not found:
        header.append(item)

print(header)

with open("insert_entries.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for d in insert_entries:
        writer.writerow([d.get(i, "") for i in header])

header.append("ID")

with open("update_entries.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for d in update_entries:
        writer.writerow([d.get(i, "") for i in header])



