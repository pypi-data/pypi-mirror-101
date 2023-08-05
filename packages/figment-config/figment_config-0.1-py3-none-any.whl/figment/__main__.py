from .launcher import FigmentLauncher
from .decorators import cli_entry
import click
import os
import logging

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}

FORMAT = '%(asctime)-15s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger('figment')
LOG.setLevel(logging.DEBUG)

def _get_config_file(cfg_file_arg):
    if cfg_file_arg:
        return cfg_file_arg
    else:
        env_cfg_file = os.environ.get('FIGMENT_CONFIG_FILE')
        if env_cfg_file is None:
            raise KeyError('FIGMENT_CONFIG_FILE environment variable not set -- please set or use \'--config-file\' option')
        return env_cfg_file

def _get_launcher(cfg_file):
    tpl_paths = [os.path.join(os.path.dirname(cfg_file), "templates"),
                 os.path.join(os.getcwd(), 'templates')]
    launcher = FigmentLauncher(tpl_paths)
    if not launcher.load_config(cfg_file):
        raise IOError('failed to load configuration file "{}"'.format(cfg_file))
    return launcher

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """
    figment - configuration management tool
    """
    pass

@main.group('make')
def make():
    """
    figment make -- produces configuration file outputs
    """
    pass

@make.command('machine')
@click.argument('name')
@click.option('-f', '--config-file', help='configuration file', metavar='CFG_FILE')
@click.option('-o', '--output-path', help='output path', required=True)
@cli_entry
def make_for_machine(name, config_file, output_path):
    """
    figment make machine -- produces configuration file outputs for a machine name
    """
    launcher = _get_launcher(_get_config_file(config_file))
    launcher.make_for_machine(name, output_path)

@make.command('host')
@click.argument('name')
@click.option('-f', '--config-file', help='configuration file', metavar='CFG_FILE')
@click.option('-o', '--output-path', help='output path', required=True)
@cli_entry
def make_for_host(name, config_file, output_path):
    """
    figment make host -- produces configuration file outputs for a machine name
    """
    launcher = _get_launcher(_get_config_file(config_file))
    launcher.make_for_machine(name, output_path)

@make.command('environment')
@click.argument('name')
@click.option('-f', '--config-file', help='configuration file', metavar='CFG_FILE')
@click.option('-o', '--output-path', help='output path', required=True)
@cli_entry
def make_for_environment(name, config_file, output_path):
    """
    figment make environment -- produces configuration file outputs for an environment name
    """
    launcher = _get_launcher(_get_config_file(config_file))
    launcher.make_for_environment(name, output_path)

@make.command('env')
@click.argument('name')
@click.option('-f', '--config-file', help='configuration file', metavar='CFG_FILE')
@click.option('-o', '--output-path', help='output path', required=True)
@cli_entry
def make_for_env(name, config_file, output_path):
    """
    figment make env -- produces configuration file outputs for an environment name
    """
    launcher = _get_launcher(_get_config_file(config_file))
    launcher.make_for_environment(name, output_path)

@make.command('all')
@click.option('-f', '--config-file', help='configuration file', metavar='CFG_FILE')
@click.option('-o', '--output-path', help='output path', required=True)
@cli_entry
def make_all(config_file, output_path):
    """
    figment make all -- produces configuration file outputs for all enabled environments, hosts, and assets
    """
    launcher = _get_launcher(_get_config_file(config_file))
    launcher.make_all(output_path)

@main.command('validate')
@click.option('-f', '--config-file', help='configuration file', metavar='CFG_FILE')
@cli_entry
def validate(config_file):
    """
    figment validate -- validates a configuration file
    """
    launcher = _get_launcher(_get_config_file(config_file))
    status = launcher.validate()
    if status.ok:
        LOG.info("validation passed")
    else:
        LOG.warning("validation failed")
        for module, err in status.errors:
            LOG.error('{} :: {}'.format(module, err))
