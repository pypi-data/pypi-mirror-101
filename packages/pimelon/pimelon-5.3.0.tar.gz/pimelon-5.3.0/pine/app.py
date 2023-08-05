# imports - compatibility imports
from __future__ import print_function

# imports - standard imports
import json
import logging
import os
import re
import shutil
import subprocess
import sys

# imports - third party imports
import click
import git
import requests
import semantic_version
from six.moves import reload_module

# imports - module imports
import pine
from pine.config.common_site_config import get_config
from pine.utils import color, CommandFailedError, build_assets, check_git_for_shallow_clone, exec_cmd, get_cmd_output, get_melon, restart_supervisor_processes, restart_systemd_processes, run_melon_cmd


logger = logging.getLogger(pine.PROJECT_NAME)


class InvalidBranchException(Exception): pass
class InvalidRemoteException(Exception): pass

class MajorVersionUpgradeException(Exception):
	def __init__(self, message, upstream_version, local_version):
		super(MajorVersionUpgradeException, self).__init__(message)
		self.upstream_version = upstream_version
		self.local_version = local_version

def get_apps(pine_path='.'):
	try:
		with open(os.path.join(pine_path, 'sites', 'apps.txt')) as f:
			return f.read().strip().split('\n')
	except IOError:
		return []

def add_to_appstxt(app, pine_path='.'):
	apps = get_apps(pine_path=pine_path)
	if app not in apps:
		apps.append(app)
		return write_appstxt(apps, pine_path=pine_path)

def remove_from_appstxt(app, pine_path='.'):
	apps = get_apps(pine_path=pine_path)
	if app in apps:
		apps.remove(app)
		return write_appstxt(apps, pine_path=pine_path)

def write_appstxt(apps, pine_path='.'):
	with open(os.path.join(pine_path, 'sites', 'apps.txt'), 'w') as f:
		return f.write('\n'.join(apps))

def is_git_url(url):
	pattern = r"(?:git|ssh|https?|git@[-\w.]+):(\/\/)?(.*?)(\.git)?(\/?|\#[-\d\w._]+?)$"
	return bool(re.match(pattern, url))

def get_excluded_apps(pine_path='.'):
	try:
		with open(os.path.join(pine_path, 'sites', 'excluded_apps.txt')) as f:
			return f.read().strip().split('\n')
	except IOError:
		return []

def add_to_excluded_apps_txt(app, pine_path='.'):
	if app == 'melon':
		raise ValueError('Melon app cannot be excludeed from update')
	if app not in os.listdir('apps'):
		raise ValueError('The app {} does not exist'.format(app))
	apps = get_excluded_apps(pine_path=pine_path)
	if app not in apps:
		apps.append(app)
		return write_excluded_apps_txt(apps, pine_path=pine_path)

def write_excluded_apps_txt(apps, pine_path='.'):
	with open(os.path.join(pine_path, 'sites', 'excluded_apps.txt'), 'w') as f:
		return f.write('\n'.join(apps))

def remove_from_excluded_apps_txt(app, pine_path='.'):
	apps = get_excluded_apps(pine_path=pine_path)
	if app in apps:
		apps.remove(app)
		return write_excluded_apps_txt(apps, pine_path=pine_path)

def get_app(git_url, branch=None, pine_path='.', skip_assets=False, verbose=False, restart_pine=True, overwrite=False):
	if not os.path.exists(git_url):
		if not is_git_url(git_url):
			orgs = ['melon', 'monak']
			for org in orgs:
				url = 'https://api.github.com/repos/{org}/{app}'.format(org=org, app=git_url)
				res = requests.get(url)
				if res.ok:
					data = res.json()
					if 'name' in data:
						if git_url == data['name']:
							git_url = 'https://github.com/{org}/{app}'.format(org=org, app=git_url)
							break
				else:
					pine.utils.log("App {app} not found".format(app=git_url), level=2)
					sys.exit(1)

		# Gets repo name from URL
		repo_name = git_url.rstrip('/').rsplit('/', 1)[1].rsplit('.', 1)[0]
		shallow_clone = '--depth 1' if check_git_for_shallow_clone() else ''
		branch = '--branch {branch}'.format(branch=branch) if branch else ''
	else:
		repo_name = git_url.split(os.sep)[-1]
		shallow_clone = ''
		branch = '--branch {branch}'.format(branch=branch) if branch else ''

	if os.path.isdir(os.path.join(pine_path, 'apps', repo_name)):
		# application directory already exists
		# prompt user to overwrite it
		if overwrite or click.confirm('''A directory for the application "{0}" already exists.
Do you want to continue and overwrite it?'''.format(repo_name)):
			shutil.rmtree(os.path.join(pine_path, 'apps', repo_name))
		elif click.confirm('''Do you want to reinstall the existing application?''', abort=True):
			app_name = get_app_name(pine_path, repo_name)
			install_app(app=app_name, pine_path=pine_path, verbose=verbose, skip_assets=skip_assets)
			sys.exit()

	print('\n{0}Getting {1}{2}'.format(color.yellow, repo_name, color.nc))
	logger.log('Getting app {0}'.format(repo_name))
	exec_cmd("git clone {git_url} {branch} {shallow_clone} --origin upstream".format(
		git_url=git_url,
		shallow_clone=shallow_clone,
		branch=branch),
		cwd=os.path.join(pine_path, 'apps'))

	app_name = get_app_name(pine_path, repo_name)
	install_app(app=app_name, pine_path=pine_path, verbose=verbose, skip_assets=skip_assets)


