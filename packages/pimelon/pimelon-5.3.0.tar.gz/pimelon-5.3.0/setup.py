from setuptools import find_packages, setup
from pine import PROJECT_NAME, VERSION

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

setup(
	name=PROJECT_NAME,
	description='Web based Integrated Enterprise Information System (IEIS)',
	author='Alphamonak Solutions',
	author_email='amonak@monakerp.com',
	version=VERSION,
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
	entry_points='''
[console_scripts]
pine=pine.cli:cli
''',
)
