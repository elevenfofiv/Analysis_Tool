from fileinput import filename
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import *
from PyQt5 import uic
import read_data


form_class = uic.loadUiType('./ui/MainWindows.ui')[0]

# class communication(QObject):
#     """
#     Slot 함수 내 반환값 활용을 위한 Pyqtsignal 활용
#     """
#     filename = pyqtSignal(list)
#     sheetname = pyqtSignal(str)

#     def getFilename(self):
#         self.fileName = QFileDialog.getOpenFileNames(None, 'Open Files', './data/')[0]
    
#     def runFilename(self):
#         self.filename.emit(self.fileName)

#     def getSheetname(self,data):
#         self.method = sheetListDialog(data)
        

#     def runSheetname(self):
#         print(self.sheetName)
#         self.sheetname.emit(self.sheetName)
        


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

        # self.communicator = communication()
        # self.communicator.filename.connect(self.linearAnalysis)

        self.actionLoad.triggered.connect(self.getFilename)
        self.actionLinear_Analysis.triggered.connect(self.linearAnalysis)

    def getFilename(self):
        global filename
        filename = QFileDialog.getOpenFileNames(None, 'Open Files', './data/')[0]

    def linearAnalysis(self):
        """
        linear Analysis를 진행하기 위한 Data read 및 전처리
        """
        try:
            data = read_data.dataTreatment(filename).dataRead()
            dataKey = list(data.keys())
            sheetlist = sheetListDialog(dataKey)
            global sheetname
            sheetname = sheetlist.selectedItem()
            print(sheetname)
        except NameError:
            QMessageBox.warning(self,'Error', 'You sholud load files to analysis', QMessageBox.Ok)

        
        
        

class sheetListDialog(QDialog):
    """
    Dictionary형태로 저장된 Data의 Key 값을 Display & Select하는 기능
    """
    def __init__(self, dataKeys, parent=None):
        """
        sheetListDialog의 생성자
        """
        super(sheetListDialog, self).__init__(parent)

        sheetListDialog_ui = './ui/sheetList.ui'

        self.sheetList = uic.loadUi(sheetListDialog_ui, self)
        # self.selItem = None
        # self.sheetCommunicator = communication()

        self.sheetList.okayPushButton.clicked.connect(itemListDialog.displayItem)
        self.sheetList.sheetListWidget.itemClicked.connect(self.selectedItem)

        for key in dataKeys:
            self.sheetList.sheetListWidget.addItem(key)
        self.sheetList.show()

    def selectedItem(self):
        selItem = self.sheetList.sheetListWidget.currentItem().text()
        return selItem


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