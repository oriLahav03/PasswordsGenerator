from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QComboBox, QCompleter, QMessageBox
from appdirs import unicode

from mail_sender import Mail


class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from purposes_options_comboBox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

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


PURPOSE_OPTIONS_LIST = ['Choose option or type your own', 'Instagram', 'Facebook', 'Gmail']


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, my_mainWindow, parent=None):
        super(MainWindow, self).__init__(parent)

        self.central_widget = QtWidgets.QWidget(my_mainWindow)
        self._translate = QtCore.QCoreApplication.translate

        # Create the main window
        self.my_mainWindow = my_mainWindow
        my_mainWindow.setObjectName("Passwords Generator")
        my_mainWindow.setCentralWidget(self.central_widget)
        my_mainWindow.setWindowTitle(self._translate("Passwords Generator", "Passwords Generator"))

        self.length_counter_spinBox = QtWidgets.QSpinBox(self.central_widget)
        self.purposes_options_comboBox = ExtendedComboBox(my_mainWindow)
        self.email_input = QtWidgets.QTextEdit(self.central_widget)

        # Create the main font
        self.font = QtGui.QFont()
        self.font.setFamily("MS PGothic")
        self.font.setPointSize(15)

        # Create the layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName("mainLayout")

    def create_welcome_message_label(self):
        welcome_message_label = QtWidgets.QLabel(self.central_widget)
        font = QtGui.QFont()
        font.setFamily("MS PGothic")
        font.setPointSize(20)
        font.setUnderline(True)
        welcome_message_label.setFont(font)
        welcome_message_label.setMaximumHeight(50)
        welcome_message_label.setMouseTracking(True)
        welcome_message_label.setAlignment(QtCore.Qt.AlignCenter)
        welcome_message_label.setObjectName("welcome_message")
        welcome_message_label.setText(self._translate("Passwords Generator", "Welcome to Password Generator!"))
        self.verticalLayout.addWidget(welcome_message_label)

    def create_vertical_line(self):
        vertical_line = QtWidgets.QFrame(self.central_widget)
        vertical_line.setFrameShape(QtWidgets.QFrame.HLine)
        vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        vertical_line.setObjectName("vertical_line")
        self.verticalLayout.addWidget(vertical_line)

    def create_enter_email_label(self):
        enter_email_label = QtWidgets.QLabel(self.central_widget)
        enter_email_label.setMaximumHeight(35)
        enter_email_label.setFont(self.font)
        enter_email_label.setAlignment(QtCore.Qt.AlignCenter)
        enter_email_label.setObjectName("enter_email_label")
        enter_email_label.setText(self._translate("Passwords Generator", "Please enter your email:"))
        self.verticalLayout.addWidget(enter_email_label)

    def create_email_input(self):
        self.email_input.setMaximumHeight(35)
        self.email_input.setFont(self.font)
        self.email_input.setObjectName("email_input")
        self.verticalLayout.addWidget(self.email_input)

    def create_choose_purpose_label(self):
        choose_purpose_label = QtWidgets.QLabel(self.central_widget)
        choose_purpose_label.setMaximumHeight(35)
        choose_purpose_label.setFont(self.font)
        choose_purpose_label.setAlignment(QtCore.Qt.AlignCenter)
        choose_purpose_label.setObjectName("choose_purpose_label")
        choose_purpose_label.setText(self._translate("Passwords Generator", "Choose the purpose of the password:"))
        self.verticalLayout.addWidget(choose_purpose_label)

    def create_choose_purpose_comboBox(self):
        self.purposes_options_comboBox.setMaximumHeight(35)
        self.purposes_options_comboBox.setFont(self.font)
        self.purposes_options_comboBox.addItems(PURPOSE_OPTIONS_LIST)
        self.purposes_options_comboBox.setObjectName("purposes_options_comboBox")
        self.purposes_options_comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.purposes_options_comboBox)

    def create_enter_password_length_label(self):
        enter_password_length_label = QtWidgets.QLabel(self.central_widget)
        enter_password_length_label.setMaximumHeight(35)
        enter_password_length_label.setFont(self.font)
        enter_password_length_label.setAlignment(QtCore.Qt.AlignCenter)
        enter_password_length_label.setObjectName("enter_password_length_label")
        enter_password_length_label.setText(
            self._translate("Passwords Generator", "Please enter the wanted password length:"))
        self.verticalLayout.addWidget(enter_password_length_label)

    def create_password_length_spinBox(self):
        self.length_counter_spinBox.setMaximumHeight(35)
        self.length_counter_spinBox.setFont(self.font)
        self.length_counter_spinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.length_counter_spinBox.setObjectName("length_counter_spinBox")
        self.verticalLayout.addWidget(self.length_counter_spinBox)

    def create_generate_button(self):
        generate_button = QtWidgets.QPushButton(self.central_widget)
        generate_button.setMaximumHeight(35)
        generate_button.setFont(self.font)
        generate_button.setObjectName("generate_button")
        generate_button.setText(self._translate("Passwords Generator", "Generate"))
        self.verticalLayout.addWidget(generate_button)
        return generate_button

    def setupUi(self):
        # Create the main widget
        self.central_widget.setObjectName("central_widget")

        # Create the welcome message label
        self.create_welcome_message_label()

        # Create a vertical line
        self.create_vertical_line()

        # Create the enter email label
        self.create_enter_email_label()

        # Create the email input filed
        self.create_email_input()

        # Create a vertical line
        self.create_vertical_line()

        # Create the choose purpose label
        self.create_choose_purpose_label()

        # Create the choose purpose area
        self.create_choose_purpose_comboBox()

        # Create a vertical line
        self.create_vertical_line()

        # Create the enter password length label
        self.create_enter_password_length_label()

        # Create the password length counter
        self.create_password_length_spinBox()

        # Create a vertical line
        self.create_vertical_line()

        # Create the generate button
        generate_button = self.create_generate_button()

        QtCore.QMetaObject.connectSlotsByName(self.my_mainWindow)
        generate_button.clicked.connect(self.purpose_selected)

    def purpose_selected(self):
        email = self.email_input.toPlainText()
        purpose = self.purposes_options_comboBox.currentText()
        length = self.length_counter_spinBox.text()

        if purpose == PURPOSE_OPTIONS_LIST[0]:
            QMessageBox.critical(QtWidgets.QWidget(), 'Fail', 'Please choose purpose')
            return

        try:
            mail = Mail()
            mail.get_info_from_user(email, purpose, length)
        except Exception as e:
            if 'successfully' not in str(e):
                QMessageBox.critical(QtWidgets.QWidget(), 'Fail', str(e))
            else:
                QMessageBox.about(QtWidgets.QWidget(), 'Success!', str(e))
