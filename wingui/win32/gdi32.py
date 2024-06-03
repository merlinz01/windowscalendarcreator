
import ctypes
from .const import CLR_INVALID
from .types import winapifunc, winstruct, nullcheck, typedef

gdi32 = ctypes.windll.gdi32

# Typedefs
typedef('HANDLE', 'HDC')
typedef('HANDLE', 'HFONT')
typedef('HANDLE', 'HGDIOBJ')
typedef('HANDLE', 'HPEN')
typedef('HANDLE', 'HPALETTE')
typedef('DWORD', 'COLORREF')
typedef(ctypes.c_wchar * 32, 'WCHAR_ARRAY_32')

# Structs
winstruct('DEVMODE', '''
WCHAR_ARRAY_32 dmDeviceName;
WORD dmSpecVersion;
WORD dmDriverVersion;
WORD dmSize;
WORD dmDriverExtra;
DWORD dmFields;
SHORT dmOrientation;
SHORT dmPaperSize;
SHORT dmPaperLength;
SHORT dmPaperWidth;
SHORT dmScale;
SHORT dmCopies;
SHORT dmDefaultSource;
SHORT dmPrintQuality;
SHORT dmColor;
SHORT dmDuplex;
SHORT dmYResolution;
SHORT dmTTOption;
SHORT dmCollate;
WCHAR_ARRAY_32 dmFormName;
WORD dmLogPixels;
DWORD dmBitsPerPel;
DWORD dmPelsWidth;
DWORD dmPelsHeight;
DWORD dmDisplayFlags;
DWORD dmDisplayFrequency;
DWORD dmICMMethod;
DWORD dmICMIntent;
DWORD dmMediaType;
DWORD dmDitherType;
DWORD dmReserved1;
DWORD dmReserved2;
DWORD dmPanningWidth;
DWORD dmPanningHeight;
''')

winstruct('DOCINFO', '''
INT cbSize;
LPCWSTR lpszDocName;
LPCWSTR lpszOutput;
LPCWSTR lpszDatatype;
DWORD fwType;''')

winstruct('LOGBRUSH', '''
UINT lbStyle;
COLORREF lbColor;
ULONG_PTR lbHatch;''')

winstruct('XFORM', '''
FLOAT eM11;
FLOAT eM12;
FLOAT eM21;
FLOAT eM22;
FLOAT eDx;
FLOAT eDy;''')

# Functions
AbortDoc = winapifunc(gdi32, None,
    'INT AbortDoc(HDC hdc);')

BeginPath = winapifunc(gdi32, nullcheck,
    'WINBOOL BeginPath(HDC hdc);')

BitBlt = winapifunc(gdi32, nullcheck,
    'WINBOOL BitBlt(HDC hdc, INT x, INT y, INT cx, INT cy, HDC hdcSrc, INT x1, '
                   'INT y1, DWORD rop);')

CancelDC = winapifunc(gdi32, nullcheck,
    'WINBOOL CancelDC(HDC hdc);')

CreateBrushIndirect = winapifunc(gdi32, nullcheck,
    'HBRUSH CreateBrushIndirect(LOGBRUSH* plbrush);')

CreateDC = winapifunc(gdi32, nullcheck,
    'HDC CreateDCW(LPCWSTR pwszDriver, LPCWSTR pwszDevice, LPCWSTR pszPort, '
                  'DEVMODE* pdm);')

CreateCompatibleBitmap = winapifunc(gdi32, nullcheck,
    'HBITMAP CreateCompatibleBitmap(HDC hdc, INT nWidth, INT nHeight);')

CreateCompatibleDC = winapifunc(gdi32, nullcheck,
    'HDC CreateCompatibleDC(HDC hdc);')

CreateFont = winapifunc(gdi32, nullcheck,
    'HFONT CreateFontW(INT cHeight, INT cWidth, INT cEscapement, '
                      'INT cOrientation, INT cWeight, DWORD bItalic, '
                      'DWORD bUnderline, DWORD bStrikeOut, DWORD iCharSet, '
                      'DWORD iOutPrecision, DWORD iClipPrecision, '
                      'DWORD iQuality, DWORD iPitchAndFamily, '
                      'LPCWSTR pszFaceName);')

CreatePatternBrush = winapifunc(gdi32, nullcheck,
    'HBRUSH CreatePatternBrush(HBITMAP hbm);')

CreatePen = winapifunc(gdi32, nullcheck,
    'HPEN CreatePen(INT iStyle, INT cWidth, COLORREF color);')

DeleteDC = winapifunc(gdi32, nullcheck,
    'WINBOOL DeleteDC(HDC hdc);')

