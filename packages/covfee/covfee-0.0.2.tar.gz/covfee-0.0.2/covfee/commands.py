import os
import sys
import json
from shutil import which
from colorama import init, Fore
from halo import Halo

import click
from covfee.server.orm import app
from .cli.utils import working_directory
from .cli.project_folder import ProjectFolder



@click.command()
def cmd_start_webpack():
    folder = ProjectFolder(os.getcwd())
    if not folder.is_project():
        return print(Fore.RED+'Working directory is not a valid covfee project folder. Did you run covfee-maker in the current folder?')

    cwd = os.getcwd()
    # run the dev server
    covfee_client_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'client')
    with working_directory(covfee_client_path):
        os.system('npx webpack serve' +
        ' --env COVFEE_WD=' + cwd +
        ' --config ./webpack.dev.js')


def start_dev():
    os.environ['UNSAFE_MODE_ON'] = 'enable'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'covfee.server.start:create_app'
    os.system(sys.executable + ' -m flask run')


@click.command()
def cmd_start_dev():
    start_dev()


def start_prod(unsafe):
    folder = ProjectFolder(os.getcwd())
    if not folder.is_project():
        raise Exception('Working directory is not a valid covfee project folder.')
    if unsafe:
        os.environ['UNSAFE_MODE_ON'] = 'enable'
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_APP'] = 'covfee.server.start:create_app'
    os.system(f'gunicorn -b {app.config["SERVER_SOCKET"]} \'covfee.server.start:create_app()\'')


@click.command()
@click.option('--unsafe', is_flag=True, help='Disables authentication.')
@click.option('--no-launch', is_flag=True, help='Disables launching of the web browser.')
def cmd_start_prod(unsafe, no_launch):
    folder = ProjectFolder(os.getcwd())
    if not folder.is_project():
        return print(Fore.RED+'Working directory is not a valid covfee project folder. Did you run covfee-maker in the current folder?')

    if not no_launch:
        open_covfee_admin()

    start_prod(unsafe)


def build():
    folder = ProjectFolder(os.getcwd())
    if not folder.is_project():
        raise Exception('Working directory is not a valid covfee project folder.')

    cwd = os.getcwd()

    bundle_path = app.config['PROJECT_WWW_PATH']
    covfee_client_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'client')

    with working_directory(covfee_client_path):
        os.system('npx webpack' +
                ' --env COVFEE_WD=' + cwd +
                ' --config ./webpack.prod.js' + ' --output-path '+bundle_path)


def build_master():
    bundle_path = app.config['MASTER_BUNDLE_PATH']
    covfee_client_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'client')
    with working_directory(covfee_client_path):
        os.system('npx webpack' +
                    ' --config ./webpack.prod.js' + ' --output-path '+bundle_path)

@click.command()
@click.option('--master', is_flag=True, help='Builds the covfee master bundles.')
def cmd_build(master):
    if master:
        build_master()
    else:
        build()


def install_js():
    cli_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cli')
    with working_directory(cli_path):
        os.system('npm install')

    client_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'client')
    with working_directory(client_path):
        os.system('npm install')


@click.command()
def cmd_install_js():
    install_js()

def print_admin_url():
    print(Fore.GREEN + f' * covfee is available at {app.config["ADMIN_URL"]}')

def open_covfee_admin():
    if which('xdg-open') is not None:
        os.system(f'xdg-open {app.config["ADMIN_URL"]}')
    elif sys.platform == 'darwin' and which('open') is not None:
        os.system(f'open {app.config["ADMIN_URL"]}')
    else:
        print_admin_url()


@click.command()
def cmd_open():
    open_covfee_admin()
