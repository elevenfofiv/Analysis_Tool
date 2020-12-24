import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtWidgets import *
from PyQt5 import uic
import read_data


form_class = uic.loadUiType('./ui/MainWindows.ui')[0]

class communication(QObject):
            
    """
    Slot 함수 내 반환값 활용을 위한 Pyqtsignal 활용
    """
    filename = pyqtSignal(list)
    sheetname = pyqtSignal(str)

    def getFilename(self):
        self.fileName = QFileDialog.getOpenFileNames(None, 'Open Files', './data/')[0]
    
    def runFileName(self):
        self.filename.emit(self.fileName)

    def getSheetname(self,data):
        sheetList = sheetListDialog(data)
        self.sheetName = sheetList.selectedItem()
        print(self.sheetName)



class mainWindows(QMainWindow, form_class):
    """
    Main 창 관련 Class
    """
    def __init__(self):
        """
        mainWindows Class 생성자
        """
        super().__init__()
        self.setupUi(self)

        self.communicator = communication()
        self.actionLoad.triggered.connect(self.communicator.getFilename)
        self.communicator.filename.connect(self.linearAnalysis)
        self.actionLinear_Analysis.triggered.connect(self.communicator.runFileName)


        

    def linearAnalysis(self,loadFileNames):
        """
        linear Analysis를 진행하기 위한 Data read 및 전처리
        """
        try:
            data = read_data.dataTreatment(loadFileNames).dataRead()
            dataKey = list(data.keys())
            self.communicator.getSheetname(dataKey)
            # selectDataKey = sheetListDialog(dataKey)
            # print(selectDataKey)
            # print(data[selectDataKey].head())
            # global analysisData
            # analysisData = data[selectDataKey]
            # itemLists = list(analysisData)
            # itemListDialog().displayItem(itemLists)

        except NameError:
            QMessageBox.warning(self,'Error', 'You sholud load files to analysis', QMessageBox.Ok)
            

class sheetListDialog(QDialog):
    """
    Dictionary형태로 저장된 Data의 Key 값을 Display & Select하는 기능
    """
    # def __init__(self, dataKeys, parent=None):
    def __init__(self, dataKeys):
        """
        sheetListDialog의 생성자
        """
        super().__init__()
        # super().__init__(parent)

        sheetListDialog_ui = './ui/sheetList.ui'

        self.sheetList = uic.loadUi(sheetListDialog_ui, self)
        for key in dataKeys:
            self.sheetList.sheetListWidget.addItem(key)
        self.sheetList.show()
        self.sheetCommunicator = communication()
        self.sheetCommunicator.sheetname.connect(itemListDialog.displayItem)
        self.sheetList.okayPushButton.clicked.connect(self.sheetCommunicator.getSheetname)
        
    def selectedItem(self):
        """
        Sheet Name QlistWidget에서 Sheet Name Selected
        """
        selectSheetName = self.sheetList.sheetListWidget.
        return selectSheetName


class itemListDialog(QDialog):
    """
    반환된 Data를 Table Form Windows로 Display
    """
    def __init__(self, parent=None):
        """
        tableFormWindows 생성자
        """
        super(itemListDialog, self).__init__(parent)

        itemListDialog_ui = './ui/itemList.ui'
        self.itemList = uic.loadUi(itemListDialog_ui, self)
        
    def displayItem(self, itemLists):
        """
        읽어들인 DataFrame의 Column 값을 별도의 창을 통해 Display & Select하는 함수
        """
        for item in itemLists:
            self.itemList.inputItemlistWidget.addItem(item)
            self.itemList.outputItemlistWidget.addItem(item)
        self.itemList.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = mainWindows()
    mainWindow.show()
    app.exec_()