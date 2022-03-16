from brix import Handler
from collections import Counter

'''FUNCTION TO UPDATE THE ONLINE GRID'''
def change_road_campus(geogrid_data):
    for cell in geogrid_data:
        if cell['name'] == 'Campus':
            cell['name'] = 'Road'
            cell['height'] = 25
    return geogrid_data

table_name = 'geneticcity'
H = Handler(table_name, quietly=False)
H.update_geogrid_data(change_road_campus)

'''geogrid_data = H.get_geogrid_data()
roads = [cell for cell in geogrid_data if cell['name']=='Road']
print(roads)'''