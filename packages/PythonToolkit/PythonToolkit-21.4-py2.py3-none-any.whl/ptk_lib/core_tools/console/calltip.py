import wx
from wx.lib.scrolledpanel import ScrolledPanel
from ptk_lib.controls import iconbutton

from .autocomps import scan_line

#engine task to get call tip
def get_call_tip(globals, locals, name):
    import inspect
    # get a ref to the object
    try:
        obj = eval(name,globals, locals)
    except:
        obj=None
    
    # no object / None
    if obj is None:
        return None
        
    # object is a builtin function
    # Builtin functions may not have an argspec that we can get use docstring
    elif inspect.isbuiltin(obj):
        try:
            argspec = name+str(inspect.signature(obj))
        except:
            argspec = ''
        doc = inspect.getdoc(obj) 
        calltip = ''
        if argspec!='':calltip = calltip+argspec+'\n\n'
        if doc!='': calltip = calltip+doc
        
    # object is a class use argspec and doc strings from class and init
    elif inspect.isclass(obj):
        try:
            argspec = name+str(inspect.signature(obj))
        except:
            argspec = ''
        # get class doc and constructor doc
        doc1 = inspect.getdoc(obj) 
        doc2 = inspect.getdoc(obj.__init__)
        calltip = ''
        if argspec!='':calltip = calltip+argspec+'\n\n'
        if doc1!='': calltip = calltip+doc1+'\n\n'
        if doc2!='': calltip = calltip+doc2
                
    # is a callable
    # show __call__ docstring as well
    # (some objects np.unfunc doc is on the object not __call__)
    elif callable(obj):
        #get call args
        try:
            argspec = name+str(inspect.signature(obj))
        except:
            argspec = ''
        doc1 = inspect.getdoc(obj.__call__)
        doc2 = inspect.getdoc(obj)
        calltip = ''
        if argspec!='':calltip = calltip+argspec+'\n\n'
        if doc1!='': calltip = calltip+doc1+'\n\n'
        if doc2!='': calltip = calltip+doc2
    else:
        try:
            argspec = name+str(inspect.signature(obj))
            doc = inspect.getdoc(obj)
            calltip = argspec+'\n\n'+doc
        except:
            calltip = None
        
    #check for empty calltips
    if calltip =='':
        return None
    return calltip

