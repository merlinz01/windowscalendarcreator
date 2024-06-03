from .win32 import const, gdi32, kernel32, user32, types


class DC:
    def __init__(self, hdc):
        self.hdc = hdc
        self._gdiobjects = {}

    def AbortDoc(self):
        gdi32.AbortDoc(self.hdc)

    def BeginPath(self):
        gdi32.BeginPath(self.hdc)

    def BitBlt(self, dx, dy, dwidth, dheight, sourceDC, sx, sy, rop):
        gdi32.BitBlt(self.hdc, dx, dy, dwidth, dheight, sourceDC, sx, sy, rop)

    def Cancel(self):
        gdi32.CancelDC(self.hdc)

    @classmethod
    def Create(cls, driver, device, initdata=None):
        return cls(gdi32.CreateDC(driver, device, 0, initdata))

    @classmethod
    def CreateCompatible(cls, hdc):
        return cls(gdi32.CreateCompatibleDC(hdc))

    def CreateCompatibleBitmap(self, width, height):
        return gdi32.CreateCompatibleBitmap(self.hdc, width, height)

    def Delete(self):
        gdi32.DeleteDC(self.hdc)
        for obj in self._gdiobjects.values():
            gdi32.DeleteObject(obj)
        del self.hdc

    def DPtoLP(self, *points):
        count = len(points)
        array = (types.gettype('POINT') * count)(*points)
        gdi32.DPtoLP(self.hdc, array, count)
        return [(pt.x, pt.y) for pt in array]

    def DrawEdge(self, left, top, right, bottom, eType, flags):
        user32.DrawEdge(
            self.hdc, types.alloc('RECT', left, top, right, bottom).ref(),
            eType, flags)

    def DrawFocusRect(self, left, top, right, bottom):
        rect = types.alloc('RECT', left, top, right, bottom)
        user32.DrawFocusRect(self.hdc, rect)

    def DrawIcon(self, x, y, hicon):
        user32.DrawIcon(self.hdc, x, y, hicon)

    def DrawText(self, left, top, right, bottom, text, fmt):
        rect = types.alloc('RECT', left, top, right, bottom)
        user32.DrawText(self.hdc, text, len(text), rect, fmt)
        return rect.left, rect.top, rect.right, rect.bottom

    def DrawText2(self, x, y, w, h, text, fmt):
        rect = types.alloc('RECT', x, y, x + w, y + h)
        user32.DrawText(self.hdc, text, len(text), rect.ref(), fmt)
        return rect.left, rect.top, rect.right, rect.bottom

    def EndDoc(self):
        gdi32.EndDoc(self.hdc)

    def EndPage(self):
        gdi32.EndPage(self.hdc)

    def EndPath(self):
        gdi32.EndPath(self.hdc)

    def FillPath(self, stroke=False):
        if stroke:
            gdi32.StrokeAndFillPath(self.hdc)
        else:
            gdi32.FillPath(self.hdc)

    def FillRect(self, left, top, right, bottom, brush):
        user32.FillRect(
            self.hdc, types.alloc('RECT', left, top, right, bottom).ref(), brush)

    def GetClipBox(self):
        rect = types.alloc('RECT')
        gdi32.GetClipBox(self.hdc, rect.ref())
        return rect.left, rect.top, rect.right, rect.bottom

    def GetDeviceCaps(self, nIndex):
        return gdi32.GetDeviceCaps(self.hdc, nIndex)

    def GetMapMode(self):
        return gdi32.GetMapMode(self.hdc)

    def GetPointHeight(self, points, ppi=72):
        return -kernel32.MulDiv(
            points, gdi32.GetDeviceCaps(self.hdc, const.LOGPIXELSY), ppi)

    def GetTextExtentPoint32(self, text):
        size = types.alloc('SIZE')
        gdi32.GetTextExtentPoint32(self.hdc, text, len(text), size.ref())
        return size

    def Line(self, x1, y1, x2, y2):
        self.MoveTo(x1, y1)
        self.LineTo(x2, y2)

    def LineTo(self, x, y):
        gdi32.LineTo(self.hdc, x, y)

    def LPtoDP(self, *points):
        count = len(points)
        array = (types.gettype('POINT') * count)(*points)
        gdi32.LPtoDP(self.hdc, array, count)
        return tuple((pt.x, pt.y) for pt in array)

    def MoveTo(self, x, y):
        gdi32.MoveToEx(self.hdc, x, y, None)

    def Rectangle(self, left, top, right, bottom):
        gdi32.Rectangle(self.hdc, left, top, right, bottom)

    def Reset(self, devmode):
        return gdi32.ResetDC(self.hdc, devmode)

    def SelectObject(self, hgdiobj):
        return gdi32.SelectObject(self.hdc, hgdiobj)

    def SetBkColor(self, color):
        return gdi32.SetBkColor(self.hdc, color)

    def SetBkMode(self, transparent=False):
        return gdi32.SetBkMode(self.hdc, 1 if transparent else 2)

    def SetBrush(self, style=const.BS_SOLID, color=0, hatch=0):
        key = ('B', style, color, hatch)
        try:
            b = self._gdiobjects[key]
        except KeyError:
            self._gdiobjects[key] = b = gdi32.CreateBrushIndirect(
                types.alloc('LOGBRUSH', style, color, hatch).ref())
        self.SelectObject(b)
        return b

    def SetBrushOrg(self, x, y):
        pt = types.alloc('POINT')
        gdi32.SetBrushOrgEx(self.hdc, x, y, pt.ref())
        return pt

    def SetFont(self, **kw):
        args = (
            kw.get('height'),
            kw.get('width', 0),
            kw.get('escapement', 0),
            kw.get('orientation', 0),
            kw.get('weight', 0),
            kw.get('italic', 0),
            kw.get('underline', 0),
            kw.get('strikeout', 0),
            kw.get('charset', 0),
            kw.get('output_precision', 0),
            kw.get('clip_precision', 0),
            kw.get('quality', 0),
            kw.get('pitch_and_family', 0),
            kw.get('name'))
        try:
            f = self._gdiobjects[args]
        except KeyError:
            self._gdiobjects[args] = f = gdi32.CreateFont(*args)
        self.SelectObject(f)
        return f

    def SetGraphicsMode(self, mode):
        gdi32.SetGraphicsMode(self.hdc, mode)

    def SetMapMode(self, mode):
        gdi32.SetMapMode(self.hdc, mode)

    def SetPen(self, style=const.PS_SOLID, width=0, color=0):
        key = ('P', style, width, color)
        try:
            p = self._gdiobjects[key]
        except KeyError:
            self._gdiobjects[key] = p = gdi32.CreatePen(style, width, color)
        self.SelectObject(p)
        return p

    def SetStretchBltMode(self, mode):
        return gdi32.SetStretchBltMode(self.hdc, mode)

    def SetTextColor(self, color):
        return gdi32.SetTextColor(self.hdc, color)

    def SetWorldTransform(self, eM11=1, eM12=0, eM21=0, eM22=1, eDx=0, eDy=0):
        xf = types.alloc('XFORM', eM11, eM12, eM21, eM22, eDx, eDy)
        gdi32.SetWorldTransform(self.hdc, xf.ref())

    def StartDoc(self, docname):
        docinfo = types.alloc('DOCINFO')
        # noinspection PyProtectedMember
        docinfo.cbSize = docinfo._size
        docinfo.lpszDocName = docname
        gdi32.StartDoc(self.hdc, docinfo.ref())

    def StartPage(self):
        gdi32.StartPage(self.hdc)

    def StretchBlt(self, xDest, yDest, wDest, hDest, hdcSrc,
                   xSrc, ySrc, wSrc, hSrc, rop):
        gdi32.StretchBlt(self.hdc, xDest, yDest, wDest, hDest, hdcSrc,
                         xSrc, ySrc, wSrc, hSrc, rop)

    def TextOut(self, x, y, text):
        gdi32.TextOut(self.hdc, x, y, text, len(text))

    BkColor = property(fset=SetBkColor)
    BkMode = property(fset=SetBkMode)
    ClipBox = property(fget=GetClipBox)
    GraphicsMode = property(fset=SetGraphicsMode)
    MapMode = property(GetMapMode, SetMapMode)
    StretchBltMode = property(fset=SetStretchBltMode)
    TextColor = property(fset=SetTextColor)
    
