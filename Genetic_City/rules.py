def accesibility():
    return
def green_space_balance_amount(no_parks,no_blocks,percentage_obj):
    percentage = no_parks/no_blocks*100
    if percentage < percentage_obj:
        fitness = percentage-percentage_obj
    if percentage > percentage_obj:
        fitness = percentage_obj-percentage
    return fitness
def green_space_balance_width():
    return
def diversity_of_housing():
    return
def diversity_of_office():
    return
def house_office_walkable():
    return
def access_to_parks():
    return
def house_office_balance():
    return
def green_space():
    return