#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from userconf import ConfigAppDirs

class Configure(ConfigAppDirs):
	'''
	Classe para configurações básicas do sistema operacional, diretórios
	pastas e arquivos necessários para este programa.
	'''
	def __init__(self, appname):
		super().__init__(appname)
		from platform import system as kernel_type
		self.__kernel_type = kernel_type()
		self.create_common_dirs() # Criar diretórios deste app.
		del kernel_type
		
