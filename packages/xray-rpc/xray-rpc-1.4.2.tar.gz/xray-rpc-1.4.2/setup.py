# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xray_rpc',
 'xray_rpc.app.commander',
 'xray_rpc.app.dispatcher',
 'xray_rpc.app.dns',
 'xray_rpc.app.dns.fakedns',
 'xray_rpc.app.log',
 'xray_rpc.app.log.command',
 'xray_rpc.app.policy',
 'xray_rpc.app.proxyman',
 'xray_rpc.app.proxyman.command',
 'xray_rpc.app.reverse',
 'xray_rpc.app.router',
 'xray_rpc.app.router.command',
 'xray_rpc.app.stats',
 'xray_rpc.app.stats.command',
 'xray_rpc.common.log',
 'xray_rpc.common.net',
 'xray_rpc.common.protocol',
 'xray_rpc.common.serial',
 'xray_rpc.core',
 'xray_rpc.proxy.blackhole',
 'xray_rpc.proxy.dns',
 'xray_rpc.proxy.dokodemo',
 'xray_rpc.proxy.freedom',
 'xray_rpc.proxy.http',
 'xray_rpc.proxy.mtproto',
 'xray_rpc.proxy.shadowsocks',
 'xray_rpc.proxy.socks',
 'xray_rpc.proxy.trojan',
 'xray_rpc.proxy.vless',
 'xray_rpc.proxy.vless.encoding',
 'xray_rpc.proxy.vless.inbound',
 'xray_rpc.proxy.vless.outbound',
 'xray_rpc.proxy.vmess',
 'xray_rpc.proxy.vmess.inbound',
 'xray_rpc.proxy.vmess.outbound',
 'xray_rpc.transport.global',
 'xray_rpc.transport.internet',
 'xray_rpc.transport.internet.domainsocket',
 'xray_rpc.transport.internet.grpc',
 'xray_rpc.transport.internet.grpc.encoding',
 'xray_rpc.transport.internet.headers.http',
 'xray_rpc.transport.internet.headers.noop',
 'xray_rpc.transport.internet.headers.srtp',
 'xray_rpc.transport.internet.headers.tls',
 'xray_rpc.transport.internet.headers.utp',
 'xray_rpc.transport.internet.headers.wechat',
 'xray_rpc.transport.internet.headers.wireguard',
 'xray_rpc.transport.internet.http',
 'xray_rpc.transport.internet.kcp',
 'xray_rpc.transport.internet.quic',
 'xray_rpc.transport.internet.tcp',
 'xray_rpc.transport.internet.tls',
 'xray_rpc.transport.internet.udp',
 'xray_rpc.transport.internet.websocket',
 'xray_rpc.transport.internet.xtls']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.36.1,<2.0.0',
 'grpcio>=1.36.1,<2.0.0',
 'httpx>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'xray-rpc',
    'version': '1.4.2',
    'description': 'gRPC files generated from Xray source code.',
    'long_description': None,
    'author': 'laoshan-taoist',
    'author_email': '65347330+laoshan-taoist@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
