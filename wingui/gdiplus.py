from .win32 import gdiplus, types
gpconst = gdiplus.gpconst

class GdiPlus:
    def __enter__(self):
        self.token = types.alloc('ULONG_PTR')
        inpt = types.alloc('GdiplusStartupInput', 1, None, False, False)
        output = types.alloc('GdiplusStartupOutput')
        gdiplus.GdiplusStartup(
            types.byref(self.token), inpt.ref(), output.ref())
    def __exit__(self, exc, val, tb):
        gdiplus.GdiplusShutdown(self.token)

class Image:
    def __init__(self, ptr):
        self.ptr = ptr
    def Dispose(self):
        gdiplus.DisposeImage(self.ptr)
    @classmethod
    def FromFile(cls, filename):
        ptr = types.alloc('LPGpImage')
        gdiplus.LoadImageFromFile(filename, types.byref(ptr))
        return cls(ptr)
    def SaveToFile(self, filename, format):
        clsid = GetEncoderClsid(format)
        gdiplus.SaveImageToFile(self.ptr, filename, clsid.ref(), None)

class Bitmap(Image):
##    def Free(self):
##        gdiplus.Free(self.ptr)
    def CloneAreaI(self, x, y, width, height,
                   format=gpconst.PixelFormatUndefined):
        ptr = types.alloc('LPGpBitmap')
        gdiplus.CloneBitmapAreaI(
            x, y, width, height, format, self.ptr, types.byref(ptr))
        return self.__class__(ptr)
    @classmethod
    def FromFile(cls, filename):
        ptr = types.alloc('LPGpBitmap')
        gdiplus.CreateBitmapFromFile(filename, types.byref(ptr))
        return cls(ptr)
    @classmethod
    def FromGraphics(cls, width, height, graphics):
        ptr = types.alloc('LPGpBitmap')
        gdiplus.CreateBitmapFromGraphics(
            width, height, graphics, types.byref(ptr))
        return cls(ptr)
    @classmethod
    def FromHBITMAP(cls, hbitmap):
        ptr = types.alloc('LPGpBitmap')
        gdiplus.CreateBitmapFromHBITMAP(hbitmap, None, types.byref(ptr))
        return cls(ptr)
    def GetHBITMAP(self, background=0x00000000):
        hb = types.alloc('HBITMAP')
        gdiplus.CreateHBITMAPFromBitmap(
            self.ptr, types.byref(hb), background)
        return hb
    def SetResolution(self, xdpi: float, ydpi: float):
        gdiplus.BitmapSetResolution(self.ptr, xdpi, ydpi)

class Graphics:
    def __init__(self, ptr):
        self.ptr = ptr
    def Delete(self):
        gdiplus.DeleteGraphics(self.ptr)
    @classmethod
    def FromHDC(cls, hdc):
        ptr = types.alloc('LPGpGraphics')
        gdiplus.CreateFromHDC(hdc, types.byref(ptr))
        self = cls(ptr)
        return self

def GetEncoderClsid(format):
    num = types.alloc('UINT') # number of image encoders 
    size = types.alloc('UINT') # size of the image encoder array in bytes 
    gdiplus.GetImageEncodersSize(types.byref(num), types.byref(size))
    if size.value == 0:
      raise OSError('GetImageEncodersSize() failed')
    pImageCodecInfo = (types.gettype('ImageCodecInfo') * num.value)()
    ptr = types.cast(types.pointer(pImageCodecInfo), 'ImageCodecInfo*')
    gdiplus.GetImageEncoders(num, size, ptr)
    for info in pImageCodecInfo: 
        if info.MimeType.value == format:
            return info.Clsid;
    raise ValueError('encoder not found')
