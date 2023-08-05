"""
AUI modified aui libary version and addon bits

AUIFrame - a frame class to easily add some aui related functionally:
    - add toolbars complete with a menu checkitem   
    - save and load layouts complete with menu checkitems

AuiToolBar_Label_mixin
"""

import pickle
import wx

#switch aui libary
USE_AGW = True
if USE_AGW:
    import wx.lib.agw.aui as aui
else:
    import wx.aui as aui

#from . import toolstrip as ts


#---Layout class----------------------------------------------------------------
class Layout():
    def __init__(self,parent,menu,
                    name="",pos=(-1,-1),size=(800,600),max=False,layout="",
                    data=None):
        """
        Create a new aui window (=parent) layout .
        Adds a checkitem in menu if not None.

        Create from values:
            name    = layout name string,
            pos     = frame position tuple,
            size    = frame size tuple,
            max     = frame maximised boolean,
            layout  = aui layout string 

        Create from a pickled string generated from GetSaveString, if data is
        not None
        """
        #references to the parent frame and menu to use
        self.parent = parent
        self.menu = menu 
        self.menuitem = None

        if data==None:
            #store info
            self.name = name
            self.pos  = pos
            self.size = size
            self.max  = max
            self.layout = str(layout)
        else:
            self.LoadString(data)

        #Add a menu item
        if menu!=None:
            self.AddMenuItem(menu)

    def Apply(self):
        """Apply these settings to the parent frame"""
        #only set size/position if not maximising
        if (self.max is False):
            #set size and position
            self.parent.SetSize(self.size)
            self.parent.SetPosition(self.pos)
        elif (self.parent.IsMaximized() is False):
            self.parent.Maximize()

        #load aui layout
        try:
            if self.layout!="":
                self.parent.auimgr.LoadPerspective(self.layout)
        except:
            pass

    def SaveCurrentState(self):
        """Saves the current state of the console frame to this layout"""
        #store maximised state - but not iconised!
        self.max = self.parent.IsMaximized()
        iconized = self.parent.IsIconized()

        #store size and position
        if (self.max is True) or (iconized is True):
            self.size = (800,600)#use default size
            self.pos  = (-1,-1)  #use default pos
        else:
            self.size = self.parent.GetSize()
            self.pos = self.parent.GetScreenPosition()

        #aui layout
        self.layout = self.parent.auimgr.SavePerspective()

    def AddMenuItem(self,menu):
        """Add a menu item to menu to load this layout"""
        id = wx.NewId()  
        self.menuitem = wx.MenuItem(menu, id ,self.name,"Load this layout")
        menu.Append(self.menuitem)
        self.parent.Bind(wx.EVT_MENU,lambda event: self.Apply(), self.menuitem)

    def Rename(self,new):
        """Renames the layout and alters the asociated menu item"""
        #make sure name is a string
        self.name = new
        #find and change the menu item
        if self.menuitem is not None:
            self.menuitem.SetItemLabel(self.name)   

    def RemoveMenuItem(self):
        """Removes this layouts menu """
        if self.menuitem is not None:
            self.menu.RemoveItem(self.menuitem) 
            self.menuitem.Destroy()
            self.menuitem = None

    def GetSaveString(self):
        """Returns a save string for writing to the config"""
        data = (self.name,self.pos,self.size,self.max,self.layout)
        s = str(pickle.dumps(data)) #make a python3 string not bytes
        return s

    def LoadString(self,data):
        """Load settings from a save string"""
        data = eval(data) #convert from "b'xxxxxx'" string to bytes object
        self.name,self.pos,self.size,self.max,self.layout  = pickle.loads(data) 

