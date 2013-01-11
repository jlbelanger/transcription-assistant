#!/usr/bin/python
import globals as g
import os
import pygame
import wx
import wx.media
from math import floor

class Interface(wx.Frame):
	def __init__(self, parent):
		self.frame = wx.Frame
		self.frame.__init__(self, parent, style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
		self.PREV_TEXT = ''
		
		self.intializeInterface()
		
		self.SetSize((g.WINDOW_WIDTH, g.WINDOW_HEIGHT))
		self.SetTitle(g.TITLE)
		self.Centre()
		self.Show(True)
		return
		
	def intializeInterface(self):
		# create media player
		self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
		
		# create panel, sizer
		self.panel = wx.Panel(self)
		self.sizer = wx.GridBagSizer(5, 1)
		
		# create file panel
		self.initializeFilePanel()
		self.sizer.Add(self.pnlFile, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT, border=g.BORDER)
		
		# create seek slider panel
		self.initializeSeekSliderPanel()
		self.sizer.Add(self.pnlSeekSlider, pos=(1, 0), flag=wx.LEFT|wx.RIGHT, border=g.BORDER)
		
		# create media buttons panel
		self.initializeMediaButtonsPanel()
		self.sizer.Add(self.pnlMediaButtons, pos=(2, 0), flag=wx.ALL, border=g.BORDER)
		
		# create text box
		self.txtTextBox = wx.TextCtrl(self.panel, style=wx.TE_RICH|wx.TE_MULTILINE, size=(g.WINDOW_WIDTH - 20 - g.BORDER * 2, g.WINDOW_HEIGHT - 180 - g.BORDER * 6))
		self.txtTextBox.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.sizer.Add(self.txtTextBox, pos=(3, 0), flag=wx.LEFT|wx.RIGHT, border=g.BORDER)
		
		# create text buttons panel
		self.initializeTextButtonsPanel()
		self.sizer.Add(self.pnlTextButtons, pos=(4, 0), flag=wx.ALL, border=g.BORDER)
		
		# set panel sizer
		self.panel.SetSizerAndFit(self.sizer)
		
		# create slider timer
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimer)
		self.timer.Start(100)
		
		# create joystick listener
		self.joystick = wx.Joystick()
		if self.joystick.GetNumberJoysticks() > 0 and self.joystick.IsOk():
			self.joystick.SetCapture(self)
			self.Bind(wx.EVT_JOY_BUTTON_DOWN, self.onJoystick)
		return
		
	def initializeFilePanel(self):
		# create panel, sizer
		self.pnlFile = wx.Panel(self.panel)
		self.szrFile = wx.GridBagSizer(1, 2)
		
		# create load button
		self.imgLoad = wx.Image(g.IMAGE_DIRECTORY + 'button_load.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		buttonWidth = self.imgLoad.GetWidth() + g.BUTTON_PADDING
		buttonHeight = self.imgLoad.GetHeight() + g.BUTTON_PADDING
		self.btnLoad = wx.BitmapButton(self.pnlFile, bitmap=self.imgLoad, size=(buttonWidth, buttonHeight))
		self.btnLoad.SetLabel('Load File')
		self.btnLoad.SetToolTip(wx.ToolTip('Load File'))
		self.btnLoad.Bind(wx.EVT_BUTTON, self.onLoad)
		self.szrFile.Add(self.btnLoad, pos=(0, 0))
		
		# create filename label
		self.lblFilename = wx.StaticText(self.pnlFile, label='no file loaded', style=wx.ALIGN_LEFT, size=wx.Size(g.WINDOW_WIDTH - buttonWidth, buttonHeight))
		font = self.lblFilename.GetFont() 
		font.SetWeight(wx.BOLD) 
		self.lblFilename.SetFont(font) 
		self.szrFile.Add(self.lblFilename, pos=(0, 1), flag=wx.TOP|wx.LEFT, border=9)
		
		# set panel sizer
		self.pnlFile.SetSizerAndFit(self.szrFile)
		return
		
	def initializeSeekSliderPanel(self):
		# create panel, sizer
		self.pnlSeekSlider = wx.Panel(self.panel)
		self.szrSeekSlider = wx.GridBagSizer(1, 3)
		
		# create slider
		self.slider = wx.Slider(self.pnlSeekSlider, value=0, minValue=0, maxValue=0, size=wx.Size(g.WINDOW_WIDTH - 90 - g.BORDER * 2, -1))
		self.slider.Enable(False)
		self.slider.Bind(wx.EVT_SLIDER, self.onSeek)
		self.szrSeekSlider.Add(self.slider, pos=(1, 0))

		# create current time label
		self.lblCurrentTime = wx.StaticText(self.pnlSeekSlider, label='0:00', style=wx.ALIGN_CENTRE)
		self.szrSeekSlider.Add(self.lblCurrentTime, pos=(1, 1))
		
		# create total time label
		self.lblTotalTime = wx.StaticText(self.pnlSeekSlider, label='/ 0:00', style=wx.ALIGN_CENTRE)
		self.szrSeekSlider.Add(self.lblTotalTime, pos=(1, 2))
		
		# set panel sizer
		self.pnlSeekSlider.SetSizerAndFit(self.szrSeekSlider)
		return
		
	def initializeMediaButtonsPanel(self):
		# create panel, sizer
		numButtons = len(g.BUTTON_IMAGES)
		self.pnlMediaButtons = wx.Panel(self.panel)
		self.szrMediaButtons = wx.GridBagSizer(1, numButtons)
		
		# create buttons
		buttonFunctions = [self.onPlayPause, self.onRewind, self.onStop, self.onForward, self.onSlower, self.onNormalSpeed, self.onFaster]
		self.img = []
		self.btn = []
		self.imgPlay = wx.Image(g.IMAGE_DIRECTORY + g.BUTTON_IMAGES[g.BUTTON_PLAY], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.imgPause = wx.Image(g.IMAGE_DIRECTORY + 'button_pause.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		for buttonNum, buttonImage in enumerate(g.BUTTON_IMAGES):
			if buttonImage != '':
				self.img.append(wx.Image(g.IMAGE_DIRECTORY + g.BUTTON_IMAGES[buttonNum], wx.BITMAP_TYPE_ANY).ConvertToBitmap())
				buttonWidth = self.img[buttonNum].GetWidth() + g.BUTTON_PADDING
				buttonHeight = self.img[buttonNum].GetHeight() + g.BUTTON_PADDING
				self.btn.append(wx.BitmapButton(self.pnlMediaButtons, bitmap=self.img[buttonNum], size=(buttonWidth, buttonHeight)))
			else:
				self.btn.append(wx.Button(self.pnlMediaButtons))
			self.btn[buttonNum].SetLabel(g.BUTTON_LABELS[buttonNum])
			self.btn[buttonNum].SetToolTip(wx.ToolTip(g.BUTTON_TOOLTIPS[buttonNum] + ' (' + g.BUTTON_KEYS[buttonNum] + ')'))
			self.btn[buttonNum].Enable(False)
			self.btn[buttonNum].Bind(wx.EVT_BUTTON, buttonFunctions[buttonNum])
			self.szrMediaButtons.Add(self.btn[buttonNum], pos=(0, buttonNum))
		
		# create current speed label
		self.lblCurrentSpeed = wx.StaticText(self.pnlMediaButtons, label='Current Speed: 100%', style=wx.ALIGN_LEFT)
		self.szrMediaButtons.Add(self.lblCurrentSpeed, pos=(0, numButtons + 1))
		
		# set panel sizer
		self.pnlMediaButtons.SetSizerAndFit(self.szrMediaButtons)
		return
		
	def initializeTextButtonsPanel(self):
		# create panel, sizer
		self.pnlTextButtons = wx.Panel(self.panel)
		self.szrTextButtons = wx.GridBagSizer(1, 2)
		
		# create clear text button
		self.btnClearText = wx.Button(self.pnlTextButtons)
		self.btnClearText.SetLabel('Clear Text')
		self.btnClearText.Bind(wx.EVT_BUTTON, self.onClear)
		self.szrTextButtons.Add(self.btnClearText, pos=(0, 0))
		
		# create clear text button
		self.btnUndoClearText = wx.Button(self.pnlTextButtons)
		self.btnUndoClearText.SetLabel('Undo Clear')
		self.btnUndoClearText.Bind(wx.EVT_BUTTON, self.onUndo)
		self.szrTextButtons.Add(self.btnUndoClearText, pos=(0, 1))
		
		# set panel sizer
		self.pnlTextButtons.SetSizerAndFit(self.szrTextButtons)
		return
		
	def onJoystick(self, event):
		self.onRewind(event)
		event.Skip()
		return
		
	def onLoad(self, event):
		self.dirname = ''
		fileDialog = wx.FileDialog(self, 'Choose a file', self.dirname, '', '*.mp3', wx.OPEN)
		if fileDialog.ShowModal() == wx.ID_OK:
			self.onStop(event)
			self.btn[g.BUTTON_FORWARD].Enable(False)
			self.filename = fileDialog.GetFilename()
			self.directory = fileDialog.GetDirectory()
			self.path = self.directory + '\\' + self.filename
			if not self.mediaPlayer.Load(self.path):
				wx.MessageBox('Unable to load %s: Unsupported format?' % path, 'ERROR', wx.ICON_ERROR | wx.OK)
			else:
				self.btn[g.BUTTON_PLAY].Enable(True)
				self.btn[g.BUTTON_SLOWER].Enable(True)
				self.btn[g.BUTTON_NORMAL].Enable(True)
				self.btn[g.BUTTON_FASTER].Enable(True)
				self.slider.Enable(True)
				self.lblFilename.SetLabel(self.filename)
		fileDialog.Destroy()
		return
		
	def onQuit(self, event):
		self.Close()
		return
		
	def onPlayPause(self, event):
		self.btn[g.BUTTON_STOP].Enable(True)
		self.btn[g.BUTTON_REWIND].Enable(True)
		self.btn[g.BUTTON_FORWARD].Enable(True)
		if self.mediaPlayer.GetState() != wx.media.MEDIASTATE_PLAYING:
			self.mediaPlayer.Play()
			self.showPause()
			self.slider.SetRange(0, self.mediaPlayer.Length())
			self.lblTotalTime.SetLabel('/ ' + getTimeInMinutes(self.mediaPlayer.Length()))
		else:
			self.mediaPlayer.Pause()
			self.showPlay()
		event.Skip()
		return
		
	def onStop(self, event):
		self.mediaPlayer.Stop()
		self.btn[g.BUTTON_STOP].Enable(False)
		self.btn[g.BUTTON_REWIND].Enable(False)
		self.btn[g.BUTTON_FORWARD].Enable(True)
		event.Skip()
		return
		
	def onRewind(self, event):
		time = self.mediaPlayer.Tell() - g.SKIP_SECONDS * 1000
		self.mediaPlayer.Seek(time)
		event.Skip()
		return
		
	def onForward(self, event):
		time = self.mediaPlayer.Tell() + g.SKIP_SECONDS * 1000
		self.mediaPlayer.Seek(time)
		self.btn[g.BUTTON_REWIND].Enable(True)
		self.btn[g.BUTTON_STOP].Enable(True)
		event.Skip()
		return
		
	def onSlower(self, event):
		currentPlaybackRate = self.mediaPlayer.GetPlaybackRate() - g.SPEED_INCREMENT
		self.mediaPlayer.SetPlaybackRate(currentPlaybackRate)
		self.lblCurrentSpeed.SetLabel('Current Speed: ' + str(int(currentPlaybackRate * 100)) + '%')
		event.Skip()
		return
		
	def onNormalSpeed(self, event):
		self.mediaPlayer.SetPlaybackRate(1.0)
		self.lblCurrentSpeed.SetLabel('Current Speed: 100%')
		event.Skip()
		return
		
	def onFaster(self, event):
		currentPlaybackRate = self.mediaPlayer.GetPlaybackRate() + g.SPEED_INCREMENT
		self.mediaPlayer.SetPlaybackRate(currentPlaybackRate)
		self.lblCurrentSpeed.SetLabel('Current Speed: ' + str(int(currentPlaybackRate * 100)) + '%')
		event.Skip()
		return
		
	def onSeek(self, event):
		offset = self.slider.GetValue()
		self.mediaPlayer.Seek(offset)
		if offset == 0:
			self.btn[g.BUTTON_STOP].Enable(False)
		else:
			self.btn[g.BUTTON_STOP].Enable(True)
		self.btn[g.BUTTON_REWIND].Enable(True)
		self.btn[g.BUTTON_FORWARD].Enable(True)
		event.Skip()
		return
		
	def onTimer(self, event):
		currentTimeMs = self.mediaPlayer.Tell()
		if currentTimeMs == 0 and g.PREVIOUS_TIME != 0:
			self.showPlay()
			self.btn[g.BUTTON_STOP].Enable(False)
			self.btn[g.BUTTON_REWIND].Enable(False)
		if currentTimeMs != -1:
			self.slider.SetValue(currentTimeMs)
			self.lblCurrentTime.SetLabel(getTimeInMinutes(currentTimeMs))
		g.PREVIOUS_TIME = currentTimeMs
		return
		
	def onKeyDown(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_F1:
			self.onPlayPause(event)
		elif key == wx.WXK_F2:
			self.onRewind(event)
		elif key == wx.WXK_F3:
			self.onStop(event)
		elif key == wx.WXK_F4:
			self.onForward(event)
		elif key == wx.WXK_F5:
			self.onSlower(event)
		elif key == wx.WXK_F6:
			self.onNormalSpeed(event)
		elif key == wx.WXK_F7:
			self.onFaster(event)
		event.Skip()
		return
		
	def onClear(self, event):
		self.PREV_TEXT = self.txtTextBox.GetLabel()
		self.txtTextBox.SetLabel('')
		event.Skip()
		return
		
	def onUndo(self, event):
		temp = self.txtTextBox.GetLabel()
		self.txtTextBox.SetLabel(self.PREV_TEXT)
		self.PREV_TEXT = temp
		event.Skip()
		return
		
	def showPlay(self):
		self.btn[g.BUTTON_PLAY].SetLabel(g.BUTTON_LABELS[g.BUTTON_PLAY])
		self.btn[g.BUTTON_PLAY].SetToolTip(wx.ToolTip(g.BUTTON_TOOLTIPS[g.BUTTON_PLAY] + ' (' + g.BUTTON_KEYS[g.BUTTON_PLAY] + ')'))
		self.btn[g.BUTTON_PLAY].SetBitmapLabel(self.imgPlay)
		return
		
	def showPause(self):
		self.btn[g.BUTTON_PLAY].SetLabel('Pause')
		self.btn[g.BUTTON_PLAY].SetToolTip(wx.ToolTip('Pause (' + g.BUTTON_KEYS[g.BUTTON_PLAY] + ')'))
		self.btn[g.BUTTON_PLAY].SetBitmapLabel(self.imgPause)
		return
		
def getTimeInMinutes(timeInMs):
	minutes = int(floor(timeInMs / 60000))
	seconds = str((int(timeInMs - minutes * 60) / 1000) % 60).zfill(2)
	return str(minutes) + ':' + seconds

def main():
	app = wx.App(redirect=True, filename='log.txt')
	Interface(None)
	app.MainLoop()
	return
	
if __name__ == '__main__':
	main()

# TODO
# joystick
# volume
# options (shortcut keys)