def get_app_name(pine_path, repo_name):
	# retrieves app name from setup.py
	app_path = os.path.join(pine_path, 'apps', repo_name, 'setup.py')
	with open(app_path, 'rb') as f:
		app_name = re.search(r'name\s*=\s*[\'"](.*)[\'"]', f.read().decode('utf-8')).group(1)
		if repo_name != app_name:
			apps_path = os.path.join(os.path.abspath(pine_path), 'apps')
			os.rename(os.path.join(apps_path, repo_name), os.path.join(apps_path, app_name))
		return app_name


def new_app(app, pine_path='.'):
	# For backwards compatibility
	app = app.lower().replace(" ", "_").replace("-", "_")
	logger.log('creating new app {}'.format(app))
	apps = os.path.abspath(os.path.join(pine_path, 'apps'))
	pine.set_melon_version(pine_path=pine_path)

	if pine.MELON_VERSION == 0:
		exec_cmd("{melon} --make_app {apps} {app}".format(melon=get_melon(pine_path=pine_path),
			apps=apps, app=app))
	else:
		run_melon_cmd('make-app', apps, app, pine_path=pine_path)
	install_app(app, pine_path=pine_path)


def install_app(app, pine_path=".", verbose=False, no_cache=False, restart_pine=True, skip_assets=False):
	print('\n{0}Installing {1}{2}'.format(color.yellow, app, color.nc))
	logger.log("installing {}".format(app))

	pip_path = os.path.join(pine_path, "env", "bin", "pip")
	quiet_flag = "-q" if not verbose else ""
	app_path = os.path.join(pine_path, "apps", app)
	cache_flag = "--no-cache-dir" if no_cache else ""

	exec_cmd("{pip} install {quiet} -U -e {app} {no_cache}".format(pip=pip_path, quiet=quiet_flag, app=app_path, no_cache=cache_flag))

	if os.path.exists(os.path.join(app_path, 'package.json')):
		exec_cmd("yarn install", cwd=app_path)

	add_to_appstxt(app, pine_path=pine_path)

	if not skip_assets:
		build_assets(pine_path=pine_path, app=app)

	if restart_pine:
		conf = get_config(pine_path=pine_path)

		if conf.get('restart_supervisor_on_update'):
			restart_supervisor_processes(pine_path=pine_path)
		if conf.get('restart_systemd_on_update'):
			restart_systemd_processes(pine_path=pine_path)


def remove_app(app, pine_path='.'):
	if app not in get_apps(pine_path):
		print("No app named {0}".format(app))
		sys.exit(1)

	app_path = os.path.join(pine_path, 'apps', app)
	site_path = os.path.join(pine_path, 'sites')
	pip = os.path.join(pine_path, 'env', 'bin', 'pip')

	for site in os.listdir(site_path):
		req_file = os.path.join(site_path, site, 'site_config.json')
		if os.path.exists(req_file):
			out = subprocess.check_output(["pine", "--site", site, "list-apps"], cwd=pine_path).decode('utf-8')
			if re.search(r'\b' + app + r'\b', out):
				print("Cannot remove, app is installed on site: {0}".format(site))
				sys.exit(1)

	exec_cmd("{0} uninstall -y {1}".format(pip, app), cwd=pine_path)
	remove_from_appstxt(app, pine_path)
	shutil.rmtree(app_path)
	run_melon_cmd("build", pine_path=pine_path)
	if get_config(pine_path).get('restart_supervisor_on_update'):
		restart_supervisor_processes(pine_path=pine_path)
	if get_config(pine_path).get('restart_systemd_on_update'):
		restart_systemd_processes(pine_path=pine_path)

