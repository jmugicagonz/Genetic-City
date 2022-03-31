import random                                                                   #Used to send random heights of buildings

'''FUNCTION TO UPDATE THE ONLINE GRID'''
def update_land_uses(geogrid_data, grid_list=[0], dict_landUses={0: '0'}, change_height=False):
    if change_height:
        for cell in geogrid_data:
            cell['name'] = dict_landUses[grid_list[cell['id']][0]]
            cell['height'] = grid_list[cell['id']][1]
    else:
        for cell in geogrid_data: 
            cell['name'] = dict_landUses[grid_list[cell['id']]]
    return geogrid_data