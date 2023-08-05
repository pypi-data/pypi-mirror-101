#!/usr/bin/env python
"""
Main PTK launch file - used for launching the application.
"""
import argparse
import os
import logging
import wx

#need folder on path to run inplace
try:
	import ptk_lib.app as app
	from ptk_lib import misc
except:
	import sys
	root,fname =  os.path.split(os.path.realpath(__file__))
	sys.path.insert( 0, root.rsplit( os.sep, 1)[0])
	import ptk_lib.app as app
	from ptk_lib import misc
	
	
def clear_settings():
    #create the application instance
    _app = wx.PySimpleApp()
    msg = 'Clear all PTK settings'
    title = 'Clear PTK Settings'
    dlg = wx.MessageDialog(None, msg,title,wx.OK |wx.CANCEL| wx.ICON_EXCLAMATION)
    val = dlg.ShowModal()
    dlg.Destroy()
    if val==wx.ID_OK:
        cfg = wx.FileConfig(localFilename=misc.USERDIR+'options')
        cfg.DeleteAll()

def main():
	"""
	Main entry point for launcher script
	"""
	#-------------------------------------------------------------------------------
	#get input arguments using argparse module
	parser = argparse.ArgumentParser(
			description='PTK (PythonToolKit)- an interactive python environment' )
	#optional arguments
	parser.add_argument('-c','--clear_settings', action='store_true', default=False,
						help='Clear all PTK settings')
	parser.add_argument('-f','--files',nargs='*', metavar='filename(s)', default=[], 
						help='Open the files in the editor')
	parser.add_argument('-d','--debug',action='store_true', default=False, 
						help='Enable logging of debug statements')

	#get the arguments
	args = vars(parser.parse_args())
	if args.get('clear_settings', False) is True:
		clear_settings()
	else:
		#create the application instance
		_app = app.PTKApp(name='PTK', args=args)
		#start main loop
		_app.MainLoop()

if __name__=='__main__':
	main()