def pull_apps(apps=None, pine_path='.', reset=False):
	'''Check all apps if there no local changes, pull'''
	rebase = '--rebase' if get_config(pine_path).get('rebase_on_pull') else ''

	apps = apps or get_apps(pine_path=pine_path)
	# chech for local changes
	if not reset:
		for app in apps:
			excluded_apps = get_excluded_apps()
			if app in excluded_apps:
				print("Skipping reset for app {}".format(app))
				continue
			app_dir = get_repo_dir(app, pine_path=pine_path)
			if os.path.exists(os.path.join(app_dir, '.git')):
				out = subprocess.check_output(["git", "status"], cwd=app_dir)
				out = out.decode('utf-8')
				if not re.search(r'nothing to commit, working (directory|tree) clean', out):
					print('''

Cannot proceed with update: You have local changes in app "{0}" that are not committed.

Here are your choices:

1. Merge the {0} app manually with "git pull" / "git pull --rebase" and fix conflicts.
1. Temporarily remove your changes with "git stash" or discard them completely
	with "pine update --reset" or for individual repositries "git reset --hard"
	'''.format(app))
					sys.exit(1)

	excluded_apps = get_excluded_apps()
	for app in apps:
		if app in excluded_apps:
			print("Skipping pull for app {}".format(app))
			continue
		app_dir = get_repo_dir(app, pine_path=pine_path)
		if os.path.exists(os.path.join(app_dir, '.git')):
			remote = get_remote(app)
			if not remote:
				# remote is False, i.e. remote doesn't exist, add the app to excluded_apps.txt
				add_to_excluded_apps_txt(app, pine_path=pine_path)
				print("Skipping pull for app {}, since remote doesn't exist, and adding it to excluded apps".format(app))
				continue
			logger.log('pulling {0}'.format(app))
			if reset:
				exec_cmd("git fetch --all", cwd=app_dir)
				exec_cmd("git reset --hard {remote}/{branch}".format(
					remote=remote, branch=get_current_branch(app,pine_path=pine_path)), cwd=app_dir)
			else:
				exec_cmd("git pull {rebase} {remote} {branch}".format(rebase=rebase,
					remote=remote, branch=get_current_branch(app, pine_path=pine_path)), cwd=app_dir)
			exec_cmd('find . -name "*.pyc" -delete', cwd=app_dir)


def is_version_upgrade(app='melon', pine_path='.', branch=None):
	try:
		fetch_upstream(app, pine_path=pine_path)
	except CommandFailedError:
		raise InvalidRemoteException("No remote named upstream for {0}".format(app))

	upstream_version = get_upstream_version(app=app, branch=branch, pine_path=pine_path)

	if not upstream_version:
		raise InvalidBranchException("Specified branch of app {0} is not in upstream".format(app))

	local_version = get_major_version(get_current_version(app, pine_path=pine_path))
	upstream_version = get_major_version(upstream_version)

	if upstream_version - local_version > 0:
		return (True, local_version, upstream_version)

	return (False, local_version, upstream_version)

def get_current_melon_version(pine_path='.'):
	try:
		return get_major_version(get_current_version('melon', pine_path=pine_path))
	except IOError:
		return 0

def get_current_branch(app, pine_path='.'):
	repo_dir = get_repo_dir(app, pine_path=pine_path)
	return get_cmd_output("basename $(git symbolic-ref -q HEAD)", cwd=repo_dir)

def get_remote(app, pine_path='.'):
	repo_dir = get_repo_dir(app, pine_path=pine_path)
	contents = subprocess.check_output(['git', 'remote', '-v'], cwd=repo_dir, stderr=subprocess.STDOUT)
	contents = contents.decode('utf-8')
	if re.findall('upstream[\s]+', contents):
		return 'upstream'
	elif not contents:
		# if contents is an empty string => remote doesn't exist
		return False
	else:
		# get the first remote
		return contents.splitlines()[0].split()[0]

def use_rq(pine_path):
	pine_path = os.path.abspath(pine_path)
	celery_app = os.path.join(pine_path, 'apps', 'melon', 'melon', 'celery_app.py')
	return not os.path.exists(celery_app)

def fetch_upstream(app, pine_path='.'):
	repo_dir = get_repo_dir(app, pine_path=pine_path)
	return subprocess.call(["git", "fetch", "upstream"], cwd=repo_dir)

def get_current_version(app, pine_path='.'):
	repo_dir = get_repo_dir(app, pine_path=pine_path)
	try:
		with open(os.path.join(repo_dir, os.path.basename(repo_dir), '__init__.py')) as f:
			return get_version_from_string(f.read())

	except AttributeError:
		# backward compatibility
		with open(os.path.join(repo_dir, 'setup.py')) as f:
			return get_version_from_string(f.read(), field='version')

def get_develop_version(app, pine_path='.'):
	repo_dir = get_repo_dir(app, pine_path=pine_path)
	with open(os.path.join(repo_dir, os.path.basename(repo_dir), 'hooks.py')) as f:
		return get_version_from_string(f.read(), field='develop_version')