#---Mixin class-----------------------------------------------------------------
class AUIFrame(wx.Frame):
    def __init__(self,parent,id,title,size,pos):
        """
        Add aui with support for
            - add toolbars complete with a menu checkitem   
            - save and load layouts complete with menu checkitems
        """
        wx.Frame.__init__(self, parent, id, title, size=size,pos=pos)

        #initalise an aui manager
        self.auimgr = aui.AuiManager()
        if USE_AGW:
            self.auimgr.SetAGWFlags( aui.AUI_MGR_DEFAULT |aui.AUI_MGR_AERO_DOCKING_GUIDES| aui.AUI_MGR_ALLOW_ACTIVE_PANE| wx.aui.AUI_MGR_LIVE_RESIZE)
        self.auimgr.SetManagedWindow(self)

        #list of layout objects
        self._layouts = []
        self.path = None #save path
        self.laymenu = None #menu for checkitems

        #Menu for toolbar checkitems
        self.toolsmenu = None
    
        #Menu for pane checkitems
        self.panesmenu = None

    def Destroy(self):
        """Overload to call unit on auimanager"""
        self.auimgr.UnInit()
        return wx.Frame.Destroy(self)

    #---Layouts Interface-------------------------------------------------------
    def AddLayout(self,layout=None,name="New layout"):
        """
        Save a new layout:
            If layout is None a new layout is created using the name and the
            current settings
            If menu is given a checkitem will be added to the menu
        """
        if layout is None:
            layout = Layout(self,name=name,menu=self.laymenu)
            layout.SaveCurrentState()
        self._layouts.append(layout)

    def RemoveLayout(self,n):
        """Remove the nth saved layout (including from any menus)"""
        layout = self._layouts.pop(n)
        layout.RemoveMenuItem()
        del layout

    def RenameLayout(self,n,newname):
        """Rename the nth saved layout (including from any menus)"""
        #make sure name is a string
        newname = str(newname)
        layout = self._layouts[n]
        layout.Rename(newname)

    def SetSavePath(self,path):
        """Set the save path in the wxconfig object"""
        self.path = path

    def SetLayoutsMenu(self,menu):
        """Set the menu to add layout checkitems to"""
        self.laymenu = menu
        id =wx.NewId()
        self.laymenu.Append(id,'Save Layout','Save the window layout')
        self.Bind(wx.EVT_MENU, self.OnSaveLayout, id=id)
        id =wx.NewId()
        self.laymenu.Append(id,'Rename Layout','Rename a saved window layout')
        self.Bind(wx.EVT_MENU, self.OnRenameLayout, id=id)
        id =wx.NewId()
        self.laymenu.Append(id,'Delete Layout','Delete a saved window layout')
        self.Bind(wx.EVT_MENU, self.OnDeleteLayout, id=id)
        self.laymenu.AppendSeparator()

    def SaveLayouts(self):
        """
        Save the layouts to the path (set via SetSavePath) in the wxconfig 
        object
        """
        #check save/load path is set
        if self.path is None:
            return
        #Get the config object
        cfg = wx.GetApp().GetConfig()

        #save the current layout
        cur = Layout(self,menu=None,data=None,name='last')
        cur.SaveCurrentState()
        s = cur.GetSaveString()
        cfg.Write(self.path+"//current_layout",s)

        #delete any old saved layouts 
        cfg.DeleteGroup(self.path+"//layouts")
        #save the other layouts
        n=0
        for layout in self._layouts:
            s = layout.GetSaveString()
            cfg.Write(self.path+"//layouts//saved"+str(n),s)
            n = n+1
        cfg.Flush()

    def LoadLayouts(self):
        """
        Loads the layouts from the path (set via SetSavePath) in the wxconfig 
        object. Adds checkitems into menu set via SetLayoutsMenu
        """
        #check save/load path is set
        if self.path is None:
            return
        #Get the config object
        cfg = wx.GetApp().GetConfig()
        
        #load the saved layouts
        cfg.SetPath(self.path+"//layouts//")
        num = cfg.GetNumberOfEntries()
        for n in range(0,num):
            s = cfg.Read("saved"+str(n),"")
            if s!="":
                layout = Layout(self,menu=self.laymenu,data=s)
                self.AddLayout(layout)

        #load the current layout
        cfg.SetPath("")
        s = cfg.Read(self.path+"//current_layout","")
        if s!="":
            cur = Layout(self,menu=None,data=s)
            cur.Apply() #apply this layout
            #fix for maximise bug  - force the window to refresh the status bar position
            if cur.max is True:
               self.Maximize()
               self.SetPosition(cur.pos)
               self.SetSize(cur.size)

    #---Toolbars interfaces-----------------------------------------------------
    def SetToolbarsMenu(self,menu):
        """Set the toolbars menu to use"""
        self.toolsmenu = menu

    def AddToolbar(self, tb, tbname, pane=None, helpstring=None):
        """
        Add a toolbar to the frame complete with entry in the menu set
        via SetToolbarsMenu.

        Pass a toolbar and string for the name and an aui pane info with the 
        desired settings (or None for default settings), helpstring is the menu 
        item tip, use none for defualt.
        """
        #defualt pane settings
        if pane is None:
            pane = (aui.AuiPaneInfo().Name(tbname)
                    .Caption(tbname).ToolbarPane().CloseButton(True)
                    .CaptionVisible(False).DestroyOnClose(False).Top()
                    .LeftDockable(False).RightDockable(False))
        #check name and DestroyOnClose
        pane.Name(tbname)
        pane.DestroyOnClose(False)

        #add to the window using aui manager
        self.auimgr.AddPane(tb,pane)
        self.auimgr.Update()

        #check help string
        if helpstring is None:
            helpstring = 'Show/Hide the '+tbname+' toolbar'

        #add a tick item to the view>toolbars menu
        id = wx.NewId()
        item = wx.MenuItem(self.toolsmenu, id ,tbname,helpstring,wx.ITEM_CHECK)
        self.toolsmenu.Append(item)
        item.Check(True) #tick it

        #Bind events to handle the tick/unticking and show/hiding
        self.Bind(wx.EVT_MENU,self.OnToolsMenu,item)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateToolsMenu,item)

    #---panes interface---------------------------------------------------------
    def SetPanesMenu(self,menu):
        """Set the menu to use for displaying/hiding panes"""
        self.panesmenu = menu

    def AddPane( self, ctrl, pane, bitmap=None ):
        """Add a pane to the frame complete with entry in the menu set
        via SetPanesMenu.

        Pass the ctrl, a AuiPaneInfo obecjt with the desired settings. The pane
        name will be displayed in the view=>panes menu together with an optional
        bitmap.
        
        Returns a valid AuiPaneInfo for the pane (the one supplied will not be
        valid after it has been added!)
        """
        if self.panesmenu is None:
            raise Exception('No panes menu set')

        #add the pane to the aui manager
        self.auimgr.AddPane(ctrl, pane) 

        #add a menu entry to the panes menu
        helpstring='Show/Hide the '+pane.name+' pane'
        
        item = wx.MenuItem(self.panesmenu, -1, pane.name, 
                            helpstring, wx.ITEM_CHECK)

        #Bind events to handle the tick/unticking and show/hiding
        self.Bind(wx.EVT_MENU, self.OnPanesMenu, item)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdatePanesMenu, item)

        #set the bitmap
        if bitmap is not None:
            item.SetBitmap(bitmap)

        self.panesmenu.Append(item)

        return self.auimgr.GetPane(pane.name)

    #---event handlers----------------------------------------------------------
    def OnToolsMenu(self, event):
        """show hide a menubar"""
        id = event.GetId()
        item = self.toolsmenu.FindItemById(id)
        name = item.GetLabel()
        pane = self.auimgr.GetPane(name)
        if event.IsChecked() is True:
            pane.Show()
            wx.CallAfter(self.auimgr.Update)
        else:
            pane.Hide()
            wx.CallAfter(self.auimgr.Update)

    def OnUpdateToolsMenu(self, event):
        """check the tick state of the menu items"""
        #check the state of each toolbar in turn
        id = event.GetId()
        item = self.toolsmenu.FindItemById(id)
        name = item.GetItemLabel()
        pane = self.auimgr.GetPane(name)
        event.Check( pane.IsShown() )

    def OnPanesMenu(self, event):
        """Show/hide a pane"""
        id = event.GetId()
        item = self.panesmenu.FindItemById(id)
        name = item.GetItemLabel()
        pane = self.auimgr.GetPane(name)
        if event.IsChecked() is True:
            pane.Show()
            self.auimgr.Update()
        else:
            pane.Hide()
            self.auimgr.Update()

    def OnUpdatePanesMenu(self, event):
        """check the tick state of the menu items"""
        #check the state of each toolbar in turn
        id = event.GetId()
        item = self.panesmenu.FindItemById(id)
        name = item.GetItemLabel()
        pane = self.auimgr.GetPane(name)
        event.Check( pane.IsShown() )

    def OnSaveLayout(self,event):
        """Handles saving of an aui layout"""
        dlg = wx.TextEntryDialog(self, "Enter a name for the new layout:", "Python toolkit")
        dlg.SetValue(("New layout %d")%(len(self._layouts)+1))

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            self.AddLayout(name=name)
    
    def OnRenameLayout(self,event):
        """Handles renaming of an aui layout"""
        #get layout to change
        names = []
        for x in self._layouts:
            names.append(x.name)
        dlg = wx.SingleChoiceDialog(
                self, 'Select layout to rename:', 'Rename layout',
                names, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        
        n = dlg.GetSelection()
        dlg.Destroy()

        #get new name
        dlg = wx.TextEntryDialog(self, 'Enter new name:','Rename layout', 
                    self._layouts[n].name)
        if dlg.ShowModal() == wx.ID_OK:
            new = dlg.GetValue()
            self.RenameLayout(n,new)
        dlg.Destroy()

    def OnDeleteLayout(self,event):
        """Handles deleting an aui layout"""
        #get layout to delete
        names = []
        for x in self._layouts:
            names.append(x.name)
        dlg = wx.SingleChoiceDialog(
                self, 'Select layout to remove:', 'Remove layout',
                names, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            n = dlg.GetSelection()
            self.RemoveLayout(n)
        dlg.Destroy()
#-------------------------------------------------------------------------------
class ToolbarStaticText(wx.Control):
    """
    A static text control with the gradient background of the AuiToolbar class
    """
    def __init__(self, parent, id, text):
        wx.Control.__init__(self, parent, id, style=wx.BORDER_NONE)

        self.text = text
        w,h = self.GetTextExtent(self.text)
        pw,ph = self.Parent.GetSize()
        self.SetMinSize( (w, ph ))
       
        self.SetBackgroundColour(parent.GetBackgroundColour());
        self.SetForegroundColour(parent.GetForegroundColour());
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Parent.Bind(wx.EVT_SIZE, self.OnParentSize)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        #draw background
        wnd = self.Parent
        w, h = self.GetSize()
        rect = wx.Rect(0,0,w,h)
        tbart = self.Parent.GetArtProvider()
        tbart.DrawBackground(dc, self, rect)
        #draw text
        dc.SetFont(self.GetFont());
        tw,th = self.GetTextExtent(self.text)
        x = (w-tw)/2
        y = (h-th)/2
        dc.DrawText(self.text, x, y);

    def OnSize(self, event):
        self.Refresh()
        
    def OnParentSize(self, event):
        pw,ph = self.Parent.GetSize()
        w,h = self.GetTextExtent(self.text)
        self.SetMinSize( (w, ph) )
        event.Skip()
 
#-------------------------------------------------------------------------------
class AuiToolBar_Label_mixin():
    def AddStaticLabel(self, label):
        """
        Add a static text with the correct background
        """
        
        text = ToolbarStaticText(self, wx.ID_ANY , label)
        return self.AddControl(text)

#---Mixin class-----------------------------------------------------------------
class AUIToolStripFrame(wx.Frame):
    def __init__(self,parent,id,title,size,pos):
        """
        Add aui with support for
            - easily add keyboard shortcuts as no menu bar to handle now.
            - creates ToolStip and adds views pane for tools to add to.
            - save and load layouts complete with menu checkitems
        """
        wx.Frame.__init__(self, parent, id, title, size=size,pos=pos)

        ##Hotkeys/accelerator keys
        # - need to be done here now as there is no menubar to handle then 
        #   automatically
        # - use a list of accelerators to store accelerators and allow new ones 
        #   to be added by tools using AddAcceleratorKey/AddAcceleratorList
        self._acc_keys = [] 

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        ##create Toolstrip
        self.CreateToolStrip()

        ##Setup the aui manager parts
        self._auiPanel = wx.Panel(self ,-1) #panel - this is the part managed by the aui manager.
        sizer.Add(self._auiPanel, 1, wx.EXPAND)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        self._auiPanel.SetSizer(psizer)
        self.auimgr = aui.AuiManager()
        if USE_AGW:
            self.auimgr.SetAGWFlags( aui.AUI_MGR_DEFAULT | aui.AUI_MGR_AUTONB_NO_CAPTION |
                                    aui.AUI_MGR_AERO_DOCKING_GUIDES| aui.AUI_MGR_ALLOW_ACTIVE_PANE)
        self.auimgr.SetManagedWindow(self._auiPanel)
    
        #get pane close events to update view tab entries
        self._pane_tools = {} # pane caption:tool mapping
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)

        #list of layout objects
        self._layouts = []
        self.path = None #save path


    def CreateToolStrip(self):
        """
        Init method used to create ToolStrip - overloaded in console/editor frame.
        """
        self.ToolStrip =  ts.ToolStrip(self,-1)
        self.ToolStrip.SetStatusBar(self.StatusBar)
        self.Sizer.Add(self.ToolStrip, 0, wx.EXPAND)
    
    # Handle keypresses    
    def AddAcceleratorKey(self, flags, keycode, id):
        """
        Add an accelerator key/keyboard shortcut to the main window.
        See wx.AcceleratorTable for details.
        Use EVT_MENU bindings to event handler.
        """
        self._acc_keys.append( (flags, keycode, id))
        self.SetAcceleratorTable( wx.AcceleratorTable(self._acc_keys)  )
        
    def AddAcceleratorList( self, accelerators):
        """
        Add a list of accelerator keys/keyboard shortcurs to the main window.
        Where accelerators is a list of (flags, keycode, id) tuples.
        See wx.AcceleratorTable for details.
        Use EVT_MENU bindings to event handler.
        """
        self._acc_keys = self._acc_keys + accelerators
        self.SetAcceleratorTable( wx.AcceleratorTable(self._acc_keys)  )
    

    # Add a tool pane including view toggle button 
    def AddToolPane( self, ctrl, pane,  bitmap, label, longHelp='' ):
        """
        Add a pane to the frame complete with entry in the "View" toolstrip page.

        ctrl - the control to add
        pane - a AuiPaneInfo object with the desired settings
        bitmap - bitmap for Tool button on View page of toolstrip.
        label - label for pane and button
        longHelp - help string
        
        """
        #add the pane to the aui manager
        self.auimgr.AddPane(ctrl, pane) 

        #add a tool item to the view page
        viewPage = self.ToolStrip.GetPageByLabel('View')
        toolGroup = viewPage.GetGroupByLabel('Tools')
        tool = toolGroup.AddLabelToggleTool( -1, ts.ITEM_SMALL, bitmap,
                        label, label, longHelp)
        tool.SetToggle(pane.IsShown()) #ensure toogle state is correct
        toolGroup.Realize()

        #store the pane_caption with the tool and bind the event to automatically show/hide this pane
        tool.pane_caption = pane.caption
        self.Bind(wx.EVT_TOOL, self.OnShowToolPane, tool)

        self._pane_tools[pane.caption]=tool

        return tool

    # Needed anymore?
    #def Show(self,show=True):
    #    self.auimgr.Update()
    #    wx.Frame.Show(self,show)

    #---Layouts Interface-------------------------------------------------------
    def AddLayout(self,layout=None,name="New layout"):
        """
        Save a new layout:
            If layout is None a new layout is created using the name and the
            current settings
            If menu is given a checkitem will be added to the menu
        """
        if layout is None:
            layout = Layout(self,name=name,menu=self.laymenu)
            layout.SaveCurrentState()
        self._layouts.append(layout)

    def RemoveLayout(self,n):
        """Remove the nth saved layout (including from any menus)"""
        layout = self._layouts.pop(n)
        layout.RemoveMenuItem()
        del layout

    def RenameLayout(self,n,newname):
        """Rename the nth saved layout (including from any menus)"""
        #make sure name is a string
        newname = str(newname)
        layout = self._layouts[n]
        layout.Rename(newname)

    def SetSavePath(self,path):
        """Set the save path in the wxconfig object"""
        self.path = path

    def SaveLayouts(self):
        """
        Save the layouts to the path (set via SetSavePath) in the wxconfig 
        object
        """
        #check save/load path is set
        if self.path is None:
            return
        #Get the config object
        cfg = wx.GetApp().GetConfig()

        #save the current layout
        cur = Layout(self,menu=None,data=None,name='last')
        cur.SaveCurrentState()
        s = cur.GetSaveString()
        cfg.Write(self.path+"//current_layout",s)

        #delete any old saved layouts 
        cfg.DeleteGroup(self.path+"//layouts")
        #save the other layouts
        n=0
        for layout in self._layouts:
            s = layout.GetSaveString()
            cfg.Write(self.path+"//layouts//saved"+str(n),s)
            n = n+1
        cfg.Flush()

    def LoadLayouts(self):
        """
        Loads the layouts from the path (set via SetSavePath) in the wxconfig 
        object. Adds checkitems into menu set via SetLayoutsMenu
        """
        #check save/load path is set
        if self.path is None:
            return
        #Get the config object
        cfg = wx.GetApp().GetConfig()
        
        #load the saved layouts
        cfg.SetPath(self.path+"//layouts//")
        num = cfg.GetNumberOfEntries()
        for n in range(0,num):
            s = cfg.Read("saved"+str(n),"")
            if s!="":
                layout = Layout(self,menu=self.laymenu,data=s)
                self.AddLayout(layout)

        #load the current layout
        cfg.SetPath("")
        s = cfg.Read(self.path+"//current_layout","")
        if s!="":
            cur = Layout(self,menu=None,data=s)
            cur.Apply() #apply this layout
            #fix for maximise bug  - force the window to refresh the status bar position
            if cur.max is True:
               self.Maximize()
               self.SetPosition(cur.pos)
               self.SetSize(cur.size)


    # EVENT HANDLERS - NOT CURRENTLY USED -  LEFT FOR FUTURE USE
    def OnSaveLayout(self,event):
        """Handles saving of an aui layout"""
        dlg = wx.TextEntryDialog(self, "Enter a name for the new layout:", "Python toolkit")
        dlg.SetValue(("New layout %d")%(len(self._layouts)+1))

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            self.AddLayout(name=name)
    
    def OnRenameLayout(self,event):
        """Handles renaming of an aui layout"""
        #get layout to change
        names = []
        for x in self._layouts:
            names.append(x.name)
        dlg = wx.SingleChoiceDialog(
                self, 'Select layout to rename:', 'Rename layout',
                names, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        
        n = dlg.GetSelection()
        dlg.Destroy()

        #get new name
        dlg = wx.TextEntryDialog(self, 'Enter new name:','Rename layout', 
                    self._layouts[n].name)
        if dlg.ShowModal() == wx.ID_OK:
            new = dlg.GetValue()
            self.RenameLayout(n,new)
        dlg.Destroy()

    def OnDeleteLayout(self,event):
        """Handles deleting an aui layout"""
        #get layout to delete
        names = []
        for x in self._layouts:
            names.append(x.name)
        dlg = wx.SingleChoiceDialog(
                self, 'Select layout to remove:', 'Remove layout',
                names, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            n = dlg.GetSelection()
            self.RemoveLayout(n)
        dlg.Destroy()

    #handlers for show/hide toggle pane button
    def OnShowToolPane(self, event):
        """show/hide a tool pane"""
        id = event.GetId()
        
        viewPage = self.ToolStrip.GetPageByLabel('View')
        toolGroup = viewPage.GetGroupByLabel('Tools')
        item = toolGroup.GetTool(id)
        
        pane = self.auimgr.GetPane(item.pane_caption)
        if event.IsChecked() is True:
            pane.Show()
            self.auimgr.Update()
        else:
            pane.Hide()
            self.auimgr.Update()

    def OnPaneClose(self, event):
        pane = event.GetPane()
        print('On Close', pane.caption)

        #toogle tool pane button in view toolstrip
        if pane.caption in self._pane_tools:
            tool = self._pane_tools[pane.caption]
            tool.SetToggle( False )

        event.Skip()


#-------------------------------------------------------------------------------
class ToolbarStaticText(wx.Control):
    """
    A static text control with the gradient background of the AuiToolbar class
    """
    def __init__(self, parent, id, text):
        wx.Control.__init__(self, parent, id, style=wx.BORDER_NONE)

        self.text = text
        w,h = self.GetTextExtent(self.text)
        pw,ph = self.Parent.GetSize()
        self.SetMinSize( (w, ph ))
       
        self.SetBackgroundColour(parent.GetBackgroundColour());
        self.SetForegroundColour(parent.GetForegroundColour());
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Parent.Bind(wx.EVT_SIZE, self.OnParentSize)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        #draw background
        wnd = self.Parent
        w, h = self.GetSize()
        rect = wx.Rect(0,0,w,h)
        tbart = self.Parent.GetArtProvider()
        tbart.DrawBackground(dc, self, rect)
        #draw text
        dc.SetFont(self.GetFont());
        tw,th = self.GetTextExtent(self.text)
        x = (w-tw)/2
        y = (h-th)/2
        dc.DrawText(self.text, x, y);

    def OnSize(self, event):
        self.Refresh()
        
    def OnParentSize(self, event):
        pw,ph = self.Parent.GetSize()
        w,h = self.GetTextExtent(self.text)
        self.SetMinSize( (w, ph) )
        event.Skip()
