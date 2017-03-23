"""
Title: Kanji Scramble, Define, Shuffle

Based on Kanji Decomposition and Sentence Shuffle & Gloss, which were modifications of:the Sentence Gloss Plugin:
    Original Author: overture2112
    Ported by: Kenishi

This plugin is provided as is without any additional support.
"""
# -*- coding: utf-8 -*-
import subprocess, re, urllib, urllib2, random

#### Get decomposition data
def url( term ): return 'http://nihongo.monash.edu/cgi-bin/wwwjdic?1ZRU%s' % urllib.quote( term.encode('utf-8') )
def gurl( term ): return 'http://nihongo.monash.edu/cgi-bin/wwwjdic?1ZMJ%s' % urllib.quote( term.encode('utf-8') )

def fetchDecomp( term ): return urllib.urlopen( url( term ) ).read()
def fetchkG( term ): return urllib.urlopen( gurl( term ) ).read()

def decomp( expr ):
        if type( expr ) != unicode: expr = unicode( expr )
        x = fetchDecomp( expr )
        if 'ERROR EXIT' in x:
                showInfo(_(x))
        u = unicode( x, 'utf-8', errors='ignore' )
        ls = re.findall('<pre>\n.\s(.*?)\n</pre>', u, re.UNICODE)
        ls = ls[0].split(' ')
        rd = {u'\u5316': u'\u2E85', u'\u827E': u'\u2EBE', u'\u5208': u'\u2E89', u'\u8FBC': u'\u2ECC', u'\u521D': u'\u8864', u'\u5C1A': u'\u2E8C', u'\u8CB7': u'\u7F52', u'\u72AF': u'\u72AD',   u'\u5FD9': u'\u5FC4', u'\u793C': u'\u793B',  u'\u4E2A': u'\uD840\uDDA2', u'\u8001': u'\u2EB9', u'\u624E': u'\u624C', u'\u6770': u'\u706C', u'\u7594': u'\u7592', u'\u79B9': u'\u79B8', u'\u90A6': u'\u2ECF', u'\u9621': u'\u2ED6', u'\u6C41': u'\u6C35'}
        ls = [rd[i] if i in rd else i for i in ls]
        return ' '.join( ls )
        
def kanjiGloss( expr ):
        if type( expr ) != unicode: expr = unicode( expr )
        x = fetchkG( expr )
        if 'ERROR EXIT' in x:
                showInfo(_(x))
        u = unicode( x, 'utf-8', errors='ignore' )
        ls = re.findall(u'([\u4e00-\u9fa5]).*(?<!\}\s)(\{.*\s+\n)', u, re.UNICODE) 
        ls = [x + ': ' + y for x, y in ls]
        for i in ls:
            ik = re.findall(u'([\u4e00-\u9fa5])', u, re.UNICODE)
            id = decomp(ls[0][0])
            for j in range(len(ls)):
                ls[j] = i.replace(ls[0][0], id, 1)
        return u'<br/>\n'.join( ls )

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from anki.notes import Note
from anki.utils import stripHTML
from aqt import mw
from aqt.utils import showText, showInfo

#### Update note with decomposition 
   
def kSG( f ):
   if f['KSG']: return
   fc = re.findall(u'([\u4e00-\u9fa5])', f['Expression'], re.UNICODE)
   random.shuffle(fc)
   fcs = ''.join(fc)
   for i in range(len(fcs)):
        f[ 'KSG' ] += '<li> ' + kanjiGloss( fcs[i] ) + '<br/></li>'

def setupMenu( ed ):
	a = QAction( 'Generate decompGloss', ed )
	ed.connect( a, SIGNAL('triggered()'), lambda e=ed: onRegenDecomp( e ) )
	ed.form.menuEdit.addSeparator()
	ed.form.menuEdit.addAction( a )

def onRegenDecomp( ed ):
	n = "Generate decompGloss"
	ed.editor.saveNow()
	regenDecomp(ed, ed.selectedNotes() )   
	mw.requireReset()

def refreshSession():
	mw.col.s.flush()
	
def regenDecomp( ed, fids ):
	mw.progress.start( max=len( fids ) , immediate=True)
	for (i,fid) in enumerate( fids ):
		mw.progress.update( label='Generating decompGloss... ', value=i )
		f = mw.col.getNote(id=fid)
		try: kSG( f )
		except:
			import traceback
			print 'decompGloss failed: '
			if '_fieldOrd' in traceback.format_exc():
                                showInfo(_('Check your field names.'))
                                break
			traceback.print_exc()
		try: f.flush()
		except:
			raise Exception()
		ed.onRowChanged(f,f)
	mw.progress.finish()
	

addHook( 'browser.setupMenus', setupMenu )
