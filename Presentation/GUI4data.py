import sys
import Presentation
import matplotlib
matplotlib.use('QtAgg')
import PySide6
from PySide6.QtCore import Qt, QSize, QObject, Property, QPropertyAnimation, Signal
from PySide6.QtGui import QMatrix4x4, QQuaternion, QVector3D, QColor, QFont
from PySide6.QtWidgets import *
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6 import QtDataVisualization
from PySide6.QtDataVisualization import *
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    window = Presentation.MainWindowGUI()

    window.show()
    app.exec()
