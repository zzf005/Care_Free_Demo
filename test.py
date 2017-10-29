import wx
import cv2

class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, fps=15):
        wx.Panel.__init__(self, parent)

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

capture = cv2.VideoCapture(0)
# set width
# capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 320)
# capture.set(3, 320)
# The following command works for opencv 2.4.8 not 3.0
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)

# set height
# capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
#capture.set(4, 240)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

app = wx.App()
frame = wx.Frame(None)
cap = ShowCapture(frame, capture)
frame.Show()
app.MainLoop()