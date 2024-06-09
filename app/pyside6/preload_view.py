from PySide6 import QtCore, QtWidgets, QtGui
from app.interface import common
from app.pyside6.threads import PreloadThread
from app.pyside6 import preload_view_ui


class PreloadView(QtWidgets.QDialog):
    close = QtCore.Signal()
    runtimeError = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = preload_view_ui.Ui_PreloadView()
        self.ui.setupUi(self)
        self.build_interface()
        self.service_deployment()

    def build_interface(self):
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui.widget.setStyleSheet('background: white; border-radius: 8px')
        self.ui.progressBar.setValue(0)
        self.ui.content_label.setText(f'当前正在使用：{common.app_name}')
        self.ui.hint_label.setText('正在加载中，请稍后...')

    def service_deployment(self):
        self.thread = PreloadThread()
        self.thread.sendProgress.connect(self.ui.progressBar.setValue)
        self.thread.sendMessage.connect(self.ui.hint_label.setText)
        self.thread.finished.connect(self.on_preload_progress_finish)
        self.thread.close.connect(self.close.emit)
        self.thread.runtimeError.connect(self.runtimeError.emit)
        common.threads.append(self.thread)
        self.thread.start()

    def on_preload_progress_finish(self):
        self.close()
