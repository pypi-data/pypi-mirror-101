#!/usr/bin/env python3

from setuptools import setup


DESCRIPTION = 'Obter cotação de criptomoedas'
LONG_DESCRIPTION = 'Obtem cotação, cadastra alertas, converte unidade criptomoedas para Real(R$) do Brasil'

setup(
	name='coin_qt_gui',
	version='0.1.0',
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	author='Bruno Chaves',
	author_email='brunodasill@gmail.com',
	license='MIT',
	packages=['coin_qt_gui'],
	install_requires=['PyQt5'],
	zip_safe=False,
	url='https://github.com/Brunopvh/coin-qt-gui',
	project_urls = {
		'Código fonte': 'https://github.com/Brunopvh/coin-qt-gui',
		'Download': 'https://github.com/Brunopvh/coin-qt-gui/archive/refs/tags/0.1.0.zip'
	},
)


