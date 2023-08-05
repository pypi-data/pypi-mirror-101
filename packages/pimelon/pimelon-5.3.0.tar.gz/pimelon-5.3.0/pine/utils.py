#!/usr/bin/env python
# -*- coding: utf-8 -*-

# imports - standard imports
import compileall
import errno
import glob
import grp
import itertools
import json
import logging
import multiprocessing
import os
import pwd
import re
import select
import shutil
import site
import subprocess
import sys
from datetime import datetime
from distutils.spawn import find_executable

# imports - third party imports
import click
from crontab import CronTab
import requests
from semantic_version import Version
from six import iteritems
from six.moves.urllib.parse import urlparse

# imports - module imports
import pine


class PatchError(Exception):
	pass

class CommandFailedError(Exception):
	pass

logger = logging.getLogger(pine.PROJECT_NAME)
pine_cache_file = '.pine.cmd'
folders_in_pine = ('apps', 'sites', 'config', 'logs', 'config/pids')
sudoers_file = '/etc/sudoers.d/melon'


class color:
	nc = '\033[0m'
	blue = '\033[94m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	silver = '\033[90m'


def is_pine_directory(directory=os.path.curdir):
	is_pine = True

	for folder in folders_in_pine:
		path = os.path.abspath(os.path.join(directory, folder))
		is_pine = is_pine and os.path.exists(path)

	return is_pine


def log(message, level=0):
	levels = {
		0: color.blue + 'INFO',			# normal
		1: color.green + 'SUCCESS',		# success
		2: color.red + 'ERROR',			# fail
		3: color.yellow + 'WARN'		# warn/suggest
	}
	loggers = {
		2: logger.error,
		3: logger.warning
	}

	start_line = (levels.get(level) + ': ') if level in levels else ''
	level_logger = loggers.get(level, logger.info)
	end_line = '\033[0m'

	level_logger(message)
	print(start_line + message + end_line)


def safe_decode(string, encoding = 'utf-8'):
	try:
		string = string.decode(encoding)
	except Exception:
		pass
	return string


def check_latest_version():
	try:
		pypi_request = requests.get("https://pypi.org/pypi/pimelon/json")
	except Exception:
		# Exceptions thrown are defined in requests.exceptions
		# ignore checking on all Exceptions
		return

	if pypi_request.status_code == 200:
		pypi_version_str = pypi_request.json().get('info').get('version')
		pypi_version = Version(pypi_version_str)
		local_version = Version(pine.VERSION)

		if pypi_version > local_version:
			log("A newer version of pine is available: {0} → {1}".format(local_version, pypi_version))


def get_melon(pine_path='.'):
	melon = get_env_cmd('melon', pine_path=pine_path)
	if not os.path.exists(melon):
		print('melon app is not installed. Run the following command to install melon')
		print('pine get-app https://github.com/amonak/melon.git')
	return melon


def get_env_cmd(cmd, pine_path='.'):
	return os.path.abspath(os.path.join(pine_path, 'env', 'bin', cmd))


def init(path, apps_path=None, no_procfile=False, no_backups=False,
		melon_path=None, melon_branch=None, verbose=False, clone_from=None,
		skip_redis_config_generation=False, clone_without_update=False, ignore_exist=False, skip_assets=False,
		python='python3'):
	"""Initialize a new pine directory"""
	from pine.app import get_app, install_apps_from_path
	from pine.config import redis
	from pine.config.common_site_config import make_config
	from pine.config.procfile import setup_procfile
	from pine.patches import set_all_patches_executed

	if os.path.exists(path) and not ignore_exist:
		log('Path {path} already exists!'.format(path=path))
		sys.exit(0)
	elif not os.path.exists(path):
		# only create dir if it does not exist
		os.makedirs(path)

	for dirname in folders_in_pine:
		try:
			os.makedirs(os.path.join(path, dirname))
		except OSError as e:
			if e.errno == errno.EEXIST:
				pass

	setup_logging(pine_path=path)

	setup_env(pine_path=path, python=python)

	make_config(path)

	if clone_from:
		clone_apps_from(pine_path=path, clone_from=clone_from, update_app=not clone_without_update)
	else:
		if not melon_path:
			melon_path = 'https://github.com/amonak/melon.git'

		get_app(melon_path, branch=melon_branch, pine_path=path, skip_assets=True, verbose=verbose)

		if apps_path:
			install_apps_from_path(apps_path, pine_path=path)


	pine.set_melon_version(pine_path=path)
	if pine.MELON_VERSION > 1:
		if not skip_assets:
			update_node_packages(pine_path=path)

	set_all_patches_executed(pine_path=path)
	if not skip_assets:
		build_assets(pine_path=path)

	if not skip_redis_config_generation:
		redis.generate_config(path)

	if not no_procfile:
		setup_procfile(path, skip_redis=skip_redis_config_generation)
	if not no_backups:
		setup_backups(pine_path=path)

	copy_patches_txt(path)


def update(pull=False, apps=None, patch=False, build=False, requirements=False, backup=True, compile=True,
	force=False, reset=False, restart_supervisor=False, restart_systemd=False):
	"""command: pine update"""
	from pine import patches
	from pine.app import is_version_upgrade, pull_apps, validate_branch
	from pine.config.common_site_config import get_config, update_config

	pine_path = os.path.abspath(".")
	patches.run(pine_path=pine_path)
	conf = get_config(pine_path)

	if apps and not pull:
		apps = []

	clear_command_cache(pine_path='.')

	if conf.get('release_pine'):
		print('Release pine detected, cannot update!')
		sys.exit(1)

	if not (pull or patch or build or requirements):
		pull, patch, build, requirements = True, True, True, True

	validate_branch()
	version_upgrade = is_version_upgrade()

	if version_upgrade[0]:
		if force:
			print("Force flag has been used for a major version change in Melon and it's apps. \nThis will take significant time to migrate and might break custom apps.")
		else:
			print("This update will cause a major version change in Melon/Monak from {0} to {1}. \nThis would take significant time to migrate and might break custom apps.".format(*version_upgrade[1:]))
			click.confirm('Do you want to continue?', abort=True)

	if version_upgrade[0] or (not version_upgrade[0] and force):
		validate_upgrade(version_upgrade[1], version_upgrade[2], pine_path=pine_path)
	conf.update({ "maintenance_mode": 1, "pause_scheduler": 1 })
	update_config(conf, pine_path=pine_path)

	if backup:
		print('Backing up sites...')
		backup_all_sites(pine_path=pine_path)

	if apps:
		apps = [app.strip() for app in re.split(",| ", apps) if app]

	if pull:
		pull_apps(apps=apps, pine_path=pine_path, reset=reset)

	if requirements:
		update_requirements(pine_path=pine_path)
		update_node_packages(pine_path=pine_path)

	if patch:
		print('Patching sites...')
		patch_sites(pine_path=pine_path)

	if build:
		build_assets(pine_path=pine_path)

	if version_upgrade[0] or (not version_upgrade[0] and force):
		post_upgrade(version_upgrade[1], version_upgrade[2], pine_path=pine_path)

	if pull and compile:
		print("Compiling Python files...")
		compileall.compile_dir('../apps', quiet=1, rx=re.compile('.*node_modules.*'))

	if restart_supervisor or conf.get('restart_supervisor_on_update'):
		restart_supervisor_processes(pine_path=pine_path)

	if restart_systemd or conf.get('restart_systemd_on_update'):
		restart_systemd_processes(pine_path=pine_path)

	conf.update({ "maintenance_mode": 0, "pause_scheduler": 0 })
	update_config(conf, pine_path=pine_path)

	print("_" * 80 + "\nPine: Deployment tool for MonakERP and MonakERP Applications")


def copy_patches_txt(pine_path):
	shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches', 'patches.txt'),
		os.path.join(pine_path, 'patches.txt'))


