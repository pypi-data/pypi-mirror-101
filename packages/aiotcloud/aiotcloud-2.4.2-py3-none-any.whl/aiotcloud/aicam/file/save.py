import yaml
import os


def yaml_save(yaml_data, path=None):
    """
    yaml: data
    path: default current path
    eg:
    >> yaml_doc({'user': 'admin', 'pwd': None, 'job': ['teacher', 'nurese']})
    """
    if path is None:
        path = os.path.join(os.path.abspath('.'), 'generate.yaml')  # 创建yaml文件
    file = open(path,'w',encoding='utf-8')
    yaml.dump(yaml_data, file,default_flow_style=None)
    print("data save to ", path)
    file.close()
