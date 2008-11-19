#----------------------------------------------------------------------------
# Name:         MyNotepad.py
# Purpose:      A simple notepad
#
# Author:       Zhe Wang
#
# Created:      09/25/2008
# Copyright:    (c) 2008 Zhe Wang
# License:      GNU General Public License v2
#----------------------------------------------------------------------------

import wx  
from wx.lib.wordwrap import wordwrap  
import wx.richtext as rt  
import os, sys

class MyNotepad(wx.Frame):
    
    current_filename = ''
    content_edited = False
    text = wx.TextCtrl

    #--------------------------------------
    # On Initialize
    #--------------------------------------

    def __init__(self, parent, id, title, size=(600, 600)):

		wx.Frame.__init__(self, parent, id, title, size=(600,600))

		#Create text area here
		edit_area = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
		self.text = edit_area
		wx.CallAfter(self.text.SetFocus)
		
		#Create status bar here
		self.CreateStatusBar()
		self.SetStatusText('Ready')

		#Create menu here
		menubar = wx.MenuBar(wx.MB_DOCKABLE)

		#Create menus here
		#Menu File:
		menu_File = wx.Menu()

		ID_FILE_NEW = wx.NewId()
		ID_FILE_OPEN = wx.NewId()
		ID_FILE_SAVE = wx.NewId()
		ID_FILE_SAVE_AS = wx.NewId()
		ID_APP_EXIT = wx.NewId()

		menu_File.Append(ID_FILE_NEW, "&New\tCtrl+N", "Create a new document")
		menu_File.Append(ID_FILE_OPEN, "&Open...\tCtrl+O", "Open an existing document")
		menu_File.Append(ID_FILE_SAVE, "&Save\tCtrl+S", "Save the active document")
		menu_File.Append(ID_FILE_SAVE_AS, "Save &As...", "Save the active document with a new name")
		menu_File.AppendSeparator()
		menu_File.Append(ID_APP_EXIT, "E&xit", "Quit the application")

		self.Bind(wx.EVT_MENU, self.OnFileNew, id=ID_FILE_NEW)
		self.Bind(wx.EVT_MENU, self.OnFileOpen, id=ID_FILE_OPEN)
		self.Bind(wx.EVT_MENU, self.OnFileSave, id=ID_FILE_SAVE)
		self.Bind(wx.EVT_MENU, self.OnFileSaveAs, id=ID_FILE_SAVE_AS)
		self.Bind(wx.EVT_MENU, self.OnAppExit, id=ID_APP_EXIT)
		
		menubar.Append(menu_File, '&File')

		#Menu Edit:
		menu_Edit = wx.Menu()

		ID_EDIT_UNDO = wx.NewId()
		ID_EDIT_CUT = wx.NewId()
		ID_EDIT_COPY = wx.NewId()
		ID_EDIT_PASTE = wx.NewId()	
		ID_EDIT_DELETE = wx.NewId()
		ID_EDIT_SELECT_ALL = wx.NewId()
		
		menu_Edit.Append(ID_EDIT_UNDO, "&Undo\tCtrl+Z", "Undo")
		menu_Edit.AppendSeparator()
		menu_Edit.Append(ID_EDIT_CUT, "Cu&t\tCtrl+X", "Cut the selection and put it on the Clipboard")
		menu_Edit.Append(ID_EDIT_COPY, "&Copy\tCtrl+C", "Copy the selection and put it on the Clipboard")
		menu_Edit.Append(ID_EDIT_PASTE, "&Paste\tCtrl+V", "Insert Clipboard contents")
		menu_Edit.Append(ID_EDIT_DELETE, "&Delete\tDel", "Delete the selection")
		menu_Edit.AppendSeparator()
		menu_Edit.Append(ID_EDIT_SELECT_ALL, "Select &All\tCtrl+A", "Select all contents")
		
		self.Bind(wx.EVT_MENU, self.OnEditUndo, id=ID_EDIT_UNDO)
		self.Bind(wx.EVT_MENU, self.OnEditCut, id=ID_EDIT_CUT)
		self.Bind(wx.EVT_MENU, self.OnEditCopy, id=ID_EDIT_COPY)
		self.Bind(wx.EVT_MENU, self.OnEditPaste, id=ID_EDIT_PASTE)
		self.Bind(wx.EVT_MENU, self.OnEditDelete, id=ID_EDIT_DELETE)
		self.Bind(wx.EVT_MENU, self.OnEditSelectAll, id=ID_EDIT_SELECT_ALL)
		
		menubar.Append(menu_Edit, '&Edit')

		#Menu Help:
		menu_Help = wx.Menu()

		ID_APP_ABOUT = wx.NewId()
		
		menu_Help.Append(ID_APP_ABOUT, "&About My Notepad", "My Notepad Information")
		
		self.Bind(wx.EVT_MENU, self.OnAppAbout, id=ID_APP_ABOUT)
		
		menubar.Append(menu_Help, '&Help')
		
		#Set menu bar here
		self.SetMenuBar(menubar)

		artBmp = wx.ArtProvider.GetBitmap
		tsize = (15,15)
		
		self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
		self.toolbar.AddSimpleTool(ID_FILE_NEW, artBmp(wx.ART_NEW, wx.ART_TOOLBAR, tsize), "New")
		self.toolbar.AddSimpleTool(ID_FILE_OPEN, artBmp(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize), "Open")
		self.toolbar.AddSimpleTool(ID_FILE_SAVE, artBmp(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize), "Save")
		self.toolbar.AddSimpleTool(ID_FILE_SAVE_AS, artBmp(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize), "Save as...")
		self.toolbar.AddSeparator()
		
		self.toolbar.AddSimpleTool(ID_EDIT_CUT, artBmp(wx.ART_CUT, wx.ART_TOOLBAR, tsize), "Cut")
		self.toolbar.AddSimpleTool(ID_EDIT_COPY, artBmp(wx.ART_COPY, wx.ART_TOOLBAR, tsize), "Copy")
		self.toolbar.AddSimpleTool(ID_EDIT_PASTE, artBmp(wx.ART_PASTE, wx.ART_TOOLBAR, tsize), "Paste")
		self.toolbar.AddSeparator()

		self.toolbar.AddSimpleTool(ID_EDIT_UNDO, artBmp(wx.ART_UNDO, wx.ART_TOOLBAR, tsize), "Undo")
		
		self.toolbar.Realize()

    #--------------------------------------
    # File Menu Event Handlers
    #--------------------------------------

    #Create a new file
    def OnFileNew(self, event):
        
        result = ''
        
        #if current content is changed, prompt for saving
        if self.content_edited == True:
            dlg = wx.MessageDialog(self, "The text in the file has changed.\nDo you want to save the changes?", "My Notepad", wx.YES_NO | wx.CANCEL)
            result = dlg.ShowModal()

            if result == wx.ID_CANCEL:
                return True

            if result == wx.ID_YES:	
		result = self.OnFileSave(event)
		if result == wx.ID_CANCEL:
			return False;

        self.text.SetValue('')
        self.current_filename = ''
        self.content_edited = True

    #Open an existing file
    def OnFileOpen(self, event):
        dlg = wx.FileDialog(self, message="Open", defaultDir=os.getcwd(), defaultFile="", wildcard="Text Document(*.txt)|*.txt|All files (*.*)|*.*", style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)  
        if dlg.ShowModal() == wx.ID_OK:  
            path = dlg.GetPath()
            if path: 
                self.current_filename = path  
                self.text.LoadFile(self.current_filename, rt.RICHTEXT_TYPE_TEXT)  
                self.content_edited = True
        dlg.Destroy()

    #Save current file
    def OnFileSave(self, event):

        current_text = self.text.GetValue()
        
        #If not an opened file, prompt for filename
        if self.current_filename:
            fp = open(self.current_filename, 'w')
            fp.write(current_text)
            fp.close()
            
            self.content_edited = False
        else:
            dlg = wx.FileDialog(self, message="Save As", defaultDir=os.getcwd(), defaultFile="", wildcard="Text Document(*.txt)|*.txt|All files (*.*)|*.*", style=wx.SAVE)

            if dlg.ShowModal() == wx.ID_OK:
                self.current_filename = dlg.GetPath()
	        
	        fp = open(self.current_filename, 'w')
        	fp.write(current_text)
            	fp.close()
                
                self.content_edited = False
            else:
            	return wx.ID_CANCEL;


    #Save current file as another name
    def OnFileSaveAs(self, event):
        current_text = self.text.GetValue()
        
        dlg = wx.FileDialog(self, message="Save As", defaultDir=os.getcwd(), defaultFile="", wildcard="Text Document(*.txt)|*.txt|All files (*.*)|*.*", style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
        	self.current_filename = dlg.GetPath()
	        
		fp = open(self.current_filename, 'w')
        	fp.write(current_text)
        	fp.close()
                
        	self.content_edited = False

    #Quit
    def OnAppExit(self, event):
        
        #if current content is changed, prompt for saving
        if self.content_edited == True:
            dlg = wx.MessageDialog(self, "The text in the file has changed.\nDo you want to save the changes?", "My Notepad", wx.YES_NO | wx.CANCEL)
            result = dlg.ShowModal()

            if result == wx.ID_CANCEL:
                return True

            if result == wx.ID_YES:	
		result = self.OnFileSave(event)
		if result == wx.ID_CANCEL:
			return False;
			
        self.Close(True)\

    #--------------------------------------
    # Edit Menu Event Handlers
    #--------------------------------------

    #Undo
    def OnEditUndo(self, event):
    	self.text.Undo()
    	self.content_edited = True

    #Cut selection to clipboard
    def OnEditCut(self, event):
    	self.text.Cut()
    	self.content_edited = True

    #Copy selection to clipboard
    def OnEditCopy(self, event):
    	self.text.Copy()
    	self.content_edited = True

    #Paste from clipboard
    def OnEditPaste(self, event):
    	self.text.Paste()
    	self.content_edited = True

    #Delete selection
    def OnEditDelete(self, event):
	start, end = self.text.GetSelection()
        self.text.Remove(start, end)
        self.content_edited = True
 
    #Select all
    def OnEditSelectAll(self, event):
        self.text.SelectAll()


    #--------------------------------------
    # Help Menu Event Handlers
    #--------------------------------------
    
    #About information
    def OnAppAbout(self, event):
        dialog = wx.AboutDialogInfo()
        dialog.Name = "My Notepad"
        dialog.Version = "1.0.0"
        dialog.Description = "A simple notepad. "
        dialog.Developers = ["Zhe Wang"]
        wx.AboutBox(dialog)

class RunApp(wx.App):  
    def OnInit(self):  
        win = MyNotepad(None, 1, 'My Notepad')  
        self.SetTopWindow(win)  
        win.Show(True)  
        return True
          
if __name__ == '__main__':  
    RunApp().MainLoop()