#the calltip popupwindow
class CallTip(wx.PopupWindow):
    def __init__(self, parent, string, pos=wx.DefaultPosition):

        style = wx.BORDER_NONE
        wx.PopupWindow.__init__(self, parent,style)

        #calculate the best size - 100chars in system font should do...
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        dc = wx.ClientDC(self)
        dc.SetFont(font)
        w, h = dc.GetTextExtent('-'*110)
        self._startsize = (w,w/2)
        self.SetSize( self._startsize )
        self.SetPosition(pos)
        self.string = string

        self.SetBackgroundColour((238,232,140))

        #sizer to add everything to
        sizer  = wx.BoxSizer(wx.VERTICAL)
        
        ##close button
        self.close = iconbutton.BmpIcon(self,-1,iconbutton.close.GetBitmap())
        sizer.Add(self.close,0,wx.ALIGN_RIGHT|wx.ALL,2)
        self.close.Bind(iconbutton.EVT_ICON_CLICK, self.OnClose)

        ##contents panel and text
        self.panel = ScrolledPanel(self,-1,style=wx.BORDER_NONE)
        
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self.panel,-1,string)
        psizer.Add(self.text,1,wx.EXPAND|wx.LEFT|wx.RIGHT,5)
        self.panel.SetSizer(psizer)
        self.panel.SetupScrolling()
        sizer.Add(self.panel,1,wx.EXPAND|wx.LEFT|wx.RIGHT,5)

        ##static line
        line = wx.StaticLine(self,-1,style=wx.HORIZONTAL)
        sizer.Add(line,0,wx.EXPAND|wx.ALL,5)

        ##lock button
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.lock = iconbutton.ToggleIcon(self,-1,iconbutton.locked.GetBitmap(),
                                iconbutton.unlocked.GetBitmap())
        self.lock.SetState(False)
        self.lock.SetToolTip('Prevent autoclose')
        sizer2.Add(self.lock,0,wx.ALIGN_LEFT|wx.ALL,2)
        sizer2.AddStretchSpacer()

        ##resize button
        self.resize = iconbutton.BmpIcon(self,-1,iconbutton.resize.GetBitmap())
        sizer2.Add(self.resize,0,wx.ALIGN_BOTTOM|wx.ALL,2)
        sizer.Add(sizer2,0,wx.EXPAND,0)

        self.SetSizer(sizer)
        self.Layout()

        ##background colour
        colour = (238,232,140)
        self.close.SetBackgroundColour(colour)
        self.lock.SetBackgroundColour(colour)
        self.resize.SetBackgroundColour(colour)
        self.panel.SetBackgroundColour(colour)
        self.text.SetBackgroundColour(colour)
        line.SetBackgroundColour(colour)

        ##Window movement
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.panel.Bind(wx.EVT_MOTION, self.OnMotion)
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self.text.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.text.Bind(wx.EVT_MOTION, self.OnMotion)
        self.text.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        ##resizing
        self.sizing = False
        self.resize.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.resize.Bind(wx.EVT_MOTION, self.OnMotion)
        self.resize.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        #need to bind to parent to get keyboard/mouse events
        #parent must have keyboard focus!
        self.Parent.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Parent.Bind(wx.EVT_MOUSE_EVENTS, self.OnParentClick)

        wx.CallAfter(self.close.OnLeave,None)

    def Show(self,flag=True):
        self.Layout()
        if (flag is False) and (self.lock.GetState() is True):
            return False
        res = wx.PopupWindow.Show(self,flag)
        wx.CallAfter(self.close.OnLeave,None)
        return res
    
    def Hide(self):
        if (self.lock.GetState() is True):
            return False
        return wx.PopupWindow.Hide(self)

    def ShowCallTip(self, line):
        """
        Get calltip for the line given and show.
        """
        #show it
        if self.IsLocked():
            return
            
        #find the call object
        instr, incall, inindex, objname, remainder = scan_line(line)
        if incall is False:
            return
            
        #get the tip
        tip = self.Parent.run_task('get_call_tip', (objname,))
        
        #hide it
        self.Hide()

        #no tip found
        if tip is None:
            return
        
        #set call tip
        self.string = tip
        self.text.SetLabel(tip)
        self.SetSize(self._startsize)
        self.panel.SetupScrolling()
        self.panel.Scroll(0,0)
        self.Layout()
        self.SetBestPosition()
        self.Show()
        
    def SetBestPosition(self):
        """
        Set the best position for the popup
        """
        #calculate where to show the calltip
        wpos = self.Parent.PointFromPosition(self.Parent.GetCurrentPos())
        spos = self.Parent.ClientToScreen(wpos)
        size = self.Parent.GetSize()
        maxy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        maxx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        spos.x = spos.x+50 #shift over a bit
        if spos.x > maxx:
            spos.x = maxx-size.x
            spos.y = spos.y-size.y-50
        if spos.y>maxy-size.y:
            spos.y = maxy-size.y
        if spos.y<0:
            spos.y = 0
        self.SetPosition(spos)
        
    def Lock(self,flag=True):
        self.lock.SetState(flag)

    def UnLock(self):
        self.lock.SetState(False)

    def IsLocked(self):
        return self.lock.GetState()


    #---events------------------------------------------------------------------
    def OnLeftDown(self, event):
        obj = event.GetEventObject()
        self.ldPos = obj.ClientToScreen(event.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        if obj==self.resize:
            #resize
            self.sizing = True
            self.wSize = self.GetSize()
        self.CaptureMouse()
        event.Skip()
 
    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            dPos = event.GetEventObject().ClientToScreen(event.GetPosition())
            if self.sizing:
                w = self.wSize.width + (dPos.x - self.ldPos.x)
                h = self.wSize.height + (dPos.y - self.ldPos.y)
                self.SetDimensions(self.wPos.x,self.wPos.y,w,h)
            else:
                nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                        self.wPos.y + (dPos.y - self.ldPos.y))
                self.Move(nPos)

    def OnLeftUp(self,event):
        self.ReleaseMouse()
        self.sizing = False

    def OnClose(self,event):
        self.UnLock()
        self.Hide()

    def OnSize(self,event):
        try:
            w,h = self.GetSize()
            self.text.SetLabel(self.string)
            sw = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
            self.text.Wrap(w-sw-20)
            self.Layout()
        except:
            pass
            
    def OnParentClick(self, event):
        """Capture clicks in parent stc"""
        #if hidden pass to parent
        if self.IsShown() is False:
            event.Skip()
            return
            
        #otherwise check for clicks
        if event.ButtonDown():
            self.Hide()
        event.Skip()
        
    def OnKeyDown(self, event):
        """Key down event handler of (parent stc)."""
        #get key info
        key         = event.GetKeyCode() #always capital letters here
        #controlDown = event.CmdDown()    #use CmdDown to support mac command button and win/linux ctrl
        #altDown     = event.AltDown()
        #shiftDown   = event.ShiftDown()
        
        #if the calltip popup is not shown pass the events to the parent
        if self.IsShown() is False:
            event.Skip()
            return
        
        #escape close calltip but do not pass to parent as this will clear the 
        #command as well
        if key == wx.WXK_ESCAPE:
            self.Hide()
        else:
            #pass to parent
            event.Skip()
            
class DummyCallTip():
    """
    Used for Mac OS where popup window is not supported
    """
    def __init__(self, parent, string, pos=wx.DefaultPosition):
        pass

    def Show(self,flag=True):
        return True
    
    def ShowCallTip(self, line):
        """
        Get calltip for the line given and show.
        """
        pass
        
    def IsShown(self):
        return False

    def Hide(self):
        return True

    def SetPosition(self, pos):
        return True

    def Lock(self,flag=True):
        pass

    def UnLock(self):
        pass

    def IsLocked(self):
        return False

#use simple address ctrl on mac
if wx.Platform == '__WXMAC__':
    CallTip = DummyCallTip
