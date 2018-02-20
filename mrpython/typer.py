import ast
from mrpython.type_annotation_parser import TypeAnnotationParser

class AssignAggregator(ast.NodeVisitor):
    def __init__(self):
        self.func_name = '__main__'
        self.assigns = {'__main__': []}

    def visit_Assign(self, node):
        self.assigns[self.func_name].append(node)

    def visit_FunctionDef(self, node):
        self.func_name = node.name
        self.assigns[self.func_name] = []

class Type():
    def __init__(self, kind, lineno=None):
        self.kind = kind
        # Useful for parse information
        self.lineno = lineno

    def __eq__(self, other):
        '''This is defined as type equity - as defined by the kind string'''
        return self.kind == other.kind

    def class_eq(self, other):
        ''' '''
        return self.kind == self.kind and\
        self.lineno == other.lineno

    def __repr__(self):
        res = "Type(\"" + self.kind + "\""
        if self.lineno:
            res += ", " + str(self.lineno)
        return res + ")"

def get_annotations_from_ast(tree, codelines):
    ''' ast -> string list -> Type dict)
        Returns a dictionary of type information from an
        ast and a list of lines of code. The latter is needed
        in order to get back the annotation.
    '''
    type_dict = {}
    walker = AssignAggregator()
    parser = TypeAnnotationParser()
    walker.visit(tree)

    for func_name in walker.assigns:
        type_dict[func_name] = {}
        for assign in walker.assigns[func_name]:
            parse_result = parser.parse_from_string(codelines[assign.lineno - 2])
            if not parse_result.iserror:
                var_type = Type(parse_result.content.type, assign.lineno - 1)
                type_dict[func_name][parse_result.content.name] = var_type

    return type_dict

def get_annotations(code_str):
    ''' String -> Type Dict
        Returns a type dictionnary from a code string.
        If two type annotations refer to the same variable,
        the previous annotations is erased.
        '''
    codelines = code_str.split("\n")
    return get_annotations_from_ast(ast.parse(code_str), codelines)