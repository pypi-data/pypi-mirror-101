import os
from json import JSONEncoder

class FigmentJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()
        else:
            return o

class Named:
    def __init__(self):
        self.name = ''

    def validate(self, sender, sentinel):
        if not len(self.name.strip()):
            sentinel.error(sender, "\"name\" is empty")

class Environment(Named):
    def __init__(self):
        super().__init__()
        self.hosts = []
        self.disabled = False
        self.outputs = []

    def __str__(self):
        return "Environment(name: {}, hosts: {}, disabled: {}, outputs: {})".format(repr(self.name), repr(self.hosts), repr(self.disabled), repr(self.outputs))

    def validate(self, sender, sentinel):
        super().validate(sender, sentinel)
        used = set()
        for h in self.hosts:
            if h.name in used:
                sentinel.error((*sender, self.name), "host \"{}\" already used in environment \"{}\"".format(h.name, self.name))
            else:
                h.validate((*sender, self.name), sentinel)
            used.add(h.name)

    def to_dict(self):
        return {'name': self.name,
                'hosts': [h.to_dict() for h in self.hosts],
                'disabled': self.disabled,
                'outputs': [o.to_dict() for o in self.outputs]}

class Machine(Named):
    def __init__(self):
        super().__init__()
        self.host = ''
        self.disabled = False
        self.assets = []
        self.constraints = []
        self.outputs = []

    def validate(self, sender, sentinel):
        super().validate(sender, sentinel)
        if not len(self.host.strip()):
            sentinel.error((*sender, self.name), "\"host\" is empty")
        for asset in self.assets:
            asset.validate((*sender, self.name), sentinel)
        for c in self.constraints:
            c.validate((*sender, self.name), sentinel)
        for o in self.outputs:
            o.validate((*sender, self.name), sentinel)
    
    def __str__(self):
        return "Machine(name: {}, host: {}, disabled: {}, assets: {}, constraints: {}, outputs: {})".format(repr(self.name), repr(self.host), repr(self.disabled), repr(self.assets), repr(self.constraints), repr(self.outputs))

    def to_dict(self):
        return {'name': self.name,
                'host': self.host,
                'disabled': self.disabled,
                'assets': [a.to_dict() for a in self.assets],
                'constraints': [c.to_dict() for c in self.constraints],
                'outputs': [o.to_dict() for o in self.outputs]}

class Asset(Named):
    def __init__(self, schema):
        super().__init__()
        self.definition = schema
        self.disabled = False
        self.data = {}
        self.outputs = []

    def __getattr__(self, name):
        return self.data[name]

    def validate(self, sender, sentinel):
        super().validate(sender, sentinel)
        self.definition.validate_asset((*sender, self.name), self, sentinel)
        for outp in self.outputs:
            outp.validate((*sender, self.name), sentinel)

    def __str__(self):
        return "Asset(name: {}, data: {}, disabled: {}, outputs: {})".format(repr(self.name), repr(self.data), repr(self.disabled), repr(self.outputs))

    def to_dict(self):
        return {'name': self.name,
                'disabled': self.disabled,
                'data': self.data,
                'outputs': [o.to_dict() for o in self.outputs],
                'type': self.definition.name}

class FileOutput:
    def __init__(self):
        super().__init__()
        self.perms = None
        self.template = None
        self.output = ''
        self.disabled = False

    def _validate_perms(self):
        perms = self.perms
        for p in (0o400,0o200,0o100):
            if perms >= p:
                perms -= p
        for p in (0o40,0o20,0o10):
            if perms >= p:
                perms -= p
        for p in (4,2,1):
            if perms >= p:
                perms -= p
        return perms == 0

    def validate(self, sender, sentinel):
        if not len(self.output.strip()):
            sentinel.error((*sender, self.__class__.__name__), '"output" is empty')
        if self.template is not None and not len(self.template.strip()):
            sentinel.error((*sender, self.__class__.__name__), '"template" is empty')
        if self.perms is not None and not self._validate_perms():
            sentinel.error((*sender, self.__class__.__name__), '"perms" ({}) are invalid permission set'.format(self.perms))

    def __str__(self):
        return "FileOutput(disabled: {}, perms: {}, template: {}, output: {})".format(repr(self.disabled), repr(self.perms), repr(self.template), repr(self.output))

    def to_dict(self):
        return {'perms': self.perms,
                'template': self.template,
                'output': self.output,
                'disabled': self.disabled}

class Field(Named):
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'

    def __init__(self):
        super().__init__()
        self.type = None
        self.disabled = False
        self.required = False
        self.tags = []
        self.default = None

    def validate_data(self, sender, value, sentinel):
        if self.required and value is None:
            sentinel.error((*sender, self.name), '"{}" is required'.format(self.name))
            return

        if self.type == self.STRING:
            if not isinstance(value, str) and value is not None:
                sentinel.error((*sender, self.name), '"{}" is not a string'.format(value))
        elif self.type == self.INT:
            if not isinstance(value, int) and value is not None:
                sentinel.error((*sender, self.name), '"{}" is not an int'.format(value))
        elif self.type == self.FLOAT:
            if not isinstance(value, float) and not isinstance(value, int) and value is not None:
                sentinel.error((*sender, self.name), '"{}" is not a float'.format(value))
        elif self.type == self.BOOL:
            if not isinstance(value, bool) and value is not None:
                sentinel.error((*sender, self.name), '"{}" is not a bool'.format(value))
        else:
            sentinel.error((*sender, self.name), '"{}" data type is undefined ("{}")'.format(self.name, self.type))

    def __str__(self):
        return "Field(name: {}, disabled: {}, type: {}, required: {}, tags: {}, default: {})".format(repr(self.name), repr(self.disabled), repr(self.type), repr(self.required), repr(self.tags), repr(self.default))

    def to_dict(self):
        return {'name': self.name,
                'type': self.type,
                'disabled': self.disabled,
                'required': self.required,
                'tags': self.tags,
                'default': self.default}

class Object(Named):
    def __init__(self):
        super().__init__()
        self.disabled = False
        self.outputs = []
        self.fields = {}

    def validate(self, sender, sentinel):
        super().validate(sentinel)
        for outp in self.outputs:
            outp.validate((*sender, self.name), sentinel)
        for field in self.fields.values():
            field.validate((*sender, self.name), sentinel)

    def validate_asset(self, sender, asset, sentinel):
        asset_fields = set(asset.data.keys())
        for field_id, field in self.fields.items():
            field.validate_data((*sender, self.name), asset.data.get(field_id), sentinel)
            asset_fields.discard(field_id)
        if asset_fields:
            sentinel.error((*sender, self.name), "extra fields specified: {}".format(', '.join(asset_fields)))
        for output in self.outputs:
            output.validate((*sender, self.name), sentinel)

    def __str__(self):
        return "Object(name: {}, disabled: {}, outputs: {}, fields: {})".format(repr(self.name), repr(self.disabled), repr(self.outputs), repr(self.fields))

    def to_dict(self):
        return {'name': self.name,
                'disabled': self.disabled,
                'outputs': [o.to_dict() for o in self.outputs],
                'fields': dict((key, value.to_dict()) for key, value in self.fields.items())}

class Constraint(Named):
    def __init__(self):
        self.code = None

    def __str__(self):
        return "Constraint(name: {}, code: {})".format(repr(self.name), repr(self.code))

    def to_dict(self):
        return {'name': self.name,
                'code': self.code}
