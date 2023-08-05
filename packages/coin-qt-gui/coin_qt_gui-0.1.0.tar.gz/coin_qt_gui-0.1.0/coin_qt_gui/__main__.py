#!/usr/bin/env python3

from PyQt5.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout,
	QPushButton, QAction, qApp,
	QSpacerItem, QLabel, QComboBox,
	QSizePolicy, QMainWindow, QApplication,
	QGridLayout, QMessageBox, QFileDialog,
	QGroupBox, QLineEdit,
)

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QIcon, QPixmap
from datetime import datetime
from threading import Thread
import time
import json
import os, sys

if os.name == 'posix':
	if os.getlogin() == 'root':
		print("Você não pode ser o 'root' para executar este programa.")
		sys.exit(1)

github_repo = 'https://github.com/Brunopvh/coin-qt-gui'
__author__ = 'Bruno Chaves'
__version__ = '2021-04-02'
__appname__ = 'coin-qt-gui'
__script__ = os.path.realpath(__file__)


dir_of_executable = os.path.dirname(__script__)  # diretório do arquivo principal
dir_of_project = os.path.abspath(os.path.join(dir_of_executable, '..'))  # Diretório do projeto
sys.path.insert(0, dir_of_executable)

from configure import Configure
import downloader

cfg = Configure(__appname__)

class MessageWindow(QWidget):
	'''
	https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
	https://stackoverflow.com/questions/40227047/python-pyqt5-how-to-show-an-error-message-with-pyqt5
	'''

	def __init__(self):
		super().__init__()
		self.msgBox = QMessageBox()

	def msgOK(self, text: str):
		self.msgBox.setText(text)
		self.msgBox.exec()

	def msgError(self, text=''):
		self.msgBox.setIcon(QMessageBox.Critical)
		self.msgBox.setText(text)
		# self.msg.setInformativeText('More information')
		self.msgBox.setWindowTitle("Error")
		self.msgBox.exec_()

class GuiWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		#self.setGeometry(200, 100, 700, 550)
		self._min_width = 700
		self._min_height = 410
		self.setFixedSize(self._min_width, self._min_height)
		#self.setMinimumSize(self._min_width, self._min_height)
		self.setWindowTitle('Coin Qt Gui')


		self.contentor_A = QWidget()
		self.contentor_B = QWidget()
		self.setCentralWidget(self.contentor_A)  # +
		self.gridMaster_A = QGridLayout(self)

		self.A = WidgetsA(self.contentor_A)
		#self.B = WidgetsB(self.contentor_B)

		self.setup_Bar()
		self.setup_Widgets()

	def setup_Bar(self):
		# Opção abrir.
		openAct = QAction('&Abrir', self)
		openAct.setStatusTip('Abrir cotação/json')
		openAct.triggered.connect(self.open_act)

		# Opção salvar.
		saveAct = QAction('&Salvar', self)
		saveAct.setStatusTip('Salvar Json')
		saveAct.triggered.connect(self.save_act)

		# Opção sair.
		exitAct = QAction(QIcon('exit.png'), '&Sair', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Sair')
		# exitAct.triggered.connect(qApp.quit)
		exitAct.triggered.connect(self.exitApp)

		# Definir menu arquivo.
		self.statusBar()
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&Arquivo')

		# Adicionar ações do menu arquivo.
		fileMenu.addAction(openAct)
		fileMenu.addAction(saveAct)
		fileMenu.addAction(exitAct)
		"""
		# Definir menu Opções
		optionsMenu = menubar.addMenu('&Opções')

		# opções -> main
		optMain = QAction('&Principal', self)
		optMain.setStatusTip('Selecionar cryptomoeda padrão')
		# saveAct.triggered.connect(self.gui_widgets.act_btn_save)

		optionsMenu.addAction(optMain)
		"""

		aboutMenu = menubar.addMenu('&Sobre')
		versionMenu = aboutMenu.addMenu('Versão')
		versionMenu.addAction(__version__)
		authorMenu = aboutMenu.addMenu('Autor')
		authorMenu.addAction(__author__)
		siteMenu = aboutMenu.addMenu('Site')
		siteMenu.addAction(github_repo)

		#aboutMenu.addAction(__author__)
		#aboutMenu.addMenu('Autor')
		#aboutMenu.addMenu('Versão')

	def setup_Widgets(self):

		self.gridMaster_A.addWidget(self.A, 0, 0)
		self.setLayout(self.gridMaster_A)
		QMetaObject.connectSlotsByName(self)

		# Atualizar botões
		Thread(target=self.A.set_status_ethernet).start()
		Thread(target=self.A.update_value_buttons).start()

		self.show()

	def exitApp(self):
		qApp.quit()

	def open_act(self):
		self.A.open_offline_json()

	def save_act(self):
		self.A.save_act()


class WidgetsA(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.__value_buy = '' # Corrigir
		self.__value_buy_string = ''
		self.list_coin_names = ['Etherium', 'Bitcoin']
		self.url_coins = {
			'Bitcoin': 'https://www.mercadobitcoin.net/api/BTC/ticker/',
			'Etherium': 'https://www.mercadobitcoin.net/api/ETH/ticker/',
		}

		self._min_width = 650
		self._min_height = 130
		self.__alert_json = {}
		self.__alert_json_file = cfg.get_file_config()
		self.__alert_json_file += '.json'

		# Container A
		self.combo_names = QComboBox()
		self.combo_names.setFixedSize(90, 25)
		self.combo_names.addItems(self.list_coin_names)
		self.label_text_real = QLabel('Cotação(R$)', self)
		self.label_real_value = QLabel(self.__value_buy, self)
		self.label_date_text = QLabel('Data/Hora', self)
		self.label_date_text_value = QLabel(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		
		# Botão atualizar
		self.btn_atualizar = QPushButton("Atualizar", self)
		self.btn_atualizar.setFixedSize(90, 25)
		self.btn_atualizar.clicked.connect(self.update_value_buttons)
		label_api = QLabel('API', self)
		label_api.setFixedSize(40, 25)
		self.label_api_url = QLabel(self.url_coins[self.combo_names.currentText()], self)
		self.label_api_url.setFixedSize(380, 15)

		# Grid A
		self.grid_A = QGridLayout()
		self.grid_A.addWidget(self.btn_atualizar, 0, 0, Qt.AlignLeft)
		self.grid_A.addWidget(self.combo_names, 0, 1, Qt.AlignLeft)
		self.grid_A.addWidget(self.label_text_real, 0, 2, Qt.AlignLeft)
		self.grid_A.addWidget(self.label_real_value, 0, 3, Qt.AlignLeft)
		self.grid_A.addWidget(self.label_date_text, 0, 4, Qt.AlignLeft)
		self.grid_A.addWidget(self.label_date_text_value, 0, 5, Qt.AlignLeft)
		self.grid_A.addWidget(label_api, 1, 0, Qt.AlignLeft)
		self.grid_A.addWidget(self.label_api_url, 1, 1, Qt.AlignLeft)

		# GroupBox A
		self.group_A = QGroupBox('Cotação em tempo real')
		self.group_A.setStyleSheet('QGroupBox  {color: red;}')
		self.group_A.setFixedSize(self._min_width, 150)
		self.group_A.setLayout(self.grid_A)

		# Container B
		self.label_text_real_insert_num = QLabel('Valor(R$)', self)
		self.label_text_real_insert_num.setFixedSize(90, 25)
		self.label_text_real_insert_num_value = QLineEdit(self)
		self.label_text_real_insert_num_value.setFixedSize(90, 25)
		self.L_coin_name = QLabel(self.combo_names.currentText(), self)
		self.L_coin_name.setFixedSize(90, 25)
		self.L_coin_name_value = QLabel('0', self)
		self.L_coin_name_value.setFixedSize(90, 25)
		self.btn_converter = QPushButton('Converter', self)
		self.btn_converter.setFixedSize(70, 25)
		self.btn_converter.clicked.connect(self.act_brl_to_coin)

		self.grid_B = QGridLayout()
		self.grid_B.addWidget(self.label_text_real_insert_num, 0, 0)
		self.grid_B.addWidget(self.label_text_real_insert_num_value, 0, 1)
		self.grid_B.addWidget(self.L_coin_name, 1, 0)
		self.grid_B.addWidget(self.L_coin_name_value, 1, 1)
		self.grid_B.addWidget(self.btn_converter, 1, 2)
		self.group_B = QGroupBox('Conversões Real/Coin')
		self.group_B.setStyleSheet('QGroupBox  {color: red;}')
		self.group_B.setFixedSize(280, 100)
		self.group_B.setLayout(self.grid_B)

		# Container C
		self.label_alert_text = QLabel(self.combo_names.currentText(), self)
		self.label_alert_value = QLineEdit(self)
		self.label_alert_value.setFixedSize(90, 25)
		self.combo_alert_min_max = QComboBox()
		self.combo_alert_min_max.setFixedSize(70, 25)
		self.combo_alert_min_max.addItems(['Min', 'Max'])
		self.btn_cadastrar = QPushButton('Ligar', self)
		self.btn_cadastrar.setFixedSize(90, 25)
		self.btn_cadastrar.clicked.connect(self.act_add_json_alert)
		self.label_alert_info = QLabel('Aguardando alerta', self)
		self.label_alert_info.setFixedSize(220, 25)

		self.grid_C = QGridLayout()

		self.grid_C.addWidget(self.label_alert_text, 0, 0, Qt.AlignLeft)
		self.grid_C.addWidget(self.label_alert_info, 0, 1, Qt.AlignLeft)
		self.grid_C.addWidget(self.combo_alert_min_max, 1, 0, Qt.AlignLeft)
		self.grid_C.addWidget(self.label_alert_value, 1, 1, Qt.AlignLeft)
		self.grid_C.addWidget(self.btn_cadastrar, 1, 2, Qt.AlignLeft)
		
		self.group_C = QGroupBox('Alerta')
		self.group_C.setFixedSize(350, 110)
		self.group_C.setLayout(self.grid_C)

		# Container D
		label_ethernet_text = QLabel('Status Internet: ', self)
		label_ethernet_text.setFixedHeight(13)
		self.label_status_eth = QLabel(self)
		label_last_update = QLabel('Ultima atualização: ', self)
		self.label_last_update_time = QLabel(time.ctime().split()[3])

		# Grid D
		self.grid_D = QGridLayout()
		self.grid_D.addWidget(label_ethernet_text, 0, 0)
		self.grid_D.addWidget(self.label_status_eth, 0, 1)
		self.grid_D.addWidget(label_last_update, 0, 2)
		self.grid_D.addWidget(self.label_last_update_time, 0, 3)
		# Group D
		self.group_D = QGroupBox()
		self.group_D.setFixedSize(self._min_width, 60)
		self.group_D.setLayout(self.grid_D)

		# Grid Principal 1
		self.grid_master = QGridLayout()
		self.grid_master.addWidget(self.group_A, 0, 0, Qt.AlignHCenter)
		self.grid_master.addWidget(self.group_B, 1, 0, Qt.AlignLeft)
		self.grid_master.addWidget(self.group_C, 1, 0, Qt.AlignRight)
		self.grid_master.addWidget(self.group_D, 2, 0, Qt.AlignLeft)
		self.setLayout(self.grid_master)

	def get_url_coin(self):
		"""Retorna a url/api de acordo com a moeda selecionada"""
		_name_coin = self.combo_names.currentText()
		return self.url_coins[_name_coin]

	def set_value_buy(self):
		"""Setar o atributo self.__value_buy"""
		_url = self.get_url_coin()
		try:
			_buy = float(downloader.request_api_page(_url))
		except Exception as err:
			print(err)
			self.__value_buy = 'Erro'
			self.__value_buy_string = 'Erro'
		else:
			_buy_string = str('{:.2f}'.format(_buy))
			self.__value_buy = _buy
			self.__value_buy_string = _buy_string

	def update_value_buttons(self):
		"""Atualizar os labels"""
		Thread(target=self.set_status_ethernet).start()
		self.set_value_buy()
		self.label_real_value.setText(self.__value_buy_string)
		self.label_api_url.setText(self.get_url_coin())
		self.label_last_update_time.setText(time.ctime().split()[3])
		self.label_date_text_value.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.label_alert_text.setText(self.combo_names.currentText())
		self.check_alert()

	def get_online_json(self):
		_online_json = downloader.get_html_page(self.get_url_coin())
		return json.loads(_online_json)

	def act_brl_to_coin(self):
		'''Converter valor em Reais(R$) para coin selecionada'''
		self.L_coin_name.setText(self.combo_names.currentText())
		self.update_value_buttons()
		try:
			_real_brasil = float(self.label_text_real_insert_num_value.text())
		except Exception as err:
			print(err)
			print(type(err))
			_msg = f"Digite apenas numeros no campo {self.label_text_real_insert_num.text()}\nUse '.' para separar números decimais."
			MessageWindow().msgError(_msg)
			return None
		else:
			try:
				_res = _real_brasil / self.__value_buy
			except Exception as err:
				print(err)
				_string_res = 'Erro'
			else:
				_string_res = str('{:.8f}'.format(_res))
			finally:
				self.L_coin_name_value.setText(_string_res)

	def set_alert_json_current_values(self):
		"""Atualizar os dados do atributo self.__alert_json"""
		self.__alert_json.update({'coin': self.combo_names.currentText()})
		self.__alert_json.update({'value': self.label_alert_value.text()})
		self.__alert_json.update({'alert': self.combo_alert_min_max.currentText()})

	def open_offline_json(self):
		f = self.dialog_open_file()
		try:
			with open(f, 'rt') as file:
				__lines = json.load(file)
		except Exception as err:
			print(err)
			MessageWindow().msgError('Erro ao tentar abrir o arquivo')
		else:
			MessageWindow().msgOK("Cotação salva: {}".format(__lines['ticker']['buy']))

	def save_act(self):
		"""Click no menu Arquivo -> Salvar"""
		f = self.dialog_save_file()
		if os.path.isdir(os.path.dirname(f)) == False:
			MessageWindow().msgError('Erro')
			return

		with open(f, 'w') as file:
			json.dump(self.get_online_json(), file, indent=4)

	def act_add_json_alert(self):
		"""Salvar os dados de alerta no json"""
		self.set_alert_json_current_values()
		with open(self.__alert_json_file, 'w') as f:
			json.dump(self.__alert_json, f, indent=4)

		if os.path.isfile(self.__alert_json_file) == True:
			MessageWindow().msgOK('Alerta Cadastrado com sucesso')
		else:
			MessageWindow().msgError('Falha ao tentar cadastrar alerta')
			self.label_alert_info.setText('Erro')

	def check_alert(self):
		if os.path.isfile(self.__alert_json_file) == False:
			pass

		try:
			with open(self.__alert_json_file, 'rt') as f:
				__lines = json.load(f)
		except Exception as err:
			print(err)
			self.label_alert_info.setText('Erro')
			return

		print(__lines)
		text_alert = 'Alerta definido ({})'.format(__lines['coin'])
		try:
			_value = float(__lines['value'])
		except Exception as err:
			print(err)
			self.label_alert_info.setText('Erro')
			return

		try:
			if __lines['alert'] == 'Min':
				if float(self.__value_buy) < _value:
					text_alert = 'ALERTA Min ({}) atingido'.format(__lines['coin'])
			elif __lines['alert'] == 'Max':
				if float(self.__value_buy) > _value:
					text_alert = 'ALERTA Max ({}) atingido'.format(__lines['coin'])
		except Exception as err:
			print(err)
		finally:
			self.label_alert_info.setText(text_alert)

	def set_status_ethernet(self):
		"""Setar o texto do label_status_ethernet"""

		if bool(downloader.ping("https://google.com")) == True:
			self.label_status_eth.setText("Conectado")
		else:
			self.label_status_eth.setText("Offline")
			MessageWindow().msgError("Você esta sem conexão com a internet.")

	def dialog_save_file(self):
		"""
		Abre caixa de dialogo para salvar um arquivo, fixado como json.
		"""
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName = QFileDialog.getSaveFileName(
			self, "QFileDialog.getSaveFileName()",
			"",
			"Arquivos de Json (*.json);;All Files (*)",
			options=options)
		if fileName:
			f = fileName[0].strip().replace(' ', '_')
			return f
		else:
			return None

	def dialog_open_file(self):
		'''
		Caixa de seleção para selecionar/abrir um arquivo.
		'''
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.json)", options=options)
		if fileName:
			return fileName
		else:
			return None


if __name__ == "__main__":
	app = QApplication(sys.argv)
	wind = GuiWindow()
	wind.show()
	app.exec_()
