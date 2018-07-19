'''
Created on Jul 18, 2018

@author: kumykov

Removes project versions that have an emty BOM
'''
from bds.HubRestApi import HubInstance
from sys import argv


def remove_empty_versions(project_id, cleanup=False):
    
    hub = HubInstance()
    project = hub.get_project_by_id(project_id, limit=100)

    print (project['name'])
    versions = hub.get_project_versions(project, limit=200)
    print ("\t versions found %s" % versions['totalCount'])
    versionlist = versions['items']
    for index in range(len(versionlist) - 1):
        while True:
            count = 0
            try:
                va = versionlist[index]
                components = hub.get_version_components(va, limit=1)
                totalCount = components['totalCount']
                print ("Vesion {} has {} components".format(va['versionName'], totalCount))
                if cleanup and totalCount == 0:
                    print ("removing {}".format(va['_meta']['href']))
                    hub.execute_delete(va['_meta']['href'])
                break   
            except Exception:
                count += 1
                print ("Oops! Attempt number {} failed".format(count))
                if count > 3:
                    break
                continue
            else:
                break



#
# main
# 
cleanup = len(argv) > 2
with open(argv[1], "r") as f:
    projectlist = f.readlines() 

for line in projectlist:
    project_id = line.split()[0]
    project_name = line.split()[2]
    print ("Processing {} ".format(project_name))
    remove_empty_versions(project_id)






        