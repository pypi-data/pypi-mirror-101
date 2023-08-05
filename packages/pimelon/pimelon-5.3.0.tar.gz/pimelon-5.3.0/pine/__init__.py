VERSION = "5.3.0"
PROJECT_NAME = "pimelon"
MELON_VERSION = None


def set_melon_version(pine_path='.'):
	from .app import get_current_melon_version
	global MELON_VERSION
	if not MELON_VERSION:
		MELON_VERSION = get_current_melon_version(pine_path=pine_path)