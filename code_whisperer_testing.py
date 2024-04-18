def load_json_file(file_name):
    '''loads json file and returns the data as a dict
    if the file does not exist, create it and return an empty dict
    Parameters: 
    file_name: str
    return: dict
    '''
    import json
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open(file_name, 'w') as f:
            json.dump({}, f)
        return {}
    
    