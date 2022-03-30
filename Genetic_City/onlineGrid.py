import random                                                                   #Used to send random heights of buildings

'''FUNCTION TO UPDATE THE ONLINE GRID'''
def update_land_uses(geogrid_data, grid_list=[0], dict_landUses={0: '0'}, height=1):
    for cell in geogrid_data:
        #cell['name'] = dict_landUses[grid_list[cell['id']]]
        randomTall = random.uniform(0,1)
        randomH = random.randint(0,height)
        cell['name'] = dict_landUses[grid_list[cell['id']]]
        if cell['name'] == 'Industrial': 
            if randomTall >= 0.8: cell['height'] = 4*randomH
            else: cell['height'] = 2*randomH
        elif cell['name'] == 'Residential': 
            if randomTall >= 0.8: cell['height'] = randomH
            else: cell['height'] = 2*randomH
        elif cell['name'] == 'Campus': cell['height'] = 0
    return geogrid_data