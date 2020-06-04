from o24.backend.models.shared import Action, Funnel
from o24.globals import *

def create_funnel_node(current, json_key_title):
    #check if already create
    if current.get('node_id', None) is not None:
        return None

    action = Action.get_by_key(current.get('key'))
    if not action:
        raise Exception('No such action for key:{0}'.format(current.get('key', None)))
    
    data = {
        'action' : action.id,
        'data' : current.get('data', ''),
        'json' : current,
        'json_key_title' : json_key_title
    }
    if current.get('root', None):
        data['root'] = current.get('root')
    

    node = Funnel.create_node(data)
    return node

def create_nodes(funnel_dict):

    json_key_titles = []
    nodes_created = {}
    #create nodes in a database
    for key, node in funnel_dict.items():
        new_node = create_funnel_node(node, key)
        if not new_node:
            raise Exception("Can't create node: create_funnel_node error")
        
        new_node.reload()
        if key in json_key_titles:
            print("Error: trying to create 2 times for key={0}".format(key))
        json_key_titles.append(key)
        nodes_created[key] = new_node

    #connect nodes:
    for key, node in funnel_dict.items():
        found_node = nodes_created[key]
        
        if key in [FINISHED_ACTION, SUCCESS_ACTION]:
            continue

        if_true_node_title = node.get('if_true')
        if_false_node_title = node.get('if_false')

        if_true_id = nodes_created[if_true_node_title].id
        if_false_id = nodes_created[if_false_node_title].id

        found_node.if_true = if_true_id
        found_node.if_false = if_false_id

        found_node._commit()
    
    print(json_key_titles)


#THIS ONE CALLED FIRST
def construct_funnel(funnel_dict):
    if not funnel_dict:
        raise Exception("trying to construct funnel for empty funnel_dict:{0}".format(funnel_dict))

    create_nodes(funnel_dict)

    return True

