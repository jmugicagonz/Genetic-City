import json
import requests

def post_indicators(table_name, dict_of_indicators):
        headers = {'Content-Type': 'application/json'}
        url='https://cityio.media.mit.edu/api/table/{}'.format(table_name)
        indicators = [{"indicator_type":"numeric","name":key,"value":dict_of_indicators[key],"ref_value":0.7,"viz_type":"radar"} for key in dict_of_indicators]
        print("Indicators are: {}".format(indicators))
        r = requests.post(url+'/indicators', data = json.dumps(indicators), headers=headers)