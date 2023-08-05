#!/usr/bin/env python3
"""
Advanced toolbar libary:

Custom toolbar class (ToolPanel) with support for tools with dropdown menus and
complex tool arrangements such as 1x large icon , 2x small stacked icons.

Toolstrip a ribbon like menu/toolbar replacement with page highlighting groups
and complex tool arrangements.


TODO:
-----
AddressBar in ToolStrip class - a full width ToolPanel.
QuickTools in ToolStrip class - a small toolpanel in tab bar

HomeTab/Icon tabs   -   add bitmap support to tabs - may need to resize tabbar/tabs?
Groups - highlighting of groups?
Tabbar - scrolling icons when tabs to wide.
ToolPanel - overflow group when toolpanel not wide enough.
Demo panel.

Usage:

Toolbars - use ToolPanels:
1) Create ToolPanel
2) add tools, ToolPanel.Realize() to layout tools

ToolStrip:
1) Create ToolStripPage:
2) add groups
3) add tools to groups followed by ToolStripGroup.Realize() to layout tools
"""
import wx

#%%-----------------------------------------------------------------------------
# events
#-------------------------------------------------------------------------------
from wx.lib.newevent import NewEvent
EvtToolStripTabClick , EVT_TOOLSTRIP_TABCLICK = NewEvent() #wx event to for ts tabs


#%%-----------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
#item sizes
ITEM_MAX = -1        #fills all available rows
ITEM_SMALL = 1       #1 row high
ITEM_MEDIUM = 2      #2 rows
ITEM_LARGE = 3       #3 rows

#example of layout styles defining row heights/ number of rows
LAYOUT_TOOLBAR_16x1 = (16,1)      #Toolbar single row of icons 16px bitmaps
LAYOUT_TOOLBAR_22x1 = (22,1)      #Toolbar single row of icons 22px bitmaps

LAYOUT_TOOLBAR_16x2 = (16,2)      #Toolbar single row of icons 32px bitmaps or 2x16px icons
LAYOUT_TOOLBAR_22x2 = (22,2)      #Toolbar 2x row of icons 22px bitmaps

LAYOUT_TOOLBAR_32x1 = (32,1)      #Toolbar single row of icons 32px bitmaps
LAYOUT_TOOLBAR_16x3 = (16,3)      #Toolbar layout with single row of 32px bitmaps & labels or 3x16px icons
LAYOUT_RIBBON = (16,3)            #Ribbon bar style is 3xsmall icons

#some predefined page highlighting colours
HL_RED  =  (255,100,100)
HL_BLUE =  (100,100,255)
HL_GREEN = (100,255,100)
HL_CYAN =  (0,200,150)
HL_YELLOW = (227,227,0)
HL_ORANGE = (255,100,0)
HL_PINK   = (255,0,200)
HL_PURPLE = (170,0,200)

def PopStatusText(self, n=0):
    """ Wrap PopStatus text to catch errors """
    try:
        self.PopStatusText(n)
    except:
        pass
        
