import sys
import subprocess

from system import Interpreter, Intel8080

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'PySide2'])
    from PySide2 import QtCore, QtGui, QtWidgets


DEBUG = True
CLOCK = 2000000  # Hz
REFRESH = 60  # Hz


def DebugPrint(text):
    if(DEBUG):
        print(text)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.core = EmuCore()
        self.emu_thread = QtCore.QThread()
        self.core.moveToThread(self.emu_thread)
        self.emu_thread.started.connect(self.core.run)

        self.open_act = QtWidgets.QAction('Open ROM', self)
        self.open_act.triggered.connect(Util.Launch)

        exit_act = QtWidgets.QAction('Exit', self)
        exit_act.triggered.connect(self.emu_thread.quit)
        exit_act.triggered.connect(QtWidgets.qApp.quit)

        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        filemenu.addAction(self.open_act)
        filemenu.addAction(exit_act)

        self.native = QtGui.QBitmap(224, 256)
        self.native.fill(QtCore.Qt.color1)
        self.scaled = QtWidgets.QLabel(self)
        self.scaled.setPixmap(self.native.scaled(672, 768, QtCore.Qt.KeepAspectRatio))
        self.setCentralWidget(self.scaled)

        self.painter = QtGui.QPainter(self.native)
        self.painter.setPen(QtCore.Qt.color0)

        self.setGeometry(624, 146, 672, 788)  # Improve this later
        self.setWindowTitle('Space Invaders')
        self.setWindowIcon(QtGui.QIcon('icon.bmp'))
        self.show()

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    @QtCore.Slot(list)
    def Draw(self, state):
        self.native.fill(QtCore.Qt.color1)
        for i in range(256):  # Height
            index = 0x2400 + (i << 5)
            for j in range(32):
                vram_byte = state.memory[index]
                index += 1
                for k in range(8):
                    if(vram_byte & 1):
                        self.painter.drawPoint(i, 255 - j*8 - k)
                    vram_byte = vram_byte >> 1

        self.scaled.setPixmap(ui.native.scaled(672, 768))
        self.scaled.repaint()
        return

    def keyPressEvent(self, event):
        print(event.key())
    
    def keyReleaseEvent(self, event):
        print(event.key())


class Util():
    @staticmethod
    def Launch():
        filepath = QtWidgets.QFileDialog.getOpenFileName(None, 'Open ROM', '', 'Space Invaders ROM (*.*)')
        if(filepath[0] != ''):
            ui.core.romname = filepath[0]
            ui.emu_thread.start()


class EmuCore(QtCore.QObject):
    gfx_upl = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self.romname = ''

    def run(self):
        i8080 = Intel8080()
        i8080.LoadROM(self.romname)
        interp = Interpreter()

        ui.open_act.setEnabled(False)

        self.gfx_upl.connect(ui.Draw, type=QtCore.Qt.DirectConnection)
        while(True):
            interp.ExecInstr(i8080)
            self.gfx_upl.emit(i8080)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
