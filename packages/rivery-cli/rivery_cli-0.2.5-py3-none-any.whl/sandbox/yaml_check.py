import yaml
import pathlib

main_yaml = """
Package:
 - !include _shape_yaml    
 - !include _path_yaml
"""

_shape_yaml = """
# Define
Rectangle: &id_Rectangle
    name: Rectangle
    width: &Rectangle_width 20
    height: &Rectangle_height 10
    area: !product [*Rectangle_width, *Rectangle_height]

Circle: &id_Circle
    name: Circle
    radius: &Circle_radius 5
    area: !product [*Circle_radius, *Circle_radius, pi]

# Setting
Shape:
    property: *id_Rectangle
    color: red
"""

_path_yaml = """
# Define
Root: &BASE /path/src/

Paths: 
    a: &id_path_a !join [*BASE, a]
    b: &id_path_b !join [*BASE, b]

# Setting
Path:
    input_file: *id_path_a
"""


# define custom tag handler
def yaml_import(loader, node):
    other_yaml_file = loader.construct_scalar(node)
    current_path = pathlib.Path('.')
    print(current_path.absolute().parents)
    print(other_yaml_file)
    return yaml.load(eval(other_yaml_file), Loader=yaml.SafeLoader)


def yaml_product(loader, node):
    import math
    list_data = loader.construct_sequence(node)
    result = 1
    pi = math.pi
    for val in list_data:
        result *= eval(val) if isinstance(val, str) else val
    return result


def yaml_join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])


def yaml_ref(loader, node):
    ref = loader.construct_sequence(node)
    return ref[0]


def yaml_dict_ref(loader: yaml.loader.SafeLoader, node):
    dict_data, key, const_value = loader.construct_sequence(node)
    return dict_data[key] + str(const_value)


def main():
    # register the tag handler
    yaml.SafeLoader.add_constructor(tag='!include', constructor=yaml_import)
    yaml.SafeLoader.add_constructor(tag='!product', constructor=yaml_product)
    yaml.SafeLoader.add_constructor(tag='!join', constructor=yaml_join)
    yaml.SafeLoader.add_constructor(tag='!ref', constructor=yaml_ref)
    yaml.SafeLoader.add_constructor(tag='!dict_ref', constructor=yaml_dict_ref)

    config = yaml.load(main_yaml, Loader=yaml.SafeLoader)

    pk_shape, pk_path = config['Package']
    pk_shape, pk_path = pk_shape['Shape'], pk_path['Path']
    print(f"shape name: {pk_shape['property']['name']}")
    print(f"shape area: {pk_shape['property']['area']}")
    print(f"shape color: {pk_shape['color']}")

    print(f"input file: {pk_path['input_file']}")


if __name__ == '__main__':
    main()