#%%-----------------------------------------------------------------------------
# Painter object so all painting code is all in one place and can easily be
# changed.
#-------------------------------------------------------------------------------
class Painter():
    def __init__(self):
        """
        The Painter defines all colours and painting of toolPanels and 
        toolStrip elements in one place for easy customisation
        """
        #panel attributess
        self.panel_hl = (255,255,255)    #panel top gradient backgound colour
        self.panel_bg = (240,240,240)    #panel bottom gradient background colour
        
        #tabbar/tab/page attributes
        self.tabbar_bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR)   
        
        #tab label text colour used for active/hovered tabs
        self.tab_labels1 =  wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)
        
        #inactive tabs label colour
        self.tab_labels2 =  wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)
        
        #page border colour
        self.page_border = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW) 

        #tab spacing size in px
        self.tab_spacing = 4 
        
        #page gradient colours
        self.page_hl = (255,255,255) #page top gradient backgound colour
        self.page_bg = (230,230,230) #page bottom gradient background colour

        #group labels
        self.group_labels = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT) 
        
    def paintTab(self, tab, current=False, hover=False, highlighted=False):
        """
        Paint a ToolStripTab
            current - the current tab True/False flag
            hover  - mouse hovering True/False flag
        """
        dc = wx.BufferedPaintDC(tab)
        gc = wx.GraphicsContext.Create(dc)
        
        #draw background
        pos = tab.GetPosition()
        self.paintTabBar( dc, tab.Parent, pos)
        
        w, h = tab.GetClientSize() 
        tx = self.tab_spacing-1
        ty = 2
        tw = w - self.tab_spacing
        th = h - 2 

        if (highlighted is True):
            #highlighted tab
            #set brush
            col1 = tab.hl_col     
            col2 = self.page_hl     
            gradbrush = gc.CreateLinearGradientBrush( 0, -h,0, h+7,col1,col2  )
            gc.SetBrush( gradbrush )
            #set pen
            gc.SetPen(wx.Pen( tab.hl_col, width=1))
            dc.SetTextForeground( self.tab_labels1 )

        elif (current is True):
            #current tab but not highlighted
            gc.SetBrush( wx.Brush( self.page_hl ) )
            gc.SetPen(wx.Pen( self.page_border, width=1))
            #draw tab
            dc.SetTextForeground( self.tab_labels1 )
        elif (hover is True):
            #hover over unhighlighted tab
            gc.SetBrush( wx.Brush( self.page_hl )) #wx.TRANSPARENT_BRUSH )
            gc.SetPen( wx.Pen( self.page_border, width=1))
            dc.SetTextForeground( self.tab_labels1 )

        else:
            #not active, not hover, not highlighted
            gc.SetBrush( wx.TRANSPARENT_BRUSH )
            gc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetTextForeground( self.tab_labels2 )

        #draw tab
        #gc.DrawRoundedRectangle(tx, ty, tw, h+5 , 3) 
        gc.DrawRectangle(tx, ty, tw, h+5 ) 

        #add label
        dc.SetFont(tab.GetFont())
        textw,texth = tab.GetTextExtent('yl')
        rect = (self.tab_spacing, 2, tw, th)
        dc.DrawLabel(tab.Label, rect, alignment=wx.ALIGN_CENTER, indexAccel=-1)
 
    #Painting methods for the container control and childrens backgrounds
    def paintPanel( self, dc, panel, pos=(0,0)):
        """
        Paint the ToolPanel background to a child control.
            dc - the child dc to paint background to.
            toolbar - the parent/grandparent toolbar
            pos - the pos of the child relative to the panel
        """        
        #calculate x,y offset to draw background at
        w, h = panel.GetClientSize() 
        rect = (-pos[0], -pos[1],w, h)
        
        #draw background        
        #solid b/g 
        #dc.SetPen(wx.Pen(self.panel_bg))
        #dc.SetBrush(wx.Brush(self.panel_bg))
        #dc.DrawRectangle(*rect)
        
        #gradient b/g
        dc.GradientFillLinear( rect, self.panel_hl, self.panel_bg, wx.SOUTH)
        
    def paintPage( self, dc, page, pos=(0,0)):
        """
        Paint the toolstrip page background a child control
            dc - the dc to paint background to.
            page - the parent page
            pos - the pos of the child relative to the panel
        """
        #calculate x,y offset to draw background at
        w, h = page.GetClientSize() 
        x,y = pos
        rect =  (-x, -y, w, h)

        #tab position and size
        tx,ty = page.tab.GetPosition()
        tw,th = page.tab.GetSize()

        #solid b/g
        rect = (-x, -y, w, h-1)
        #dc.SetPen(wx.Pen(self.page_hl))
        #dc.SetBrush(wx.Brush(self.page_hl))
        #dc.DrawRectangle(*rect)

        #gradient b/g
        dc.GradientFillLinear( rect, self.page_hl, self.page_bg, wx.SOUTH)

        #draw highlighting gradients if set
        if page.highlight is True:
            #top gradient goes from th above the tab to 6 below - to match gradient 
            #used for tab
            dc.GradientFillLinear( (-x,-y-(2*th), w ,(2*th)+7), page.hl_col, self.page_hl, wx.SOUTH)
            #bottom
            #dc.GradientFillLinear( (-x,-y+h-7,w,30), page.hl_col, self.page_bg, wx.NORTH)

        #draw strip border
        #use page highlighting colour if set
        if page.highlight is True:
            col = page.hl_col  
        else:
            col = self.page_border  
        dc.SetPen(wx.Pen( col ,width=1))

        #top - draw top to tab then tab to end
        dc.DrawLine( -x, -y, -x+tx+self.tab_spacing, -y)    #top: to active tab
        dc.DrawLine( -x+tx+tw-1, -y, w, -y)    #top: active tab to end
        dc.DrawLine( -x, -y+h-1, -x+w, -y+h-1)  #bottom
        
    def paintGroup( self, dc, group, pos=(0,0)):
        """
        Paint the group background to a child control
            dc - the child dc to paint background to.
            group - the parent group
            pos - the pos of the child relative to the group
        """
        #default implementation is paint the page background gradient
        x,y = pos
        w, h = group.Size #use the groups actual size    
        rect = (-x, -y-2, w, h+4) #add on bit for page border
        dc.GradientFillLinear( rect, self.page_hl, self.page_bg, wx.SOUTH)
        
        #gx,gy = group.GetPosition()
        #x,y = pos[0]+gx, pos[1]+gy
        #group.page._draw_bg(dc, (x,y) )
    
        #draw seperator on rhs
        dc.GradientFillLinear((w-1, 1, w, h-1), self.page_hl, self.page_border, wx.SOUTH)

        #draw label
        dc.SetFont(group.GetFont())
        dc.SetPen(wx.Pen(self.group_labels,width=1))
        dc.SetTextForeground( self.group_labels )
        rect = (3, h-group.labelH, w-6, group.labelH)
        dc.DrawLabel(group.label, rect, alignment=wx.ALIGN_CENTER, indexAccel=-1)
    
    def paintGroupOverflow( self, dc, overflow, pos=(0,0)):
        """
        Paint the group overflow background to a child control
            dc - the child dc to paint background to.
            group overflow - the parent group overflow
            pos - the pos of the child relative to the group
        """
        #calculate x,y offset to draw background at
        w, h = overflow.GetClientSize() 
        x,y = pos
        rect =  (-x, -y, w, h)
        
        #solid b/g  for top half
        dc.SetPen(wx.Pen(self.page_hl))
        dc.SetBrush(wx.Brush(self.page_hl))
        dc.DrawRectangle(*rect)

        #gradient b/g for bottom half
        rect = (-x, -y+(h//2), w, (h//2)+1)
        dc.GradientFillLinear( rect, self.page_hl, self.page_bg, wx.SOUTH)

        #draw label
        group = overflow.group
        dc.SetFont(group.GetFont())
        dc.SetPen(wx.Pen(self.group_labels,width=1))
        dc.SetTextForeground( self.group_labels )
        rect = (3, h-group.labelH, w-6, group.labelH)
        dc.DrawLabel(group.label, rect, alignment=wx.ALIGN_CENTER, indexAccel=-1)
    
    def paintMinGroup(self,dc, group, pos=(0,0)):
        """
        Paint the minimised group
        """
        w, h = group.GetClientSize()        

        #default implementation is paint the page background
        gx,gy = group.GetPosition()
        x,y = pos[0]+gx, pos[1]+gy
        group.page._draw_bg(dc, (x,y) )
    
        #draw button bezel - only when hovered/depressed
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is group
        
        if hover is False:
            pass
        else:
            if group.IsEnabled() is False:
                state = wx.CONTROL_DISABLED
            elif hover is True:
                state = wx.CONTROL_PRESSED
            #draw
            rect = wx.Rect(0, 0, w-2, h)
            wx.RendererNative.Get().DrawPushButton(group, dc, rect, state)

        #draw group icon
        iw = 30
        y=12
        x=((w-2-iw)//2) # shift across to account for rhs sep
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen( self.group_labels, width=1))
        dc.DrawRoundedRectangle(x, y, iw, iw , 2) 

        dc.SetBrush( wx.Brush( self.group_labels ))
        dc.DrawRoundedRectangle(x, y+iw-6, iw, 8 , 2) 

        #draw seperator on rhs
        w, h = group.GetClientSize()    
        dc.GradientFillLinear((w-1, 1, w, h-1), self.page_hl, self.page_border, wx.SOUTH)

        #draw label
        dc.SetFont(group.GetFont())
        dc.SetPen(wx.Pen(self.group_labels,width=1))
        dc.SetTextForeground( self.group_labels )
        rect = (3, h-group.labelH, w-6, group.labelH)
        dc.DrawLabel(group.label, rect, alignment=wx.ALIGN_CENTER, indexAccel=-1)
    
    def paintTabBar( self, dc, tabbar, pos=(0,0)):
        """
        Paint the tabbar background to a child control
            dc - the child dc to paint background to
            tabbar - the parent tabbar
            pos - the pos of the child relative to the tabbar
        """
        #calculate x,y offset to draw background at
        w, h = tabbar.GetClientSize() 
        
        #draw background        
        #solid b/g 
        dc.SetPen(wx.Pen( self.tabbar_bg ))
        dc.SetBrush(wx.Brush( self.tabbar_bg ))
        rect =  (-pos[0], -pos[1],w, h)
        dc.DrawRectangle(*rect)
        
#default painter
DEFAULT_PAINTER = Painter

#%%-----------------------------------------------------------------------------
# ToolPanel -  wxPanel classes to hold/manage tools
#-------------------------------------------------------------------------------
class ToolPanel(wx.Panel):
    def __init__(self, parent, id, layout=LAYOUT_TOOLBAR_16x1, borders=(5,5,2,2), painter=DEFAULT_PAINTER):
        """
        A simple panel containing can be a parent for Tools
            layout=LAYOUT_RIBBON_3x16 tuple of (bmp_h,rowN)
            borders = left, right, top, bottom
        """
        wx.Panel.__init__(self, parent, id=-1, style=wx.BORDER_NONE)        

        self.painter = painter()        #create a painter

        #set the font size to size 8
        font = wx.SystemSettings.GetFont( wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize( 8 )
        self.SetFont( font )

        #internal attribiutes
        self.bmpSize = layout[0]
        self.rowN = layout[1]
        self.borders=borders

        #get row height 
        tw,th = self.GetTextExtent('yl') #text height
        bh = (self.bmpSize + 8) #get bitmap height with border
        if th > bh:
            rowH = th
        else:
            rowH = bh
        self.rowH = rowH
        
        #set min size to have the correct height
        self.SetMinSize( (-1, self.rowH*self.rowN + self.borders[2]+self.borders[3]))
        
        #list of tools added, the layout of the tools populated by Realize() and
        # the optimium size
        self.tools = []
        self._layout = [] #list of columns in layout, each a list of (tool, hrows, wprop)
        self.optSize = (0,0)
        
        #status bar for tools to use
        self._statusbar = None #using a protect attribute to allow overriding in subclasses
  
        #bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE,             self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
        
    #---internal methods--------------------------------------------------------
    def _draw_bg(self, dc, pos):
        """
        Internal painting method to allow children to paint the panel's 
        background to the dc and appear transparent.
        dc - dc to draw to
        pos - position of child relative to the ToolPanel
        """
        self.painter.paintPanel(dc, self, pos)
        
    #---Layout -----------------------------------------------------------------
    def Layout(self):
        """
        Positions and sizes tools in the current layout.
        """
        #print('in layout')
        self.Freeze()
        # wxPanel internal sizes:
        # MinSize   -    toolpanel min size (-1, rowH*nRows + borders[2] + borders[3])
        # MaxSize   -    (-1,-1) no max panel size to allow filling frames etc.
        # BestSize  -    seems to be close to set value but subtracts window border?
        
        # 1) get sizes for all tools and min size for controls
        # calculate min full size for toolpanel: 
        #   sum( max width of each column)
        #   max width of each column is max of tools/ctrls in column
        # store interally as self.optSize
        # make list of resizable tools/ctrls and total proportion settings to 
        # allocate spare space in next step
        
        #min size for panel
        min_w = 0
        resizable = []  #list of tools that may need resizing
        total_prop = 0  #sum of all proportion value for resizable tools
        for col in self._layout: #loop over cols in layout
            colMax = 0
            colProp = 0
            for tool, hrows, wprop in col:   #loop over tools in col
            
                #find widest control in columm
                
                # a resizable control
                if wprop !=0:
                    tsize = tool.MinSize[0] #resizable use minSize
                    resizable.append((tool, hrows, wprop))
                    total_prop = total_prop + wprop
                    
                # a spacer with width given by int(tool) pixels
                elif isinstance(tool, int):
                    tsize = tool
                    
                # a non-resizable control
                else:
                    tsize = tool.Size[0]
                
                #check if tool is the largest in this column
                if tsize > colMax:
                    colMax = tsize

            #add this column to min panel size
            min_w = min_w + colMax
        
        #add on any borders
        min_w = min_w +self.borders[0] + self.borders[1]
        min_h = self.rowH * self.rowN + self.borders[2] + self.borders[3]

        #respect any min size set for the panel
        if min_w < self.MinSize[0]:
            min_w = self.MinSize[0]
        if min_h < self.MinSize[1]:
            min_h = self.MinSize[1]

        #set panel min size
        self.optSize = (min_w,min_h)
        self.SetMinSize( self.optSize )
        
        # 2) alocate any extra space available to the resizable tools using the
        # proportion value.
        w,h = self.GetSize()
        excess = w - min_w
        if excess >0:
            for tool,hrows,wprop in resizable:
                w = tool.MinSize[0] + ((excess/total_prop)*wprop)
                tool.SetSize( (w, tool.Size[1]) )  #set only width

        # 3) Position the tools
        x = self.borders[0]
        y0 = self.borders[2]
        
        for col in self._layout: #loop over cols in layout
            colMax = 0  #max width of the column
            y = y0      #top row
            for tool,hrows,wprop in col:   #loop over tools in col and set position
            
                # a spacer
                if isinstance(tool, int):
                    tsize = tool
                # a control
                else:
                    #check for unallocated tool hieght in row and centre if necessary
                    available = hrows*self.rowH
                    pady = (available - tool.Size[1])/2
                    tool.SetPosition((x,y+pady))
                    
                #update y position
                y = y + (hrows * self.rowH)
                if tool.Size[0] > colMax:
                    colMax = tool.Size[0] 
                    
            #move to next column
            x = x+colMax

        self.Thaw()
        
    def Realize(self):
        """
        Called after all tools have been added to the ToolPanel or tools have 
        been hidden - this calculates positions in columns for each tool using 
        the ToolPanel layout
        
        Layout() then positions and sizes the tools.
        """
        #print('in realize')
        self._layout = [] #list of columns in layout
        
        #layout tools into columns and store internally.
        row = 0         #row counter
        col = []        #list of tool,prop in column
        for n in range(0, len(self.tools)):
            #unpack the tool number of rows and width proportion 
            tool, hrows, wprop = self.tools[n]
            
            #check tool height in rows
            if hrows > self.rowN:
                raise Exception('Number of rows requested for tool is too large for current layout!')
                            
            if (row + hrows)<=self.rowN:
                #fits in this column with spare space
                col.append((tool, hrows, wprop))
                #adjust current row counter
                row = row+hrows
            else:
                #need to start a new column
                self._layout.append(col)
                col = []
                col.append( (tool, hrows, wprop) )
                #adjust current row counter
                row = hrows
        
            if row==self.rowN:
                #need to start a new column
                self._layout.append(col)
                col = []
                row = 0 
        
        #position and size the tools using the layout determined above.
        self.Layout()

    #--- interfaces methods/attributes------------------------------------------
    # add control should have args like a sizer.
    #   hrows
    #   wprop
    #   flags= wx.ALIGN_CENTER, wx.EXPAND, wx.ALIGN_TOP, wx.ALIGN_BOTTOM, wx.ALL, wx.LEFT, wx.RIGHT, wx.TOP
    
    
    def AddControl(self, control, hrows=ITEM_MAX, wprop=0):
        """
        Add a control to the group.
        
        hrows - fill h rowsrows in a column.
        wprop - width proportion to use, if greater than 
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item size > number of rows')
        if hrows==ITEM_MAX:
            hrows = self.rowN

        #parent if necessary
        if control.Parent is not self:
            control.Reparent(self)
        
        maxH = self.rowH*hrows
        tsize = control.GetSize()
        
        if (tsize[1]>self.rowH*hrows):
            control.SetSize( (tsize[0],maxH) )
            control.SetMinSize( (tsize[0],maxH) )
            control.SetMaxSize( (-1,maxH) )
    
        #add itemSize attribute to control
        control.itemSize = self.rowN
        self.tools.append( (control, hrows, wprop) )
        
    def AddSpacer(self, width=0, hrows=ITEM_SMALL):
        """
        Add a spacer
        
        width - width in pixels (for horizontal spacing)
        hrows - number of rows to fill (set to ITEM_MAX for vertical spacing)
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item size > number of rows')
        if hrows==ITEM_MAX:
            hrows = self.rowN
        self.tools.append((int(width),hrows,0))

    def AddSeparator(self, hrows=ITEM_MAX):
        """
        Add a seperator item
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item size > number of rows')
        if hrows==ITEM_MAX:
            hrows = self.rowN
            
        line = Seperator(self, hrows)
        self.tools.append((line,hrows,0))
        return line
        
    def AddStaticLabel(self, label, hrows=ITEM_SMALL):
        """
        Add a static text label
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item hrows > number of rows')
        if hrows==ITEM_MAX:
            hrows = self.rowN
            
        text = StaticText(self, -1, hrows, label )
        self.tools.append( (text,hrows,0) )
        return text

    def AddNormalTool(self, id=-1, hrows=ITEM_SMALL, bitmap=wx.NullBitmap, shortHelp='', longHelp=''):
        """
        Add a normal button tool.
        hrows = number of rows (ITEM_SMALL, ITEM_MEDIUM, ITEM_LARGE)
            ITEM_SMALL = 1 row,  bitmap size of upto1x bmpSize
            ITEM_MEDIUM = 2 rows,  bitmap size of upto 2x bmpSize
            ITEM_LARGE  = 3 rows,  bitmap size of upto 3x bmpSize
        Returns new ToolItem.
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item hrows > number of rows')
        if hrows==ITEM_MAX:
            hrows = self.rowN
            
        #generate an id if needed
        if id == wx.ID_ANY:
            id = wx.NewId()
            
        #create tool
        b = ButtonItem(self, id, hrows, bitmap)
        
        #set help tips
        b.SetShortHelp(shortHelp)
        b.SetLongHelp(longHelp)
        
        #add control
        self.tools.append( (b,hrows,0) ) 
        
        return b
        
    def AddToggleTool(self, id=-1, hrows=ITEM_SMALL, bitmap=wx.NullBitmap, shortHelp='', longHelp=''):
        """
        Add a toggle button tool.
        hrows = number of rows (ITEM_SMALL, ITEM_MEDIUM, ITEM_LARGE)
        
        Returns new ToolItem.
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item hrows > number of rows')
        if hrows==ITEM_MAX:
            hrows = self.rowN
            
        #generate an id if needed
        if id == wx.ID_ANY:
            id = wx.NewId()
            
        #create tool
        b = ToggleItem(self, id, hrows, bitmap)
        
        #set help tips
        b.SetShortHelp(shortHelp)
        b.SetLongHelp(longHelp)
        
        #add control
        self.tools.append( (b,hrows,0) ) 
        
        return b
    
    def AddDropDownTool(self, id=-1, hrows=ITEM_SMALL, bitmap=wx.NullBitmap, 
                        direction=wx.HORIZONTAL, shortHelp='', longHelp=''):
        """
        Add a DrownDown button tool (bitmap and dropdown arrow).
        hrows = number of rows (ITEM_SMALL, ITEM_MEDIUM, ITEM_LARGE)
        direction = drop arrow below (wx.VERTICAL) or alongside (wx.HORIZONTAL)
        
        Returns new ToolItem.
        """
        #check size
        if hrows> self.rowN:
            raise ValueError('Item hrows > number of rows')
        
        #generate an id if needed
        if id == wx.ID_ANY:
            id = wx.NewId()
            
        #create tool
        b = DropDownItem(self, id, hrows, bitmap, direction)
        
        #set help tips
        b.SetShortHelp(shortHelp)
        b.SetLongHelp(longHelp)
        
        #add control
        self.tools.append( (b,hrows,0)) 
        
        return b

    def AddLabelTool(self, id=-1, hrows=ITEM_SMALL, bitmap=wx.NullBitmap, label='', shortHelp='', longHelp=''):
        """
        Add a button tool with a label.
        valid hrows: = number of rows only 
            ITEM_SMALL - single row small bitmap and single line of text
            ITEM_LARGE - three rows 2xrow bitmap and upto two lines of text.
        
        Returns new ToolItem.
        """
        #check size
        if hrows not in [ITEM_SMALL, ITEM_LARGE]:
            raise ValueError('Item hrows restricted to ITEM_SMALL=1, ITEM_LARGE=2')
        
        #generate an id if needed
        if id == wx.ID_ANY:
            id = wx.NewId()
            
        #create tool
        if hrows == ITEM_SMALL:
            b = sLabelItem(self, id, bitmap, label)
        elif hrows == ITEM_LARGE:
            b = lLabelItem(self, id, bitmap, label)
        
        #set help tips
        b.SetShortHelp(shortHelp)
        b.SetLongHelp(longHelp)
        
        #add control
        self.tools.append( (b,hrows,0))  
        
        return b

    def AddLabelToggleTool(self, id=-1, hrows=ITEM_SMALL, bitmap=wx.NullBitmap, label='', shortHelp='', longHelp=''):
        """
        Add a toggle button tool with a label.
        valid hrows: = number of rows only 
            ITEM_SMALL - single row, small bitmap and single line of text
            ITEM_LARGE - three rows 2xrow bitmap (2x bmpSize) and upto two lines of text.

        Returns new ToolItem.
        """
        #check size
        if hrows not in [ITEM_SMALL, ITEM_LARGE]:
            raise ValueError('Item hrows restricted to ITEM_SMALL=1, ITEM_LARGE=2')
        
        #generate an id if needed
        if id == wx.ID_ANY:
            id = wx.NewId()
            
        #create tool
        if hrows == ITEM_SMALL:
            b = sLabelToggleItem(self, id, bitmap, label)
        elif hrows == ITEM_LARGE:
            b = lLabelToggleItem(self, id, bitmap, label)
        
        #set help tips
        b.SetShortHelp(shortHelp)
        b.SetLongHelp(longHelp)
        
        #add control
        self.tools.append((b,hrows,0)) 
        
        return b
    
    def AddLabelDropDownTool(self, id=-1, hrows=ITEM_SMALL, bitmap=wx.NullBitmap, label='', shortHelp='', longHelp=''):
        """
        Add a button tool with a label and seperate dropdown menu
        valid hrows: = number of rows only 
            ITEM_SMALL - single row small bitmap and single line of text
            ITEM_LARGE - three rows 2xrow bitmap and upto two lines of text.
        
        Returns new ToolItem.
        """
        #check size
        if hrows not in [ITEM_SMALL, ITEM_LARGE]:
            raise ValueError('Item hrows restricted to ITEM_SMALL=1, ITEM_LARGE=2')
        
        #generate an id if needed
        if id == wx.ID_ANY:
            id = wx.NewId()
            
        #create tool
        if hrows == ITEM_SMALL:
            b = sLabelDropDown(self, id, bitmap, label)
        elif hrows == ITEM_LARGE:
            b = lLabelDropDown(self, id, bitmap, label)
        
        #set help tips
        b.SetShortHelp(shortHelp)
        b.SetLongHelp(longHelp)
        
        #add control
        self.tools.append((b,hrows,0)) 
        
        return b

    def AcceptsFocus(self):
        """ 
        Overloaded panel class method
        """
        return False

    def ToggleTool(self, id, flag=True):
        """
        Toggle a tool state.
        """
        if isinstance(flag, bool) is False:
            raise ValueError('Expected a boolean for flag argument')

        #get the tool
        b = self.GetTool(id)
        try:
            b.SetToggle(flag)
        except:
            raise Exception('Not a toggle tool!')
            
    def EnableTool( self, id, flag=True ):
        """
        Enable a tool
        """
        if isinstance(flag, bool) is False:
            raise ValueError('Expected a boolean for flag argument')

        #get the tool
        b = self.GetTool(id)
        res = b.Enable(flag)
        return res
    
    def DisableTool( self, id ):
        """
        Disable a tool
        """
        return self.EnableTool( id, False)
        
    def SetToolBitmap( self, id, bmp):
        """
        Set tool bitmap
        """
        #get the tool
        b = self.GetTool(id)
        try:
            b.SetBitmap(bmp)
        except:
            raise Exception('Not a bitmap tool!')
            
    def SetToolShortHelp(self, id, shortHelp=''):
        """
        Set the tools short help string
        """
        #get the tool
        b = self.GetTool(id)
        b.SetShortHelp(shortHelp)
        
    def SetToolLongHelp(self, id, longHelp=''):
        """
        Set the tools long help string
        """
        #get the tool
        b = self.GetTool(id)
        b.SetLongHelp( longHelp)
        
    def GetTool(self, id):
        """
        Returns the tool withid given or None
        """
        for t,nrows,prop in self.tools:
            if t.GetId() == id:
                return t
        return None
        
    def IsTool(self, id):
        """ Is the id given a tool """
        if self.GetTool(id) is None:
                return False
        return True

    def SetStatusBar(self, statusbar):
        """
        Set the status bar to display help strings
        """
        self._statusbar = statusbar
        
    @property
    def statusbar(self):
        """
        Get the statusbar used to display help strings
        """
        #use a property and self._statusbar to allow ToolStrip groups to all use the parents status bar!
        return self._statusbar
        
    #event handlers
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.painter.paintPanel(dc, self, (0,0))
        #self._draw_bg(dc, (0,0))
        
    def OnSize(self, event):
        #print('in onsize')
        self.Layout()
        self.Refresh(False)

#%%-----------------------------------------------------------------------------
# Components for ToolStrip 
#-------------------------------------------------------------------------------
# Main class
class ToolStrip(wx.Panel):
    """
    Tool strip
    """
    def __init__(self, parent, id=-1, painter=DEFAULT_PAINTER):

        wx.Panel.__init__(self, parent, id, style=wx.BORDER_NONE)

        self.current_page = 0           #active page/tab number
        self.statusbar = None           #statusbar to display help strings
        self.painter = painter()        #create a painter
        
        #internal structures for tabs/pages
        # VSizer:
        #   -   TabBar
        #   -   Current page 
        #   -  [ other pages hidden ]
        #   -  [ optional addrses bar toolpanel ]
        self.pages = []         #list of page objects
        self.page_labels = {}    #dict of name: page objects
        self._pagesizer = wx.BoxSizer( wx.VERTICAL)     #sizer for pages
        self.tabBar = ToolStripTabBar(self, -1)
        self._pagesizer.Add(self.tabBar, 0, wx.EXPAND)
        self.addressBar = None
        self.SetSizer(self._pagesizer)
        
        #get the default colours from parent toolstrip
        self.SetBackgroundColour(self.painter.tabbar_bg)
        
    def AcceptsFocus(self):
        """ 
        Overloaded panel class method
        """
        return False

    def Collapse(self):
        """
        Collapses the toolstrip to only the tabbar
        """
        page = self.GetCurrentPage()
        page.Hide()
        #page.SetMinSize((-1,1))
        self.Parent.Layout()
    
    def Restore(self):
        """
        Restores the toolstrip to show pages
        """
        page = self.GetCurrentPage()
        #page.SetMinSize( (-1,page.GetBestSize()[1]) )
        page.Show()
        self.Parent.Layout()
        
    def IsCollapsed(self):
        """
        Returns the state of the ToolStrip (True=Collapsed)
        """
        page = self.GetCurrentPage()
        if page.GetSize()[1] != page.GetBestSize()[1]:
            return True
        return False
        
    def SetStatusBar(self, statusbar):
        """
        Set the status bar to display help strings
        """
        self.statusbar = statusbar
        
    def AddPage(self, label, page=None, longHelp=''):
        """
        Add a ToolStripPage and ToolStripTab to the ToolStrip .
        
        label - tab label string
        page - the page to add or None to create a new page.
        longHelp - help string for display in statusbar
        
        Returns the page object
        """
        #create page
        if page is None:
            page = ToolStripPage( self, -1)
            
        if isinstance( page, ToolStripPage) is False:
            raise ValueError('Expected a ToolStripPage instance')
        
        #set page label/help string
        page.SetLabel(label) #ensure page label is correct
        page.SetLongHelp(longHelp)
        
        #add to tab bar
        tab = self.tabBar.AddTab(label, longHelp)
        page.SetTab(tab) #set the page tab
        
        #add to sizer and list
        self._pagesizer.Insert(1,page, 1, wx.EXPAND)
        self.pages.append(page)
        
        if label in self.page_labels:
            raise ValueError('Toolstrip already has page with label: '+str(label))
        self.page_labels[label] = page
        
        #hide page if not current page
        if (self.current_page!=len(self.pages) -1):
            page.Hide()
            
        #set first page as active
        if len(self.pages)==1:
            self.SetPage(0)
            
        return page

    def GetPages(self):
        """
        Returns a list of the pages added to the tool strip
        """
        return self.pages
        
    def GetPage(self, n):
        """
        Returns the nth page
        """
        return self.pages[n]
        
    def GetPageByLabel(self, label):
        """
        Return the page with the label given
        """
        if label in self.page_labels is False:
            raise ValueError('No page with label: '+str(label))
        return self.page_labels[label]
        
    def GetCurrentPage(self):
        """
        Get the current toolstrip page
        """
        return self.pages[ self.current_page]

    def SetPage(self, n):
        """
        Set the current page
        """
        self.Freeze()
        
        if (n < 0):
            raise ValueError('Page index must be >=0')
        if (n > len(self.pages) -1 ):
            raise ValueError('Page index out of range')
            
        #hide old page
        try:
            page = self.pages[self.current_page]
            page.Hide()
            page.tab.isCurrent = False
        except IndexError:
            pass
    
        #update current page
        self.current_page = n
        
        #show/hide pages
        try:
            page = self.pages[self.current_page]
            page.SetMinSize( (-1,page.GetBestSize()[1]) )
            page.Show()
            page.tab.isCurrent = True

        except IndexError:
            pass
        self.Parent.Layout()
        self.Layout()
        self.Thaw()
    
    def GetPageIndex(self, page):
        """
        Returns the page index of the ToolStripPage instance or None if not a page in 
        this ToolStrip
        """
        n = self.pages.index(page)
        return n
        
    def GetPageByLabel(self, label):
        """
        Returns the page with the label given or None
        """
        for page in self.pages:
            if page.Label == label:
                return page
        return None

    def GetTool(self, id):
        """
        Returns the tool withid given or None
        """
        for page in self.pages:
            res = page.GetTool(id)
            if res is not None:
                return res
        return None
    
    #address bar -  a full width toolpanel across the bottom of the strip
    def AddAddressBar(self, toolPanel=None, layout=LAYOUT_TOOLBAR_16x1):
        """
        Add an AddressBar to the bottom of the toolstrip this is a full width 
        ToolPanel.
        
        toolPanel - A ToolPanel instance to use as the address bar or None to 
                    create a new ToolPanel
        layout    - the layout to use if toolPanel is None.
        
        Returns: the ToolPanel instance used as the address bar
        """
        if self.addressBar is not None:
            raise Exception('AddressBar already exists - use GetAddressBar()')
        
        if toolPanel is None: #create a new panel
            self.addressBar = ToolPanel( self, -1, layout)
        elif isinstance( toolPanel, ToolPanel):
            self.addressBar = toolPanel
        else:
            raise ValueError('Expected a ToolPanel instance')
            
        self.addressBar.SetBackgroundColour(self.painter.page_bg)
        self._pagesizer.Add(self.addressBar, 0, wx.EXPAND)
        
        return self.addressBar

    def GetAddressBar(self):
        """
        Returns the address bar ToolPanel or None
        """
        return self.addressBar
    
#tabbar class a container holding tabs 
class ToolStripTabBar(wx.Panel):
    def __init__(self, parent, id=-1):
        """
        ToolStrip tabbar
        TODO:
            scrolling tabs when too many
            quick launch toolbar on right hand side.
        """
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_NONE)
        self.painter = parent.painter

        self.tabs = [] #list of tabs

        #set tab size according to label and font size
        textw,texth_max = self.GetTextExtent('yl') #get size of text
        size = (-1 , texth_max+4)
        self.SetInitialSize(size)
    
        #bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE,             self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
        self.Bind(wx.EVT_LEFT_DCLICK,      self.OnLeftDCLick)
        
    def AcceptsFocus(self):
        """ 
        Overloaded panel class method
        """
        return False

    def AddTab(self, label, longHelp=''):
        """
        Create a new tab for the page given
        """
        tab =  ToolStripTab( self, label, longHelp)
        self.tabs.append(tab)
    
        #adjust tabbar size if necessary
        w,h = self.GetMinSize()
        tw,th = tab.GetSize()
        if th>h:
            self.SetMinSize( (w,th) )
            
        #recalculate layout
        self.Layout()
        
        return tab
        
    def AddSpacer(self, width=20):
        """
        Add a spacer to the tab bar to seperate tab groups
        """
        self.tabs.append(width)
    
    def GetTab(self, n):
        """
        Get the nth tab
        """
        return self.tabs[n]
    
    def Layout(self):
        """
        Recalculate tab positions/sizes based upon tabbar size
        """
        #freeze while we do layout
        self.Freeze()
        
        #simple implementation just lays out lays out tabs in rows
        cw,ch = self.GetClientSize()        
        x = 0 #starting tab position
        for t in self.tabs:
            
            if isinstance(t, ToolStripTab) is True:
                if t.IsShown() is False:
                    pass
                else:
                    tw,th = t.GetSize()
                    y = ch-th
                    #set the tab position if necessary
                    ox,oy = t.GetPosition()
                    if ox!=x or oy!=y:
                        t.SetPosition((x,y))
                    #update x
                    x = x+tw
            else: #spacer
                x = x + t

        self.Thaw()
        self.Refresh()
    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Parent.painter.paintTabBar( dc, self, (0,0))
        
    def OnSize(self, event):
        self.Refresh(False) #do background
        self.Layout() #relayout
        event.Skip()
        
    def OnLeftDCLick(self, event):
        #collapse/expand toolstrip
        if self.Parent.IsCollapsed():
            self.Parent.Restore()
        else:
            self.Parent.Collapse()
        event.Skip()
     
# Tab classes
class ToolStripTab(wx.Control):
    """
    The tab class for ToolStrip pages
    """
    def __init__(self, parent, label='', longHelp=''):
        wx.Control.__init__(self, parent, id=-1, style=wx.BORDER_NONE)
        
        #set the font size to 9 point (hardcoded font size) 
        font = wx.SystemSettings.GetFont( wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize( 9 )
        self.SetFont( font )
        
        #attributes
        self.toolStrip = parent.Parent
        self.SetLabel(label)
        self.longHelp = longHelp
        self.isCurrent = False
        
        #set tab size according to label and font size
        textw,texth_max = self.GetTextExtent('yl') #get size of text
        textw,texth = self.GetTextExtent(self.Label) #get size of text
        size = (textw+22 , texth_max+4)
        self.SetInitialSize(size)
        
        #highlighting
        self.highlight = False
        self.hl_col = HL_BLUE

        #bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE,             self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)

        self.Bind(wx.EVT_LEFT_DOWN,        self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,          self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK,      self.OnLeftDCLick)
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

    def AcceptsFocus(self):
        """ 
        Overloaded base class method
        """
        return False
    
    def SetHighlight(self, flag=True, colour=HL_RED):
        """
        Enable or disable the tab highlighting
        """
        if isinstance(flag, bool) is False:
            raise ValueError('Expected True/False')
        self.highlight = flag
        
        #make sure it is a valid colour
        colour = wx.Colour(colour)
        self.hl_col = colour
        self.Refresh()
    
    def PopupMenu(self, menu, pt=None):
        """Pop up a menu for the dropdown"""
        if pt is None:
            w,h = self.GetSize()
            pt = (0,h)
        wx.Control.PopupMenu(self, menu, pt)
        
    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        self.toolStrip.painter.paintTab( self, self.isCurrent, hover, self.highlight)

    def OnMouseEnter(self, event):
        self.Refresh()
        if self.toolStrip.statusbar is not None:
            #Do this as enter can be called before exit!
            wx.CallAfter(self.toolStrip.statusbar.PushStatusText, self.longHelp)
        event.Skip()

    def OnMouseLeave(self, event):
        self.Refresh()
        if self.toolStrip.statusbar is not None:
            #Do this as enter can be called before exit!
            wx.CallAfter(PopStatusText, self.toolStrip.statusbar)
        event.Skip()

    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        self.CaptureMouse()
        event.Skip()

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            
            pt_win, pt = wx.FindWindowAtPointer()
            hover = pt_win is self
            
            #post event if mouse over button
            if hover:
                evt = EvtToolStripTabClick()
                evt.SetEventObject( self)
                wx.PostEvent(self, evt)
                
            self.Refresh(False)
        event.Skip()
        
    def OnLeftDCLick(self, event):
        #collapse/expand toolstrip
        if self.toolStrip.IsCollapsed():
            self.toolStrip.Restore()
        else:
            self.toolStrip.Collapse()
        event.Skip()
        
    def OnSize(self, event):
        self.Refresh()
        event.Skip()

# Page class
class ToolStripPage(wx.Panel):
    """
    Tool strip page  - a page of tool controls in the Toolstrip
    """
    def __init__(self, parent, id=-1):

        #check parent is a ToolStrip
        if isinstance( parent, ToolStrip) is False:
            raise ValueError('Expected a ToolStrip parent instance')
            
        #base class init
        wx.Panel.__init__(self, parent, id )
        self.SetDoubleBuffered(True)
        self.SetBackgroundColour(self.Parent.painter.page_bg)
        
        self.painter = parent.painter       #use toolstrip painter
        self.groups = []    #list of (group, proportion) toolcontainers on this page
        self.group_labels = {}    #dict of name: group objects

        #page highlighting
        self.highlight = False
        self.hl_col = HL_BLUE

        #bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE,             self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
        
    def AcceptsFocus(self):
        """ 
        Overloaded panel class method
        """
        return False

    @property
    def statusbar(self):
        """
        Return the parent statusbar
        """
        return self.Parent.statusbar
        
    def _draw_bg(self, dc, pos):
        """
        Internal painting method to allow children to paint the page's 
        background to the dc and appear transparent.
        dc - dc to draw to
        pos - position of child relative to page
        """
        self.painter.paintPage(dc, self, pos)
        
    def AcceptsFocus(self):
        """ 
        Overloaded panel class method
        """
        return False

    def Layout(self):
        """
        Recalculate group positions/sizes based upon page size
        """
        #freeze while we do layout
        self.Freeze()
        
        #get page size
        cw,ch = self.GetClientSize()
        #1st pass loop over groups and maximise
        tw = 0          #total width used
        resizable = []  #list of groups that may need resizing
        total_prop = 0  #sum of all proportion value for resizable groups
        for g, prop in self.groups:
            if g.IsShown():
                w,h = g.GetMaximisedSize()
                tw = tw+w
                if prop !=0:
                    resizable.append((g, prop))
                    total_prop = total_prop + prop

        #2nd pass minimize groups until the total width is ok or no more groups 
        #to minimise also ensure groups are maximised
        for g, prop in reversed(self.groups): #minimise from rhs
            if tw<cw:
                #total width is ok, make sure the group is maximised
                if g.IsMinimised():
                    g.MaximiseGroup()

            elif g.IsShown():
                ow,oh = g.GetMaximisedSize()
                if g.IsMinimised() is False:
                    g.MinimiseGroup()
                nw,nh = g.GetSize()
                tw = tw-ow+nw
                
        #3rd pass allocate any unused space to the groups or minimise groups
        excess = cw - tw
        if excess >0:
            for g,prop in resizable:
                if g.IsMinimised() is False:
                    w,h = g.GetMaximisedSize()
                    w = w + ((excess/total_prop)*prop)
                    g.Freeze()
                    g.SetSize( (w, h) )
                    g.Thaw()            
        
        #4th pass to position groups if needed and set page size.
        x = 0
        y = 2 #2px top border
        maxh = 0
        for g,prop in self.groups:
            if g.IsShown():
                ox,oy = g.GetPosition()
                if ox!=x or oy!=y:
                    g.SetPosition((x,y))
                w,h = g.GetSize()
                x = x+w
                if h>maxh:
                    maxh = h
        
        size = (-1, maxh+4)
        self.SetSize( size)
        self.SetMinSize( size)
        self.Thaw()
        self.Refresh()
      
    def SetTab(self, tab):
        """
        Called when adding a page to the ToolStrip to set the tab representing 
        this page
        """
        #store a reference to the tab for this page
        self.tab = tab
        self.tab.Bind( EVT_TOOLSTRIP_TABCLICK, self.OnTab)
        
    #---ToolStrip page interfaces-----------------------------------------------
    def SetLongHelp(self, longHelp):
        """
        Set the long help string
        """
        self.longHelp = longHelp

    def SetHighlight(self, flag=True, colour=HL_RED):
        """
        Enable or disable the page highlighting
        """
        if isinstance(flag, bool) is False:
            raise ValueError('Expected True/False')
        self.highlight = flag
        
        #make sure it is a valid colour
        colour = wx.Colour(colour)
        self.hl_col = colour
        self.Refresh()
        self.tab.SetHighlight(flag, colour)

    def AddGroup(self, layout=LAYOUT_RIBBON, label='', prop=0,  longHelp=''):
        """
        Add a group to the page
        """
        if label in self.group_labels:
            raise ValueError('ToolstripPage already has group with label: '+str(label))
            
        group = ToolStripGroup(self, -1, label, layout, longHelp)
        self.groups.append( (group, prop))
        self.group_labels[label] = group
        
        self.Layout()
        
        return group
        
    def GetGroup(self, n):
        """
        Get the group at position n
        """
        return self.groups[n][0]
    
    def GetGroupByLabel(self, label):
        """
        Return the group with the label given
        """
        if label in self.group_labels is False:
            raise ValueError('No group with label: '+str(label))
        return self.group_labels[label]
       
    def HidePage(self):
        """
        Hide the page and tab
        """
        self.Hide()
        self.tab.Hide()
        self.Parent.tabBar.Layout()
        
    def ShowPage(self):
        """
        Show the page and tab
        """
        self.tab.Show()
        self.Parent.tabBar.Layout()
        n = self.Parent.GetPageIndex(self)
        if n is None:
            raise Exception('Page is not in parent ToolStrip!?')
        self.Parent.SetPage(n)
        self.Parent.Refresh()
        
    #event handlers
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.painter.paintPage( dc, self)

    def OnSize(self, event):
        self.Refresh() #repaint background
        self.Layout() #adjust group layout

    def OnTab(self, event):
        #handler for tab clicks
        n = self.Parent.GetPageIndex(self)
        if n is None:
            raise Exception('Page is not in parent ToolStrip!?')
        self.Parent.SetPage(n)
        self.Parent.Refresh()
        
#group class - a ToolPanel subclass
class ToolStripGroup(ToolPanel):
    def __init__(self, page, id, label, layout, longHelp=''):
        """
        A collection of controls/tools in a group
        """
        #check parent is a ToolPanel
        if isinstance( page, ToolStripPage) is False:
            raise ValueError('Expected a ToolStripPage parent instance')

        ToolPanel.__init__(self, page, id, layout)
  
        #set the font size to size 8
        #font = wx.SystemSettings.GetFont( wx.SYS_DEFAULT_GUI_FONT)
        #font.SetPointSize( 8 )
        #self.SetFont( font )
        
        self.painter = page.painter #store ref to painter
        #remove _statusbar as using parent, ToolStrips setting
        del self._statusbar
        
        #group attributes
        self.page = page
        self.label = label

        #set the borders to include space for the label
        self.labelH = self.GetTextExtent('ypl')[1] -1
        self.labelW = self.GetTextExtent(self.label)[0] +12
        self.borders = [5,5, 0, self.labelH]
        self.longHelp = longHelp
        
        #overflow panel
        self.minimised = False #minimised flag
        self.overflow = TSGroupOverflow(self)
        
        #set the min size to include label
        min_w = self.labelW + self.borders[0] + self.borders[1]
        min_h = (self.rowN*self.rowH) + self.labelH
        if min_w < 60:
            min_w = 60 #absolute min for group.
        self.optSize= (min_w, min_h)
        self.SetMinSize( self.optSize )

        #bind event
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)

    def MinimiseGroup(self):
        """
        Minimise the group to the icon view
        """
        #print('in min', self.label)
        #reparent tools to the overflow
        for tool, hrows, wprop in self.tools:
            if isinstance(tool, int):
                pass
            else: 
                tool.Reparent(self.overflow)
            
        #enable the minimised view
        self.minimised = True
        #set the size of the group to just label width
        w = self.labelW
        if w<60:
            w = 60
        h = (self.rowN*self.rowH) + self.labelH
        self.SetMinSize( (w,h))
        self.SetSize( (w,h))
        
        #set the overflow size
        self.overflow.SetSize(self.optSize)
        
        #refresh
        self.Refresh()

    def MaximiseGroup(self):
        """
        Maximise the group to tool views
        """
        #print('in max', self.label)
        #close the popup if open
        self.overflow.Hide()
        
        #reparent tools
        for tool, hrows, wprop in self.tools:
            if isinstance(tool, int):
                pass
            else:
                tool.Reparent(self)
            
        #diable minimised view
        self.minimised = False
        #set the size of the group to the best size
        self.SetSize( self.optSize)
        self.SetMinSize( self.optSize)

    def IsMinimised(self):
        """
        Returns True/False flag indicated the group is minimised
        """
        return self.minimised
        
    def GetMaximisedSize(self):
        """
        Returns the maximised size of the group
        """
        return self.optSize
    
    def ShowGroupOverflow(self):
        self.overflow.Show()

    def HideGroupOverflow(self):
        self.overflow.Hide()

    #---overloaded ToolPanel methods--------------------------------------------
    def Realize(self):
        """
        Called after all tools have been added to the ToolPanel positions/sizes
        the tools.
        """
        #print('in realize:',self.label)

        #make sure all tools have the correct parent as any tools added since
        #the last call will still be parented to the panel rather than overflow
        #if the panel is in it's minimsied state.
        if self.minimised:
            self.MinimiseGroup()
            
        ToolPanel.Realize(self)
        
        #set the size of the overflow window
        self.overflow.SetInitialSize( self.optSize)

    @property
    def statusbar(self):
        """
        Return the parent statusbar
        """
        return self.Parent.statusbar
        
    def SetStatusBar(self, statusbar):
        """
        Set the status bar to display help strings
        """
        raise Exception('Cannot set statusbar using parent ToolPanel settings')
    
    def _draw_bg(self, dc, pos):
        """
        Internal painting method to allow children to paint the group's 
        background to the dc and appear transparent.
        dc - dc to draw to
        pos - position of child relative to the group
        """
        self.painter.paintGroup(dc, self, pos)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        if self.minimised:
            self.painter.paintMinGroup( dc, self )
        else:
            self.painter.paintGroup(dc, self, (0,0))
            
    def OnLeave(self, event):
        
        #print('on leave', self.label, self.HasCapture())
        #update statusbar
        if self.statusbar is not None:
            #Do this as enter can be called before exit!
            wx.CallAfter(PopStatusText, self.statusbar)

        #if overflow shown - check if leaving to the overflow
        if self.overflow.IsShown():
            
            #check if mouse inside group or overflow
            pos = self.ClientToScreen(event.GetPosition())
            
            group_rect = self.GetScreenRect()
            in_group = group_rect.Contains(pos)
            
            overflow_rect = self.overflow.GetScreenRect()
            in_overflow = overflow_rect.Contains(pos)
                        
            #close overflow if leaving group or overflow.
            if (in_group is False) and (in_overflow is False):
                self.HideGroupOverflow()
                self.Refresh()
        else:
            self.Refresh()
            

    def OnEnter(self, event):
        
        #print('on enter', self.label, self.HasFocus())
                
        #update statusbar
        if self.Parent.statusbar is not None:
            #Do this as enter can be called before exit!
            wx.CallAfter(self.statusbar.PushStatusText, self.longHelp)
            
        #if minimised show overflow
        if self.minimised and self.overflow.IsShown() is False:
            self.ShowGroupOverflow()
    
    def OnSize(self, event):
        #print('in onsize', self.label)
        if self.minimised is False:
            self.Layout()
        self.Refresh(False)
        

#group overflow - popup window class to reparent groups to when minimised
#using a frame to avoid issues with focus
class TSGroupOverflow(wx.Frame):
    def __init__(self, group):
        """
        Overflow panel to display minimised ToolGroups
        """
        wx.Frame.__init__(self, group, style=wx.BORDER_SIMPLE|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR)
        
        self.group = group
        self.page = group.page
        self.painter = group.painter
        self.rowN = group.rowN
        self.rowH = group.rowH
        self.labelH = group.labelH
        self.label = group.label
        
        if self.HasCapture():
            self.ReleaseMouse()
            
        #bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE,  self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        #self.Bind(wx.EVT_KILL_FOCUS, self.group.OnLeave)
        
    def Show(self):
        
        #redraw group icon with button down
        self.group.Refresh()

        #show the popup
        w,h = self.group.GetMaximisedSize()
        self.SetSize((w,h))
        spos = self.group.ClientToScreen( (0, h-3) )
        self.SetPosition(spos)
        wx.Frame.Show(self)
        self.SetFocus()

    def Hide(self):
        wx.Frame.Hide(self)
        self.group.Refresh()
    
    #--- Methods/attributes required by tools ----------------------------------
    @property
    def statusbar(self):
        """
        Return the parent statusbar
        """
        return self.group.statusbar
        
    def _draw_bg(self, dc, pos):
        """
        Internal painting method to allow children to paint the group's 
        background to the dc and appear transparent.
        dc - dc to draw to
        pos - position of child relative to the group overflow
        """ 
        x,y = pos
        self.painter.paintGroupOverflow(dc, self, pos)
        
    #--- events ----------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.painter.paintGroupOverflow(dc, self, (0,0))
        
    def OnSize(self, event):
        self.Refresh(False)
        event.Skip()      
        
    def OnLeave(self, event):
        #if overflow shown - check if leaving to the overflow
        if self.IsShown():
            
            #check if mouse inside group or overflow
            pos = self.ClientToScreen(event.GetPosition())
            
            group_rect = self.group.GetScreenRect()
            in_group = group_rect.Contains(pos)
            
            overflow_rect = self.GetScreenRect()
            in_overflow = overflow_rect.Contains(pos)
                        
            #close overflow if leaving group or overflow.
            if (in_group is False) and (in_overflow is False):
                self.Hide()

#-------------------------------------------------------------------------------
# Tools with adjustable sizes
#-------------------------------------------------------------------------------
class ToolItem(wx.Control):
    """
    Base class for toolpanel/toolstrip tools
    """
    def __init__(self, parent, id=-1, size=ITEM_SMALL, shortHelp='', longHelp=''):

        if isinstance( parent, ToolPanel) is False:
            raise ValueError('Expected a ToolPanel parent instance')

        wx.Control.__init__(self, parent, id, style=wx.BORDER_NONE)
        self.itemSize = size
        
        #set tool size according to the parent ToolContainer max size
        h = parent.rowH*size
        self.SetInitialSize( (-1,h) )
        self.SetMaxSize(  (-1,h) )
        
        #set the font size
        font = sysfont = wx.SystemSettings.GetFont( wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize( 8)
        self.SetFont( font )
        
        #bind event
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnToolLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnToolEnter)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)

        #set help strings
        self.SetShortHelp( shortHelp)
        self.SetLongHelp( longHelp)

    def AcceptsFocus(self):
        """ 
        Overloaded base class method
        """
        return False
        
    def SetShortHelp(self, shortHelp):
        """
        Set the short help string
        """
        self.SetToolTip(shortHelp)

    def SetLongHelp(self, longHelp):
        """
        Set the long help string
        """
        self.longHelp = longHelp
        
    def SetToolSize(self, size):
        """
        Call to set the tool size
        """
        self.SetInitialSize( size )
        self.SetMaxSize(  size )

    def SetToolWidth(self, w):
        """
        Call to set the tool width
        """
        size = self.GetSize()
        new = ( w, size[1] )
        self.SetInitialSize( new )
        self.SetMaxSize(  new )

    def SetToolHeight(self, h):
        """
        Called by the ToolPanel when changing tool height
        """
        size = self.GetSize()
        new = ( size[0], h )
        self.SetInitialSize( new )
        self.SetMaxSize(  new )

    def OnToolLeave(self, event):
        if self.Parent.statusbar is not None:
            #Do this as enter can be called before exit!
            wx.CallAfter(PopStatusText, self.Parent.statusbar)
        event.Skip()

    def OnToolEnter(self, event):
        if self.Parent.statusbar is not None:
            #Do this as enter can be called before exit!
            wx.CallAfter(self.Parent.statusbar.PushStatusText, self.longHelp)
        event.Skip()



class StaticText(ToolItem):
    """
    A static text control with the same background as the ToolPanel/ToolStrip class
    """
    def __init__(self, parent, id, size, label):
        ToolItem.__init__(self, parent, id, size)

        self.Label = label
        w,h = self.GetTextExtent(self.Label)
        self.SetToolWidth(w+4)
       
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        w, h = self.GetClientSize()        

        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
        
        #draw text
        dc.SetFont(self.GetFont())
        tw,th = self.GetTextExtent(self.Label)
        x = (w-tw)/2
        y = (h-th)/2
        dc.DrawText(self.Label, x, y)

class Seperator(ToolItem):
    """
    A seperator control with the gradient background ToolPanel class
    """
    def __init__(self, parent, size):
        ToolItem.__init__(self, parent, -1, size)
        self.SetToolWidth(8)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):

        dc = wx.BufferedPaintDC(self)
        w, h = self.GetClientSize()        

        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
    
        #draw lines
        dc.SetPen(wx.Pen('#A2A2A2',width=1))
        dc.DrawLine( (w/2)-1, 4, (w/2)-1, h-5)
        dc.SetPen(wx.Pen('#FFFFFF',width=1))
        dc.DrawLine( (w/2), 4, (w/2), h-5)

