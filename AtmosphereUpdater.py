from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import sys
import os
import shutil
import time

class Ui_Dialog(QDialog):
	def __init__(self, *args):
		super(Ui_Dialog, self).__init__(*args)
		loadUi(r'Resources\AtmosphereUpdater.ui', self)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowIcon(QIcon('Resources\Atmosphere.ico'))
		self.Button.clicked.connect(self.Update)
		self.comboBox.currentTextChanged.connect(self.comboBoxRefresh)
		self.textBrowser.append('本软件完全免费，严禁用于商业用途')
		global PathBool 
		PathBool = False
		self.Button.setEnabled(False)

	def move_file(self,orgin_path,moved_path):
		dir_files=os.listdir(orgin_path)            
		for file in  dir_files:
			file_path=os.path.join(orgin_path,file)  
			if os.path.isfile(file_path):          
				if os.path.exists(os.path.join(moved_path,file)):
					#print(file)
					continue
				else:
					shutil.copy(file_path, moved_path)
			if os.path.isdir(file_path):  
				path1 = os.path.join(os.path.abspath(moved_path), file)	
				if os.path.exists(path1) == False:			
					shutil.copytree(file_path,path1)
				#else:
				#	print(path1)

	def DeleteFiles(self,path,remainDirsList,fileList):
		dirsList = []
		dirsList = os.listdir(path)
		for file in dirsList:	
			if file not in remainDirsList:
				filepath = os.path.join(path,file)
				if os.path.isdir(filepath):
					#print(filepath)
					shutil.rmtree(filepath, True)			
				elif file not in fileList:
					#print(filepath)
					os.remove(filepath)

	def getDirectory(self):
		global upd_path
		upd_path = QFileDialog.getExistingDirectory(None,"选择文件夹","C:/")
		if os.path.exists(upd_path+'\\atmosphere\\') == True and os.path.exists(upd_path+'\\bootloader\\') == True:
			self.textBrowser.append('升级包所在路径为 ' + upd_path)
			self.textBrowser.append('升级过程因TF卡读写速度和文件数量需要等待几分钟到十几分钟，期间请勿关闭本程序')
			self.Button.setText('开始升级')
			global PathBool
			PathBool = True
		else:
			self.textBrowser.append('升级包目录不匹配，请重新选择目录')
	def installNew(self):

		
		path_bak =os.path.abspath(self.comboBox.currentText() + '\\AU_Bak\\')
		if not os.path.exists(path_bak):
			os.makedirs(path_bak)
		else:
			shutil.rmtree(path_bak,True)
			os.makedirs(path_bak)
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents\\0100000000001000')
		if os.path.exists(path):
			shutil.rmtree(path,True)	
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents\\0100000000001013')
		if os.path.exists(path):
			shutil.rmtree(path,True)	
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents\\0100000000001007')
		if os.path.exists(path):
			shutil.rmtree(path,True)	
		path =os.path.abspath(self.comboBox.currentText()+'\\atmosphere\\contents')
		shutil.copytree(path, path_bak+'\\contents\\')
		path =os.path.abspath(self.comboBox.currentText()+'\\switch\\Checkpoint\\saves')
		if os.path.exists(path):		
			shutil.copytree(path, path_bak+'\\Checkpoint\\saves')
		path = self.comboBox.currentText()+'\\'
		dirsList=['Nintendo','emuMMC','AU_Bak']
		fileList=['license.dat']
		self.DeleteFiles(path,dirsList,fileList)


		global upd_path
		source = upd_path
		target = self.comboBox.currentText()+'\\'
		self.move_file(source,target)

		source = path_bak+'\\Checkpoint\\'
		target = self.comboBox.currentText()+'\\switch\\Checkpoint\\'
		if os.path.exists(source):
			self.move_file(source,target)

		source = path_bak+'\\contents\\'
		target = self.comboBox.currentText()+'\\atmosphere\\contents\\'
		if os.path.exists(source):
			self.move_file(source,target)

		shutil.rmtree(path_bak,True)
		self.textBrowser.append('完成')
		reply = QMessageBox.information(self,'完成',"升级成功",QMessageBox.Yes,QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			os._exit(0)


	@pyqtSlot()			
	def Update(self):
		global PathBool
		if PathBool == False:
			self.getDirectory()
		else:
			self.installNew()

	@pyqtSlot()
	def comboBoxRefresh(self):
		if os.path.exists(self.comboBox.currentText()+'\\atmosphere\\') == True and os.path.exists(self.comboBox.currentText()+'\\emummc\\') == True:
			self.textBrowser.append('TF卡盘符更改为 '+self.comboBox.currentText())
			self.Button.setEnabled(True)
		else:
			self.textBrowser.append('读取错误，请重新选择TF卡所在盘符')
			self.Button.setEnabled(False)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui=Ui_Dialog()
	
	ui.show()
	sys.exit(app.exec_()) 