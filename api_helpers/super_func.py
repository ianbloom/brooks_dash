from api_helpers.lm_api import *

# These functions occur a logical level higher than those in lm_api
def SUBGROUP_GETTER_ID(_lm_id, _lm_key, _lm_account, _group_id):
    # GETS subgroup and returns full path
    # Build HTTP query
    resource_path = f'/device/groups/{_group_id}'
    query_params  = ''
    data          = ''

    # Obtain response
    return_dict = LM_GET(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    body = json.loads(return_dict['body'])

    # Full path will be used in the definition of subsequent dynamic groups
    group_full_path = body['fullPath']
    name            = body['name']

    return_dict['name'] = name
    return_dict['path'] = group_full_path

    return return_dict

def SUBGROUP_GETTER_NAME(_lm_id, _lm_key, _lm_account, _name):
    # GETS subgroup and returns id
    # Build HTTP query
    resource_path = '/device/groups'
    query_params  = f'?filter=name:"{_name}"'
    data          = ''

    # Obtain response
    response_dict = LM_GET(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    body = json.loads(response_dict['body'])
    code = response_dict['code']

    if(code != 200):
        print(f'Failed to obtain "{_name}" device group, check credentials')

    return_dict = {}
    return_dict['body'] = body
    return_dict['code'] = code

    return return_dict

def SUBGROUP_POSTER_NAME(_lm_id, _lm_key, _lm_account, _name):
    # POST subgroup with the _name
    # Build HTTP query
    resource_path = '/device/groups'
    query_params  = ''

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['groupType']   = 'Normal'
    data_dict['description'] = 'Devices organized by device type'
    data_dict['parentId']    = '1'
    data_dict['name']        = _name

    # Convert to JSON string
    data = json.dumps(data_dict)

    # Obtain response
    response_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    body = json.loads(response_dict['body'])
    code = response_dict['code']

    if(code != 200):
        print(f'Failed to instantiate "{_name}" device group, check credentials')

    return_dict = {}
    return_dict['body'] = body
    return_dict['code'] = code

    return return_dict

def SUBGROUP_PROPS(_lm_id, _lm_key, _lm_account, _group_id):
    # POST subgroup with the _name
    # Build HTTP query
    resource_path = f'/device/groups/{_group_id}/properties'
    query_params  = ''

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['inheritList'] = []
    data_dict['type']        = 'custom'
    data_dict['name']        = 'dbt_api_id.key'
    data_dict['value']       = _lm_id

    # Convert to JSON string
    data = json.dumps(data_dict)

    # Obtain response
    response_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    body = json.loads(response_dict['body'])
    code = response_dict['code']

    if(code != 200):
        print(f'Failed to post device properties, check credentials')

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['inheritList'] = []
    data_dict['type']        = 'custom'
    data_dict['name']        = 'dbt_api_key.key'
    data_dict['value']       = _lm_key

    # Convert to JSON string
    data = json.dumps(data_dict)

   # Obtain response
    response_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    body = json.loads(response_dict['body'])
    code = response_dict['code']

    if(code != 200):
        print(f'Failed to post device properties, check credentials')

    return 0

def PROPERTYSOURCE_POSTER(_lm_id, _lm_key, _lm_account, _filepath):
    # Build HTTP query
    resource_path = '/setting/logicmodules/importfile'
    query_params  = '?type=propertyrules'

    file = open(_filepath, 'r')
    json = file.read()
    # Close file after reading
    file.close()

    # The file name is the business after the last /
    file_name = _filepath.split('/')[-1]
    print(file_name)

    data = '''------XXX
Content-Disposition: form-data; name="file"; filename="''' + file_name + '''"
Content-Type: application/json
''' + json + '''
------XXX--'''

    print(data)
    return_dict = PROP_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)

    return return_dict

def PROPERTYSOURCE_IMPORTER(_lm_id, _lm_key, _lm_account, _lm_locator):
    # Build HTTP query
    resource_path = '/setting/registry/property_rule'
    query_params  = ''

    data_dict = {}
    data_dict['locator'] = _lm_locator
    data_dict['lmLocator'] = _lm_locator
    data_dict['id'] = _lm_locator

    data = json.dumps(data_dict)

    print(data)
    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)

    return return_dict

