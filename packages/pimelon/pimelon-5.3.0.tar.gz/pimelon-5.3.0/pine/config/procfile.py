# imports - standard imports
import os

# imports - third party imports
import click

# imports - module imports
import pine
from pine.app import use_rq
from pine.config.common_site_config import get_config
from pine.utils import find_executable


def setup_procfile(pine_path, yes=False, skip_redis=False):
	config = get_config(pine_path=pine_path)
	procfile_path = os.path.join(pine_path, 'Procfile')
	if not yes and os.path.exists(procfile_path):
		click.confirm('A Procfile already exists and this will overwrite it. Do you want to continue?',
			abort=True)

	procfile = pine.config.env.get_template('Procfile').render(
		node=find_executable("node") or find_executable("nodejs"),
		use_rq=use_rq(pine_path),
		webserver_port=config.get('webserver_port'),
		CI=os.environ.get('CI'),
		skip_redis=skip_redis)

	with open(procfile_path, 'w') as f:
		f.write(procfile)