class ButtonItem(ToolItem):
    """
    A bitmap button tool item.
    """
    def __init__(self,parent,id=-1, size=ITEM_SMALL, bmp=wx.NullBitmap):

        ToolItem.__init__(self, parent, id, size)

        self.down = False  #button is down (pressed)
        self.bmp = None
        self.bmp_disabled = None
        
        #set the bitmap
        self.SetBitmap(bmp)

        #set width to square
        bw = (bmp.GetWidth() + 8) #get bitmap height with border
        self.SetToolWidth(bw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Bind(wx.EVT_LEFT_DOWN,        self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,          self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK,      self.OnLeftDown)
        self.Bind(wx.EVT_MOTION,           self.OnMotion)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

    def SetBitmap(self, bmp):
        """
        Set the bitmap
        """
        #check bitmap size and parent toolcontainer size
        w,h = bmp.GetSize()
        max = (self.itemSize*self.Parent.bmpSize)
        if h>max:
            raise Exception('Tool height should be samller than 2xparent bmpSize')
        
        #store bitmap internally
        self.bmp = bmp
        self.bmp_disabled = bmp.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()

        self.Refresh()
        
    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
    
        #draw bezel
        self._paintBezel(dc)
        
        #draw bitmap
        self._paintBitmap(dc)
    
    def _paintBezel(self,dc):
        w, h = self.GetClientSize()        

        #draw bezel
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        if hover is False and self.down is False:
            pass

        else:
            if self.IsEnabled() is False:
                state = wx.CONTROL_DISABLED
            elif hover and self.down is False:
                state = wx.CONTROL_CURRENT
            elif hover and self.down is True:
                state = wx.CONTROL_PRESSED
            elif self.down is True:
                state = wx.CONTROL_PRESSED
            #draw
            rect = wx.Rect(0, 0, w, h)
            wx.RendererNative.Get().DrawPushButton(self, dc, rect, state)

    def _paintBitmap(self, dc):
        w, h = self.GetClientSize()        

        #draw bitmap
        bmp = self.bmp
        if not self.IsEnabled():
            bmp = self.bmp_disabled
        bw,bh = bmp.GetWidth(), bmp.GetHeight()
        if self.down is True:
            dx = dy = 1
        else:
            dx = dy = 0
        hasMask = bmp.GetMask() != None
        
        #align bitmap at top regardless of height of button (for ribbon style tall buttons)
        dc.DrawBitmap(bmp, (w-bw)/2+dx, 4+dy, hasMask)

    def OnMouseEnter(self, event):
        self.Refresh()
        event.Skip()

    def OnMouseLeave(self, event):
        self.Refresh(False)
        event.Skip()

    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        self.down = True
        self.CaptureMouse()
        self.Refresh(False)
        event.Skip()

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down is True:    # if the button was down when the mouse was released...
                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                wx.PostEvent(self.Parent, evt) 
                
                #if parent window is an overflow close it
                #if isinstance(self.Parent, TSGroupOverflow):
                #    self.Parent.Hide()
                    
            self.down = False
            self.Refresh(False)

    def OnMotion(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return

        if event.LeftIsDown() and self.HasCapture():
            #check if hovering over this button
            x,y = event.GetPosition()
            w,h = self.GetClientSize()
            if x<w and x>=0 and y<h and y>=0:
                #over button
                self.down = True
            else:
                #not over button
                self.down = False
            self.Refresh(False)
        event.Skip()
    
class ToggleItem(ButtonItem):
    """
    A togglable bitmap button item.
    """
    def __init__(self, parent,id=-1,size=ITEM_SMALL, bmp=wx.NullBitmap):

        ButtonItem.__init__(self, parent, id, size, bmp)
        self.state = False  #check/toggle state
    
    def SetToggle(self, flag):
        if isinstance(flag, bool) is False:
            raise ValueError('Expected a boolean')
        self.state = flag
        self.down = flag
        self.Refresh()

    def GetToggle(self):
        return self.state

    #---events------------------------------------------------------------------    
    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        #(toggle state= not self.state)
        self.down = not self.state
        self.CaptureMouse()
        self.SetFocus()
        self.Refresh()

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down != self.state:
                #set state
                self.state = not self.state
                
                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                evt.SetInt( int(self.state))
                wx.PostEvent(self.Parent, evt)  

            self.Refresh()

    def OnMotion(self, event):
        if not self.IsEnabled():
            return
        if event.LeftIsDown() and self.HasCapture():
            x,y = event.GetPosition()
            w,h = self.GetClientSize()
            if x<w and x>=0 and y<h and y>=0:
                #over button flip state
                self.down = not self.state
                self.Refresh()
                return
            if (x<0 or y<0 or x>=w or y>=h):
                #not over button set back to state
                self.down = self.state
                self.Refresh()
                return
        event.Skip()

class DropDownItem(ToggleItem):
    """
    A bitmap button item with a drop down button for menus etc positioned either 
    to the left or below the item.
    """
    def __init__(self, parent, id=-1, size=ITEM_SMALL, bmp=wx.NullBitmap, direction=wx.HORIZONTAL):

        ToggleItem.__init__(self, parent, id, size, bmp)
        
        self.dir = direction
        self._showDiv = True # show the dropdown division and toggle the check stage - on by default
        bmpsize = bmp.GetSize()    
        
        #set size to appropiate size for the bitmap used + drop button  
        if self.dir == wx.HORIZONTAL:
            self.but_w = bmpsize[0]+6     
            self.drp_w = 14# int(bmpsize[0]*0.5)
            w = self.but_w+ self.drp_w 
        elif self.dir == wx.VERTICAL:
            self.but_w = bmpsize[0]+8     
            self.drp_w = (parent.rowH*size)-4-(parent.bmpSize*2) #use remaining height
            w = self.but_w
        else:
            raise ValueError('Unknown direction, expected: wx.VERTICAL or wx.HORIZONTAL')
        self.SetToolWidth(w)

    def ShowToggleDivision(self, on=True):
        """
        Set wether to show the toggle button division
        """
        if isinstance(on, bool) is False:
            raise ValeuError
        self._showDiv = on  #make sure we set a bool

    def PopupMenu(self, menu, pt=None):
        """Pop up a menu for the dropdown"""
        if pt is None:
            w,h = self.GetSize()
            pt = (0,h)
        wx.Control.PopupMenu(self, menu, pt)
        self.SetToggle(False)
                         
        #if parent window is an overflow close it
        if isinstance(self.Parent, TSGroupOverflow):
            self.Parent.Hide()
        
    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
        
        #draw bezel
        self._paintBezel(dc)
        
        #draw bitmap
        self._paintBitmap(dc)
        
        #draw dropdown
        if self.dir == wx.HORIZONTAL:
            self._paintDropDownH(dc)
        else:
            self._paintDropDownV(dc)
            
    def _paintBitmap(self, dc):
        w, h = self.GetClientSize()        

        #draw bitmap
        bmp = self.bmp
        if not self.IsEnabled():
            bmp = self.bmp_disabled
        bw,bh = bmp.GetWidth(), bmp.GetHeight()
        if self.down is True:
            dx = dy = 1
        else:
            dx = dy = 0
        hasMask = bmp.GetMask() != None
        
        #align bitmap at top regardless of height of button (for ribbon style tall buttons)
        if self.dir == wx.HORIZONTAL:
            w = self.but_w #use width excluding dropdown
        dc.DrawBitmap(bmp, (w-bw)/2+dx, 4+dy, hasMask)

    def _paintDropDownH(self, dc):
        w, h = self.GetClientSize()        

        #if mouse over the control draw the dividing line
        x1 = self.but_w -1
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        if (hover or self.down) and self._showDiv:
            #draw partial vertical line
            dc.SetPen(wx.Pen('#A2A2A2',width=1))
            dc.DrawLine( x1, 8, x1, h-8)

        #draw dropdown
        #Do dropdown
        #   -arrs  x0  +arrs
        #        #######     y0
        #         #####          (height/2) -2
        #          ###
        #           #
        #       (width/2) -1
        arrs = 3
        x0 = x1 + (self.drp_w/2)
        y0 = (h/2) - arrs//2
        dc.SetPen(wx.Pen('#787878',width=1))
        dc.SetBrush(wx.Brush( '#787878' ))
        dc.DrawPolygon(( (x0-arrs, y0), (x0+arrs, y0), (x0, y0+arrs) ))
        
    def _paintDropDownV(self, dc):
        w, h = self.GetClientSize()        
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        #if mouse over the control draw the dividing line
        y1 = h-self.drp_w+1
        if (hover or self.down) and self._showDiv:
            #draw partial horizontal line
            dc.SetPen(wx.Pen('#A2A2A2',width=1))
            dc.DrawLine( 8, y1, w-8, y1)
            
        #draw dropdown
        #Do dropdown
        #   -arrs   x0  +arrs
        #        #######     y0
        #         #####          (height/2) -2
        #          ###
        #           #
        #       (width/2) -1
        arrs = 3
        x0 = w/2
        y0 = y1+4
        dc.SetPen(wx.Pen('#787878',width=1))
        dc.SetBrush(wx.Brush( '#787878' ))
        dc.DrawPolygon(( (x0-arrs, y0), (x0+arrs, y0), (x0, y0+arrs) ))

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down != self.state:

                #Check if it is over the dropdown or button
                x,y = event.GetPosition()
                w,h = self.GetSize()
                if self.dir ==wx.HORIZONTAL:
                    rect = wx.Rect( self.but_w, 0, self.drp_w, h)
                else:
                    rect = wx.Rect( 0, h-self.drp_w, w, self.drp_w)
                    
                pt = self.ScreenToClient(wx.GetMousePosition())
                if rect.Contains(pt):
                    #set toggle state only if on dropdown
                    self.state = not self.state
                elif self._showDiv is False:
                    #or if show division is false
                    self.state = not self.state
                else:
                    self.down = not self.down
                    self.state = False
                    
                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                evt.SetInt( int(self.state))
                wx.PostEvent(self.Parent, evt)  
                
                #if a normal click not a dropdown and parent window is an overflow close it
                #if (not self.state) and isinstance(self.Parent, TSGroupOverflow):
                #    self.Parent.Hide()

            self.Refresh()

#%%-----------------------------------------------------------------------------
# Small label tools - 1 row height - horizontal label
#-------------------------------------------------------------------------------
class sLabelItem(ButtonItem):
    """
    A small bitmap button with label and optional dropdown arrow.
    """
    def __init__(self, parent,id=-1,bmp=wx.NullBitmap, label=''):

        ButtonItem.__init__(self, parent, id, ITEM_SMALL, bmp)
        
        #internal attributes
        self.Label = label #label string
        self.SetLabel(label) #sets size
        self.down = False  #button is down (pressed)
        self.has_dropdown = False #has a dropdown arrrow added to label
    
    def PopupMenu(self, menu, pt=None):
        """Pop up a menu for the dropdown"""
        if pt is None:
            w,h = self.GetSize()
            pt = (0,h)
        wx.Control.PopupMenu(self, menu, pt)
        self.SetToggle(False)

    def SetLabel(self, label=''):
        """Set the label"""
        self.Label = label
        tw,th = self.GetTextExtent(self.Label)
        self.SetToolWidth( self.Parent.rowH + tw + 10) #+10 space for dropdown arrow
        
    def SetDropdown(self, flag=True):
        """
        Add a dropdown arrow to the end of the label
        """
        self.has_dropdown = bool(flag)
    
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        
        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
        
        #draw bezel
        self._paintBezel(dc)
        #draw bitmap
        self._paintBitmap(dc)
        #draw label
        self._paintLabel(dc)
    
    def _paintBezel(self, dc):
        w, h = self.GetClientSize()        

        #draw bezel
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        if hover is False and self.down is False:
            pass

        else:
            if self.IsEnabled() is False:
                state = wx.CONTROL_DISABLED
            elif hover and self.down is False:
                state = wx.CONTROL_CURRENT
            elif hover and self.down is True:
                state = wx.CONTROL_PRESSED
            elif self.down is True:
                state = wx.CONTROL_PRESSED
            #draw
            rect = wx.Rect(0, 0, w, h)
            wx.RendererNative.Get().DrawPushButton(self, dc, rect, state)

    def _paintBitmap(self, dc):
        w, h = self.GetClientSize()        

        #draw bitmap
        bmp = self.bmp
        if not self.IsEnabled():
            bmp = self.bmp_disabled
        bw,bh = bmp.GetWidth(), bmp.GetHeight()
        if self.down is True:
            dx = dy = 1
        else:
            dx = dy = 0
            
        x0 = (h-bh)//2 #centered on lhs (use height here as normal button is square)
        hasMask = bmp.GetMask() != None
        dc.DrawBitmap(bmp, x0+dx, ((h-bh)//2)+dy, hasMask)

    
    def _paintLabel(self, dc):
        w, h = self.GetClientSize()        

        #draw label
        x0 = h +1 #move label over to edge of square
        #setup
        dc.SetFont(self.GetFont())     
        dc.SetPen(wx.Pen('#000000',width=1))
        dc.SetBrush(wx.Brush( '#000000' ))   
        dc.SetTextForeground( '#000000')
        rect =  (x0,2,w-2,h-2)
        dc.DrawLabel( self.Label, rect, alignment=wx.ALIGN_CENTER_VERTICAL, indexAccel=-1)

        #draw arrow
        if self.has_dropdown is True:
            arrs = 3 #half width of arrow
            tw,th = dc.GetTextExtent(self.Label)
            ax = x0 + tw +1
            ay = ((h-2)//2) -2   #2px above center of line
            dc.DrawPolygon(( (ax-arrs, ay), (ax+arrs, ay), (ax, ay+arrs) ))

class sLabelToggleItem(sLabelItem):
    """
    A togglable bitmap button item.
    """
    def __init__(self, parent,id=-1,bmp=wx.NullBitmap, label=''):

        sLabelItem.__init__(self, parent, id, bmp,label)
        self.state = False  #check/toggle state
    
    def SetToggle(self, flag):
        if isinstance(flag, bool) is False:
            raise ValueError('Expected a boolean')
        self.state = flag
        self.down = flag
        self.Refresh()

    def GetToggle(self):
        return self.state

    #---events------------------------------------------------------------------    
    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        #(toggle state= not self.state)
        self.down = not self.state
        self.CaptureMouse()
        self.SetFocus()
        self.Refresh()

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down != self.state:
                #set state
                self.state = not self.state
                
                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                evt.SetInt( int(self.state))
                wx.PostEvent(self.Parent, evt)  
            self.Refresh()

    def OnMotion(self, event):
        if not self.IsEnabled():
            return
        if event.LeftIsDown() and self.HasCapture():
            x,y = event.GetPosition()
            w,h = self.GetClientSize()
            if x<w and x>=0 and y<h and y>=0:
                #over button flip state
                self.down = not self.state
                self.Refresh()
                return
            if (x<0 or y<0 or x>=w or y>=h):
                #not over button set back to state
                self.down = self.state
                self.Refresh()
                return
        event.Skip()
 
class sLabelDropDown(sLabelToggleItem):
    """
    A bitmap button item with a drop down button for menus etc.
    """
    def __init__(self, parent,id=-1, bmp=wx.NullBitmap, label=''):

        sLabelToggleItem.__init__(self, parent, id, bmp, label)

    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        
        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
        
        #draw bezel
        self._paintBezel(dc)
        #draw bitmap
        self._paintBitamp(dc)
        #draw label
        self._paintLabel(dc)
    
        #if mouse over the control draw the dividing line
        x1 = self.but_w -2
        w = self.but_w -1 + self.drp_w
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        if hover or self.down:
            #draw partial vertical line
            dc.SetPen(wx.Pen('#A2A2A2',width=1))
            dc.DrawLine( x1, 6, x1, h-6)

    def _paintLabel(self, dc):
        """Overloaded to draw dividing line"""
        sLabelToggleItem._paintLabel(self, dc)

        #seperator line - if mouse over the control draw the dividing line
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        if hover or self.down:
            w, h = self.GetClientSize()        
            x0 = h +1 #move label over to edge of square
            #draw partial vertical line
            dc.SetPen(wx.Pen('#A2A2A2',width=1))
            dc.DrawLine( x0, 0, x0, h)
            
    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down != self.state:

                #Check if it is over the dropdown or button
                x,y = event.GetPosition()
                w,h = self.GetSize()
                rect = wx.Rect( self.but_w, 0, self.drp_w, h)
                pt = self.ScreenToClient(wx.GetMousePosition())
                if rect.Contains(pt):
                    #set toggle state only if on dropdown
                    self.state = not self.state
                else:
                    self.down = not self.down

                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                evt.SetInt( int(self.state))
                wx.PostEvent(self.Parent, evt)  

                #if a normal click not a dropdown and parent window is an overflow close it
                #if (not self.state) and isinstance(self.Parent, TSGroupOverflow):
                #    self.Parent.Hide()
                    
            self.Refresh()

#%%-----------------------------------------------------------------------------
# Large Tools  - 3x row height
#-------------------------------------------------------------------------------
class lLabelItem(ToolItem):
    """
    A bitmap button with label tool item:
    The bitmap needs to be 2x the bitmap size with
    """
    def __init__(self,parent,id=-1, bmp=wx.NullBitmap, label=''):

        ToolItem.__init__(self, parent, id, size=ITEM_LARGE,)
        
        #internal attributes
        self.Label = label #label string
        self.down = False  #button is down (pressed)
        self.has_dropdown = False #has a dropdown arrrow added to label
        self.bmp = None
        self.bmp_disabled = None
        
        #set the bitmap
        self.SetBitmap(bmp)
        
        #set size to optimium width for the bitmap
        h = self.Parent.rowH *3
        w = self.Parent.rowH *2
        tw,th = self.GetTextExtent(self.Label)
        if tw>w:
            w = tw+2
        self.SetToolSize( (w,h) )
        
        self.sep_y =self.Parent.rowH *2 -6 #start of label region

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN,        self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,          self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK,      self.OnLeftDown)
        self.Bind(wx.EVT_MOTION,           self.OnMotion)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

    def SetBitmap(self, bmp):
        """
        Set the bitmap
        """
        #check bitmap size and parent toolcontainer size
        w,h = bmp.GetSize()
        if h>2*(self.Parent.rowH-6) or w>2*(self.Parent.rowH-6):
            raise Exception('Tool bitmap size + border = greater than 2x row height')
        
        #store bitmap internally
        self.bmp = bmp
        self.bmp_disabled = bmp.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()

        self.Refresh()

    def PopupMenu(self, menu, pt=None):
        """Pop up a menu for the dropdown"""
        if pt is None:
            w,h = self.GetSize()
            pt = (0,h)
        wx.Control.PopupMenu(self, menu, pt)
        self.SetToggle(False)

        #if parent window is an overflow close it
        if isinstance(self.Parent, TSGroupOverflow):
            self.Parent.Hide()
            
    def SetDropdown(self, flag=True):
        """
        Add a dropdown arrow to the end of the label
        """
        self.has_dropdown = bool(flag)

    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
        
        #draw bezel
        self._paintBezel(dc)
        
        #draw bitmap
        self._paintBitmap(dc)
        
        #draw label
        self._paintLabel(dc, self.has_dropdown)
        
    def _paintBezel(self, dc):
        w, h = self.GetClientSize()        
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self
        if hover is False and self.down is False:
            pass
        else:
            if self.IsEnabled() is False:
                state = wx.CONTROL_DISABLED
            elif hover and self.down is False:
                state = wx.CONTROL_CURRENT
            elif hover and self.down is True:
                state = wx.CONTROL_PRESSED
            elif self.down is True:
                state = wx.CONTROL_PRESSED
            #draw
            rect = wx.Rect(0, 0, w, h)
            wx.RendererNative.Get().DrawPushButton(self, dc, rect, state)

    def _paintBitmap(self,dc):
        w, h = self.GetClientSize()        
        rowH = self.Parent.rowH
        
        #draw bitmap
        bmp = self.bmp
        if not self.IsEnabled():
            bmp = self.bmp_disabled
        bw,bh = bmp.GetSize()
        if self.down is True:
            dx = dy = 1
        else:
            dx = dy = 0
        hasMask = bmp.GetMask() != None
        
        dc.DrawBitmap(bmp, (w-bw)/2+dx, h-(2*rowH)-(bh/2)+dy, hasMask)
        
    def _paintLabel( self, dc, dropdown = False):
        """
        Paint the label and optionally a dropdown arrow
        """
        #draw label and dropdown
        #Do dropdown
        #   -arrs  x0  +arrs
        #        #######     y0
        #         #####          (height/2) -2
        #          ###
        #           #
        #       (width/2) -1
        w, h = self.GetClientSize()   
        arrs = 3 #half width of arrow
     
        #space available for each line label
        lh = (h-self.sep_y-2)//2     
        
        #y positions of each line
        y0 = self.sep_y+1 #top of 1st line
        y1 = self.sep_y+lh #top of 2nd line
        
        #setup
        dc.SetFont(self.GetFont())     
        dc.SetPen(wx.Pen('#000000',width=1))
        dc.SetBrush(wx.Brush( '#000000' ))   
        dc.SetTextForeground( '#000000')

        #determine how many label lines and where to draw labels/arrow
        lines = self.Label.splitlines()
        nlines = len(lines)
        
        if nlines==0:
            #No label
            #draw arrow only
            if dropdown is True:
                ax = w//2
                ay = self.sep_y + lh -2 #2px above center of label area
                dc.DrawPolygon(( (ax-arrs, ay), (ax+arrs, ay), (ax, ay+arrs) ))
            
        elif nlines==1:
            #single line label - arrow on next line
            #draw label
            rect =  (1,y0,w-2,h-lh)
            dc.DrawLabel( lines[0], rect, alignment=wx.ALIGN_TOP|wx.ALIGN_CENTER_HORIZONTAL, indexAccel=-1)
            
            #draw arrow
            if dropdown is True:
                ax = w//2
                ay = y1 + (lh//2 ) -2   #2px above center of 2nd line
                dc.DrawPolygon(( (ax-arrs, ay), (ax+arrs, ay), (ax, ay+arrs) ))
            
        else:
            #two line label - arrow at end of 2nd line
            
            #draw label line 1
            rect =  (1,y0,w-2,lh)
            dc.DrawLabel( lines[0], rect, alignment=wx.ALIGN_TOP|wx.ALIGN_CENTER_HORIZONTAL, indexAccel=-1)
            
            #draw label line 2
            if dropdown:
                #center text and label
                tw,th = dc.GetTextExtent(self.Label.splitlines()[1])
                rect =  ((w//2)-(tw//2)-arrs, y1,tw+(2*arrs)+2, lh)
                dc.DrawLabel( lines[1], rect, alignment=wx.ALIGN_TOP, indexAccel=-1)
            else:
                #center text only
                rect =  (1,y1,w-2,lh)
                dc.DrawLabel( lines[1], rect, alignment=wx.ALIGN_TOP|wx.ALIGN_CENTER_HORIZONTAL, indexAccel=-1)
            
            #draw arrow
            if dropdown is True:
                ax = (w//2) + (tw//2) + arrs
                ay = y1+(lh//2) -2 #2px above center of 2nd line
                dc.DrawPolygon(( (ax-arrs, ay), (ax+arrs, ay), (ax, ay+arrs) ))
       
    def OnMouseEnter(self, event):
        self.Refresh(False)
        event.Skip()

    def OnMouseLeave(self, event):
        self.Refresh(False)
        event.Skip()

    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        self.down = True
        self.CaptureMouse()
        self.Refresh(False)
        event.Skip()

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down is True:    # if the button was down when the mouse was released...
                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                wx.PostEvent(self.Parent, evt) 
                
                #if parent window is an overflow close it, unless this is a 
                #popup button in which case the popup should close the dropdown
                #if (self.has_dropdown is False) and isinstance(self.Parent, TSGroupOverflow):
                #    self.Parent.Hide()
                
            self.down = False
            self.Refresh(False)

    def OnMotion(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return

        if event.LeftIsDown() and self.HasCapture():
            #check if hovering over this button
            x,y = event.GetPosition()
            w,h = self.GetClientSize()
            if x<w and x>=0 and y<h and y>=0:
                #over button
                self.down = True
            else:
                #not over button
                self.down = False
            self.Refresh(False)
        event.Skip()

class lLabelToggleItem(lLabelItem):
    """
    A togglable bitmap button  with label tool item.
    """
    def __init__(self, parent,id=-1,bmp=wx.NullBitmap, label=''):

        lLabelItem.__init__(self, parent, id, bmp, label)
        self.state = False  #check/toggle state
    
    def SetToggle(self, flag):
        if isinstance(flag, bool) is False:
            raise ValueError('Expected a boolean')
        self.state = flag
        self.down = flag
        self.Refresh()

    def GetToggle(self):
        return self.state

    #---events------------------------------------------------------------------    
    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        #(toggle state= not self.state)
        self.down = not self.state
        self.CaptureMouse()
        self.SetFocus()
        self.Refresh()

    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down != self.state:
                #set state
                self.state = not self.state
                
                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                evt.SetInt( int(self.state))
                wx.PostEvent(self.Parent, evt)  
  
                #if parent window is an overflow close it, unless this is a 
                #popup button in which case the popup should close the dropdown
                #if (self.has_dropdown is False) and isinstance(self.Parent, TSGroupOverflow):
                #    self.Parent.Hide()
                
            self.Refresh()

    def OnMotion(self, event):
        if not self.IsEnabled():
            return
        if event.LeftIsDown() and self.HasCapture():
            x,y = event.GetPosition()
            w,h = self.GetClientSize()
            if x<w and x>=0 and y<h and y>=0:
                #over button flip state
                self.down = not self.state
                self.Refresh()
                return
            if (x<0 or y<0 or x>=w or y>=h):
                #not over button set back to state
                self.down = self.state
                self.Refresh()
                return
        event.Skip()

class lLabelDropDown(lLabelToggleItem):
    """
    A bitmap button item  with a label with a drop down button for menus etc.
    """
    def __init__(self, parent,id=-1, bmp=wx.NullBitmap, label=''):

        lLabelToggleItem.__init__(self, parent, id, bmp, label)
        self.has_dropdown = True #draw dropdown arrow with label

    #---events------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        #draw background via parent container to ensure matching background
        pos = self.GetPosition()
        self.Parent._draw_bg(dc, pos)
        
        #draw bezel
        self._paintBezel(dc)
        
        #draw bitmap
        self._paintBitmap(dc)
        
        #seperator line - if mouse over the control draw the dividing line
        w, h = self.GetClientSize()  
        pt_win, pt = wx.FindWindowAtPointer()
        hover = pt_win is self      
        if hover or self.down:
            #draw partial vertical line
            dc.SetPen(wx.Pen('#A2A2A2',width=1))
            dc.DrawLine( 1, self.sep_y, w-2, self.sep_y)
            
        #add label and dropdown arrow
        self._paintLabel(dc, self.has_dropdown)
         
    def OnLeftUp(self, event):
        if not self.IsEnabled() or not self.HasCapture():
            return
        if self.HasCapture():
            self.ReleaseMouse()
            if self.down != self.state:

                #Check if it is over the label or button
                x,y = event.GetPosition()
                w,h = self.GetSize()
                rect = wx.Rect( 0, self.sep_y, w, h-self.sep_y)
                pt = self.ScreenToClient(wx.GetMousePosition())
                if rect.Contains(pt):
                    #set toggle state only if on dropdown
                    self.state = not self.state
                else:
                    self.down = not self.down

                #post an EVT_TOOL via the parent tool panel
                id  = event.GetId()
                evt = wx.CommandEvent( wx.wxEVT_COMMAND_TOOL_CLICKED, id)
                evt.SetEventObject(self)
                evt.SetInt( int(self.state))
                wx.PostEvent(self.Parent, evt)  
 
                #if parent window is an overflow close it, unless the dropdown 
                # was clicked in which case the popup should close the dropdown
                #if (self.state is False) and isinstance(self.Parent, TSGroupOverflow):
                #    self.Parent.Hide()
                
            self.Refresh()



#%%-----------------------------------------------------------------------------
# test code
#-------------------------------------------------------------------------------
def test_strip():

    new_bmpL     =  wx.ArtProvider.GetBitmap( wx.ART_NEW, size=(32,32) )
    new_bmpS     =  wx.ArtProvider.GetBitmap( wx.ART_NEW, size=(16,16) )
    open_bmpS    =  wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN , size=(16,16) )
    open_bmpL    =  wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN , size=(32,32) )
    save_bmpS    =  wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE , size=(16,16) )
    save_bmpL   =  wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE , size=(32,32) )
    
    paste_bmp   =  wx.ArtProvider.GetBitmap( wx.ART_PASTE , size=(32,32) )
    cut_bmp   =  wx.ArtProvider.GetBitmap( wx.ART_CUT , size=(16,16) )
    copy_bmp   =  wx.ArtProvider.GetBitmap( wx.ART_COPY , size=(16,16) )
    clear_bmp   =  wx.ArtProvider.GetBitmap( wx.ART_DELETE , size=(16,16) )
    
    f = wx.Frame(None, -1, 'test')
    sb = f.CreateStatusBar()
    sizer = wx.BoxSizer( wx.VERTICAL)

    #create a Toolstrip
    ts =  ToolStrip(f,-1)
    
    #set the status bar to use
    ts.SetStatusBar(sb)

    ##create page1
    page1 = ts.AddPage( label='Home', longHelp='Access application settings')
    
    #group1
    g1 = page1.AddGroup( label='New', longHelp='Create new or open new file')
    g1.AddLabelTool( wx.ID_NEW, ITEM_LARGE, new_bmpL, 'New\nfile', 
                    'New file', 'Open a new file')

    g1.AddLabelDropDownTool( wx.ID_NEW, ITEM_LARGE, new_bmpL, 'Ney\nfily', 
                    'New file', 'Open a new file')

    g1.AddLabelDropDownTool( wx.ID_OPEN, ITEM_LARGE, open_bmpL, 'Open',
                    'New file', 'Open a new file')

    g1.AddLabelDropDownTool( wx.ID_SAVE, ITEM_LARGE, save_bmpL, '',
                    'New file', 'Open a new file')
    g1.Realize()


    def handler(event):
        print('In Handler', event.GetEventObject(), event.GetId(),event.IsChecked())
        
    def menu_handler(event):

        if event.IsChecked():
            #open menu
            menu = wx.Menu()
            
            for n in range(0,5):
                item = wx.MenuItem(menu, -1 ,'File'+str(n), '', wx.ITEM_NORMAL)
                menu.Append(item)
            tool = event.GetEventObject()
            tool.PopupMenu(menu)
            menu.Destroy()
        else:
            print('clicked')

    page1.Bind(wx.EVT_TOOL, handler, id=wx.ID_NEW)
    page1.Bind(wx.EVT_TOOL, menu_handler, id=wx.ID_OPEN)
    
    #group 2
    g2 = page1.AddGroup( label='Clipboard')
    
    g2.AddLabelTool( wx.ID_PASTE, ITEM_LARGE,  bitmap=paste_bmp, label='Paste', 
                shortHelp='Paste', longHelp='Paste from clipboard')
    
    g2.AddNormalTool( wx.ID_CUT, ITEM_SMALL,  bitmap=cut_bmp, 
                    shortHelp='Cut', longHelp='Cut to clipboard')
    g2.AddNormalTool( -1, ITEM_SMALL, bitmap=copy_bmp,
                    shortHelp='Copy', longHelp='Copy to clipboard')
    g2.AddNormalTool( -1, ITEM_SMALL, bitmap=clear_bmp,
                    shortHelp='Clear', longHelp='Clear')
    g2.Realize()
    
    #group3
    g3 = page1.AddGroup( label='Workspace')
    
    #add a control
    #p = wx.TextCtrl( g3, -1, size=(100,-1))
    #p.SetBackgroundColour('blue')
    #g3.AddControl( p, hrows=1, wprop=1)
    
    add = wx.ComboBox( g3, -1, "", choices=['PATH1','/home/tom/PythonToolkit/pythontoolkit-code/dev/ribbon'],
                        size=(200,32), style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
    add.SetMinSize((200,32))
    
    g3.AddControl( add, 0, wprop=1)
        

    g3.AddLabelTool( wx.ID_NEW, ITEM_LARGE, new_bmpL, 'New\nfile', 
                    'New file', 'Open a new file')

    g3.AddLabelDropDownTool( wx.ID_NEW, ITEM_LARGE, new_bmpL, 'Ney\nfily', 
                    'New file', 'Open a new file')

    g3.AddLabelDropDownTool( wx.ID_OPEN, ITEM_LARGE, open_bmpL, 'Open',
                    'New file', 'Open a new file')

    g3.AddLabelDropDownTool( wx.ID_SAVE, ITEM_LARGE, save_bmpL, '',
                    'New file', 'Open a new file')
    g3.Realize()

    
    ##page 2
    page2 = ts.AddPage( label='Engine', longHelp='Engine and python environment control')

    #group1
    g1 = page2.AddGroup( label='New')
    g1.AddLabelTool( wx.ID_NEW, ITEM_LARGE, new_bmpL, 'New\nfile', 
                    'New file', 'Open a new file')

    g1.AddLabelDropDownTool( wx.ID_NEW, ITEM_LARGE, new_bmpL, 'Ney\nfily', 
                    'New file', 'Open a new file')

    g1.AddLabelDropDownTool( wx.ID_OPEN, ITEM_LARGE, open_bmpL, 'Open',
                    'New file', 'Open a new file')

    g1.AddLabelDropDownTool( wx.ID_SAVE, ITEM_LARGE, save_bmpL, '',
                    'New file', 'Open a new file')
    g1.Realize()

    #group2
    g2 = page2.AddGroup( label='Tools')
    g2.Realize()

    ##page 3
    page3 = ts.AddPage( label='Editor', longHelp='Engine and python environment control')

    #group1
    g1 = page3.AddGroup( label='New')
    g1.AddNormalTool( wx.ID_NEW, ITEM_MEDIUM, new_bmpL, 
                    'New file', 'Open a new file')

    g1.AddLabelTool( wx.ID_OPEN, ITEM_LARGE, new_bmpL,'new',
                    'New file', 'Open a new file')

    g1.AddNormalTool( wx.ID_SAVE, ITEM_MEDIUM, save_bmpL,
                    'New file', 'Open a new file')
    g1.Realize()

    #group2
    g2 = page3.AddGroup( label='Clipboard')
    
    g2.AddLabelTool( wx.ID_PASTE, ITEM_LARGE,  bitmap=paste_bmp, label='Paste', 
                shortHelp='Paste', longHelp='Paste from clipboard')
    
    g2.AddNormalTool( wx.ID_CUT, ITEM_SMALL,  bitmap=cut_bmp, 
                    shortHelp='Cut', longHelp='Cut to clipboard')
    g2.AddNormalTool( -1, ITEM_SMALL, bitmap=copy_bmp,
                    shortHelp='Copy', longHelp='Copy to clipboard')
    g2.AddNormalTool( -1, ITEM_SMALL, bitmap=clear_bmp,
                    shortHelp='Clear', longHelp='Clear')
    g2.Realize()

    ##pages 3,4
    page3 = ts.AddPage( label='Tools', longHelp='Use and add custom tools')
    page4 = ts.AddPage( label='Help', longHelp='Access help resources')

    #the content
    panel = wx.Panel(f,-1)
    panel.SetBackgroundColour('white')
    
    #frame layout
    sizer.Add(ts, 0, wx.EXPAND)
    sizer.Add(panel, 1, wx.EXPAND)
    f.SetSizer(sizer)
    f.Layout()
    f.Refresh()
    f.Show()
    return f, ts
    
def test_panel():
        
    new_bmpL     =  wx.ArtProvider.GetBitmap( wx.ART_NEW, size=(32,32) )
    new_bmpS     =  wx.ArtProvider.GetBitmap( wx.ART_NEW, size=(16,16) )
    open_bmpS    =  wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN , size=(16,16) )
    open_bmpL    =  wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN , size=(32,32) )
    save_bmpS    =  wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE , size=(16,16) )
    save_bmpL   =  wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE , size=(32,32) )
    

    f = wx.Frame(None, -1, 'test')
    sb = f.CreateStatusBar()

    tb =  ToolPanel(f, -1, layout=LAYOUT_RIBBON)
    
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add( tb, 1, wx.EXPAND)
    f.SetSizer(sizer)
    
    tb.SetStatusBar(sb)

    tool = tb.AddLabelTool( wx.ID_NEW, ITEM_LARGE, bitmap=new_bmpL, 
                                label='New\nfile' , shortHelp='New file', 
                                longHelp='Open a new file')
    tool.SetDropdown(True) #add a drop down label
    
    tb.AddSpacer( width=96, hrows=ITEM_SMALL)
    
    tb.AddLabelToggleTool( wx.ID_NEW, ITEM_LARGE,  bitmap=open_bmpL, 
                                label='Open\nfile', shortHelp='Open a file', 
                                longHelp='Open a new file')
                
    #three buttons
    tb.AddNormalTool( wx.ID_SAVE, ITEM_SMALL,  bitmap=save_bmpS, 
                    shortHelp='New file', longHelp='Open a new file')
                    
    tb.AddToggleTool( -1, ITEM_SMALL, bitmap=new_bmpS,
                    shortHelp='Toggle new', longHelp='Toggle a new file')
    tb.AddToggleTool( -1, ITEM_SMALL, bitmap=new_bmpS,
                   shortHelp='Toggle new', longHelp='Toggle a new file')

    #add a seperator
    tb.AddSeparator(ITEM_MAX)
    
    #add a control
    p = wx.Panel( tb, -1, size=(100,-1))
    p.SetBackgroundColour('blue')
    tb.AddControl( p, hrows=1, wprop=1)
    
    #add a seperator
    tb.AddSeparator(ITEM_MAX)

    tb.AddLabelToggleTool( wx.ID_NEW, ITEM_LARGE,  bitmap=open_bmpL, 
                                label='Open\nfile', shortHelp='Open a file', 
                                longHelp='Open a new file')
                                
    #split the next position into three buttons
    tb.AddLabelTool( wx.ID_SAVE, ITEM_SMALL,  bitmap=save_bmpS, label='New file',
                    shortHelp='New file', longHelp='Open a new file')
    tb.AddLabelToggleTool( -1, ITEM_SMALL, bitmap=new_bmpS, label='New',
                    shortHelp='Toggle new', longHelp='Toggle a new file')
    tb.AddLabelToggleTool( -1, ITEM_SMALL, bitmap=open_bmpS, label='Open file',
                    shortHelp='Toggle open', longHelp='Toggle a open file')

    tb.Realize()
    
    #the content
    panel = wx.Panel(f,-1)
    panel.SetBackgroundColour('white')
    
    #frame layout
    sizer = wx.BoxSizer( wx.VERTICAL)
    sizer.Add(tb, 0, wx.EXPAND)
    sizer.Add(panel, 1, wx.EXPAND)
    f.SetSizer(sizer)
    f.Show()
    return f, tb



if __name__ == '__main__':
    app = wx.App() 
    f, tb = test_strip()
    app.MainLoop()