def clone_apps_from(pine_path, clone_from, update_app=True):
	from .app import install_app
	print('Copying apps from {0}...'.format(clone_from))
	subprocess.check_output(['cp', '-R', os.path.join(clone_from, 'apps'), pine_path])

	node_modules_path = os.path.join(clone_from, 'node_modules')
	if os.path.exists(node_modules_path):
		print('Copying node_modules from {0}...'.format(clone_from))
		subprocess.check_output(['cp', '-R', node_modules_path, pine_path])

	def setup_app(app):
		# run git reset --hard in each branch, pull latest updates and install_app
		app_path = os.path.join(pine_path, 'apps', app)

		# remove .egg-ino
		subprocess.check_output(['rm', '-rf', app + '.egg-info'], cwd=app_path)

		if update_app and os.path.exists(os.path.join(app_path, '.git')):
			remotes = subprocess.check_output(['git', 'remote'], cwd=app_path).strip().split()
			if 'upstream' in remotes:
				remote = 'upstream'
			else:
				remote = remotes[0]
			print('Cleaning up {0}'.format(app))
			branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=app_path).strip()
			subprocess.check_output(['git', 'reset', '--hard'], cwd=app_path)
			subprocess.check_output(['git', 'pull', '--rebase', remote, branch], cwd=app_path)

		install_app(app, pine_path, restart_pine=False)

	with open(os.path.join(clone_from, 'sites', 'apps.txt'), 'r') as f:
		apps = f.read().splitlines()

	for app in apps:
		setup_app(app)


