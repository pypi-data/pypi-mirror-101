import yaml


def yaml_read(path):
    """
    path: default current path generate.yaml
    eg:
    >> yaml_read("generate.yaml")
    """
    yaml.warnings({'YAMLLoadWarning': False})
    f = open(path, 'r', encoding='utf-8')
    cfg = f.read()
    data = yaml.load(cfg)
    f.close()
    return data


