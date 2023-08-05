import yaml
import pathlib

with open(pathlib.Path(r'C:\workspace\rivery_cli\logics\60005bb389f000001ef047aa.yaml'), 'r') as yml_:
    content = yaml.safe_load(yml_)
print(content)