def exec_cmd(cmd, cwd='.'):
	import shlex
	print("{0}$ {1}{2}".format(color.silver, cmd, color.nc))
	cwd_info = "cd {0} && ".format(cwd) if cwd != "." else ""
	cmd_log = "{0}{1}".format(cwd_info, cmd)
	logger.debug(cmd_log)
	cmd = shlex.split(cmd)
	return_code = subprocess.call(cmd, cwd=cwd, universal_newlines=True)
	if return_code:
		logger.warning("{0} executed with exit code {1}".format(cmd_log, return_code))


def which(executable, raise_err = False):
	exec_ = find_executable(executable)

	if not exec_ and raise_err:
		raise ValueError('{executable} not found.'.format(
			executable = executable
		))

	return exec_


def get_venv_path():
	venv = which('virtualenv')

	if not venv:
		current_python = sys.executable
		with open(os.devnull, "wb") as devnull:
			is_venv_installed = not subprocess.call([current_python, "-m", "venv", "--help"], stdout=devnull)
		if is_venv_installed:
			venv = "{} -m venv".format(current_python)

	return venv or log("virtualenv cannot be found", level=2)

def setup_env(pine_path='.', python='python3'):
	melon = os.path.join(pine_path, "apps", "melon")
	pip = os.path.join(pine_path, "env", "bin", "pip")
	virtualenv = get_venv_path()

	exec_cmd('{} -q env -p {}'.format(virtualenv, python), cwd=pine_path)

	if os.path.exists(melon):
		exec_cmd('{} install -q -U -e {}'.format(pip, melon), cwd=pine_path)


def setup_socketio(pine_path='.'):
	exec_cmd("npm install socket.io redis express superagent cookie babel-core less chokidar \
		babel-cli babel-preset-es2015 babel-preset-es2016 babel-preset-es2017 babel-preset-babili", cwd=pine_path)


def patch_sites(pine_path='.'):
	pine.set_melon_version(pine_path=pine_path)

	try:
		if pine.MELON_VERSION == 0:
			exec_cmd("{melon} --latest all".format(melon=get_melon(pine_path=pine_path)), cwd=os.path.join(pine_path, 'sites'))
		else:
			run_melon_cmd('--site', 'all', 'migrate', pine_path=pine_path)
	except subprocess.CalledProcessError:
		raise PatchError


def build_assets(pine_path='.', app=None):
	pine.set_melon_version(pine_path=pine_path)

	if pine.MELON_VERSION == 0:
		exec_cmd("{melon} --build".format(melon=get_melon(pine_path=pine_path)), cwd=os.path.join(pine_path, 'sites'))
	else:
		command = 'pine build'
		if app:
			command += ' --app {}'.format(app)
		exec_cmd(command, cwd=pine_path)


def get_sites(pine_path='.'):
	sites_path = os.path.join(pine_path, 'sites')
	sites = (site for site in os.listdir(sites_path) if os.path.exists(os.path.join(sites_path, site, 'site_config.json')))
	return sites


def setup_backups(pine_path='.'):
	from pine.config.common_site_config import get_config
	logger.log('setting up backups')

	pine_dir = os.path.abspath(pine_path)
	user = get_config(pine_path=pine_dir).get('melon_user')
	logfile = os.path.join(pine_dir, 'logs', 'backup.log')
	pine.set_melon_version(pine_path=pine_path)
	system_crontab = CronTab(user=user)

	if pine.MELON_VERSION == 0:
		backup_command = "cd {sites_dir} && {melon} --backup all".format(melon=get_melon(pine_path=pine_path),)
	else:
		backup_command = "cd {pine_dir} && {pine} --verbose --site all backup".format(pine_dir=pine_dir, pine=sys.argv[0])

	job_command = "{backup_command} >> {logfile} 2>&1".format(backup_command=backup_command, logfile=logfile)

	if job_command not in str(system_crontab):
		job = system_crontab.new(command=job_command, comment="pine auto backups set for every 12 hours")
		job.every(12).hours()
		system_crontab.write()