def get_upstream_version(app, branch=None, pine_path='.'):
	repo_dir = get_repo_dir(app, pine_path=pine_path)
	if not branch:
		branch = get_current_branch(app, pine_path=pine_path)
	try:
		contents = subprocess.check_output(['git', 'show', 'upstream/{branch}:{app}/__init__.py'.format(branch=branch, app=app)], cwd=repo_dir, stderr=subprocess.STDOUT)
		contents = contents.decode('utf-8')
	except subprocess.CalledProcessError as e:
		if b"Invalid object" in e.output:
			return None
		else:
			raise
	return get_version_from_string(contents)

def get_repo_dir(app, pine_path='.'):
	return os.path.join(pine_path, 'apps', app)

def switch_branch(branch, apps=None, pine_path='.', upgrade=False, check_upgrade=True):
	from pine.utils import update_requirements, update_node_packages, backup_all_sites, patch_sites, build_assets, post_upgrade
	apps_dir = os.path.join(pine_path, 'apps')
	version_upgrade = (False,)
	switched_apps = []

	if not apps:
		apps = [name for name in os.listdir(apps_dir)
			if os.path.isdir(os.path.join(apps_dir, name))]
		if branch=="v0.x.x":
			apps.append('shopping_cart')

	for app in apps:
		app_dir = os.path.join(apps_dir, app)

		if not os.path.exists(app_dir):
			pine.utils.log("{} does not exist!".format(app), level=2)
			continue

		repo = git.Repo(app_dir)
		unshallow_flag = os.path.exists(os.path.join(app_dir, ".git", "shallow"))
		pine.utils.log("Fetching upstream {0}for {1}".format("unshallow " if unshallow_flag else "", app))

		pine.utils.exec_cmd("git remote set-branches upstream  '*'", cwd=app_dir)
		pine.utils.exec_cmd("git fetch --all{0} --quiet".format(" --unshallow" if unshallow_flag else ""), cwd=app_dir)

		if check_upgrade:
			version_upgrade = is_version_upgrade(app=app, pine_path=pine_path, branch=branch)
			if version_upgrade[0] and not upgrade:
				pine.utils.log("Switching to {0} will cause upgrade from {1} to {2}. Pass --upgrade to confirm".format(branch, version_upgrade[1], version_upgrade[2]), level=2)
				sys.exit(1)

		print("Switching for "+app)
		pine.utils.exec_cmd("git checkout -f {0}".format(branch), cwd=app_dir)

		if str(repo.active_branch) == branch:
			switched_apps.append(app)
		else:
			pine.utils.log("Switching branches failed for: {}".format(app), level=2)

	if switched_apps:
		pine.utils.log("Successfully switched branches for: " + ", ".join(switched_apps), level=1)
		print('Please run `pine update --patch` to be safe from any differences in database schema')

	if version_upgrade[0] and upgrade:
		update_requirements()
		update_node_packages()
		reload_module(pine.utils)
		backup_all_sites()
		patch_sites()
		build_assets()
		post_upgrade(version_upgrade[1], version_upgrade[2])


def switch_to_branch(branch=None, apps=None, pine_path='.', upgrade=False):
	switch_branch(branch, apps=apps, pine_path=pine_path, upgrade=upgrade)

def switch_to_master(apps=None, pine_path='.', upgrade=True):
	switch_branch('master', apps=apps, pine_path=pine_path, upgrade=upgrade)

def switch_to_develop(apps=None, pine_path='.', upgrade=True):
	switch_branch('develop', apps=apps, pine_path=pine_path, upgrade=upgrade)

def get_version_from_string(contents, field='__version__'):
	match = re.search(r"^(\s*%s\s*=\s*['\\\"])(.+?)(['\"])(?sm)" % field, contents)
	return match.group(2)

def get_major_version(version):
	return semantic_version.Version(version).major

def install_apps_from_path(path, pine_path='.'):
	apps = get_apps_json(path)
	for app in apps:
		get_app(app['url'], branch=app.get('branch'), pine_path=pine_path, skip_assets=True)

def get_apps_json(path):
	if path.startswith('http'):
		r = requests.get(path)
		return r.json()

	with open(path) as f:
		return json.load(f)

def validate_branch():
	installed_apps = set(get_apps())
	check_apps = set(['melon', 'monak'])
	intersection_apps = installed_apps.intersection(check_apps)

	for app in intersection_apps:
		branch = get_current_branch(app)

		if branch == "master":
			print("""'master' branch is renamed to 'version-4' since 'version-5' release.
As of January 2020, the following branches are
version		Melon			Monak
4		version-4		version-4
5		version-5		version-5
6		develop			develop

Please switch to new branches to get future updates.
To switch to your required branch, run the following commands: pine switch-to-branch [branch-name]""")

			sys.exit(1)
