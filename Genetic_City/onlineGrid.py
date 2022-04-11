import json
import requests
import ipdb

'''FUNCTION TO UPDATE THE ONLINE GRID'''
def update_land_uses(geogrid_data, grid_list=[0], dict_landUses={0: '0'}):
    for cell in geogrid_data:
        cell['name'] = dict_landUses[grid_list[cell['id']][0]]
        cell['height'] = grid_list[cell['id']][1]

    headers = {'Content-Type': 'application/json'}
    #r = requests.post('http://127.0.0.1:1234/landuse', data = json.dumps(geogrid_data), headers=headers)
    # ipdb.set_trace() 
    return geogrid_data

'''FUNCTION TO UPDATE THE ONLINE INDICATORS'''
def post_indicators(table_name, dict_of_indicators, dict_of_ref_indicators):
    headers = {'Content-Type': 'application/json'}
    url='https://cityio.media.mit.edu/api/table/{}'.format(table_name)
    # The reference value is the one from the last iteration
    indicators = [{"indicator_type":"numeric","name":key,"value":dict_of_indicators[key], "viz_type":"radar"} for key in dict_of_indicators]

    for key in range(len(indicators)):
        indicators [key]["ref_value"] = dict_of_ref_indicators [key]

    print("Indicators are: {}".format(indicators))
    dict_of_ref_indicators = list(dict_of_indicators.values())
   
    r = requests.post(url+'/indicators', data = json.dumps(indicators), headers=headers)
    return dict_of_ref_indicators
    #r = requests.post('http://127.0.0.1:1234/indicator', data = json.dumps(indicators), headers=headers)

    # ipdb.set_trace()