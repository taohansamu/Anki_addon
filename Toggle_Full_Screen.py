# -*- coding: utf-8 -*-
# Copyright: Jannick Dürolf; ported  from Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This plugin adds the ability to toggle full screen mode. It adds an item to
# the tools menu.
#

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from aqt import mw

def onFullScreen():
    mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)

a = QAction(mw)
a.setText("Toggle Full Screen")
a.setShortcut("F11")
mw.form.menuTools.addAction(a)
mw.connect(a, SIGNAL("triggered()"), onFullScreen)
