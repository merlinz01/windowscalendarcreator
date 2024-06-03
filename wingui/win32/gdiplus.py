
import ctypes
from .types import gettype, winapifunc, winfunctype, winstruct, typedef, okcheck
# ensure types
from . import user32, gdi32

gdiplus = ctypes.windll.gdiplus

class GdiPlusError(OSError):
    'GpStatus error return codes'

STATUSCODES = (
    'Ok',
    'Generic Error',
    'Invalid Parameter',
    'Out Of Memory',
    'Object Busy',
    'Insufficient Buffer',
    'Not Implemented',
    'Win32 Error',
    'Wrong State',
    'Aborted',
    'File Not Found',
    'Value Overflow',
    'Access Denied',
    'Unknown Image Format',
    'Font Family Not Found',
    'Font Style Not Found',
    'Not TrueType Font',
    'Unsupported Gdiplus Version',
    'Gdiplus Not Initialized',
    'Property Not Found',
    'Property Not Supported',
    'Profile Not Found')

def statuscheck(res, func, args):
    if res != 0:
        try: err = STATUSCODES[res]
        except IndexError:
            err = f'error code {res}'
        raise GdiPlusError(err)
    return None

# Typedefs
typedef('INT', 'GpStatus')
typedef('UINT', 'UINT32')
typedef('LPVOID', 'DebugEventProc')
typedef('LPVOID', 'LPGpImage', True)
typedef('LPVOID', 'LPGpBitmap', True)
typedef('LPVOID', 'LPGpGraphics', True)
typedef('DWORD', 'ARGB')
typedef('FLOAT', 'REAL')
typedef('INT', 'PixelFormat')
typedef(gettype('CHAR')*8, 'UCHAR_ARRAY_8')

# Function types
winfunctype('INT NotificationHookProc(ULONG_PTR*);')
winfunctype('VOID NotificationUnhookProc(ULONG_PTR);')

# Structs
winstruct('GUID', '''
ULONG Data1;
USHORT Data2;
USHORT Data3;
UCHAR_ARRAY_8 Data4;''')
typedef('GUID', 'CLSID', True)

winstruct('GdiplusStartupInput', '''
UINT32 GdiplusVersion;
DebugEventProc DebugEventCallback;
BOOL SuppressBackgroundThread;
BOOL SuppressExternalCodecs;''')

winstruct('GdiplusStartupOutput', '''
NotificationHookProc NotificationHook;
NotificationUnhookProc NotificationUnhook;''')

winstruct('ImageCodecInfo', '''
CLSID Clsid;
GUID FormatID;
LPCWSTR CodecName;
LPCWSTR DllName;
LPCWSTR FormatDescription;
LPCWSTR FilenameExtension;
LPCWSTR MimeType;
DWORD Flags;
DWORD Version;
DWORD SigCount;
DWORD SigSize;
BYTE* SigPattern;
BYTE* SigMask;''')

winstruct('EncoderParameter', '''
GUID Guid;
ULONG NumberOfValues;
ULONG Type;
LPVOID Value;''')

# This struct is supposed to expand with more EncoderParameters, but...
winstruct('EncoderParameters', '''
UINT Count;
EncoderParameter Parameters;''')

# Functions
BitmapSetResolution = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipBitmapSetResolution(LPGpBitmap bitmap, REAL xdpi, REAL ydpi);')

CloneBitmapAreaI = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipCloneBitmapAreaI(INT x, INT y, INT width, INT height, '
        'PixelFormat format, LPGpBitmap srcBitmap, LPGpBitmap* dstBitmap);')

CreateBitmapFromFile = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipCreateBitmapFromFile(LPCWSTR filename, LPGpBitmap* bitmap);')

CreateBitmapFromGraphics = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipCreateBitmapFromGraphics('
        'INT width, INT height, LPGpGraphics target, LPGpBitmap* bitmap);')

CreateBitmapFromHBITMAP = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipCreateBitmapFromHBITMAP(HBITMAP hbitmap, HPALETTE hpal, '
                                    'LPGpBitmap* bitmap);')

CreateFromHDC = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipCreateFromHDC(HDC hdc, LPGpGraphics* graphics);')

CreateHBITMAPFromBitmap = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipCreateHBITMAPFromBitmap(LPGpBitmap bitmap, HBITMAP* hbmReturn, '
                                    'ARGB background);')

DeleteGraphics = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipDeleteGraphics(LPGpGraphics graphics);')

DisposeImage = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipDisposeImage(LPGpImage image);')

Free = winapifunc(gdiplus, None,
    'VOID GdipFree(LPVOID GpObject);')

GetImageEncoders = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipGetImageEncoders(UINT numEncoders, UINT size, '
                             'ImageCodecInfo* encoders);')

GetImageEncodersSize = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipGetImageEncodersSize(UINT* numEncoders, UINT* size);')

LoadImageFromFile = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipLoadImageFromFile(LPCWSTR filename, LPGpImage* image);')

SaveImageToFile = winapifunc(gdiplus, statuscheck,
    'GpStatus GdipSaveImageToFile(LPGpImage img, LPCWSTR filename, '
                            'CLSID* encoder, EncoderParameters* params);')

GdiplusStartup = winapifunc(gdiplus, statuscheck,
    'GpStatus GdiplusStartup(ULONG_PTR* token, GdiplusStartupInput* input, '
                       'GdiplusStartupOutput* output);')

GdiplusShutdown = winapifunc(gdiplus, None,
    'GpStatus GdiplusShutdown(ULONG_PTR token);')

# Constants
class gpconst:
    PixelFormatIndexed = 0x00010000
    PixelFormatGDI = 0x00020000
    PixelFormatAlpha = 0x00040000
    PixelFormatPAlpha = 0x00080000
    PixelFormatExtended = 0x00100000
    PixelFormatCanonical = 0x00200000
    PixelFormatUndefined = 0
    PixelFormatDontCare = 0
    PixelFormat1bppIndexed = 1 | (1<<8) | PixelFormatIndexed | PixelFormatGDI
    PixelFormat4bppIndexed = 2 | (4<<8) | PixelFormatIndexed | PixelFormatGDI
    PixelFormat8bppIndexed = 3 | (8<<8) | PixelFormatIndexed | PixelFormatGDI
    PixelFormat16bppGrayScale = 4 | (16<<8) | PixelFormatExtended
    PixelFormat16bppRGB555 = 5 | (16<<8) | PixelFormatGDI
    PixelFormat16bppRGB565 = 6 | (16<<8) | PixelFormatGDI
    PixelFormat16bppARGB1555 = 7 | (16<<8) | PixelFormatAlpha | PixelFormatGDI
    PixelFormat24bppRGB = 8 | (24<<8) | PixelFormatGDI
    PixelFormat32bppRGB = 9 | (32<<8) | PixelFormatGDI
    PixelFormat32bppARGB = \
        10 | (32<<8) | PixelFormatAlpha | PixelFormatGDI | PixelFormatCanonical
    PixelFormat32bppPARGB = \
	11 | (32<<8) | PixelFormatAlpha | PixelFormatPAlpha | PixelFormatGDI
    PixelFormat48bppRGB = 12 | (48<<8) | PixelFormatExtended
    PixelFormat64bppARGB = \
	13 | (64<<8) | PixelFormatAlpha | PixelFormatCanonical \
	| PixelFormatExtended
    PixelFormat64bppPARGB = \
	14 | (64<<8) | PixelFormatAlpha | PixelFormatPAlpha \
	| PixelFormatExtended
    PixelFormatMax = 15
