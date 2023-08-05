# imports - standard imports
import json
import os
from collections import defaultdict

# imports - module imports
from pine.config.nginx import make_nginx_conf
from pine.utils import get_sites


def get_site_config(site, pine_path='.'):
	config_path = os.path.join(pine_path, 'sites', site, 'site_config.json')
	if not os.path.exists(config_path):
		return {}
	with open(config_path) as f:
		return json.load(f)

def put_site_config(site, config, pine_path='.'):
	config_path = os.path.join(pine_path, 'sites', site, 'site_config.json')
	with open(config_path, 'w') as f:
		return json.dump(config, f, indent=1)

def update_site_config(site, new_config, pine_path='.'):
	config = get_site_config(site, pine_path=pine_path)
	config.update(new_config)
	put_site_config(site, config, pine_path=pine_path)

def set_nginx_port(site, port, pine_path='.', gen_config=True):
	set_site_config_nginx_property(site, {"nginx_port": port}, pine_path=pine_path, gen_config=gen_config)

def set_ssl_certificate(site, ssl_certificate, pine_path='.', gen_config=True):
	set_site_config_nginx_property(site, {"ssl_certificate": ssl_certificate}, pine_path=pine_path, gen_config=gen_config)

def set_ssl_certificate_key(site, ssl_certificate_key, pine_path='.', gen_config=True):
	set_site_config_nginx_property(site, {"ssl_certificate_key": ssl_certificate_key}, pine_path=pine_path, gen_config=gen_config)

def set_site_config_nginx_property(site, config, pine_path='.', gen_config=True):
	if site not in get_sites(pine_path=pine_path):
		raise Exception("No such site")
	update_site_config(site, config, pine_path=pine_path)
	if gen_config:
		make_nginx_conf(pine_path=pine_path)

def set_url_root(site, url_root, pine_path='.'):
	update_site_config(site, {"host_name": url_root}, pine_path=pine_path)

def add_sector(site, sector, ssl_certificate, ssl_certificate_key, pine_path='.'):
	sectors = get_sectors(site, pine_path)
	for d in sectors:
		if (isinstance(d, dict) and d['sector']==sector) or d==sector:
			print("Sector {0} already exists".format(sector))
			return

	if ssl_certificate_key and ssl_certificate:
		sector = {
			'sector' : sector,
			'ssl_certificate': ssl_certificate,
			'ssl_certificate_key': ssl_certificate_key
		}

	sectors.append(sector)
	update_site_config(site, { "sectors": sectors }, pine_path=pine_path)

def remove_sector(site, sector, pine_path='.'):
	sectors = get_sectors(site, pine_path)
	for i, d in enumerate(sectors):
		if (isinstance(d, dict) and d['sector']==sector) or d==sector:
			sectors.remove(d)
			break

	update_site_config(site, { 'sectors': sectors }, pine_path=pine_path)

def sync_sectors(site, sectors, pine_path='.'):
	"""Checks if there is a change in sectors. If yes, updates the sectors list."""
	changed = False
	existing_sectors = get_sectors_dict(get_sectors(site, pine_path))
	new_sectors = get_sectors_dict(sectors)

	if set(existing_sectors.keys()) != set(new_sectors.keys()):
		changed = True

	else:
		for d in list(existing_sectors.values()):
			if d != new_sectors.get(d['sector']):
				changed = True
				break

	if changed:
		# replace existing sectors with this one
		update_site_config(site, { 'sectors': sectors }, pine_path='.')

	return changed

def get_sectors(site, pine_path='.'):
	return get_site_config(site, pine_path=pine_path).get('sectors') or []

def get_sectors_dict(sectors):
	sectors_dict = defaultdict(dict)
	for d in sectors:
		if isinstance(d, str):
			sectors_dict[d] = { 'sector': d }

		elif isinstance(d, dict):
			sectors_dict[d['sector']] = d

	return sectors_dict
