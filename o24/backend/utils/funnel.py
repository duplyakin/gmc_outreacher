from o24.backend.models.shared import Action, Funnel

def create_funnel_node(current):
    #check if already create
    if current.get('node_id', None) is not None:
        return None

    action = Action.get_by_key(current.get('key'))
    if not action:
        raise Exception('No such action for key:{0}'.format(current.get('key', None)))
    
    data = {
        'action' : action.id,
        'data' : current.get('data', ''),
        'json' : current
    }
    if current.get('root', None):
        data['root'] = current.get('root')
    

    node = Funnel.create_node(data)
    return node

def create_nodes(funnel_dict):
    root = funnel_dict.get('root')
    current = root
    stack = []

    # Create actions
    while True:
        if current is not None:
            stack.append(current) 
            key = current.get('if_true', None)
            current = funnel_dict.get(key, None)

        elif(stack):
            current = stack.pop()
            node = create_funnel_node(current)
            if node:
                current['node_id'] = node.id

            key = current.get('if_false', None)
            current = funnel_dict.get(key, None)
        else:
            break


def connect_funnel_node(current, funnel_dict):
    node = Funnel.get_node(current.get('node_id'))
    if not node:
        raise Exception("No such node id:{0}".format(current.get('node_id', None)))
    
    data = {}
    true_key = current.get('if_true', None)
    if true_key:
        data['if_true'] = funnel_dict.get(true_key)['node_id']
    
    false_key = current.get('if_false', None)
    if false_key:
        data['if_false'] = funnel_dict.get(false_key)['node_id']

    node.update_data(data)

    return node

def connect_nodes(funnel_dict):
    root = funnel_dict.get('root')
    current = root
    stack = []

    # Create actions
    while True:
        if current is not None:
            stack.append(current)  
            key = current.get('if_true', None)
            current = funnel_dict.get(key, None)

        elif(stack):
            current = stack.pop()
            connect_funnel_node(current, funnel_dict)

            key = current.get('if_false', None)
            current = funnel_dict.get(key, None)
        else:
            break


def construct_funnel(funnel_dict):
    if not funnel_dict:
        raise Exception("trying to construct funnel for empty funnel_dict:{0}".format(funnel_dict))

    create_nodes(funnel_dict)

    connect_nodes(funnel_dict)

    return True

