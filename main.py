import hashlib
import sys
import subprocess

from system import Interpreter, Intel8080

try:
    import PyQt5.QtCore as QtCore
    import PyQt5.QtGui as QtGui
    import PyQt5.QtWidgets as QtWidgets
except:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
    import PyQt5.QtCore as QtCore
    import PyQt5.QtGui as QtGui
    import PyQt5.QtWidgets as QtWidgets

if(sys.version.startswith('3.7')):
    print('Please use Python 3.6.x, as 3.7 is broken with the keyboard module.')
    sys.exit(1)

try:
    import keyboard
except:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'keyboard'])
    import keyboard

DEBUG = True
CLOCK = 2000000  # Hz
REFRESH = 60  # Hz
CYCLES_PER_FRAME = 10  # int(CLOCK / REFRESH)


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

        self.open_act = QtWidgets.QAction('Open ROM', self)
        self.open_act.triggered.connect(Util.Launch)

        exit_act = QtWidgets.QAction('Exit', self)
        exit_act.triggered.connect(self.emu_thread.quit)
        exit_act.triggered.connect(QtWidgets.qApp.quit)

        """ self.save_act = QtWidgets.QAction('Save state', self)
        self.save_act.triggered.connect(self.core.sys8.SaveState)
        self.save_act.setEnabled(False)

        self.load_act = QtWidgets.QAction('Load state', self)
        self.load_act.triggered.connect(self.core.sys8.LoadState)
        self.load_act.setEnabled(False) """

        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        filemenu.addAction(self.open_act)
        filemenu.addAction(exit_act)
        """ emumenu = menubar.addMenu('Emulation')
        emumenu.addAction(self.save_act)
        emumenu.addAction(self.load_act) """

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

    @QtCore.pyqtSlot(list)
    def Draw(self, gfx):
        self.native.fill(QtCore.Qt.color1)
        for i in range(256):
            for j in range(224):
                if(gfx[i][j]):
                    self.painter.drawPoint(j, i)

        self.scaled.setPixmap(ui.native.scaled(672, 768))
        self.scaled.repaint()
        return


class Util():
    @staticmethod
    def HashRom(romname):
        with open(romname, 'rb') as rom:
            md5 = hashlib.new('md5')
            md5.update(rom.read())
            return(md5.hexdigest())

    @staticmethod
    def Launch():
        filepath = QtWidgets.QFileDialog.getOpenFileName(None, 'Open ROM', '', 'Space Invaders ROM (*.*)')
        if(filepath[0] != ''):
            ui.core.romname = filepath[0]
            ui.emu_thread.started.connect(ui.core.run)
            ui.emu_thread.start()


class EmuCore(QtCore.QObject):
    gfx_upl = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.romname = ''
        self.locked = False

    def run(self):
        i8080 = Intel8080(self.romname)
        interp = Interpreter()
        self.romhash = Util.HashRom(self.romname)

        ui.open_act.setEnabled(False)
        """ ui.save_act.setEnabled(True)
        ui.load_act.setEnabled(True) """

        self.gfx_upl.connect(ui.Draw, type=QtCore.Qt.BlockingQueuedConnection)
        # keyboard.hook(i8080.KeyAction)
        while(True):
            interp.ExecInstr(i8080)
            """ curr_ccl = 0
            while(curr_ccl < CYCLES_PER_FRAME):
                if(not self.locked):
                    interp.ExecInstri8080)
                    curr_ccl += 1
                    self.gfx_upl.emit(i8080.gfx) """


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
