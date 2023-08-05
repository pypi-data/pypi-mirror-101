import click


def print_pine_version(ctx, param, value):
	"""Prints current pine version"""
	if not value or ctx.resilient_parsing:
		return

	import pine
	click.echo(pine.VERSION)
	ctx.exit()

@click.group()
@click.option('--version', is_flag=True, is_eager=True, callback=print_pine_version, expose_value=False)
def pine_command(pine_path='.'):
	import pine
	pine.set_melon_version(pine_path=pine_path)


from pine.commands.make import init, get_app, new_app, remove_app, exclude_app_for_update, include_app_for_update, pip
pine_command.add_command(init)
pine_command.add_command(get_app)
pine_command.add_command(new_app)
pine_command.add_command(remove_app)
pine_command.add_command(exclude_app_for_update)
pine_command.add_command(include_app_for_update)
pine_command.add_command(pip)


from pine.commands.update import update, retry_upgrade, switch_to_branch, switch_to_master, switch_to_develop
pine_command.add_command(update)
pine_command.add_command(retry_upgrade)
pine_command.add_command(switch_to_branch)
pine_command.add_command(switch_to_master)
pine_command.add_command(switch_to_develop)


from pine.commands.utils import (start, restart, set_nginx_port, set_ssl_certificate, set_ssl_certificate_key, set_url_root,
	set_mariadb_host, set_default_site, download_translations, backup_site, backup_all_sites, release, renew_lets_encrypt,
	disable_production, pine_src, prepare_beta_release, set_redis_cache_host, set_redis_queue_host, set_redis_socketio_host, find_pinees, migrate_env,
	generate_command_cache, clear_command_cache)
pine_command.add_command(start)
pine_command.add_command(restart)
pine_command.add_command(set_nginx_port)
pine_command.add_command(set_ssl_certificate)
pine_command.add_command(set_ssl_certificate_key)
pine_command.add_command(set_url_root)
pine_command.add_command(set_mariadb_host)
pine_command.add_command(set_redis_cache_host)
pine_command.add_command(set_redis_queue_host)
pine_command.add_command(set_redis_socketio_host)
pine_command.add_command(set_default_site)
pine_command.add_command(download_translations)
pine_command.add_command(backup_site)
pine_command.add_command(backup_all_sites)
pine_command.add_command(release)
pine_command.add_command(renew_lets_encrypt)
pine_command.add_command(disable_production)
pine_command.add_command(pine_src)
pine_command.add_command(prepare_beta_release)
pine_command.add_command(find_pinees)
pine_command.add_command(migrate_env)
pine_command.add_command(generate_command_cache)
pine_command.add_command(clear_command_cache)

from pine.commands.setup import setup
pine_command.add_command(setup)


from pine.commands.config import config
pine_command.add_command(config)

from pine.commands.git import remote_set_url, remote_reset_url, remote_urls
pine_command.add_command(remote_set_url)
pine_command.add_command(remote_reset_url)
pine_command.add_command(remote_urls)

from pine.commands.install import install
pine_command.add_command(install)
