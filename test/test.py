import unittest, wx

import os, sys
import MyNotepad

class MN_DefaultSizeTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		assert mn_win.GetSize() == (600, 600), 'Default Size 600x600 does NOT work normally'

class MN_TextCtrlTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.text.SetValue('TEXT CTRL TEST')
		assert mn_win.text.GetValue() == 'TEXT CTRL TEST', 'Text Ctrl does NOT work normally'

class MN_NewFileTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.OnFileNew(mn_win)
		assert mn_win.text.GetValue() == '', 'Create New File does NOT work normally'
		assert mn_win.current_filename == '', 'Create New File does NOT work normally'
 
class MN_SaveFileTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.text.SetValue('TEST SAVE FILE')
		mn_win.current_filename = './testsave.txt'
		mn_win.OnFileSave(mn_win)
		assert os.path.isfile(mn_win.current_filename), 'Save File does NOT work normally'

		fp = open(mn_win.current_filename, 'r')
        	filecontent = fp.read()
        	fp.close()
		
		assert filecontent == mn_win.text.GetValue(), 'Save File does NOT work normally'
		assert mn_win.content_edited == False, 'Save File does NOT work normally'

class MN_OpenFileTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		result = mn_win.text.LoadFile('./testopen.txt', wx.richtext.RICHTEXT_TYPE_TEXT)
		assert result != 0, 'Open File does NOT work normally'
		assert mn_win.text.GetValue() == 'TEST OPEN FILE', 'Open File does NOT work normally'

class MN_SelectAllTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.text.SetValue('TEST SELECT ALL')
		mn_win.OnEditSelectAll(mn_win)
		start, end = mn_win.text.GetSelection()
		assert mn_win.text.GetValue()[start:end] == mn_win.text.GetValue(), 'Select All does NOT work normally'

class MN_DeleteSelectionTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.text.SetValue('TEST DELETE')
		mn_win.OnEditSelectAll(mn_win)
		mn_win.OnEditDelete(mn_win)
		assert mn_win.text.GetValue() == '', 'Delete selection does NOT work normally'

class MN_CopySelectionTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.text.SetValue('TEST COPY')
		mn_win.OnEditSelectAll(mn_win)
		mn_win.OnEditCopy(mn_win)
		data = wx.TextDataObject()
		if wx.TheClipboard.Open():
		            success = wx.TheClipboard.GetData(data)
		            wx.TheClipboard.Close()

		assert mn_win.text.GetValue() == data.GetText(), 'Copy selection does NOT work normally'
		
class MN_PasteTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		data = wx.TextDataObject()
		data.SetText('TEST PASTE')
		if wx.TheClipboard.Open():
		            success = wx.TheClipboard.SetData(data)
		            wx.TheClipboard.Close()

		mn_win.OnEditPaste(mn_win)
		assert mn_win.text.GetValue() == data.GetText(), 'Paste does NOT work normally'

class MN_CutSelectionTest(unittest.TestCase):
	def runTest(self):
		app = wx.App(0)
		frame = wx.Frame(None)
		mn_win = MyNotepad.MyNotepad(None, 1, 'My Notepad')
		mn_win.text.SetValue('TEST CUT')
		mn_win.OnEditSelectAll(mn_win)
		mn_win.OnEditCut(mn_win)
		data = wx.TextDataObject()
		if wx.TheClipboard.Open():
		            success = wx.TheClipboard.GetData(data)
		            wx.TheClipboard.Close()

		assert mn_win.text.GetValue() == '' and data.GetText() == 'TEST CUT', 'CUT selection does NOT work normally'
		
if __name__ == '__main__':
	unittest.main()