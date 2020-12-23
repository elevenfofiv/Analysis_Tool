import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
import read_data


form_class = uic.loadUiType('./ui/MainWindows.ui')[0]

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

        self.actionLoad.triggered.connect(self.openLoadWindows)
        self.actionLinear_Analysis.triggered.connect(self.linearAnalysis)
        

    def openLoadWindows(self):
        """
        Menu > Flie > Load 누를 시, QFileDialog 열기
        Load하는 파일 명은 전역 변수로 설정됨
        """
        global loadFileNames
        
        loadFileNames = QFileDialog.getOpenFileNames(self, 'Open Files', './data/')[0]
        

    def linearAnalysis(self):
        """
        linear Analysis를 진행하기 위한 Data read 및 전처리
        """
        try:
            data = read_data.dataTreatment(loadFileNames).dataRead()
            dataKey = list(data.keys())
            sheetListDialog().displaySheet(dataKey)
            selectDataKey = sheetListDialog().selectedItem()
            print(selectDataKey)
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
    def __init__(self, parent=None):
        """
        sheetListDialog의 생성자
        """
        super(sheetListDialog, self).__init__(parent)
        sheetListDialog_ui = './ui/sheetList.ui'
        self.sheetList = uic.loadUi(sheetListDialog_ui, self)

        self.sheetList.sheetListWidget.itemClicked.connect(self.selectedItem)
        

    def displaySheet(self, dataKeys):
        """
        Dictionary의 Key값을 Display
        """
        for key in dataKeys:
            self.sheetList.sheetListWidget.addItem(key)
        
        
    def selectedItem(self):
        """
        Sheet Name QlistWidget에서 Sheet Name Selected
        """
        return self.sheetList.sheetListWidget.currentItem().text()


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