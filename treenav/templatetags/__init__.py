import re

from django.template import Node, Variable
from django.template import VariableDoesNotExist

tag_argument = re.compile(r'(\'|")?[a-zA-Z0-9_.-]+(=|\'|")?((\'|")?[a-zA-Z0-9_.-]+(\'|")?)?')


def parse_args_kwargs(parser, token):
    tag_name, arg_str = token.contents.split(' ', 1)
    args = []
    kwargs = {}

    for match in tag_argument.finditer(arg_str):
        arg = match.group()
        if '=' in arg:
            k, v = arg.split('=', 1)
            kwargs[str(k)] = v
        else:
            args.append(arg)

    return tag_name, args, kwargs


class CaktNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in list(kwargs.items())])

    def render_with_args(self, context, *args, **kwargs):
        raise Exception('render_with_args must be implemented the class that inherits CaktNode')

    def render(self, context):
        args = []
        for arg in self.args:
            try:
                args.append(arg.resolve(context))
            except VariableDoesNotExist:
                args.append(None)

        kwargs = {}
        for k, arg in list(self.kwargs.items()):
            try:
                kwargs[k] = arg.resolve(context)
            except VariableDoesNotExist:
                kwargs[k] = None

        return self.render_with_args(context, *args, **kwargs)
