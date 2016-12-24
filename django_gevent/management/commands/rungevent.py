import gevent
import signal
from django.core.servers.basehttp import get_internal_wsgi_application
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from exceptions import NotImplementedError
from gevent import wsgi
from gevent import server

class Command(BaseCommand):
	help = 'Running Django server based on gevent'

	def add_arguments(self, parser):
		parser.add_argument(
			'-i', '--ip',
			action='store',
			nargs=1,
			default=['0.0.0.0'],
			help='Optional ip address(default: 0.0.0.0)',
			metavar='ipaddr'
		)
		parser.add_argument(
			'-p', '--port',
			action='store',
			nargs=1,
			default=[8080],
			type=int,
			help='Optional port number(default: 8080)',
			metavar='port'
		)
		parser.add_argument(
			'-t', '--tcp_port',
			action='store',
			nargs=1,
			default=[8081],
			type=int,
			help='Optional tcp port number(default: 8081)',
			metavar='tcp_port'
		)
		parser.add_argument(
			'--pool_size',
			action='store',
			nargs=1,
			type=int,
			help='Optional greenlets pool size(default: default)',
			metavar='pool_size'
		)

	def TcpHandler(self, socket, address):
		raise NotImplementedError

	def handle(self, *args, **options):
		addr = options['ip'][0]
		port = options['port'][0]
		tcp_port = options['tcp_port'][0]
		pool = options['pool_size']
		if pool is None:
			pool = 'default'
		else:
			pool = pool[0]

		tcphandle = getattr(settings, 'TCPHANDLER', self.TcpHandler)

		wsgi_application = get_internal_wsgi_application()
		wsgi_server = wsgi.WSGIServer((addr, port), wsgi_application, spawn=pool)

		tcp_server = server.StreamServer((addr, tcp_port), tcphandle, spawn=pool)

		gevent.signal(signal.SIGTERM, wsgi_server.close)
		gevent.signal(signal.SIGINT, wsgi_server.close)
		gevent.signal(signal.SIGTERM, tcp_server.close)
		gevent.signal(signal.SIGINT, tcp_server.close)

		wsgi_server.start()
		tcp_server.start()

		self.stdout.write('Greenlets Pool Size: %s' % pool)
		self.stdout.write('Starting Django server based on gevent at http://%s:%s/' % (addr, port))
		self.stdout.write('Starting Django tcp server based on gevent at tcp://%s:%s/' % (addr, tcp_port))
		self.stdout.write('Quit the server with CONTROL-C.')

		gevent.wait()
