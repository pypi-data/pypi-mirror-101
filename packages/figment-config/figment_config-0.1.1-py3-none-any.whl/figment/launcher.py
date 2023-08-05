from .config import Configuration
from .exception import FigmentException
from .template import TemplateLoader
from .sentinel import Sentinel
import os
import logging

LOG = logging.getLogger(__name__)

class FigmentLauncher:
    def __init__(self, tpl_dirs):
        self._cfg = Configuration()
        self._tpl_dirs = tpl_dirs

    def load_config(self, filename):
        if os.path.isfile(filename):
            self._cfg.load(filename)
            return True
        else:
            return False

    def clear(self):
        self._cfg.clear()

    def save_config(self, filename):
        self._cfg.save(filename)

    def _get_template_loader(self, out_dir):
        return TemplateLoader(self._tpl_dirs, out_dir, self._cfg.assets, self._cfg.machines, self._cfg.environments)

    def validate(self):
        sentinel = Sentinel()
        self._cfg.validate(sentinel)
        return sentinel

    def _assert_valid(self):
        status = self.validate()
        if not status.ok:
            output = "validation failed\n"
            for group, msg in status.errors:
                output += "\t{} :: {}\n".format(group, msg)
            raise FigmentException(output)

    def make_for_machine(self, name, output_dir, tpl_args = {}):
        self._assert_valid()
        machine = self._cfg.machines.get(name)
        if machine is None:
            raise FigmentException('machine "{}" does not exist'.format(name))

        if machine.disabled:
            LOG.warn('machine "{}" is disabled'.format(machine.name))
            return
        LOG.info('>> machine: "{}"'.format(machine.name))
        loader = self._get_template_loader(output_dir)
        for outp in machine.outputs:
            loader.render(outp, {'machine': machine})
        for asset in machine.assets:
            if asset.disabled:
                LOG.warn('asset "{}" is disabled'.format(asset.name))
                continue
            elif asset.definition.disabled:
                LOG.warn('asset definition "{}" is disabled'.format(asset.definition.name))
                continue

            LOG.info('>>> asset: "{}"'.format(asset.name))
            tpl_data = tpl_args.copy()
            tpl_data.update({'machine': machine, 'asset': asset, 'object': asset.definition})

            for outp in asset.outputs:
                loader.render(outp, tpl_data)
            for obj_outp in asset.definition.outputs:
                loader.render(obj_outp, tpl_data)

    def make_for_environment(self, name, output_dir):
        env = self._cfg.environments.get(name)
        if env is None:
            raise FigmentException('environment "{}" does not exist'.format(name))
        elif env.disabled:
            LOG.warn('environment "{}" is disabled'.format(env.name))
            return
        LOG.info('> environment: "{}"'.format(name))
        if env.outputs:
            loader = self._get_template_loader(output_dir)
            for outp in env.outputs:
                loader.render(outp, {'environment': env})

        for machine in env.hosts:
            self.make_for_machine(machine.name, output_dir, {'environment': env})

    def make_all(self, output_dir):
        for env in self._cfg.environments.keys():
            self.make_for_environment(env, output_dir)
