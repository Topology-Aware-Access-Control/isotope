template = '''
defaults:
  numReplicas: 1
services:
- isEntrypoint: true
  name: svc-0
  script:
'''

import json
import yaml
import sys

tree_levels = sys.argv[1] # 2
tree_m = sys.argv[2] # 5
calls_m = sys.argv[3] # 2
filename = f"tree-{tree_levels}-{tree_m}-{calls_m}.yaml" # tree-2-5.yaml

def write_topology(services):
    topology = {
        "defaults": {
            "numReplicas": 1,
            "requestSize": 0,
            "responseSize": 0,
        }
    }

    services_list = []
    for ele in services:
        ser = services[ele]
        ser['name'] = ele
        if 'script' in ser:
            script = ser['script']
            ser['script'] = []
            for ele in script:
                ser['script'] += [{'call': ele}]

            ser['script'] = [ser['script']]
        
        services_list.append(ser)
    
    with open(filename, "w") as f:
        f.write(yaml.dump(services_list))
    print("total services: ", len(services_list))


def create_tree(levels, k):
    services = {
        'svc-0': {
            'isEntrypoint': True,
            'script': []
        }
    }
    root = 'svc-0'
    queue = [root]

    while len(queue) > 0:
        top = queue[-1]
        queue = queue[:-1]

        if (top.count('-') >= levels):
            continue

        new_level = []
        services[top]['script'] = []

        for i in range(0, k):
            new_level.append(top+'-'+str(i))

            if i < int(calls_m):
                services[top]['script'] += [new_level[-1]]
                
        for ele in new_level:
            services[ele] = {}
            queue = [ele] + queue
        
    write_topology(services)

def create_chain(k):
    pass

create_tree(int(tree_levels), int(tree_m))