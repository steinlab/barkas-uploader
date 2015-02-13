#!/usr/bin/env python
# Barkas Uploader 0.1

import dropbox
from PyQt5.QtCore import QDir, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QFileDialog, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpinBox,
                             QVBoxLayout, QWidget)



class Screenshot(QWidget):
    def __init__(self):
        super(Screenshot, self).__init__()

        self.screenshotLabel = QLabel()
        self.screenshotLabel.setSizePolicy(QSizePolicy.Expanding,
                                           QSizePolicy.Expanding)
        self.screenshotLabel.setAlignment(Qt.AlignCenter)
        self.screenshotLabel.setMinimumSize(240, 160)

        self.createOptionsGroupBox()
        self.createButtonsLayout()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.screenshotLabel)
        # mainLayout.addWidget(self.optionsGroupBox)
        mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(mainLayout)

        self.shootScreen()
        self.delaySpinBox.setValue(5)

        self.setWindowTitle("Barkas Uploader 0.1")
        self.resize(300, 200)

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.screenshotLabel.size(), Qt.KeepAspectRatio)
        if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
            self.updateScreenshotLabel()

    def newScreenshot(self):
        if self.hideThisWindowCheckBox.isChecked():
            self.hide()
        self.newScreenshotButton.setDisabled(True)

        QTimer.singleShot(self.delaySpinBox.value() * 1,
                          self.shootScreen)

    def saveScreenshot(self):
        format = 'png'
        initialPath = QDir.currentPath() + "/Screenshoot." + format

        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", initialPath,
                                                  "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
        if fileName:
            self.originalPixmap.save(fileName, format)

    def saveDropboxScreenshot(self):
        client = dropbox.client.DropboxClient('NsnEOg0nZHQAAAAAAAAUWYsLigDlpUq8alBAGYFxdRZttDLfq57j45ePB-7kVOTJ')
        print('linked account: ', client.account_info())

        f = open('working-draft.txt', 'rb')
        response = client.put_file('/magnum-opus.txt', f)
        print ('uploaded: ', response)

        folder_metadata = client.metadata('/')
        print ('metadata: ', folder_metadata)

        f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
        out = open('magnum-opus.txt', 'wb')
        out.write(f.read())
        out.close()
        print (metadata)

    def shootScreen(self):
        if self.delaySpinBox.value() != 0:
            QApplication.instance().beep()

        screen = QApplication.primaryScreen()
        if screen is not None:
            self.originalPixmap = screen.grabWindow(0)
        else:
            self.originalPixmap = QPixmap()

        self.updateScreenshotLabel()

        self.newScreenshotButton.setDisabled(False)
        if self.hideThisWindowCheckBox.isChecked():
            self.show()

    def updateCheckBox(self):
        if self.delaySpinBox.value() == 0:
            self.hideThisWindowCheckBox.setDisabled(True)
        else:
            self.hideThisWindowCheckBox.setDisabled(False)

    def createOptionsGroupBox(self):
        self.optionsGroupBox = QGroupBox("Options")

        self.delaySpinBox = QSpinBox()
        self.delaySpinBox.setSuffix(" s")
        self.delaySpinBox.setMaximum(60)
        self.delaySpinBox.valueChanged.connect(self.updateCheckBox)

        self.delaySpinBoxLabel = QLabel("Screenshot Delay:")

        self.hideThisWindowCheckBox = QCheckBox("Hide This Window")

        optionsGroupBoxLayout = QGridLayout()
        optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
        optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
        optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0, 1, 2)
        self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

    def createButtonsLayout(self):
        self.newScreenshotButton = self.createButton("Новый скриншот",
                                                     self.newScreenshot)

        self.saveDropboxScreenshotButton = self.createButton("Сохранить в Dropbox",
                                                             self.saveDropboxScreenshot)

        self.saveScreenshotButton = self.createButton("Сохранить",
                                                      self.saveScreenshot)

        self.quitScreenshotButton = self.createButton("Выход", self.close)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.newScreenshotButton)
        self.buttonsLayout.addWidget(self.saveScreenshotButton)
        self.buttonsLayout.addWidget(self.saveDropboxScreenshotButton)
        self.buttonsLayout.addWidget(self.quitScreenshotButton)

    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

    def updateScreenshotLabel(self):
        self.screenshotLabel.setPixmap(self.originalPixmap.scaled(
            self.screenshotLabel.size(), Qt.KeepAspectRatio,
            Qt.SmoothTransformation))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    screenshot = Screenshot()
    screenshot.show()
    sys.exit(app.exec_())
