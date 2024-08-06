
import source.data_manager as data_manager

org_settings_file = "data/organisation_data.json"
data = data_manager.read_data_from_file(org_settings_file)

def get_teams(key):
    return data['teams'][key.lower()]