DeleteObject = winapifunc(gdi32, nullcheck,
    'WINBOOL DeleteObject(HGDIOBJ ho);')

DPtoLP = winapifunc(gdi32, nullcheck,
    'WINBOOL DPtoLP(HDC hdc, POINT* lppt, INT c);')

EndDoc = winapifunc(gdi32, None,
    'INT EndDoc(HDC hdc);')

EndPage = winapifunc(gdi32, None,
    'INT EndPage(HDC hdc);')

EndPath = winapifunc(gdi32, nullcheck,
    'WINBOOL EndPath(HDC hdc);')

FillPath = winapifunc(gdi32, nullcheck,
    'WINBOOL FillPath(HDC hdc);')

GetBitmapDimensionEx = winapifunc(gdi32, nullcheck,
    'WINBOOL GetBitmapDimensionEx(HBITMAP hbit, SIZE* lpsize);')

GetClipBox = winapifunc(gdi32, nullcheck,
    'INT GetClipBox(HDC hdc, RECT* lprect);')

GetDeviceCaps = winapifunc(gdi32, None,
    'INT GetDeviceCaps(HDC hdc, INT index);')

GetMapMode = winapifunc(gdi32, nullcheck,
    'INT GetMapMode(HDC hdc);')

GetStockObject = winapifunc(gdi32, nullcheck,
    'HANDLE GetStockObject(INT i);')

GetTextExtentPoint32 = winapifunc(gdi32, nullcheck,
    'WINBOOL GetTextExtentPoint32W(HDC hdc, LPCWSTR lpString, INT c, '
                                  'SIZE* psizl);')

LineTo = winapifunc(gdi32, nullcheck,
    'WINBOOL LineTo(HDC hdc, INT x, INT y);')

LPtoDP = winapifunc(gdi32, nullcheck,
    'WINBOOL LPtoDP(HDC hdc, POINT* lppt, INT c);')

MoveToEx = winapifunc(gdi32, nullcheck,
    'WINBOOL MoveToEx(HDC hdc, INT x, INT y, POINT* lpPoint);')

Rectangle = winapifunc(gdi32, nullcheck,
    'WINBOOL Rectangle(HDC hdc, INT left, INT top, INT right, INT bottom);')

ResetDC = winapifunc(gdi32, nullcheck,
    'HDC ResetDCW(HDC hdc, DEVMODEW* lpdm);')

SelectObject = winapifunc(gdi32, nullcheck,
    'HGDIOBJ SelectObject(HDC hdc, HGDIOBJ h);')

def clr_invalid_check(res, func, args):
    if res == CLR_INVALID:
        raise ValueError('invalid color (CLR_INVALID)')
    return res
SetBkColor = winapifunc(gdi32, clr_invalid_check,
    'COLORREF SetBkColor(HDC hdc, COLORREF color);')

SetBkMode = winapifunc(gdi32, nullcheck,
    'INT SetBkMode(HDC hdc, INT iBkMode);')

SetBrushOrgEx = winapifunc(gdi32, nullcheck,
    'WINBOOL SetBrushOrgEx(HDC hdc, INT x, INT y, POINT* lppt);')

SetGraphicsMode = winapifunc(gdi32, nullcheck,
    'INT SetGraphicsMode(HDC hdc, INT iMode);')

SetMapMode = winapifunc(gdi32, nullcheck,
    'INT SetMapMode(HDC hdc, INT iMode);')

SetStretchBltMode = winapifunc(gdi32, nullcheck,
    'INT SetStretchBltMode(HDC hdc, INT mode);')

SetTextColor = winapifunc(gdi32, clr_invalid_check,
    'COLORREF SetTextColor(HDC hdc, COLORREF crColor);')

SetWorldTransform = winapifunc(gdi32, nullcheck,
    'BOOL SetWorldTransform(HDC hdc, XFORM* lpXform);')

StartDoc = winapifunc(gdi32, None,
    'INT StartDocW(HDC hdc, DOCINFOW* lpdi);')

StartPage = winapifunc(gdi32, None,
    'INT StartPage(HDC hdc);')

StretchBlt = winapifunc(gdi32, nullcheck,
    'WINBOOL StretchBlt(HDC hdcDest, INT xDest, INT yDest, INT wDest, '
                       'INT hDest, HDC hdcSrc, INT xSrc, INT ySrc, INT wSrc, '
                       'INT hSrc, DWORD rop);')

StrokeAndFillPath = winapifunc(gdi32, nullcheck,
    'WINBOOL StrokeAndFillPath(HDC hdc);')

TextOut = winapifunc(gdi32, nullcheck,
    'WINBOOL TextOutW(HDC hdc, INT x, INT y, LPCWSTR lpString, INT c);')
