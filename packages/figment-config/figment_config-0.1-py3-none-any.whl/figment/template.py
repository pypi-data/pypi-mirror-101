from jinja2 import Environment, FileSystemLoader
from .structs import FileOutput, FigmentJSONEncoder

import logging
import json
import os

LOG = logging.getLogger(__name__)

class TemplateLoader(object):
    def __init__(self, tpl_paths, out_path, assets, machines, environments):
        self._env = Environment(loader=FileSystemLoader(tpl_paths, followlinks=True))
        self._assets = assets
        self._machines = machines
        self._environments = environments
        self._output_dir = out_path

    def render(self, outp: FileOutput, template_data={}):
        if outp.disabled:
            # TODO: log
            return
        globals_ = {'assets': self._assets, 'machines': self._machines, 'environments': self._environments}
        template_data.update(globals_)

        tpl_file = outp.template.format(**template_data)
        out_file = os.path.join(self._output_dir, outp.output.format(**template_data))
        
        os.makedirs(os.path.dirname(out_file), 0o755, exist_ok=True)

        tpl = self._env.get_template(tpl_file)
        tpl.globals['to_json'] = lambda x: json.dumps(x, cls=FigmentJSONEncoder)

        with open(out_file, 'w') as fd:
            fd.write(tpl.render(**template_data))
        LOG.info('file output: "{}"'.format(out_file))

        if outp.perms is not None:
            os.chmod(out_file, outp.perms)
