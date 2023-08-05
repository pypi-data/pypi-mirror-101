import logging

LOG = logging.getLogger(__name__)

class ConstraintRunner(object):
    def __init__(self, assets, constraint):
        self._assets = assets
        self._constraint = constraint

    def run(self, sentinel):
        class AssetAccessor(object):
            def __init__(self, assets):
                self._assets = assets

            def _get_all_fields(self):
                for asset in self._assets:
                    for field_name, field_def in asset.definition.fields.items():
                        yield (asset, field_def, asset.data.get(field_name))

            def fields(self, **kwargs):
                tags = kwargs.get('tags')
                if tags:
                    for asset, field_def, field_value in self._get_all_fields():
                        for tag in field_def.tags:
                            if tag in tags:
                                yield (asset, field_def, field_value)
                else:
                    return self._get_all_fields()

        class Context(object):
            def __init__(self, name, sentinel, assets):
                self._name = name
                self._sentinel = sentinel
                self._assets = AssetAccessor(assets)
            
            def error(self, msg):
                self._sentinel.error(self._name, msg)

            @property
            def assets(self):
                return self._assets

        code = 'def _run_constraint():\n\t'+('\n\t'.join(self._constraint.code.split('\n')))+'\n_run_constraint()'
        ctx = Context(self._constraint.name, sentinel, self._assets)
        #LOG.info('running constraint check "{}"'.format(self._constraint.name))
        exec(code, {'self': ctx})
