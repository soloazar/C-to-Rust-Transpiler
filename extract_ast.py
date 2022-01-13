from __future__ import print_function

import json
import sys
import re


#sys.path.extend(['.', '..'])

from pycparser import parse_file, c_ast
from pycparser.plyparser import Coord



RE_CHILD_ARRAY = re.compile(r'(.*)\[(.*)\]')
RE_INTERNAL_ATTR = re.compile('__.*__')


class CJsonError(Exception):
    pass


def memodict(fn):
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = fn(key)
            return ret
    return memodict().__getitem__


@memodict
def child_attrs_of(klass):
   
    non_child_attrs = set(klass.attr_names)
    all_attrs = set([i for i in klass.__slots__ if not RE_INTERNAL_ATTR.match(i)])
    return all_attrs - non_child_attrs


def from_dict(node_dict):
    class_name = node_dict.pop('_nodetype')

    klass = getattr(c_ast, class_name)
   
    objs = {}
    for key, value in node_dict.items():
        if key == 'coord':
            objs[key] = _parse_coord(value)
        else:
            objs[key] = _convert_to_obj(value)

   
    return klass(**objs)


def from_json(ast_json):
    return from_dict(json.loads(ast_json))



def file_to_dict(filename):
    """ Load C file into dict representation of ast """
    ast = parse_file(filename, use_cpp=True)
   
    return to_dict(ast)
def file_to_json(filename, **kwargs):
    """ Load C file into json string representation of ast """
    ast = parse_file(filename, use_cpp=True)
    return to_json(ast, **kwargs)



def _convert_to_obj(value):
   
    value_type = type(value)
    if value_type == dict:
        return from_dict(value)
    elif value_type == list:
        return [_convert_to_obj(item) for item in value]
    else:
        # String
        return value


def to_dict(node):
    klass = node.__class__

    result = {}

    # Metadata
    result['_nodetype'] = klass.__name__

    # Local node attributes
    for attr in klass.attr_names:
        result[attr] = getattr(node, attr)

    # Coord object
    if node.coord:
        result['coord'] = str(node.coord)
    else:
        result['coord'] = None

    # Child attributes
    for child_name, child in node.children():
        match = RE_CHILD_ARRAY.match(child_name)
        if match:
            array_name, array_index = match.groups()
            array_index = int(array_index)
            result[array_name] = result.get(array_name, [])
            if array_index != len(result[array_name]):
                raise CJsonError('Internal ast error. Array {} out of order. '
                    'Expected index {}, got {}'.format(
                    array_name, len(result[array_name]), array_index))
            result[array_name].append(to_dict(child))
        else:
            result[child_name] = to_dict(child)

    # Any child attributes that were missing need "None" values in the json.
    for child_attr in child_attrs_of(klass):
        if child_attr not in result:
            result[child_attr] = None

    return result

def to_json(node, **kwargs):
    """ Convert ast node to json string """
    return json.dumps(to_dict(node), **kwargs)


def _parse_coord(coord_str):
    if coord_str is None:
        return None

    vals = coord_str.split(':')
    vals.extend([None] * 3)
    filename, line, column = vals[:3]
    return Coord(filename, line, column)

def export_ast():
    ast_dict_temp = file_to_dict("sample.c")
    ast = from_dict(ast_dict_temp)
    ast_json= (to_json(ast, sort_keys=True, indent=4))
    ast_dict=json.loads(ast_json)
    return ast_dict,ast_json



if __name__ == "__main__":
    ast_dict = file_to_dict("sample.c")
    print(ast_dict)
    ast = from_dict(ast_dict)
    print(ast)
    print(to_json(ast, sort_keys=True, indent=4))
