# imports - standard imports
import os

# imports - third party imports
import click
from crontab import CronTab
from six.moves.urllib.request import urlretrieve

# imports - module imports
import pine
from pine.config.common_site_config import get_config
from pine.config.nginx import make_nginx_conf
from pine.config.production_setup import service
from pine.config.site_config import get_sectors, remove_sector, update_site_config
from pine.utils import CommandFailedError, exec_cmd, update_common_site_config


def setup_letsencrypt(site, custom_sector, pine_path, interactive):

	site_path = os.path.join(pine_path, "sites", site, "site_config.json")
	if not os.path.exists(os.path.dirname(site_path)):
		print("No site named "+site)
		return

	if custom_sector:
		sectors = get_sectors(site, pine_path)
		for d in sectors:
			if (isinstance(d, dict) and d['sector']==custom_sector):
				print("SSL for Sector {0} already exists".format(custom_sector))
				return

		if not custom_sector in sectors:
			print("No custom domain named {0} set for site".format(custom_sector))
			return

	if interactive:
		click.confirm('Running this will stop the nginx service temporarily causing your sites to go offline\n'
			'Do you want to continue?',
			abort=True)

	if not get_config(pine_path).get("dns_multitenant"):
		print("You cannot setup SSL without DNS Multitenancy")
		return

	create_config(site, custom_sector)
	run_certbot_and_setup_ssl(site, custom_sector, pine_path, interactive)
	setup_crontab()


def create_config(site, custom_sector):
	config = pine.config.env.get_template('letsencrypt.cfg').render(sector=custom_sector or site)
	config_path = '/etc/letsencrypt/configs/{site}.cfg'.format(site=custom_sector or site)
	create_dir_if_missing(config_path)

	with open(config_path, 'w') as f:
		f.write(config)


def run_certbot_and_setup_ssl(site, custom_sector, pine_path, interactive=True):
	service('nginx', 'stop')
	get_certbot()

	try:
		interactive = '' if interactive else '-n'
		exec_cmd("{path} {interactive} --config /etc/letsencrypt/configs/{site}.cfg certonly".format(path=get_certbot_path(), interactive=interactive, site=custom_sector or site))
	except CommandFailedError:
		service('nginx', 'start')
		print("There was a problem trying to setup SSL for your site")
		return

	ssl_path = "/etc/letsencrypt/live/{site}/".format(site=custom_sector or site)
	ssl_config = { "ssl_certificate": os.path.join(ssl_path, "fullchain.pem"),
					"ssl_certificate_key": os.path.join(ssl_path, "privkey.pem") }

	if custom_sector:
		remove_sector(site, custom_sector, pine_path)
		sectors = get_sectors(site, pine_path)
		ssl_config['sector'] = custom_sector
		sectors.append(ssl_config)
		update_site_config(site, { "sectors": sectors }, pine_path=pine_path)
	else:
		update_site_config(site, ssl_config, pine_path=pine_path)

	make_nginx_conf(pine_path)
	service('nginx', 'start')


def setup_crontab():
	job_command = '/opt/certbot-auto renew -a nginx --post-hook "systemctl reload nginx"'
	job_comment = 'Renew lets-encrypt every month'
	print("Setting Up cron job to {0}".format(job_comment))

	system_crontab = CronTab(user='root')

	for job in system_crontab.find_comment(comment=job_comment): # Removes older entries
		system_crontab.remove(job)

	job = system_crontab.new(command=job_command, comment=job_comment)
	job.setall('0 0 */1 * *') # Run at 00:00 every day-of-month
	system_crontab.write()


def create_dir_if_missing(path):
	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))


def get_certbot():
	certbot_path = get_certbot_path()
	create_dir_if_missing(certbot_path)

	if not os.path.isfile(certbot_path):
		urlretrieve ("https://dl.eff.org/certbot-auto", certbot_path)
		os.chmod(certbot_path, 0o744)


def get_certbot_path():
	return "/opt/certbot-auto"


def renew_certs():
	# Needs to be run with sudo
	click.confirm('Running this will stop the nginx service temporarily causing your sites to go offline\n'
		'Do you want to continue?',
		abort=True)

	setup_crontab()

	service('nginx', 'stop')
	exec_cmd("{path} renew".format(path=get_certbot_path()))
	service('nginx', 'start')


def setup_wildcard_ssl(sector, email, pine_path, exclude_base_sector):

	def _get_sectors(sector):
		sector_list = [sector]

		if not sector.startswith('*.'):
			# add wildcard caracter to sector if missing
			sector_list.append('*.{0}'.format(sector))
		else:
			# include base sector based on flag
			sector_list.append(sector.replace('*.', ''))

		if exclude_base_sector:
			sector_list.remove(sector.replace('*.', ''))

		return sector_list

	if not get_config(pine_path).get("dns_multitenant"):
		print("You cannot setup SSL without DNS Multitenancy")
		return

	get_certbot()
	sector_list = _get_sectors(sector.strip())

	email_param = ''
	if email:
		email_param = '--email {0}'.format(email)

	try:
		exec_cmd("{path} certonly --manual --preferred-challenges=dns {email_param} \
			--server https://acme-v02.api.letsencrypt.org/directory \
			--agree-tos -d {sector}".format(path=get_certbot_path(), sector=' -d '.join(sector_list),
			email_param=email_param))

	except CommandFailedError:
		print("There was a problem trying to setup SSL")
		return

	ssl_path = "/etc/letsencrypt/live/{sector}/".format(sector=sector)
	ssl_config = {
		"wildcard": {
			"sector": sector,
			"ssl_certificate": os.path.join(ssl_path, "fullchain.pem"),
			"ssl_certificate_key": os.path.join(ssl_path, "privkey.pem")
		}
	}

	update_common_site_config(ssl_config)
	setup_crontab()

	make_nginx_conf(pine_path)
	print("Restrting Nginx service")
	service('nginx', 'restart')