def setup_sudoers(user):
	if not os.path.exists('/etc/sudoers.d'):
		os.makedirs('/etc/sudoers.d')

		set_permissions = False
		if not os.path.exists('/etc/sudoers'):
			set_permissions = True

		with open('/etc/sudoers', 'a') as f:
			f.write('\n#includedir /etc/sudoers.d\n')

		if set_permissions:
			os.chmod('/etc/sudoers', 0o440)

	template = pine.config.env.get_template('melon_sudoers')
	melon_sudoers = template.render(**{
		'user': user,
		'service': find_executable('service'),
		'systemctl': find_executable('systemctl'),
		'nginx': find_executable('nginx'),
	})
	melon_sudoers = safe_decode(melon_sudoers)

	with open(sudoers_file, 'w') as f:
		f.write(melon_sudoers)

	os.chmod(sudoers_file, 0o440)
	log("Sudoers was set up for user {}".format(user), level=1)


def setup_logging(pine_path='.'):
	LOG_LEVEL = 15
	logging.addLevelName(LOG_LEVEL, "LOG")
	def logv(self, message, *args, **kws):
		if self.isEnabledFor(LOG_LEVEL):
			self._log(LOG_LEVEL, message, args, **kws)
	logging.Logger.log = logv

	if os.path.exists(os.path.join(pine_path, 'logs')):
		log_file = os.path.join(pine_path, 'logs', 'pine.log')
		hdlr = logging.FileHandler(log_file)
	else:
		hdlr = logging.NullHandler()

	logger = logging.getLogger(pine.PROJECT_NAME)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.DEBUG)

	return logger


def get_process_manager():
	for proc_man in ['honcho', 'foreman', 'forego']:
		proc_man_path = find_executable(proc_man)
		if proc_man_path:
			return proc_man_path


def start(no_dev=False, concurrency=None, procfile=None, no_prefix=False):
	program = get_process_manager()
	if not program:
		raise Exception("No process manager found")
	os.environ['PYTHONUNBUFFERED'] = "true"
	if not no_dev:
		os.environ['DEV_SERVER'] = "true"

	command = [program, 'start']
	if concurrency:
		command.extend(['-c', concurrency])

	if procfile:
		command.extend(['-f', procfile])

	if no_prefix:
		command.extend(['--no-prefix'])

	os.execv(program, command)


def get_git_version():
	'''returns git version from `git --version`
	extracts version number from string `get version 1.9.1` etc'''
	version = get_cmd_output("git --version")
	version = safe_decode(version)
	version = version.strip().split()[2]
	version = '.'.join(version.split('.')[0:2])
	return float(version)


def check_git_for_shallow_clone():
	from .config.common_site_config import get_config
	config = get_config('.')

	if config:
		if config.get('release_pine'):
			return False

		if not config.get('shallow_clone'):
			return False

	git_version = get_git_version()
	if git_version > 1.9:
		return True


def get_cmd_output(cmd, cwd='.', _raise=True):
	output = ""
	try:
		output = subprocess.check_output(cmd, cwd=cwd, shell=True, stderr=subprocess.PIPE).strip()
	except subprocess.CalledProcessError as e:
		if e.output:
			output = e.output
		elif _raise:
			raise
	return safe_decode(output)


def restart_supervisor_processes(pine_path='.', web_workers=False):
	from .config.common_site_config import get_config
	conf = get_config(pine_path=pine_path)
	pine_name = get_pine_name(pine_path)

	cmd = conf.get('supervisor_restart_cmd')
	if cmd:
		exec_cmd(cmd, cwd=pine_path)

	else:
		supervisor_status = get_cmd_output('supervisorctl status', cwd=pine_path)
		supervisor_status = safe_decode(supervisor_status)

		if web_workers and '{pine_name}-web:'.format(pine_name=pine_name) in supervisor_status:
			group = '{pine_name}-web:	'.format(pine_name=pine_name)

		elif '{pine_name}-workers:'.format(pine_name=pine_name) in supervisor_status:
			group = '{pine_name}-workers: {pine_name}-web:'.format(pine_name=pine_name)

		# backward compatibility
		elif '{pine_name}-processes:'.format(pine_name=pine_name) in supervisor_status:
			group = '{pine_name}-processes:'.format(pine_name=pine_name)

		# backward compatibility
		else:
			group = 'melon:'

		exec_cmd('supervisorctl restart {group}'.format(group=group), cwd=pine_path)


