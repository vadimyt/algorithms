import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from UI.widget import Widget

loader = QUiLoader()

app = QtWidgets.QApplication(sys.argv)
window = Widget()
window.show()
app.exec()