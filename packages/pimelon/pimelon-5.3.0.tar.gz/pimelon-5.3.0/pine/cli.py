# imports - standard imports
import atexit
import json
import logging
import os
import pwd
import sys

# imports - third party imports
import click

# imports - module imports
import pine
from pine.app import get_apps
from pine.commands import pine_command
from pine.config.common_site_config import get_config
from pine.utils import PatchError, pine_cache_file, check_latest_version, drop_privileges, find_parent_pine, generate_command_cache, get_cmd_output, get_env_cmd, get_melon, is_pine_directory, is_dist_editable, is_root, log, setup_logging

from_command_line = False
change_uid_msg = "You should not run this command as root"
src = os.path.dirname(__file__)


def cli():
	global from_command_line
	from_command_line = True
	command = " ".join(sys.argv)

	change_working_directory()
	logger = setup_logging()
	logger.info(command)

	if len(sys.argv) > 1 and sys.argv[1] not in ("src", ):
		check_uid()
		change_uid()
		change_dir()

	if is_dist_editable(pine.PROJECT_NAME) and len(sys.argv) > 1 and sys.argv[1] != "src" and not get_config(".").get("developer_mode"):
		log("pine is installed in editable mode!\n\nThis is not the recommended mode of installation for production. Instead, install the package from PyPI with: `pip install pimelon`\n", level=3)

	if not is_pine_directory() and not cmd_requires_root() and len(sys.argv) > 1 and sys.argv[1] not in ("init", "find", "src"):
		log("Command not being executed in pine directory", level=3)

	if len(sys.argv) > 2 and sys.argv[1] == "melon":
		return old_melon_cli()

	elif len(sys.argv) > 1:
		if sys.argv[1] in get_melon_commands() + ["--site", "--verbose", "--force", "--profile"]:
			return melon_cmd()

		elif sys.argv[1] == "--help":
			print(click.Context(pine_command).get_help())
			print(get_melon_help())
			return

		elif sys.argv[1] in get_apps():
			return app_cmd()

	if not (len(sys.argv) > 1 and sys.argv[1] == "src"):
		atexit.register(check_latest_version)

	try:
		pine_command()
	except BaseException as e:
		return_code = getattr(e, "code", 0)
		if return_code:
			logger.warning("{0} executed with exit code {1}".format(command, return_code))
		sys.exit(return_code)


def check_uid():
	if cmd_requires_root() and not is_root():
		log('superuser privileges required for this command', level=3)
		sys.exit(1)


def cmd_requires_root():
	if len(sys.argv) > 2 and sys.argv[2] in ('production', 'sudoers', 'lets-encrypt', 'fonts',
		'print', 'firewall', 'ssh-port', 'role', 'fail2ban', 'wildcard-ssl'):
		return True
	if len(sys.argv) >= 2 and sys.argv[1] in ('patch', 'renew-lets-encrypt', 'disable-production'):
		return True
	if len(sys.argv) > 2 and sys.argv[1] in ('install'):
		return True


def change_dir():
	if os.path.exists('config.json') or "init" in sys.argv:
		return
	dir_path_file = '/etc/pimelon_dir'
	if os.path.exists(dir_path_file):
		with open(dir_path_file) as f:
			dir_path = f.read().strip()
		if os.path.exists(dir_path):
			os.chdir(dir_path)


def change_uid():
	if is_root() and not cmd_requires_root():
		melon_user = get_config(".").get('melon_user')
		if melon_user:
			drop_privileges(uid_name=melon_user, gid_name=melon_user)
			os.environ['HOME'] = pwd.getpwnam(melon_user).pw_dir
		else:
			log(change_uid_msg, level=3)
			sys.exit(1)


def old_melon_cli(pine_path='.'):
	f = get_melon(pine_path=pine_path)
	os.chdir(os.path.join(pine_path, 'sites'))
	os.execv(f, [f] + sys.argv[2:])


def app_cmd(pine_path='.'):
	f = get_env_cmd('python', pine_path=pine_path)
	os.chdir(os.path.join(pine_path, 'sites'))
	os.execv(f, [f] + ['-m', 'melon.utils.pine_helper'] + sys.argv[1:])


def melon_cmd(pine_path='.'):
	f = get_env_cmd('python', pine_path=pine_path)
	os.chdir(os.path.join(pine_path, 'sites'))
	os.execv(f, [f] + ['-m', 'melon.utils.pine_helper', 'melon'] + sys.argv[1:])


def get_melon_commands():
	if not is_pine_directory():
		return []

	if os.path.exists(pine_cache_file):
		command_dump = open(pine_cache_file, 'r').read() or '[]'
		return json.loads(command_dump)

	else:
		return generate_command_cache()


def get_melon_help(pine_path='.'):
	python = get_env_cmd('python', pine_path=pine_path)
	sites_path = os.path.join(pine_path, 'sites')
	try:
		out = get_cmd_output("{python} -m melon.utils.pine_helper get-melon-help".format(python=python), cwd=sites_path)
		return "\n\nFramework commands:\n" + out.split('Commands:')[1]
	except:
		return ""


def change_working_directory():
	"""Allows pine commands to be run from anywhere inside a pine directory"""
	cur_dir = os.path.abspath(".")
	pine_path = find_parent_pine(cur_dir)

	if pine_path:
		os.chdir(pine_path)
