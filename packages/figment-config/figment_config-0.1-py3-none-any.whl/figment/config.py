from .structs import Environment, Object, Asset, Machine, Constraint, FileOutput, Field
from .runner import ConstraintRunner
import yaml
import logging

LOG = logging.getLogger(__name__)

class Configuration(object):
    def __init__(self):
        self.clear()

    def _assert_not_reserved(self, name):
        if name in ('type', 'output', 'name', 'disabled'):
            raise KeyError('"{}" is a reserved name'.format(name))

    def validate(self, sentinel):
        for env in self._envs.values():
            env.validate(tuple(), sentinel)
        for m in self._machines.values():
            if m.constraints:
                LOG.info('running constraints for "{}"'.format(m.name))
            for c in m.constraints:
                LOG.info(' - {}'.format(c.name))
                cr = ConstraintRunner(m.assets, c)
                cr.run(sentinel)
        #for asset in self._assets:
        #    asset.validate(sentinel)

    @property
    def environments(self):
        return self._envs

    @property
    def objects(self):
        return self._objs

    @property
    def assets(self):
        return self._assets

    @property
    def machines(self):
        return self._machines

    @property
    def constraints(self):
        return self._constraints

    def _load_constraints(self, src):
        dst = {}
        for name, code in src.items():
            self._assert_not_reserved(name)
            
            item = Constraint()
            item.name = name
            item.code = code
            dst[name] = item
        return dst

    def _get_object_output(self, data):
        if data['type'] == 'file':
            fo = FileOutput()
            fo.template = data['template']
            fo.perms = data.get('perms', 644)
            fo.disabled = data.get('disabled', False)
            fo.output = data['output']
            return fo
        else:
            raise NotImplementedError('output type "{}" not supported'.format(data['type']))

    def _get_object_field(self, name, data):
        field = Field()
        self._assert_not_reserved(name)
        field.name = name
        field.type = data['type']
        field.required = data.get('required', False)
        field.tags = data.get('tags', [])
        field.default = data.get('default', None)
        field.disabled = data.get('disabled', False)
        return field

    def _get_outputs(self, data):
        return [self._get_object_output(x) for x in data]

    def _load_objects(self, src):
        dst = {}
        for name, obj_data in src.items():
            self._assert_not_reserved(name)
            
            obj = Object()
            obj.name = name
            obj.disabled = obj_data.get('disabled', False)

            obj.outputs = self._get_outputs(obj_data.get('output', []))
            
            fields = {}
            for f_name, field_data in obj_data.get('fields', {}).items():
                fields[f_name] = self._get_object_field(f_name, field_data)
            obj.fields = fields

            dst[name] = obj
        return dst

    def _load_assets(self, src, obj_defs):
        dst = {}
        for name, asset_fields in src.items():
            self._assert_not_reserved(name)
            
            asset_fields = asset_fields.copy()
            asset_type = asset_fields['type']
            del asset_fields['type']

            obj_def = obj_defs.get(asset_type)
            if not obj_def:
                raise KeyError('"{}" is not a defined object definition'.format(asset_type))
            asset = Asset(obj_def)
            asset.name = name
            if 'disabled' in asset_fields:
                asset.disabled = asset_fields['disabled']
                del asset_fields['disabled']
            if 'output' in asset_fields:
                asset.outputs = self._get_outputs(asset_fields['output'])
                del asset_fields['output']
            asset.data = asset_fields
            dst[name] = asset
        return dst

    def _associate(self, item_type_name, items, pool):
        result = []
        names = set()
        for name in items:
            item = pool.get(name)
            if not item:
                raise KeyError('{} "{}" not found'.format(item_type_name, name))
            elif name in names:
                raise KeyError('{} "{}" already included'.format(item_type_name, name))
            names.update([name])
            result.append(item)
        return result

    def _load_machines(self, src, asset_pool, constraint_pool):
        dst = {}
        for name, host_data in src.items():
            m = Machine()
            m.name = name
            m.host = host_data['host']
            m.disabled = host_data.get('disabled', False)
            m.assets = self._associate('asset', host_data.get('assets', []), asset_pool)
            m.constraints = self._associate('constraint', host_data.get('constraints', []), constraint_pool)
            m.outputs = self._get_outputs(host_data.get('output', []))

            dst[name] = m
        return dst

    def _load_environments(self, src, machine_pool):
        dst = {}
        for env_name, env_data in src.items():
            env = Environment()
            env.name = env_name
            env.disabled = env_data.get('disabled', False)
            env.hosts = self._associate('host', env_data.get('hosts', []), machine_pool)
            env.outputs = self._get_outputs(env_data.get('output', []))
            dst[env_name] = env
        return dst

    def _load_data(self, data):
        # Load from lists/dicts into business objects
        constraints = self._load_constraints(data.get('constraints', {}))
        objs = self._load_objects(data['objects'])
        assets = self._load_assets(data['assets'], objs)
        machines = self._load_machines(data['machines'], assets, constraints)
        envs = self._load_environments(data['environments'], machines)

        # Replace when all correct
        self._envs = envs
        self._objs = objs
        self._assets = assets
        self._machines = machines
        self._constraints = constraints

    def _save_object_field(self, field):
        return {'type': field.type,
                'required': field.required,
                'tags': field.tags,
                'default': field.default,
                'disabled': field.disabled}

    def _save_constraints(self):
        return dict((c.name, c.code) for c in self._constraints.values())

    def _save_objects(self):
        results = {}
        for o in self._objs:
            fields = dict((f.name, self._save_object_field(f)) for f in o.fields)
            results[o.name] = {'output': self._save_outputs(o.outputs),
                               'fields': fields,
                               'disabled': o.disabled}
        return results

    def _save_assets(self):
        results = {}
        for asset in self._assets.values():
            asset_data = asset.data.copy()
            asset_data['type'] = asset.definition.name
            asset_data['output'] = self._save_outputs(asset.outputs)
            asset_data['disabled'] = asset.disabled
            results[asset.name] = asset_data
        return results

    def _save_machines(self):
        results = {}
        for m in self._machines.values():
            results[m.name] = {'host': m.host,
                               'disabled': m.disabled,
                               'assets': [a.name for a in m.assets],
                               'constraints': [c.name for c in m.constraints],
                               'output': self._save_outputs(m.outputs)}
        return results

    def _save_outputs(self, outputs):
        results = []
        for o in outputs:
            if isinstance(o, FileOutput):
                results.append({'type': 'file',
                                'template': o.template,
                                'perms': o.perms,
                                'output': o.output,
                                'disabled': o.disabled})
            else:
                raise NotImplementedError('cannot save output type "{}"'.format(o.__class__.__name__))
        return results

    def _save_environments(self):
        results = {}
        for env in self._envs.values():
            results[env.name] = {'disabled': env.disabled,
                                 'hosts': [h.name for h in env.hosts],
                                 'output': self._save_outputs(env.outputs)}
        return results

    def _save_data(self):
        return {'constraints': self._save_constraints(),
                'objects': self._save_objects(),
                'assets': self._save_assets(),
                'machines': self._save_machines(),
                'environments': self._save_environments()}

    def load(self, filename):
        with open(filename, 'r') as fd:
            cfg_data = yaml.load(fd.read(), Loader=yaml.Loader)
            self._load_data(cfg_data)
    
    def save(self, filename):
        with open(filename, 'w') as fd:
            cfg_data = self._save_data()
            yaml.dump(cfg_data, fd)
        
    def clear(self):
        self._envs = {}
        self._objs = {}
        self._assets = {}
        self._machines = {}
        self._constraints = {}
