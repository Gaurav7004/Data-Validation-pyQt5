from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon,QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidget, QCompleter, QApplication, QFormLayout
from PyQt5.QtCore import Qt, QDir, QSortFilterProxyModel, QRegExp
import sys, re, os, csv
from random import randint, choice
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QLineEdit, QTableView, QComboBox

class ExtendedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        self.setView(QtWidgets.QListView(self))
        self.view().pressed.connect(self.handle_item_pressed)
        #self.setModel(QtGui.QStandardItemModel(self))

        # add a filter model to filter matching items
        self.pFilterModel = QtCore.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well

    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

    def filterAcceptsRow(self, source_row, source_parent):
        for key, regex in self.filters.items():
            ix = self.sourceModel().index(source_row, key, source_parent)
            if ix.isValid():
                text = self.sourceModel().data(ix)
                text = str(text)
                if regex.indexIn(text) == -1:
                    return False
        return True

    @property
    def _filters(self):
        return self.filters

    def setFilterByColumn(self, regex, column):
        self.filters[column] = regex
        self.invalidateFilter()

    # when any item get pressed 
    def handle_item_pressed(self, index): 
  
        # getting which item is pressed 
        item = self.model().itemFromIndex(index) 
  
        # make it check if unchecked and vice-versa 
        if item.checkState() == Qt.Checked: 
            item.setCheckState(Qt.Unchecked) 
        else: 
            item.setCheckState(Qt.Checked) 
  
        # calling method 
        self.check_items() 
  
    # method called by check_items 
    def item_checked(self, index): 
  
        # getting item at index 
        item = self.model().item(index, 0) 
  
        # return true if checked else false 
        return item.checkState() == Qt.Checked 
  
    # calling method 
    def check_items(self): 
        # blank list 
        checkedItems = [] 
  
        # traversing the items 
        for i in range(self.count()): 
  
            # if item is checked add it to the list 
            if self.item_checked(i): 
                checkedItems.append(i) 
  
        # call this method 
        self.update_labels(checkedItems) 
  
    # method to update the label 
    def update_labels(self, item_list): 
        global n
        n = '' 
        count = 0
  
        # traversing the list 
        for i in item_list: 
  
            # if count value is 0 don't add comma 
            if count == 0: 
                n += ' % s' % i 
            # else value is greater then 0 
            # add comma 
            else: 
                n += ', % s' % i 
  
            # increment count 
            count += 1
  
  
        # loop 
        for i in range(self.count()): 
  
            # getting label 
            text_label = self.model().item(i, 0).text() 
  
            # default state 
            if text_label.find('-') >= 0: 
                text_label = text_label.split('-')[0] 
  
            # shows the selected items 
            item_new_text_label = text_label + ' - selected index: ' + n 
  
           # setting text to combo box 
            self.setItemText(i, item_new_text_label) 
        
        return n
    # flush 
    sys.stdout.flush()



class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}

    
    @property
    def _filters(self):
        return self.filters

    def setFilterByColumn(self, regex, column):
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for key, regex in self.filters.items():
            ix = self.sourceModel().index(source_row, key, source_parent)
            if ix.isValid():
                text = self.sourceModel().data(ix)
                text = str(text)
                if regex.indexIn(text) == -1:
                    return False
        return True


def random_word():
    letters = "abcdedfg"
    word = "".join([choice(letters) for _ in range(randint(4, 7))])
    return word


class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())

        tv1 = QTableView(self)
        tv2 = QTableView(self)
        model = QStandardItemModel(8, 4, self)
        proxy = SortFilterProxyModel(self)
        proxy.setSourceModel(model)
        tv1.setModel(model)
        tv2.setModel(proxy)
        self.layout().addWidget(tv1)
        self.layout().addWidget(tv2)

        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                item = QStandardItem()
                item.setData(random_word(), Qt.DisplayRole)
                model.setItem(i, j, item)

        flayout = QFormLayout()
        self.layout().addLayout(flayout)
        for i in range(model.columnCount()):
            le = ExtendedComboBox(self)
            #le = QLineEdit(self)
            flayout.addRow("column: {}".format(i), le)
            # le.textChanged.connect(lambda text, col=i:
            #                        proxy.setFilterByColumn(QRegExp(text, Qt.CaseSensitive, QRegExp.FixedString),
            #                                                col))
            
            # le.addItems(["{0}".format(col)
            #                     for col in tv2[:i]])
            le.currentIndexChanged[str].connect(lambda text, col=i:
                                   proxy.setFilterByColumn(QRegExp(text, Qt.CaseSensitive, QRegExp.FixedString),
                                                           col))

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())