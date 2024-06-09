# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(911, 581)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_3 = QVBoxLayout(MainWindow)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_5 = QVBoxLayout(self.widget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.window_head_layout = QHBoxLayout()
        self.window_head_layout.setSpacing(0)
        self.window_head_layout.setObjectName(u"window_head_layout")
        self.header_icon_label = QLabel(self.widget)
        self.header_icon_label.setObjectName(u"header_icon_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header_icon_label.sizePolicy().hasHeightForWidth())
        self.header_icon_label.setSizePolicy(sizePolicy)
        self.header_icon_label.setScaledContents(True)

        self.window_head_layout.addWidget(self.header_icon_label)

        self.header_app_name_label = QLabel(self.widget)
        self.header_app_name_label.setObjectName(u"header_app_name_label")
        sizePolicy.setHeightForWidth(self.header_app_name_label.sizePolicy().hasHeightForWidth())
        self.header_app_name_label.setSizePolicy(sizePolicy)
        self.header_app_name_label.setStyleSheet(u"color: rgb(0, 0, 255);\n"
"font: 12pt \"\u5e7c\u5706\";\n"
"font-weight:  bold;\n"
"margin-top: 5px;\n"
"margin-bottom: 5px;\n"
"margin-left: 8px;")

        self.window_head_layout.addWidget(self.header_app_name_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.window_head_layout.addItem(self.horizontalSpacer)

        self.header_center_label = QLabel(self.widget)
        self.header_center_label.setObjectName(u"header_center_label")
        self.header_center_label.setStyleSheet(u"color: rgb(120, 120, 120);\n"
"font: 9pt \"Microsoft YaHei\";\n"
"letter-spacing: -0.4px")
        self.header_center_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.window_head_layout.addWidget(self.header_center_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.window_head_layout.addItem(self.horizontalSpacer_2)

        self.header_min_btn = QPushButton(self.widget)
        self.header_min_btn.setObjectName(u"header_min_btn")
        self.header_min_btn.setStyleSheet(u"QPushButton{\n"
"	color: rgb(255, 170, 0);\n"
"	background-color: rgb(255, 170, 0);\n"
"	min-width: 14px;\n"
"	max-width: 14px;\n"
"	min-height: 14px;\n"
"	max-height: 14px;\n"
"	border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(245, 160, 0);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(230, 150, 0);\n"
"}")

        self.window_head_layout.addWidget(self.header_min_btn)

        self.header_max_btn = QPushButton(self.widget)
        self.header_max_btn.setObjectName(u"header_max_btn")
        self.header_max_btn.setStyleSheet(u"QPushButton{\n"
"	margin-left: 5px;\n"
"	margin-right: 5px;\n"
"	color: rgb(0, 255, 0);\n"
"	background-color: rgb(0, 255, 0);\n"
"	min-width: 14px;\n"
"	max-width: 14px;\n"
"	min-height: 14px;\n"
"	max-height: 14px;\n"
"	border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(0, 244, 0);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(0, 233, 0);\n"
"}")

        self.window_head_layout.addWidget(self.header_max_btn)

        self.header_close_btn = QPushButton(self.widget)
        self.header_close_btn.setObjectName(u"header_close_btn")
        self.header_close_btn.setStyleSheet(u"QPushButton{\n"
"	color: rgb(255, 0, 0);\n"
"	background-color: rgb(255, 0, 0);\n"
"	min-width: 14px;\n"
"	max-width: 14px;\n"
"	min-height: 14px;\n"
"	max-height: 14px;\n"
"	border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(244, 0, 0);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(233, 0, 0);\n"
"}")

        self.window_head_layout.addWidget(self.header_close_btn)


        self.verticalLayout_5.addLayout(self.window_head_layout)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 8))
        self.widget_4.setMaximumSize(QSize(16777215, 8))

        self.verticalLayout_5.addWidget(self.widget_4)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 1))
        self.widget_2.setMaximumSize(QSize(16777215, 1))
        self.widget_2.setStyleSheet(u"background-color: rgb(207, 207, 207);")

        self.verticalLayout_5.addWidget(self.widget_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(60, 0))
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
"	border: none\n"
"}\n"
"QWidget {\n"
"	min-width: 60px;\n"
"}\n"
"\n"
"QPushButton {\n"
"	min-height: 30px;\n"
"	min-width: 60px;\n"
"	border: none;\n"
"	border-radius: 15px;\n"
"	color: rgb(120, 120, 120);\n"
"	font: 10pt \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(138, 138, 255);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(0, 0, 255);\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.left_widget = QWidget()
        self.left_widget.setObjectName(u"left_widget")
        self.left_widget.setGeometry(QRect(0, 0, 120, 511))
        self.left_widget.setMinimumSize(QSize(60, 0))
        self.verticalLayout_4 = QVBoxLayout(self.left_widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea.setWidget(self.left_widget)

        self.verticalLayout.addWidget(self.scrollArea)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(1, 0))
        self.widget_3.setMaximumSize(QSize(1, 16777215))
        self.widget_3.setStyleSheet(u"background-color: rgb(207, 207, 207);")

        self.horizontalLayout.addWidget(self.widget_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.content_tw = QTabWidget(self.widget)
        self.content_tw.setObjectName(u"content_tw")
        self.content_tw.setStyleSheet(u"/* \u9009\u9879\u5361\u6837\u5f0f */\n"
"QTabWidget::tab {\n"
"max-height: 0;\n"
"max-width: 0;\n"
"margin: 0;\n"
"padding: 0;\n"
"border: none;\n"
"}\n"
"QTabWidget{\n"
"border: none;\n"
"}\n"
"QTabWidget::pane{\n"
"border: none;\n"
"}\n"
"\n"
"\n"
"QMenu {\n"
"background-color: #f0f0f0;\n"
"border: 1px solid #cccccc;\n"
"padding: 4px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"padding: 12px 24px;\n"
"margin: -4px;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"background-color: #e0e0e0;\n"
"}\n"
"\n"
"QAction {\n"
"color: #333333;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"")
        self.content_tw.setTabPosition(QTabWidget.North)
        self.content_tw.setTabShape(QTabWidget.Rounded)
        self.content_tw.setElideMode(Qt.ElideNone)
        self.content_tw.setDocumentMode(False)
        self.content_tw.setTabsClosable(False)
        self.content_tw.setTabBarAutoHide(True)

        self.verticalLayout_2.addWidget(self.content_tw)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.widget)


        self.retranslateUi(MainWindow)

        self.content_tw.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.header_icon_label.setText(QCoreApplication.translate("MainWindow", u"icon", None))
        self.header_app_name_label.setText(QCoreApplication.translate("MainWindow", u"AppName", None))
        self.header_center_label.setText(QCoreApplication.translate("MainWindow", u"----------", None))
        self.header_min_btn.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.header_max_btn.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.header_close_btn.setText(QCoreApplication.translate("MainWindow", u"\u00d7", None))
    # retranslateUi

