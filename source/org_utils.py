org_mapping = {
    'world': ['jungle', 'tundra', 'badlands', 'lava', 'mesa', 'desert']
    ,'gameplay': ['axolotl', 'bee', 'goat', 'blacksmith', 'finesse']
    ,'tech-online': ['enablers', 'devexperience', 'playerjourney', 'services', 'spiceops']
}

def get_teams(missionName):
    return org_mapping[missionName.lower()]


def tmp_get_world_devs():
    # return ['KomalShashankKanukuntlaD11']
    return ['d11dbardsley', 'd11jameswood', 'd11lgraydon', 'petter-holmberg' 
                      ,'YiPeiTu-Netlight', 'jdarnald', 'veblmojang', 'JaredChickoreeD11'
                      ,'GabrielM-D11']