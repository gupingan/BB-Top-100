import sys
import typing as t
from PySide6 import QtWidgets, QtGui, QtCore
from app.interface import common
from app.pyside6 import main_window_ui, preload_view, main_graph


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = main_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.preset_load_config()
        self.build_interface()
        self.connect_ui_events()
        self.backend_service()

    def preset_load_config(self):
        preload_view_dialog = preload_view.PreloadView(self)
        preload_view_dialog.close.connect(self.display_exception_dialog)
        preload_view_dialog.runtimeError.connect(self.display_exception_dialog)
        preload_view_dialog.exec()

    def display_exception_dialog(self, error_message: str = None):
        if error_message:
            QtWidgets.QMessageBox.critical(self, '加载错误', error_message)
        else:
            QtWidgets.QMessageBox.critical(
                self,
                '加载错误',
                '预加载失败，原因可能如下：'
                '\n1.服务器已关闭，不可连接'
                '\n2.本地网络错误，连接网络有误'
                '\n2.服务器或者本地配置有误'
            )
        sys.exit(0)

    def build_interface(self):
        self.ui.header_center_label.setText(common.header_center_context)
        self.ui.header_app_name_label.setText(common.app_name)
        self.setMouseTracking(True)
        self.ui.widget.setMouseTracking(True)
        raw_pixmap = QtGui.QPixmap(common.app_icon_path)
        pixmap = raw_pixmap.scaled(26, 26, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtGui.Qt.TransformationMode.SmoothTransformation)
        self.ui.header_icon_label.setPixmap(pixmap)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.widget.setStyleSheet(f'background: {common.background_color}; border-radius: 8px')
        self.setProperty('allow_max', 1)
        self.setProperty('dragging', False)
        self.setProperty('drag_position', QtCore.QPoint())
        self.setProperty('resizing', False)
        self.setProperty('resize_direction', None)
        self.left_buttons = [
            (QtWidgets.QPushButton(common.left_button_texts[0]), main_graph.WordCloudWidget(self.ui.content_tw)),
            (QtWidgets.QPushButton(common.left_button_texts[1]), main_graph.Canvas1()),
            (QtWidgets.QPushButton(common.left_button_texts[2]), main_graph.Canvas2()),
            (QtWidgets.QPushButton(common.left_button_texts[3]), main_graph.Canvas3()),
            (QtWidgets.QPushButton(common.left_button_texts[4]), main_graph.Canvas4()),
        ]
        self.add_left_buttons(self.left_buttons)

    def add_left_buttons(self, button_widgets: t.List[t.Tuple[QtWidgets.QPushButton, QtWidgets.QWidget]]):
        left_layout = QtWidgets.QVBoxLayout(self.ui.scrollArea)
        for button, widget in button_widgets:
            button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            button.clicked.connect(self.handle_left_btn_click)
            left_layout.addWidget(button)
            widget.setParent(self.ui.content_tw)
            self.ui.content_tw.addTab(widget, button.text())

        vertical_spacer = QtWidgets.QSpacerItem(
            20, 40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        left_layout.addSpacerItem(vertical_spacer)
        self.ui.left_widget.setLayout(left_layout)
        self.ui.content_tw.tabBar().hide()
        if button_widgets:
            button_widgets[0][0].click()

    def connect_ui_events(self):
        self.ui.header_app_name_label.mouseDoubleClickEvent = lambda event: self.handle_max_btn_click()
        self.ui.header_min_btn.clicked.connect(self.showMinimized)
        self.ui.header_max_btn.clicked.connect(self.handle_max_btn_click)
        self.ui.header_close_btn.clicked.connect(self.close)
        self.ui.content_tw.currentChanged.connect(self.handle_content_current_changed)

    def backend_service(self):
        pass

    def activate_button(self, button: QtWidgets.QPushButton):
        for btn, widget in self.left_buttons:
            btn.setProperty('is_active', btn == button)
            if btn.property('is_active'):
                self.ui.content_tw.setCurrentWidget(widget)
                btn.setStyleSheet('''
                                QPushButton {
                                    color: rgb(255, 255, 255);
                                    background-color: rgb(0, 0, 255);
                                }
                                ''')
            else:
                btn.setStyleSheet('''
                                QPushButton {
                                    min-height: 30px;
                                    min-width: 60px;
                                    border: none;
                                    border-radius: 15px;
                                    color: rgb(120, 120, 120);
                                    font: 10pt "Microsoft YaHei";
                                }

                                QPushButton::hover {
                                    color: rgb(255, 255, 255);
                                    background-color: rgb(138, 138, 255);
                                }

                                QPushButton::pressed {
                                    color: rgb(255, 255, 255);
                                    background-color: rgb(0, 0, 255);
                                }
                                ''')

    def handle_max_btn_click(self):
        allow_max = self.property('allow_max')
        if allow_max:
            self.setProperty('last_geometry', self.geometry())
            self.showMaximized()
        else:
            self.setGeometry(self.property('last_geometry'))

        self.setProperty('allow_max', allow_max ^ 1)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            is_resizing, resize_direction = self.get_resize_direction(event.pos())
            self.setProperty('resizing', is_resizing)
            self.setProperty('resize_direction', resize_direction)
            if not is_resizing:
                self.setProperty('dragging', True)
                self.setProperty(
                    'drag_position', event.globalPosition().toPoint() - self.frameGeometry().topLeft())

            event.accept()

    def mouseMoveEvent(self, event):
        self.update_cursor_shape(event.pos())
        if self.property('resizing'):
            self.resize_window(event.globalPosition().toPoint())
            event.accept()
        elif self.property('dragging') and event.buttons() & QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.property('drag_position'))
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.setProperty('dragging', False)
            self.setProperty('resizing', False)
            self.unsetCursor()
            event.accept()

    def handle_left_btn_click(self):
        sender = self.sender()
        if isinstance(sender, QtWidgets.QPushButton):
            self.activate_button(sender)

    def get_resize_direction(self, pos):
        margin = 3
        rect = self.rect()
        top = rect.top()
        left = rect.left()
        right = rect.right()
        bottom = rect.bottom()

        if pos.y() <= top + margin:
            if pos.x() <= left + margin:
                return True, 'top_left'
            elif pos.x() >= right - margin:
                return True, 'top_right'
            else:
                return True, 'top'
        elif pos.y() >= bottom - margin:
            if pos.x() <= left + margin:
                return True, 'bottom_left'
            elif pos.x() >= right - margin:
                return True, 'bottom_right'
            else:
                return True, 'bottom'
        elif pos.x() <= left + margin:
            return True, 'left'
        elif pos.x() >= right - margin:
            return True, 'right'
        else:
            return False, None

    def resize_window(self, global_pos):
        rect = self.geometry()
        if self.property('resize_direction') == 'top':
            rect.setTop(global_pos.y())
        elif self.property('resize_direction') == 'bottom':
            rect.setBottom(global_pos.y())
        elif self.property('resize_direction') == 'left':
            rect.setLeft(global_pos.x())
        elif self.property('resize_direction') == 'right':
            rect.setRight(global_pos.x())
        elif self.property('resize_direction') == 'top_left':
            rect.setTopLeft(global_pos)
        elif self.property('resize_direction') == 'top_right':
            rect.setTopRight(global_pos)
        elif self.property('resize_direction') == 'bottom_left':
            rect.setBottomLeft(global_pos)
        elif self.property('resize_direction') == 'bottom_right':
            rect.setBottomRight(global_pos)
        self.setGeometry(rect)

    def update_cursor_shape(self, pos):
        is_resizing, direction = self.get_resize_direction(pos)
        if is_resizing:
            if direction in ['top', 'bottom']:
                self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
            elif direction in ['left', 'right']:
                self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
            elif direction in ['top_left', 'bottom_right']:
                self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
            elif direction in ['top_right', 'bottom_left']:
                self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
        else:
            self.unsetCursor()

    def closeEvent(self, event):
        for thread in common.threads:
            if thread.isRunning():
                thread.stop()
        self.close()

    def handle_content_current_changed(self, index: int):
        widget = self.left_buttons[index][1]
        if index in (1, 2, 3, 4) and hasattr(widget, 'plot'):
            widget.plot()