def restart_systemd_processes(pine_path='.', web_workers=False):
	pine_name = get_pine_name(pine_path)
	exec_cmd('sudo systemctl stop -- $(systemctl show -p Requires {pine_name}.target | cut -d= -f2)'.format(pine_name=pine_name))
	exec_cmd('sudo systemctl start -- $(systemctl show -p Requires {pine_name}.target | cut -d= -f2)'.format(pine_name=pine_name))


def set_default_site(site, pine_path='.'):
	if site not in get_sites(pine_path=pine_path):
		raise Exception("Site not in pine")
	exec_cmd("{melon} --use {site}".format(melon=get_melon(pine_path=pine_path), site=site),
			cwd=os.path.join(pine_path, 'sites'))


def update_env_pip(pine_path):
	env_pip = os.path.join(pine_path, 'env', 'bin', 'pip')
	exec_cmd("{pip} install -q -U pip".format(pip=env_pip))


def update_requirements(pine_path='.'):
	from pine.app import get_apps, install_app
	print('Installing applications...')

	update_env_pip(pine_path)

	for app in get_apps():
		install_app(app, pine_path=pine_path, skip_assets=True, restart_pine=False)


def update_python_packages(pine_path='.'):
	from pine.app import get_apps
	pip_path = os.path.join(pine_path, "env", "bin", "pip")
	print('Updating Python libraries...')

	update_env_pip(pine_path)
	for app in get_apps():
		print('\n{0}Installing python dependencies for {1}{2}'.format(color.yellow, app, color.nc))
		app_path = os.path.join(pine_path, "apps", app)
		exec_cmd("{0} install -q -U -e {1}".format(pip_path, app_path), cwd=pine_path)


def update_node_packages(pine_path='.'):
	print('Updating node packages...')
	from pine.app import get_develop_version
	from distutils.version import LooseVersion
	v = LooseVersion(get_develop_version('melon', pine_path = pine_path))

	# After rollup was merged, melon_version = 3.1
	# if develop_verion is 4 and up, only then install yarn
	if v < LooseVersion('4.x.x-develop'):
		update_npm_packages(pine_path)
	else:
		update_yarn_packages(pine_path)


def update_yarn_packages(pine_path='.'):
	apps_dir = os.path.join(pine_path, 'apps')

	if not find_executable('yarn'):
		print("Please install yarn using below command and try again.")
		print("`npm install -g yarn`")
		return

	for app in os.listdir(apps_dir):
		app_path = os.path.join(apps_dir, app)
		if os.path.exists(os.path.join(app_path, 'package.json')):
			print('\n{0}Installing node dependencies for {1}{2}'.format(color.yellow, app, color.nc))
			exec_cmd('yarn install', cwd=app_path)


def update_npm_packages(pine_path='.'):
	apps_dir = os.path.join(pine_path, 'apps')
	package_json = {}

	for app in os.listdir(apps_dir):
		package_json_path = os.path.join(apps_dir, app, 'package.json')

		if os.path.exists(package_json_path):
			with open(package_json_path, "r") as f:
				app_package_json = json.loads(f.read())
				# package.json is usually a dict in a dict
				for key, value in iteritems(app_package_json):
					if not key in package_json:
						package_json[key] = value
					else:
						if isinstance(value, dict):
							package_json[key].update(value)
						elif isinstance(value, list):
							package_json[key].extend(value)
						else:
							package_json[key] = value

	if package_json is {}:
		with open(os.path.join(os.path.dirname(__file__), 'package.json'), 'r') as f:
			package_json = json.loads(f.read())

	with open(os.path.join(pine_path, 'package.json'), 'w') as f:
		f.write(json.dumps(package_json, indent=1, sort_keys=True))

	exec_cmd('npm install', cwd=pine_path)


