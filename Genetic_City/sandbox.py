import requests
import json

'''indicators=[{"indicator_type":"numeric","name":"Entropy","value":0.2,"ref_value":0.7,"viz_type":"radar"},{"indicator_type":"numeric","name":"Enthalpy","value":0.3,"ref_value":0.8,"viz_type":"radar"},{"indicator_type":"numeric","name":"Thermo","value":0.4,"ref_value":0.9,"viz_type":"radar"}]
headers = {'Content-Type': 'application/json'}
table_name='geneticcity8'
url='https://cityio.media.mit.edu/api/table/{}'.format(table_name)
r = requests.post(url+'/indicators', data = json.dumps(indicators), headers=headers)'''


dict_of_indicators = {0:1,1:2,2:3,3:4,4:5}
indicators = [{"indicator_type":"numeric",str(key):"Entropy","value":dict_of_indicators[key],"ref_value":0.7,"viz_type":"radar"} for key in dict_of_indicators]
print(indicators)