def SUBGROUP_POSTER(_lm_id, _lm_key, _lm_account, _group_id, _group_full_path):
    # Build HTTP query
    resource_path = '/device/groups'
    query_params  = ''

    #################
    # Linux Servers #
    #################

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['groupType']   = 'Normal'
    data_dict['description'] = 'Linux Servers'
    data_dict['appliesTo']   = f'join(system.staticgroups,",") =~ "{_group_full_path}" && isLinux()'
    data_dict['parentId']    = f'{_group_id}'
    data_dict['name']        = 'Linux Servers'

    # Convert data_dict to JSON string
    data = json.dumps(data_dict)
    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    ###################
    # Windows Servers #
    ###################

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['groupType']   = 'Normal'
    data_dict['description'] = 'Windows Servers'
    data_dict['appliesTo']   = f'join(system.staticgroups,",") =~ "{_group_full_path}" && isWindows()'
    data_dict['parentId']    = f'{_group_id}'
    data_dict['name']        = 'Windows Servers'

    # Convert data_dict to JSON string
    data = json.dumps(data_dict)
    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)

    ###########
    # Network #
    ###########

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['groupType']   = 'Normal'
    data_dict['description'] = 'Network Devices'
    data_dict['appliesTo']   = f'join(system.staticgroups,",") =~ "{_group_full_path}" && isNetwork()'
    data_dict['parentId']    = f'{_group_id}'
    data_dict['name']        = 'Network'

    # Convert data_dict to JSON string
    data = json.dumps(data_dict)
    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)

    ##############
    # Collectors #
    ##############

    # Build data dictionary to be converted to JSON string
    data_dict                = {}
    data_dict['groupType']   = 'Normal'
    data_dict['description'] = 'Collectors'
    data_dict['appliesTo']   = f'join(system.staticgroups,",") =~ "{_group_full_path}" && isCollectorDevice()'
    data_dict['parentId']    = f'{_group_id}'
    data_dict['name']        = 'Collectors'

    # Convert data_dict to JSON string
    data = json.dumps(data_dict)
    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)

    return 0

def DASH_GROUP_POSTER(_lm_id, _lm_key, _lm_account, _name, _full_path):
    resource_path = '/dashboard/groups'
    query_params  = ''

    # Build data_dict
    data_dict = {}
    data_dict['name'] = _name
    data_dict['parentId'] = 1

    data_dict['widgetTokens']                   = []
    data_dict['widgetTokens'].append({})

    data_dict['widgetTokens'][0]['inheritList'] = []
    data_dict['widgetTokens'][0]['type']        = 'owned'
    data_dict['widgetTokens'][0]['name']        = 'defaultDeviceGroup'
    data_dict['widgetTokens'][0]['value']       = _full_path

    # Turn data dictionary into json string
    data = json.dumps(data_dict)

    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    return return_dict

def DASHBOARD_POSTER(_lm_id, _lm_key, _lm_account, _dash_group_id, _exported_json_path):
    # Example of widgets config
    #     "widgetsConfig" : {\n'
    #  '    "33" : {\n'
    #  '      "col" : 9,\n'
    #  '      "sizex" : 4,\n'
    #  '      "row" : 5,\n'
    #  '      "sizey" : 4\n'
    #  '    },\n'

    # First open the file and write to string, then parse into JSON
    file = open(_exported_json_path, "r")
    file_string = file.read()
    file.close()
    file_json = json.loads(file_string)

    # Then create dash
    resource_path = '/dashboard/dashboards'
    query_params  = ''

    data_dict = {}
    data_dict['name'] = file_json['name']
    data_dict['description'] = file_json['description']
    data_dict['groupId'] = _dash_group_id
    data_dict['sharable'] = True

    # Turn data dictionary into json string
    data = json.dumps(data_dict)

    # Make the request
    return_dict = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)
    return_json = json.loads(return_dict['body'].decode())

    # Obtain dash_id for posting widgets to
    dash_id = return_json['id']

    # Initialize widgets_config
    widgets_config = {}
    widgets = file_json['widgets']

    # Then post widgets
    for widget in widgets:
        resource_path = '/dashboard/widgets'
        query_params  = ''
        config = widget['config']
        
        # Append dashboard ID to config
        config['dashboardId'] = dash_id
        position = widget['position']
        data = json.dumps(config)

        widget_body = LM_POST(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)['body'].decode()
        widget_json = json.loads(widget_body)
        print(widget_json)
        widget_id = widget_json['id']

        # Update widgets_config dictionary
        widgets_config[f'{widget_id}'] = position
        print(widgets_config)

    # Now update Dashboard widget
    resource_path = f'/dashboard/dashboards/{dash_id}'
    query_params  = ''

    data_dict = {}
    data_dict['widgetsConfig'] = widgets_config
    data = json.dumps(data_dict)

    return_dict = LM_PATCH(_lm_id, _lm_key, _lm_account, resource_path, query_params, data)

    return 0