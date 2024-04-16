
# TODO: serialise this data!!
org_mapping = {
    'world': ['jungle', 'tundra', 'badlands', 'lava', 'mesa', 'desert']
    ,'gameplay': ['axolotl', 'bee', 'goat', 'blacksmith', 'finesse']
    ,'tech-online': ['enablers', 'devexperience', 'playerjourney', 'services', 'spiceops']
}

def get_teams(division_name):
    return org_mapping[division_name.lower()]
