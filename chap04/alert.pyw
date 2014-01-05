import sys
import time
from pyQt4.QtCore import *
from pyQt4.QtGui import *

app = QApplication(sys.argv)

try:
  message = "Alert"
  if len(sys.argv) < 2:
    raise ValueError

  hours, mins = argv[1].split(':')
  due = QTime(int(hours), int(mins))
  if not due.isValid():
    raise ValueError

  if len(argv) > 2:
    message = " ".join(argv[2:])
except ValueError:
  message = "Usage: alert.pyw HH:MM [optional message]"

label = QLabel("<font color=red size=72><b>" + message + "</b></font>")
label.setWindowFlags(Qt.SplashScreen)
label.show()
QTimer.singleShot(60000, app.quit);
app.exec_()


