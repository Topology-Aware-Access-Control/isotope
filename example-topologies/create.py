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
import copy

tree_levels = sys.argv[1] # 2
tree_m = sys.argv[2] # 5
calls_m = sys.argv[3] # 2
filename = f"tree-{tree_levels}-{tree_m}-{calls_m}.yaml" # tree-2-5.yaml
root_name = "svc-0"

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
    topology["services"] = services_list
    
    with open(filename, "w") as f:
        f.write(yaml.dump(topology))
    print("total services: ", len(services_list))

def dfs(graph, curr_node, rules):
    if ("script" not in graph[curr_node]) or (len(graph[curr_node]["script"]) < 1):
        return [",".join(rules)]
    
    res = []
    if "script" in graph[curr_node]:
        for ele in graph[curr_node]["script"]:
            res += dfs(graph, ele, list(rules) + [ele])
    
    return res

def break_paths_to_rules(paths):
    rules = set()
    for ele in paths:
        p = ele.split(",")
        p.reverse()
        for i in range(0, len(p)):
            r = list(p[i:])
            r.reverse()
            rules.add(",".join(r))
    return list(rules)

def get_service_names(services):
    names = set()
    for ele in services:
        names.add(ele)
    return list(names)


def write_rules(services):
    curr_rules = [root_name]
    paths = dfs(copy.deepcopy(services), root_name, list(curr_rules))
    rules = break_paths_to_rules(copy.deepcopy(paths))
    names = get_service_names(services)
    res = {
        "rules": rules,
        "services": names
    }
    fn = f"EXT{tree_levels}{tree_m}{calls_m}.json"
    print("total paths: ", len(paths))
    print("total rules: ", len(rules))
    print("total nodes: ", len(names))

    with open(fn, "w") as f:
        f.write(json.dumps(res, indent=4))


def create_tree(levels, k):
    services = {
        f"{root_name}": {
            'isEntrypoint': True,
            'script': []
        }
    }

    queue = [root_name]

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
        
    write_topology(copy.deepcopy(services))
    write_rules(services)


def create_chain(k):
    pass

create_tree(int(tree_levels), int(tree_m))