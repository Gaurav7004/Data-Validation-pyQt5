from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import QCompleter, QFileDialog, QTableWidget
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHeaderView, QVBoxLayout
import pandas as pd

#--------------------------------------------------- Pandas Model ------------------------------------------
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

###################
class ExtendedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

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


#--------------------------------------------------- Checkable Pandas Model  ------------------------------
class CheckablePandasModel(PandasModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.checkable_values = set()
        self._checkable_column = -1

    @property
    def checkable_column(self):
        return self._checkable_column

    @checkable_column.setter
    def checkable_column(self, column):
        if self.checkable_column == column:
            return
        last_column = self.checkable_column
        self._checkable_column = column

        if last_column == -1:
            self.beginInsertColumns(
                QtCore.QModelIndex(), self.checkable_column, self.checkable_column
            )
            self.endInsertColumns()

        elif self.checkable_column == -1:
            self.beginRemoveColumns(QtCore.QModelIndex(), last_column, last_column)
            self.endRemoveColumns()
        for c in (last_column, column):
            if c > 0:
                self.dataChanged.emit(
                    self.index(0, c), self.index(self.columnCount() - 1, c)
                )

    def columnCount(self, parent=QtCore.QModelIndex()):
        return super().columnCount(parent) + (1 if self.checkable_column != -1 else 0)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if self.checkable_column != -1:
            row, col = index.row(), index.column()
            if col == self.checkable_column:
                if role == QtCore.Qt.CheckStateRole:
                    return (
                        QtCore.Qt.Checked
                        if row in self.checkable_values
                        else QtCore.Qt.Unchecked
                    )
                return QtCore.QVariant()
            if col > self.checkable_column:
                index = index.sibling(index.row(), col - 1)
        return super().data(index, role)

    def setData(self, index, value, role):
        if self.checkable_column != -1:
            row, col = index.row(), index.column()
            if col == self.checkable_column:
                if role == QtCore.Qt.CheckStateRole:
                    if row in self.checkable_values:
                        self.checkable_values.discard(row)
                    else:
                        self.checkable_values.add(row)
                    self.dataChanged.emit(index, index, (role,))
                    return True
                return False
            if col > self.checkable_column:
                index = index.sibling(index.row(), col - 1)
        return super().setData(index, value, role)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if self.checkable_column != -1:
            if section == self.checkable_column and orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant()
            if section > self.checkable_column and orientation == QtCore.Qt.Horizontal:
                section -= 1
        return super().headerData(section, orientation, role)

    def flags(self, index):
        if self.checkable_column != -1:
            col = index.column()
            if col == self.checkable_column:
                return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
            if col > self.checkable_column:
                index = index.sibling(index.row(), col - 1)
        return super().flags(index)

#--------------------------------------------------

class CustomProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self._filters = dict()

    @property
    def filters(self):
        return self._filters

    def setFilter(self, expresion, column):
        if expresion:
            self.filters[column] = expresion
        elif column in self.filters:
            del self.filters[column]
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for column, expresion in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()
            regex = QtCore.QRegExp(
                expresion, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp
            )
            if regex.indexIn(text) == -1:
                return False
        return True


#------------------------------------------------- Main Odject Class --------------------------------------------
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1858, 1102)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(320, 129, 1521, 961))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        #----------------------------------------- tableView to display dataframe ------------------------------
        self.tableView.setFont(font)
        self.tableView.setAutoFillBackground(False)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(10, 150, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        #---------------------------------------------- upload Button --------------------------------------------
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.loadFile)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(322, 11, 1521, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)

        #------------------------------------ Uploaded File Name Display in LineEdit ------------------------------
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(322, 71, 1521, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        #-------------------------------------------- Search in LineEdit ------------------------------------------
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 220, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        #------------------------------------------- Validate Button -----------------------------------------------
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 290, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #------------------------------------------ Select Date ComboBox -----------------------------------------------------
        self.comboBox = ExtendedComboBox(Dialog)
        
        self.comboBox.setGeometry(QtCore.QRect(10, 330, 301, 51))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 410, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #------------------------------------------- Select Facility Name ComboBox --------------------------------------
        self.comboBox_2 = ExtendedComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 450, 301, 51))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(80, 10, 121, 121))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../../../../Pictures/74067_web (2).jpg"))
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 520, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        #--------------------------------------------- Reset Button ------------------------------------------------
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 590, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        #---------------------------------------------- Export Button ------------------------------------------
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.loadFile()
        # Filtering model
        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        filter_proxy_model.setFilterKeyColumn(0)
        # filter_proxy_model.setFilterKeyColumn(12)
        self.lineEdit_2.textChanged.connect(filter_proxy_model.setFilterRegExp)
        
        self.tableView.setModel(filter_proxy_model)
        self.comboBox.addItems(["{0}".format(col) for col in self.model._df['col_1'][:]])
        self.comboBox_2.addItems(["{0}".format(col) for col in self.model._df['col_13'][:]])
        self.comboBox.currentIndexChanged.connect(self.index_changed)
        self.comboBox.currentIndexChanged[str].connect(filter_proxy_model.setFilterRegExp)
        self.comboBox_2.currentIndexChanged.connect(self.index_changed)
        self.comboBox_2.currentIndexChanged[str].connect(filter_proxy_model.setFilterRegExp)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Upload"))
        self.pushButton_2.setText(_translate("Dialog", "Validate"))
        self.label.setText(_translate("Dialog", "Select Date"))
        self.label_2.setText(_translate("Dialog", "Select Facility Name"))
        self.pushButton_3.setText(_translate("Dialog", "Reset"))
        self.pushButton_4.setText(_translate("Dialog", "Export"))

    
    # Upload file button functionality
    def loadFile(self):
        global df
        
        # getting file and its name
        fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open CSV",
               (QtCore.QDir.homePath()), "CSV (*.csv)")
    
        # displaying filename in display box
        self.lineEdit.setText(fileName)
        
        # reading csv files
        df = pd.read_csv(fileName)
        
        #grab the first row for the header
        new_header = df.iloc[1] 

        #set the header row as the df header
        df.columns = new_header 

        df.dropna(how='all', axis=1)
        df.columns = ['col_' + str(ind) for ind in range(1, len(df.columns)+1)]
        df.drop(df.index[[0, 1]], inplace=True)

        # self.model = PandasModel(df)
        # self.tableView.setModel(self.model)
        
        self.model = PandasModel(df)
        self.proxy = CustomProxyModel(self)
        self.proxy.setSourceModel(self.model)
        # self.tableView.setModel(self.proxy)

        
        #self.comboBox.activated[str].connect(self.onSelectIndependentCols)
        #self.textEdit_2.activated[str].connect(self.onSelectIndependentCols)
        
        # displaying list of dependent columns in a co
        #self.comboBox.activated[str].connect(self.onSelectTargetCol) 

        # self.horizontalHeader = self.tableView.horizontalHeader()
        # self.horizontalHeader.sectionClicked.connect(
        #      self.on_view_horizontalHeader_sectionClicked
        # )

        self.pushButton.setDisabled(True)
        return df

    def index_changed(self, i):
        print(i)

    def text_changed(self, j):
        print(j)

    ####################################################################################
    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):

        self.logicalIndex   = logicalIndex
        self.menuValues     = QtWidgets.QMenu(self)
        self.signalMapper   = QtCore.QSignalMapper(self)
        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()

        actionAll = QtWidgets.QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()
        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            action = QtWidgets.QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        self.proxy.setFilter("", filterColumn)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        self.proxy.setFilter(stringAction, filterColumn)

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        self.proxy.setFilter(text, self.proxy.filterKeyColumn())

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)

    ####################################################################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
