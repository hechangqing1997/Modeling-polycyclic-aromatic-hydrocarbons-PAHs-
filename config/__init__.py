import yaml
def read_config_file(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        data=f.read()
        cfg=yaml.load(data,Loader=yaml.FullLoader)
    return cfg