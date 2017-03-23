# Author: Calumks <calumks@gmail.com>

# Get Overview class
from aqt.overview import Overview

# Replace _table method
def table(self):
    cardsNew = self.mw.col.db.first("""
select
sum(case when queue=0 then 1 else 0 end) -- new
from cards where did in %s""" % self.mw.col.sched._deckLimit())
    
    cardsTotal = self.mw.col.db.first("""
select count(id) from cards
where did in %s """ % self.mw.col.sched._deckLimit())

    cardsTotalReviews = self.mw.col.db.scalar("""
select count() from cards where did in %s and queue > 0
and due < ?""" % self.mw.col.sched._deckLimit(), self.mw.col.sched.today+1)

    counts = list(self.mw.col.sched.counts())
    finished = not sum(counts)
    for n in range(len(counts)):
        if counts[n] == 1000:
            counts[n] = "1000+"
    but = self.mw.button
    if finished:
        return '<div style="white-space: pre-wrap;">%s</div>' % (
            self.mw.col.sched.finishedMsg())
    else:
        return '''
    <table width=300 cellpadding=5>
    <tr><td align=center valign=top>
    <table cellspacing=5>
    <tr><td>%s:</td><td><b><font color=#00a>%s</font> <font color=#a00>%s</font> <font color=#0a0>%s</font></b></td></tr>
    <tr><td>%s:</td><td align=right>%s</td></tr>
    <tr><td>%s:</td><td align=right>%s</td>
    <tr><td>%s:</td><td align=right>%s</font></td></tr></table>
    </td><td align=center>
    %s</td></tr></table>''' % (
    _("Due today"), counts[0], counts[1], counts[2],
    _("Total reviews"), cardsTotalReviews,
    _("Total new cards"), cardsNew[0],
    _("Total cards"), cardsTotal[0],
    but("study", _("Study Now"), id="study"))

Overview._table = table