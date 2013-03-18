import leebrinton.util
import leebrinton.util.strutil as strutil

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class ScrollerFrame( tk.Frame ):
    def __init__( self, master, widgetClass, mode, **widgetOptions ):
        Frame.__init__( self, master )

        self._xscrollbar = None
        self._yscrollbar = None

        if 'x' in mode:
            self.grid_rowconfigure( 0, weight=1 )
            self._xscrollbar = tk.Scrollbar( self, orient=tk.HORIZONTAL )
            self._xscrollbar.grid( row=1, column=0, sticky=E+W )
        
        if 'y' in mode:
            self.grid_columnconfigure( 0, weight=1 )
            self._yscrollbar = tk.Scrollbar( self )
            self._yscrollbar.grid( row=0, column=1, sticky=N+S )

        widgetOptions['xscrollcommand'] = self._xscrollbar.set
        widgetOptions['yscrollcommand'] = self._yscrollbar.set

        self._widget = widgetClass( self, **widgetOptions )

        self._widget.grid( row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W )

        if 'x' in mode:
            self._xscrollbar.config( command=self._widget.xview )

        if 'y' in mode:
            self._yscrollbar.config( command=self._widget.yview )

        self.pack()

    def getWidget( self ):
        return self._widget

class ScrolledCanvasFrame( ScrollerFrame ):
    def __init__( self, master, **widgetOptions ):
        ScrollerFrame.__init__( self, master, Canvas, 'xy', **widgetOptions )

class ScrolledListboxFrame( ScrollerFrame ):
    def __init__( self, master, **widgetOptions ):
        ScrollerFrame.__init__( self, master, Listbox, 'y', **widgetOptions )

class ScrolledTextFrame( ScrollerFrame ):
    def __init__( self, master, **widgetOptions ):
        ScrollerFrame.__init__( self, master, Text, 'y', **widgetOptions )

def centerTopLevel( window, withMenu=False ):
    window.update_idletasks()
    
    width = window.winfo_width()
    height = window.winfo_height()

    extraWidth = 8
    extraHeight = 20
    
    if withMenu:
        extraWidth += 12
        extraHeight += 10

    xp = int((window.winfo_screenwidth() / 2) - (width / 2) - extraWidth)
    yp = int((window.winfo_screenheight() / 2) - (height / 2) - extraHeight)

    window.geometry( "%dx%d+%d+%d" % (width, height, xp, yp))

def setTopLevelIcon( window, iconName ):
    windowSystem = window.tk.call( "tk", "windowingsystem" )

    if windowSystem == "win32": # Windows
        iconName += ".ico"
    elif windowSystem == "x11": # Unix
        iconName = "@" + iconName + ".xbm"
    
    try:
        window.iconbitmap( iconName )
        # window.wm_iconbitmap( iconName ) also works
    except TclError:
        log.error( __name__, "Unable to set icon" )		

def setTopLevelIconphoto( window, photo ):
    img = photo

    if leebrinton.util.is_ver_3():
        if strutil.isString( photo ):
            img = tk.PhotoImage( file=photoname )
    else:
        if strutil.isBaseString( photo ):
            img = tk.PhotoImage( file=photoname )

    window.tk.call( 'wm', 'iconphoto', window, "-default", img )
    #window.tk.call( 'wm', 'iconphoto', root._w, img )