def backup_site(site, pine_path='.'):
	pine.set_melon_version(pine_path=pine_path)

	if pine.MELON_VERSION == 0:
		exec_cmd("{melon} --backup {site}".format(melon=get_melon(pine_path=pine_path), site=site),
				cwd=os.path.join(pine_path, 'sites'))
	else:
		run_melon_cmd('--site', site, 'backup', pine_path=pine_path)


def backup_all_sites(pine_path='.'):
	for site in get_sites(pine_path=pine_path):
		backup_site(site, pine_path=pine_path)


def is_root():
	if os.getuid() == 0:
		return True
	return False


def set_mariadb_host(host, pine_path='.'):
	update_common_site_config({'db_host': host}, pine_path=pine_path)


def set_redis_cache_host(host, pine_path='.'):
	update_common_site_config({'redis_cache': "redis://{}".format(host)}, pine_path=pine_path)


def set_redis_queue_host(host, pine_path='.'):
	update_common_site_config({'redis_queue': "redis://{}".format(host)}, pine_path=pine_path)


def set_redis_socketio_host(host, pine_path='.'):
	update_common_site_config({'redis_socketio': "redis://{}".format(host)}, pine_path=pine_path)


def update_common_site_config(ddict, pine_path='.'):
	update_json_file(os.path.join(pine_path, 'sites', 'common_site_config.json'), ddict)


def update_json_file(filename, ddict):
	if os.path.exists(filename):
		with open(filename, 'r') as f:
			content = json.load(f)

	else:
		content = {}

	content.update(ddict)
	with open(filename, 'w') as f:
		json.dump(content, f, indent=1, sort_keys=True)


def drop_privileges(uid_name='nobody', gid_name='nogroup'):
	# from http://stackoverflow.com/a/2699996
	if os.getuid() != 0:
		# We're not root so, like, whatever dude
		return

	# Get the uid/gid from the name
	running_uid = pwd.getpwnam(uid_name).pw_uid
	running_gid = grp.getgrnam(gid_name).gr_gid

	# Remove group privileges
	os.setgroups([])

	# Try setting the new uid/gid
	os.setgid(running_gid)
	os.setuid(running_uid)

	# Ensure a very conservative umask
	os.umask(0o22)


def fix_prod_setup_perms(pine_path='.', melon_user=None):
	from .config.common_site_config import get_config

	if not melon_user:
		melon_user = get_config(pine_path).get('melon_user')

	if not melon_user:
		print("melon user not set")
		sys.exit(1)

	globs = ["logs/*", "config/*"]
	for glob_name in globs:
		for path in glob.glob(glob_name):
			uid = pwd.getpwnam(melon_user).pw_uid
			gid = grp.getgrnam(melon_user).gr_gid
			os.chown(path, uid, gid)


def get_current_melon_version(pine_path='.'):
	from .app import get_current_melon_version as fv
	return fv(pine_path=pine_path)


def run_melon_cmd(*args, **kwargs):
	from .cli import from_command_line

	pine_path = kwargs.get('pine_path', '.')
	f = get_env_cmd('python', pine_path=pine_path)
	sites_dir = os.path.join(pine_path, 'sites')

	is_async = False if from_command_line else True
	if is_async:
		stderr = stdout = subprocess.PIPE
	else:
		stderr = stdout = None

	p = subprocess.Popen((f, '-m', 'melon.utils.pine_helper', 'melon') + args,
		cwd=sites_dir, stdout=stdout, stderr=stderr)

	if is_async:
		return_code = print_output(p)
	else:
		return_code = p.wait()

	if return_code > 0:
		sys.exit(return_code)


def validate_upgrade(from_ver, to_ver, pine_path='.'):
	if to_ver >= 2:
		if not find_executable('npm') and not (find_executable('node') or find_executable('nodejs')):
			raise Exception("Please install nodejs and npm")


def post_upgrade(from_ver, to_ver, pine_path='.'):
	from .config.common_site_config import get_config
	from .config import redis
	from .config.supervisor import generate_supervisor_config
	from .config.nginx import make_nginx_conf
	conf = get_config(pine_path=pine_path)
	print("-" * 80 + "Your pine was upgraded to version {0}".format(to_ver))

	if conf.get('restart_supervisor_on_update'):
		redis.generate_config(pine_path=pine_path)
		generate_supervisor_config(pine_path=pine_path)
		make_nginx_conf(pine_path=pine_path)

		if from_ver == 0 and to_ver == 1:
			setup_backups(pine_path=pine_path)

		if from_ver <= 1 and to_ver == 2:
			setup_socketio(pine_path=pine_path)

		message = """
As you have setup your pine for production, you will have to reload configuration for nginx and supervisor. To complete the migration, please run the following commands
sudo service nginx restart
sudo supervisorctl reload
		""".strip()
		print(message)


