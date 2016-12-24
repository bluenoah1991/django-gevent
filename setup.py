from setuptools import setup, find_packages

setup(
	name = 'django_gevent',
	version = '0.1',
	author = 'CodeMeow5',
	author_email = 'codemeow@yahoo.com',
	description = 'Combine TCP server with Django based on gevent',
	license = 'MIT',
	keywords = 'django,gevent,tcp',
	url = 'https://github.com/codemeow5/django-gevent',
	packages = find_packages(),
	package_data = {
		'': ['*.sh'],
	},
	install_requires = ['django', 'gevent']
)
