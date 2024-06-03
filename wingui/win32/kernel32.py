
import ctypes
from .types import winapifunc, typedef, nullcheck

kernel32 = ctypes.windll.kernel32

# Typedefs
typedef('HANDLE', 'HMODULE')
typedef('HANDLE', 'HGLOBAL')
typedef('ULONG_PTR', 'SIZE_T')

# Functions
GetModuleHandle = winapifunc(kernel32, nullcheck,
    'HMODULE GetModuleHandleW(LPCWSTR lpModuleName);')
GlobalAlloc = winapifunc(kernel32, nullcheck,
    'HGLOBAL GlobalAlloc(UINT uFlags, SIZE_T dwBytes);')
GlobalFree = winapifunc(kernel32, lambda r, f, a: nullcheck(not r, f, a),
    'HGLOBAL GlobalFree(HGLOBAL hMem);')
GlobalHandle = winapifunc(kernel32, nullcheck,
    'HGLOBAL GlobalHandle(LPVOID pMem);')
GlobalLock = winapifunc(kernel32, nullcheck,
    'LPVOID GlobalLock(HGLOBAL hMem);')
GlobalUnlock = winapifunc(kernel32, None,
    'WINBOOL GlobalUnlock(HGLOBAL hMem);')
MulDiv = winapifunc(kernel32, None,
    'INT MulDiv(INT nNumber, INT nNumerator, INT nDenominator);')
