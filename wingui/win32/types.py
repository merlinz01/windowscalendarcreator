import ctypes
# noinspection PyUnresolvedReferences
from ctypes import (
    byref, POINTER, pointer, create_unicode_buffer, WinError, wstring_at)
import re

TYPE_REG = {}


def typedef(ctype, name, withptr=False):
    if isinstance(ctype, str):
        ctype = TYPE_REG[ctype]
    TYPE_REG[name] = ctype
    if withptr:
        ptrtype = POINTER(ctype)
        typedef(ptrtype, 'LP_' + name)
        typedef(ptrtype, name + '*')


def gettype(name):
    if name.endswith('W'):
        name = name[:-1]
    elif name.endswith('W*'):
        name = name[:-2] + '*'
    return TYPE_REG[name]


def cast(obj, ctype):
    return ctypes.cast(obj, gettype(ctype))


def alloc(name, *args):
    return gettype(name)(*args)


def winapifunc(dll, errcheck, sig):
    doc = sig
    restype, sig = sig.split(' ', 1)
    name, args = sig.rstrip(');').split('(', 1)
    func = getattr(dll, name.strip())
    func.__doc__ = doc
    if errcheck:
        func.errcheck = errcheck
    if args:
        func.argtypes = [
            gettype(x.lstrip().split(' ', 1)[0])
            for x in args.split(',')]
    else:
        func.argtypes = []
    func.restype = gettype(restype.strip())
    return func


def winfunctype(sig, withptr=False):
    restype, sig = sig.lstrip().split(' ', 1)
    name, sig = sig.split('(', 1)
    sig = sig.rstrip('); ').split(',')
    ft = ctypes.WINFUNCTYPE(
        gettype(restype), *(gettype(arg.strip()) for arg in sig))
    typedef(ft, name, withptr)


_struct_re = re.compile(r'\s*(\w+\*?)\s*(\w+);')
_struct_template = ('class {name}(Structure):_fields_ = [{fields}];'
                    'ref=_ref;sizeof=_sizeof;ptr=_ptr\n{name}._size=_sizeof({name})')


def _ref(self):
    return ctypes.byref(self)


def _ptr(self):
    return ctypes.byref(self)


def sizeof(obj):
    return ctypes.sizeof(obj)


def winstruct(name, fields, withptr=True):
    fields = _struct_re.sub(r"('\g<2>', gettype('\g<1>')),", fields)
    code = _struct_template.format(name=name, fields=fields)
    lc = {}
    gb = {'Structure': ctypes.Structure,
          'gettype': gettype,
          '_ptr': _ptr,
          '_ref': _ref,
          '_sizeof': sizeof}
    exec(code, gb, lc)
    typedef(lc[name], name, withptr)


def nullcheck(res, func, args):
    if not res:
        raise WinError()
    return res


def okcheck(res, func, args):
    if res != 0:
        raise OSError(f'error code {res}')
    return res


# ===== General types =====
# LPCWSTR type that accepts int values
class LPCWSTR(ctypes.c_wchar_p):
    @classmethod
    def from_param(cls, value):
        if isinstance(value, int):
            return ctypes.cast(value, ctypes.c_wchar_p)
        return ctypes.c_wchar_p.from_param(value)


typedef(ctypes.c_ushort, 'ATOM')
typedef(ctypes.c_long, 'BOOL')
typedef(ctypes.c_ubyte, 'BYTE', True)
typedef(ctypes.c_char, 'CHAR')
typedef(ctypes.c_char_p, 'CHAR*')
typedef(ctypes.c_ulong, 'DWORD')
typedef(ctypes.c_float, 'FLOAT')
typedef(ctypes.c_void_p, 'HANDLE')
typedef(ctypes.c_void_p, 'HGLOBAL')
typedef(ctypes.c_void_p, 'HINSTANCE')
typedef(ctypes.HRESULT, 'HRESULT')
typedef(ctypes.c_int, 'INT', True)
typedef(ctypes.c_long, 'LONG')
typedef(ctypes.c_void_p, 'LPARAM')
typedef(LPCWSTR, 'LPCWSTR')
typedef(ctypes.c_void_p, 'LPVOID')
typedef(LPCWSTR, 'LPWSTR')
typedef(ctypes.c_long, 'LRESULT')
typedef(ctypes.c_short, 'SHORT')
typedef(ctypes.c_uint, 'UINT', True)
typedef(ctypes.c_uint, 'UINT_PTR')
typedef(ctypes.c_ulong, 'ULONG')
typedef(ctypes.c_ulong, 'ULONG_PTR', True)
typedef(ctypes.c_ushort, 'USHORT')
typedef(None, 'VOID')
typedef(ctypes.c_wchar, 'WCHAR')
typedef(ctypes.c_int, 'WINBOOL')
typedef(ctypes.c_ushort, 'WORD')
typedef(ctypes.c_uint, 'WPARAM')
