import ctypes
from .win32 import comdlg32, gdi32, kernel32, user32, types, const

# Constants
hInstance = kernel32.GetModuleHandle(None)
DefaultFont = gdi32.GetStockObject(17)


# Functions
def CreateBrush(style=const.BS_SOLID, color=0, hatch=0):
    lf = types.alloc('LOGBRUSH', style, color, hatch)
    return gdi32.CreateBrushIndirect(lf.ref())


def CreateFont(**kw):
    return gdi32.CreateFont(
        kw.pop('height'),
        kw.pop('width', 0),
        kw.pop('escapement', 0),
        kw.pop('orientation', 0),
        kw.pop('weight', 0),
        kw.pop('italic', 0),
        kw.pop('underline', 0),
        kw.pop('strikeout', 0),
        kw.pop('charset', 0),
        kw.pop('output_precision', 0),
        kw.pop('clip_precision', 0),
        kw.pop('quality', 0),
        kw.pop('pitch_and_family', 0),
        kw.pop('name'))


def GetBitmapDimensionEx(hbitmap):
    sz = types.alloc('SIZE')
    gdi32.GetBitmapDimensionEx(hbitmap, sz.ref())
    return sz.cx, sz.cy


def GetDevNames(handle):
    ptr = kernel32.GlobalLock(handle)
    dn = types.cast(ptr, 'DEVNAMES*').contents
    wcs = ctypes.sizeof(types.gettype('WCHAR'))
    driver = ctypes.wstring_at(ptr + dn.wDriverOffset * wcs)
    device = ctypes.wstring_at(ptr + dn.wDeviceOffset * wcs)
    output = ctypes.wstring_at(ptr + dn.wOutputOffset * wcs)
    kernel32.GlobalUnlock(handle)
    return driver, device, output


def GetFileNameDialog(dtype, **kw):
    ofn = types.alloc('OPENFILENAME')
    ofn.lStructSize = ofn.sizeof()
    ofn.hwndOwner = kw.get('hwnd', None)
    ofn.hInstance = kw.get('hinstance', None)
    # 'Text Files\x00*.txt\x00Image files\x00*.jpg;*.bmp;*.png\x00\x00'
    ffilter = kw.get('filter', None)
    if ffilter is not None:
        buf = types.create_unicode_buffer(ffilter)
        ofn.lpstrFilter = types.cast(types.pointer(buf), 'LPCWSTR')
    custfilter = kw.get('customfilter', None)
    if custfilter is not None:
        ofn.lpstrCustomFilter = custfilter
        ofn.nMaxCustFilter = len(custfilter)
    ofn.nFilterIndex = kw.get('filterindex', 0)
    fnlength = kw.get('fnlength', 260)
    fbuffer = types.create_unicode_buffer(
        kw.get('filename', ''), fnlength)
    ofn.lpstrFile = types.cast(types.pointer(fbuffer), 'LPCWSTR')
    ofn.nMaxFile = fnlength
    ofn.lpstrFileTitle = kw.get('titlebuf', None)
    ofn.nMaxFileTitle = kw.get('titlebuflength', 0)
    ofn.lpstrInitialDir = kw.get('initialdir', None)
    ofn.lpstrTitle = kw.get('title', None)
    ofn.Flags = kw.get('flags', 0)
    ofn.lpstrDefExt = kw.get('defaultext', None)
    if 'hook' in kw:
        ofn.lpfnHook = kw['hook']
    ofn.lpTemplateName = kw.get('templatename', None)
    if dtype == 'open':
        res = comdlg32.GetOpenFileName(ofn.ref())
    elif dtype == 'save':
        res = comdlg32.GetSaveFileName(ofn.ref())
    else:
        raise ValueError('type must be "open" or "save"')
    return res, ofn


def GetWindowText(hWnd):
    length = user32.GetWindowTextLength(hWnd) + 1
    buf = (types.gettype('WCHAR') * length)()
    user32.GetWindowText(hWnd, buf, length)
    return buf.value


def HIWORD(v, signed=False):
    if signed:
        return types.alloc('SHORT', HIWORD(v, False)).value
    return (v >> 16) & 0xffff


def LOWORD(v, signed=False):
    if signed:
        return types.alloc('SHORT', LOWORD(v, False)).value
    return v & 0xffff


def MAKELONG(lw, hw):
    return (lw & 0xffff) | ((hw & 0xffff) << 16)


_id = 10


def MakeID():
    global _id
    _id += 1
    return _id


def Mainloop(hwnd=None):
    msg = types.alloc('MSG')
    ref = msg.ref()
    while user32.GetMessage(ref, None, 0, 0):
        # Profound! IsDialogMessage processes most of the messages!
        if not hwnd or not user32.IsDialogMessage(hwnd, ref):
            user32.TranslateMessage(ref)
            user32.DispatchMessage(ref)


def MainloopDialog(hwnd):
    # This one seems to make some odd behavior when it comes to dialog window showing/hiding
    msg = types.alloc('MSG')
    ref = msg.ref()
    while user32.GetMessage(ref, None, 0, 0):
        user32.IsDialogMessage(hwnd, ref)
    return msg.wParam


def PrintDlg(hwnd, flags, **kw):
    pd = types.alloc('PRINTDLGEX')
    pd.lStructSize = pd.sizeof()
    pd.hwndOwner = hwnd
    pd.hDevMode = kw.pop('hdevmode', None)
    pd.hDevNames = kw.pop('devnames', None)
    pd.hDC = kw.pop('hdc', None)
    pd.Flags = flags
    pd.Flags2 = kw.pop('flags2', 0)
    pd.ExclusionFlags = kw.pop('exclusionflags', 0)
    pd.nPageRanges = kw.pop('npageranges', 0)
    pd.nMaxPageRanges = mpr = kw.pop('maxpageranges', 0)
    if mpr > 0:
        # noinspection PyProtectedMember
        ppr = kernel32.GlobalAlloc(
            const.GPTR, types.gettype('PRINTPAGERANGE')._size * mpr)
    else:
        ppr = None
    pd.lpPageRanges = ppr
    pd.nMinPage = kw.pop('minpage', 1)
    pd.nMaxPage = kw.pop('maxpage', 1000)
    pd.nCopies = kw.pop('copies', 1)
    pd.hInstance = kw.pop('hinstance', None)
    pd.lpPrintTemplateName = kw.pop('printtemplatename', None)
    pd.lpCallback = kw.pop('callback', None)
    pd.nPropertyPages = kw.pop('npropertypages', 0)
    pd.lphPropertyPages = kw.pop('propertypages', None)
    pd.nStartPage = kw.pop('startpage', 0xffffffff)  # START_PAGE_GENERAL
    pd.dwResultAction = 0
    comdlg32.PrintDlgEx(pd.ref())
    return pd
