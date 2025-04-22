import sys
from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab
from translateText import frame_ocr


class SnipWidget(QtWidgets.QWidget):
    snip_done = QtCore.Signal(object)
    def __init__(self, screen_geometry, scale_factor, overlays):
        super().__init__()
        self.screen_geometry = screen_geometry
        self.scale_factor = scale_factor
        self.overlays = overlays
        self.begin = self.end = QtCore.QPoint()

        self.setGeometry(self.screen_geometry)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.showFullScreen()

    # ----- drawing -----
    def paintEvent(self, _):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRectF(self.begin, self.end))

    # ----- mouse handling -----
    def mousePressEvent(self, e):
        self.begin = self.end = e.position().toPoint()
        self.update()

    def mouseMoveEvent(self, e):
        self.end = e.position().toPoint()
        self.update()

    def mouseReleaseEvent(self, _):
        # compute physical‐pixel bbox
        x1 = min(self.begin.x(), self.end.x()) * self.scale_factor + self.screen_geometry.x()
        y1 = min(self.begin.y(), self.end.y()) * self.scale_factor + self.screen_geometry.y()
        x2 = max(self.begin.x(), self.end.x()) * self.scale_factor + self.screen_geometry.x()
        y2 = max(self.begin.y(), self.end.y()) * self.scale_factor + self.screen_geometry.y()

        for w in self.overlays:
            w.hide()
        QtWidgets.QApplication.processEvents()

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)
        self.snip_done.emit(img)

def snip_once(save_to: Path | str | None = None):
    app = QtWidgets.QApplication.instance()
    owns_app = app is None
    if owns_app:
        app = QtWidgets.QApplication(sys.argv)

    captured = {"img": None}
    loop = QtCore.QEventLoop()

    def on_done(img):
        captured["img"] = img
        QtWidgets.QApplication.restoreOverrideCursor()
        loop.quit()

    # build overlays
    overlays = []
    for screen in app.screens():
        w = SnipWidget(screen.geometry(), screen.devicePixelRatio(), overlays)
        overlays.append(w)
    for w in overlays:
        w.snip_done.connect(on_done)

    loop.exec()

    for w in overlays:
        w.close()

    img = captured["img"]
    if save_to:
        img.save(str(save_to))

    frame_ocr(save_to)