def update_translations_p(args):
	try:
		update_translations(*args)
	except requests.exceptions.HTTPError:
		print('Download failed for', args[0], args[1])


def download_translations_p():
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	langs = get_langs()
	apps = ('melon', 'monak')
	args = list(itertools.product(apps, langs))

	pool.map(update_translations_p, args)


def download_translations():
	langs = get_langs()
	apps = ('melon', 'monak')
	for app, lang in itertools.product(apps, langs):
		update_translations(app, lang)


def get_langs():
	lang_file = 'apps/melon/melon/geo/languages.json'
	with open(lang_file) as f:
		langs = json.loads(f.read())
	return [d['code'] for d in langs]


def update_translations(app, lang):
	translations_dir = os.path.join('apps', app, app, 'translations')
	csv_file = os.path.join(translations_dir, lang + '.csv')
	url = "https://translate.monakerp.com/files/{}-{}.csv".format(app, lang)
	r = requests.get(url, stream=True)
	r.raise_for_status()

	with open(csv_file, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			# filter out keep-alive new chunks
			if chunk:
				f.write(chunk)
				f.flush()

	print('downloaded for', app, lang)


def print_output(p):
	while p.poll() is None:
		readx = select.select([p.stdout.fileno(), p.stderr.fileno()], [], [])[0]
		send_buffer = []
		for fd in readx:
			if fd == p.stdout.fileno():
				while 1:
					buf = p.stdout.read(1)
					if not len(buf):
						break
					if buf == '\r' or buf == '\n':
						send_buffer.append(buf)
						log_line(''.join(send_buffer), 'stdout')
						send_buffer = []
					else:
						send_buffer.append(buf)

			if fd == p.stderr.fileno():
				log_line(p.stderr.readline(), 'stderr')
	return p.poll()


def log_line(data, stream):
	if stream == 'stderr':
		return sys.stderr.write(data)
	return sys.stdout.write(data)


def get_pine_name(pine_path):
	return os.path.basename(os.path.abspath(pine_path))


def setup_fonts():
	fonts_path = os.path.join('/tmp', 'fonts')

	if os.path.exists('/etc/fonts_backup'):
		return

	exec_cmd("git clone https://github.com/amonak/fonts.git", cwd='/tmp')
	os.rename('/etc/fonts', '/etc/fonts_backup')
	os.rename('/usr/share/fonts', '/usr/share/fonts_backup')
	os.rename(os.path.join(fonts_path, 'etc_fonts'), '/etc/fonts')
	os.rename(os.path.join(fonts_path, 'usr_share_fonts'), '/usr/share/fonts')
	shutil.rmtree(fonts_path)
	exec_cmd("fc-cache -fv")


def set_git_remote_url(git_url, pine_path='.'):
	"Set app remote git url"
	app = git_url.rsplit('/', 1)[1].rsplit('.', 1)[0]

	if app not in pine.app.get_apps(pine_path):
		print("No app named {0}".format(app))
		sys.exit(1)

	app_dir = pine.app.get_repo_dir(app, pine_path=pine_path)
	if os.path.exists(os.path.join(app_dir, '.git')):
		exec_cmd("git remote set-url upstream {}".format(git_url), cwd=app_dir)


def run_playbook(playbook_name, extra_vars=None, tag=None):
	if not find_executable('ansible'):
		print("Ansible is needed to run this command, please install it using 'pip install ansible'")
		sys.exit(1)
	args = ['ansible-playbook', '-c', 'local', playbook_name, '-vvvv']

	if extra_vars:
		args.extend(['-e', json.dumps(extra_vars)])

	if tag:
		args.extend(['-t', tag])

	subprocess.check_call(args, cwd=os.path.join(pine.__path__[0], 'playbooks'))


def find_pinees(directory=None):
	if not directory:
		directory = os.path.expanduser("~")
	elif os.path.exists(directory):
		directory = os.path.abspath(directory)
	else:
		log("Directory doesn't exist", level=2)
		sys.exit(1)

	if is_pine_directory(directory):
		if os.path.curdir == directory:
			print("You are in a pine directory!")
		else:
			print("{0} is a pine directory!".format(directory))
		return

	pinees = []
	for sub in os.listdir(directory):
		sub = os.path.join(directory, sub)
		if os.path.isdir(sub) and not os.path.islink(sub):
			if is_pine_directory(sub):
				print("{} found!".format(sub))
				pinees.append(sub)
			else:
				pinees.extend(find_pinees(sub))

	return pinees


def migrate_env(python, backup=False):
	from pine.config.common_site_config import get_config
	from pine.app import get_apps

	nvenv = 'env'
	path = os.getcwd()
	python = which(python)
	virtualenv = which('virtualenv')
	pvenv = os.path.join(path, nvenv)
	pip = os.path.join(pvenv, 'bin', 'pip')

	# Clear Cache before Pine Dies.
	try:
		config = get_config(pine_path=os.getcwd())
		rredis = urlparse(config['redis_cache'])

		redis  = '{redis} -p {port}'.format(redis=which('redis-cli'), port=rredis.port)

		logger.log('Clearing Redis Cache...')
		exec_cmd('{redis} FLUSHALL'.format(redis = redis))
		logger.log('Clearing Redis DataBase...')
		exec_cmd('{redis} FLUSHDB'.format(redis = redis))
	except:
		logger.warning('Please ensure Redis Connections are running or Daemonized.')

	# Backup venv: restore using `virtualenv --relocatable` if needed
	if backup:
		parch = os.path.join(path, 'archived_envs')
		if not os.path.exists(parch):
			os.mkdir(parch)

		source = os.path.join(path, 'env')
		target = parch

		logger.log('Backing up Virtual Environment')
		stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		dest = os.path.join(path, str(stamp))

		os.rename(source, dest)
		shutil.move(dest, target)

	# Create virtualenv using specified python
	venv_creation, packages_setup = 1, 1
	try:
		logger.log('Setting up a New Virtual {} Environment'.format(python))
		venv_creation = exec_cmd('{virtualenv} --python {python} {pvenv}'.format(virtualenv=virtualenv, python=python, pvenv=pvenv))

		apps = ' '.join(["-e {}".format(os.path.join("apps", app)) for app in get_apps()])
		packages_setup = exec_cmd('{0} install -q -U {1}'.format(pip, apps))

		logger.log('Migration Successful to {}'.format(python))
	except:
		if venv_creation or packages_setup:
			logger.warning('Migration Error')


def is_dist_editable(dist):
	"""Is distribution an editable install?"""
	for path_item in sys.path:
		egg_link = os.path.join(path_item, dist + '.egg-link')
		if os.path.isfile(egg_link):
			return True
	return False


def find_parent_pine(path):
	"""Checks if parent directories are pinees"""
	if is_pine_directory(directory=path):
		return path

	home_path = os.path.expanduser("~")
	root_path = os.path.abspath(os.sep)

	if path not in {home_path, root_path}:
		# NOTE: the os.path.split assumes that given path is absolute
		parent_dir = os.path.split(path)[0]
		return find_parent_pine(parent_dir)


def generate_command_cache(pine_path='.'):
	"""Caches all available commands (even custom apps) via Melon
	Default caching behaviour: generated the first time any command (for a specific pine directory)
	"""

	python = get_env_cmd('python', pine_path=pine_path)
	sites_path = os.path.join(pine_path, 'sites')

	if os.path.exists(pine_cache_file):
		os.remove(pine_cache_file)

	try:
		output = get_cmd_output("{0} -m melon.utils.pine_helper get-melon-commands".format(python), cwd=sites_path)
		with open(pine_cache_file, 'w') as f:
			json.dump(eval(output), f)
		return json.loads(output)

	except subprocess.CalledProcessError as e:
		if hasattr(e, "stderr"):
			print(e.stderr.decode('utf-8'))


def clear_command_cache(pine_path='.'):
	"""Clears commands cached
	Default invalidation behaviour: destroyed on each run of `pine update`
	"""

	if os.path.exists(pine_cache_file):
		os.remove(pine_cache_file)
	else:
		print("Pine command cache doesn't exist in this folder!")
