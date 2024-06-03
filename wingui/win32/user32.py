
import ctypes
from .types import gettype, winapifunc, winfunctype, winstruct, nullcheck, typedef

user32 = ctypes.windll.user32

# Typedefs
typedef('HANDLE', 'HBITMAP', True)
typedef('HANDLE', 'HICON')
typedef('HANDLE', 'HCURSOR')
typedef('HANDLE', 'HBRUSH')
typedef('HANDLE', 'HDC')
typedef('HANDLE', 'HMENU')
typedef('HANDLE', 'HWND')
typedef(gettype('BYTE')*32, 'BYTE_ARRAY_32')

# Function types
winfunctype('LRESULT WNDPROC(HWND, UINT, WPARAM, LPARAM);')
winfunctype('WINBOOL WNDENUMPROC(HWND, LPARAM);')

# Structs
winstruct('WNDCLASSEX', '''
UINT cbSize;
UINT style;
WNDPROC lpfnWndProc;
INT cbClsExtra;
INT cbWndExtra;
HINSTANCE hInstance;
HICON hIcon;
HCURSOR hCursor;
HBRUSH hbrBackground;
LPCWSTR lpszMenuName;
LPCWSTR lpszClassName;
HICON hIconSm;''')

winstruct('RECT', '''
LONG left;
LONG top;
LONG right;
LONG bottom;''')

winstruct('SIZE', '''
LONG cx;
LONG cy;''')

winstruct('POINT', '''
LONG x;
LONG y;''')

winstruct('MSG', '''
HWND hwnd;
UINT message;
WPARAM wParam;
LPARAM lParam;
DWORD time;
POINT pt;''')

winstruct('NMHDR', '''
HWND hwndFrom;
UINT_PTR idFrom;
INT code;''')  # was UINT

winstruct('MENUITEMINFO', '''
UINT cbSize;
UINT fMask;
UINT fType;
UINT fState;
UINT wID;
HMENU hSubMenu;
HBITMAP hbmpChecked;
HBITMAP hbmpUnchecked;
ULONG_PTR dwItemData;
LPWSTR dwTypeData;
UINT cch;
HBITMAP hbmpItem;''')

winstruct('PAINTSTRUCT', '''
HDC hdc; 
BOOL fErase; 
RECT rcPaint; 
BOOL fRestore; 
BOOL fIncUpdate; 
BYTE_ARRAY_32 rgbReserved; ''')

winstruct('SCROLLINFO', '''
UINT cbSize;
UINT fMask;
INT nMin;
INT nMax;
UINT nPage;
INT nPos;
INT nTrackPos;''')

# noinspection PyCodeStyle
AnimateWindow = winapifunc(user32, nullcheck,
    'WINBOOL AnimateWindow(HWND hWnd, DWORD dwTime, DWORD dwFlags);')

AppendMenu = winapifunc(user32, nullcheck,
    'WINBOOL AppendMenuW(HMENU hMenu, UINT uFlags, UINT_PTR uIDNewItem, '
                        'LPCWSTR lpNewItem);')

BeginPaint = winapifunc(user32, nullcheck,
    'HDC BeginPaint(HWND hwnd, PAINTSTRUCT* lpPaint);')

BringWindowToTop = winapifunc(user32, nullcheck,
    'WINBOOL BringWindowToTop(HWND hWnd);')

CallWindowProc = winapifunc(user32, None,
    'LRESULT CallWindowProcW(WNDPROC lpPrevWndFunc, HWND hWnd, UINT Msg, '
                            'WPARAM wParam, LPARAM lParam);')

ChangeMenu = winapifunc(user32, nullcheck,
    'WINBOOL ChangeMenuW(HMENU hMenu, UINT cmd, LPCWSTR lpszNewItem, '
                        'UINT cmdInsert, UINT flags);')

CheckMenuItem = winapifunc(user32, None,
    'DWORD CheckMenuItem(HMENU hMenu, UINT uIDCheckItem, UINT uCheck);')

ChildWindowFromPointEx = winapifunc(user32, nullcheck,
    'HWND ChildWindowFromPointEx(HWND hwnd, POINT pt, UINT flags);')

CloseWindow = winapifunc(user32, nullcheck,
    'WINBOOL CloseWindow(HWND hWnd);')

CopyIcon = winapifunc(user32, nullcheck,
    'HICON CopyIcon(HICON hIcon);')

CopyImage = winapifunc(user32, nullcheck,
    'HANDLE CopyImage(HANDLE h, UINT type, INT cx, INT cy, UINT flags);')

CreateMenu = winapifunc(user32, nullcheck,
    'HMENU CreateMenu();')

CreatePopupMenu = winapifunc(user32, nullcheck,
    'HMENU CreatePopupMenu();')

CreateWindowEx = winapifunc(user32, nullcheck,
    'HWND CreateWindowExW(DWORD dwExStyle, LPCWSTR lpClassName, '
                         'LPCWSTR lpWindowName, DWORD dwStyle, INT X, INT Y, '
                         'INT nWidth, INT nHeight, HWND hWndParent, '
                         'HMENU hMenu, HINSTANCE hInstance, LPVOID lpParam);')

DefWindowProc = winapifunc(user32, None,
    'LRESULT DefWindowProcW(HWND hWnd, UINT Msg, WPARAM wParam, '
                           'LPARAM lParam);')

DeleteMenu = winapifunc(user32, nullcheck,
    'WINBOOL DeleteMenu(HMENU hMenu, UINT uPosition, UINT uFlags);')

DestroyCursor = winapifunc(user32, nullcheck,
    'WINBOOL DestroyCursor(HCURSOR hCursor);')

DestroyIcon = winapifunc(user32, nullcheck,
    'WINBOOL DestroyIcon(HICON hIcon);')

DestroyMenu = winapifunc(user32, nullcheck,
    'WINBOOL DestroyMenu(HMENU hMenu);')

DestroyWindow = winapifunc(user32, nullcheck,
    'WINBOOL DestroyWindow(HWND hWnd);')

DispatchMessage = winapifunc(user32, None,
    'LRESULT DispatchMessageW(MSG* lpMsg);')

DrawEdge = winapifunc(user32, nullcheck,
    'INT DrawEdge(HDC hdc, RECT* qrc, UINT edge, UINT grfFlags);')

DrawFocusRect = winapifunc(user32, nullcheck,
    'INT DrawFocusRect(HDC hdc, RECT* lprc);')

DrawIcon = winapifunc(user32, nullcheck,
    'WINBOOL DrawIcon(HDC hDC, INT X, INT Y, HICON hIcon);')

DrawMenuBar = winapifunc(user32, nullcheck,
    'WINBOOL DrawMenuBar(HWND hWnd);')

DrawText = winapifunc(user32, nullcheck,
    'INT DrawTextW(HDC hdc, LPCWSTR lpchText, INT cchText, RECT* lprc, '
                  'UINT format);')

EnableMenuItem = winapifunc(user32, nullcheck,
    'WINBOOL EnableMenuItem(HMENU hMenu, UINT uIDEnableItem, UINT uEnable);')

EnableScrollBar = winapifunc(user32, nullcheck,
    'WINBOOL EnableScrollBar(HWND hWnd, UINT wSBflags, UINT wArrows);')

EnableWindow = winapifunc(user32, None,
    'WINBOOL EnableWindow(HWND hWnd, WINBOOL bEnable);')

EndMenu = winapifunc(user32, nullcheck,
    'WINBOOL EndMenu();')

EndPaint = winapifunc(user32, None,
    'BOOL EndPaint(HWND hwnd, PAINTSTRUCT* lpPaint);')

EnumChildWindows = winapifunc(user32, nullcheck,
    'WINBOOL EnumChildWindows(HWND hWndParent, WNDENUMPROC lpEnumFunc, '
                              'LPARAM lParam);')

FillRect = winapifunc(user32, nullcheck,
    'INT FillRect(HDC hDC, RECT* lprc, HBRUSH hbr);')

FlashWindow = winapifunc(user32, nullcheck,
    'WINBOOL FlashWindow(HWND hWnd, WINBOOL bInvert);')

GetActiveWindow = winapifunc(user32, None,
    'HWND GetActiveWindow();')

GetClassInfoEx = winapifunc(user32, None,
    'WINBOOL GetClassInfoExW(HINSTANCE hInstance, LPCWSTR lpszClass, '
                            'WNDCLASSEXW* lpwcx);')

GetClassLong = winapifunc(user32, None,
    'DWORD GetClassLongW(HWND hWnd, INT nIndex);')

GetClassName = winapifunc(user32, None,
    'INT GetClassNameW(HWND hWnd, LPWSTR lpClassName, INT nMaxCount);')

GetClientRect = winapifunc(user32, nullcheck,
    'WINBOOL GetClientRect(HWND hWnd, RECT* lpRect);')

GetCursor = winapifunc(user32, None,
    'HCURSOR GetCursor();')

GetCursorPos = winapifunc(user32, nullcheck,
    'WINBOOL GetCursorPos(POINT* lpPoint);')

GetDC = winapifunc(user32, nullcheck,
    'HDC GetDC(HWND hWnd);')

GetDesktopWindow = winapifunc(user32, None,
    'HWND GetDesktopWindow();')

GetDlgCtrlID = winapifunc(user32, nullcheck,
    'INT GetDlgCtrlID(HWND hWnd);')

GetFocus = winapifunc(user32, None,
    'HWND GetFocus();')

GetForegroundWindow = winapifunc(user32, None,
    'HWND GetForegroundWindow();')

GetKeyState = winapifunc(user32, None,
    'USHORT GetKeyState(INT nVirtKey);')

GetMenu = winapifunc(user32, nullcheck,
    'HMENU GetMenu(HWND hWnd);')

GetMenuCheckMarkDimensions = winapifunc(user32, None,
    'LONG GetMenuCheckMarkDimensions();')

GetMenuItemCount = winapifunc(user32, None,
    'INT GetMenuItemCount(HMENU hMenu);')

GetMenuItemID = winapifunc(user32, None,
    'UINT GetMenuItemID(HMENU hMenu, INT nPos);')

GetMenuItemInfo = winapifunc(user32, nullcheck,
    'WINBOOL GetMenuItemInfoW(HMENU hmenu, UINT item, WINBOOL fByPosition, '
                             'MENUITEMINFOW* lpmii);')

GetMenuState = winapifunc(user32, None,
    'UINT GetMenuState(HMENU hMenu, UINT uId, UINT uFlags);')

GetMessage = winapifunc(user32, None,
    'WINBOOL GetMessageW(MSG* lpMsg, HWND hWnd, UINT wMsgFilterMin, '
                        'UINT wMsgFilterMax);')

GetNextDlgTabItem = winapifunc(user32, nullcheck,
    'HWND GetNextDlgTabItem(HWND hDlg, HWND hCtl, WINBOOL bPrevious);')

GetParent = winapifunc(user32, None,
    'HWND GetParent(HWND hWnd);')

GetScrollPos = winapifunc(user32, None,
    'INT GetScrollPos(HWND hWnd, INT nBar);')

GetScrollRange = winapifunc(user32, nullcheck,
    'WINBOOL GetScrollRange(HWND hWnd, INT nBar, '
                            'INT* lpMinPos, INT* lpMaxPos);')

GetSubMenu = winapifunc(user32, nullcheck,
    'HMENU GetSubMenu(HMENU hMenu, INT nPos);')

GetSysColor = winapifunc(user32, None,
    'DWORD GetSysColor(INT nIndex);')

GetSysColorBrush = winapifunc(user32, None,
    'HBRUSH GetSysColorBrush(INT nIndex);')

GetSystemMenu = winapifunc(user32, nullcheck,
    'HMENU GetSystemMenu(HWND hWnd, WINBOOL bRevert);')

GetTopWindow = winapifunc(user32, None,
    'HWND GetTopWindow(HWND hWnd);')

GetWindowDC = winapifunc(user32, nullcheck,
    'HDC GetWindowDC(HWND hWnd);')

GetWindowLong = winapifunc(user32, nullcheck,
    'LONG GetWindowLongW(HWND hWnd, INT nIndex);')

GetWindowRect = winapifunc(user32, nullcheck,
    'WINBOOL GetWindowRect(HWND hWnd, RECT* lpRect);')

GetWindowText = winapifunc(user32, None,
    'INT GetWindowTextW(HWND hWnd, LPWSTR lpString, INT nMaxCount);')

GetWindowTextLength = winapifunc(user32, None,
    'INT GetWindowTextLengthW(HWND hWnd);')

HiliteMenuItem = winapifunc(user32, nullcheck,
    'WINBOOL HiliteMenuItem(HWND hWnd, HMENU hMenu, UINT uIDHiliteItem, '
                           'UINT uHilite);')

InsertMenu = winapifunc(user32, nullcheck,
    'WINBOOL InsertMenuW(HMENU hMenu, UINT uPosition, UINT uFlags, '
                        'UINT_PTR uIDNewItem, LPCWSTR lpNewItem);')

InsertMenuItem = winapifunc(user32, nullcheck,
    'WINBOOL InsertMenuItemW(HMENU hmenu, UINT item, WINBOOL fByPosition, '
                            'MENUITEMINFOW* lpmi);')

InvalidateRect = winapifunc(user32, nullcheck,
    'BOOL InvalidateRect(HWND hWnd, RECT* lpRect, BOOL bErase);')

IsChild = winapifunc(user32, None,
    'WINBOOL IsChild(HWND hWndParent, HWND hWnd);')

IsDialogMessage = winapifunc(user32, None,
    'WINBOOL IsDialogMessageW(HWND hDlg, MSG* lpMsg);')

IsIconic = winapifunc(user32, None,
    'WINBOOL IsIconic(HWND hWnd);')

IsMenu = winapifunc(user32, None,
    'WINBOOL IsMenu(HMENU hMenu);')

IsWindow = winapifunc(user32, None,
    'WINBOOL IsWindow(HWND hWnd);')

IsWindowEnabled = winapifunc(user32, None,
    'WINBOOL IsWindowEnabled(HWND hWnd);')

IsWindowVisible = winapifunc(user32, None,
    'WINBOOL IsWindowVisible(HWND hWnd);')

IsZoomed = winapifunc(user32, None,
    'WINBOOL IsZoomed(HWND hWnd);')

LoadBitmap = winapifunc(user32, nullcheck,
    'HBITMAP LoadBitmapW(HINSTANCE hInstance, LPCWSTR lpBitmapName);')

LoadCursor = winapifunc(user32, nullcheck,
    'HCURSOR LoadCursorW(HINSTANCE hInstance, LPCWSTR lpCursorName);')

LoadCursorFromFile = winapifunc(user32, nullcheck,
    'HCURSOR LoadCursorFromFileW(LPCWSTR lpFileName);')

LoadIcon = winapifunc(user32, nullcheck,
    'HICON LoadIconW(HINSTANCE hInstance, LPCWSTR lpIconName);')

LoadImage = winapifunc(user32, nullcheck,
    'HANDLE LoadImageW(HINSTANCE hInst, LPCWSTR name, UINT type, INT cx, '
                      'INT cy, UINT fuLoad);')

LoadMenu = winapifunc(user32, nullcheck,
    'HMENU LoadMenuW(HINSTANCE hInstance, LPCWSTR lpMenuName);')

MessageBeep = winapifunc(user32, nullcheck,
    'WINBOOL MessageBeep(UINT uType);')

MessageBox = winapifunc(user32, None,
    'INT MessageBoxW(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType);')

ModifyMenu = winapifunc(user32, nullcheck,
    'WINBOOL ModifyMenuW(HMENU hMnu, UINT uPosition, UINT uFlags, '
                        'UINT_PTR uIDNewItem, LPCWSTR lpNewItem);')

MoveWindow = winapifunc(user32, nullcheck,
    'WINBOOL MoveWindow(HWND hWnd, INT X, INT Y, INT nWidth, INT nHeight, '
                       'WINBOOL bRepaint);')

PeekMessage = winapifunc(user32, None,
    'WINBOOL PeekMessageW(MSG* lpMsg, HWND hWnd, UINT wMsgFilterMin, '
                         'UINT wMsgFilterMax, UINT wRemoveMsg);')

PostMessage = winapifunc(user32, None,
    'WINBOOL PostMessageW (HWND hWnd, UINT Msg, WPARAM wParam, LPARAM lParam);')

PostQuitMessage = winapifunc(user32, None,
    'VOID PostQuitMessage(INT nExitCode);')

PostThreadMessage = winapifunc(user32, None,
    'WINBOOL PostThreadMessageW(DWORD idThread, UINT Msg, WPARAM wParam, '
                               'LPARAM lParam);')

PrintWindow = winapifunc(user32, nullcheck,
    'WINBOOL PrintWindow (HWND hwnd, HDC hdcBlt, UINT nFlags);')

ReleaseDC = winapifunc(user32, None,
    'INT ReleaseDC(HWND hWnd, HDC hDC);')

ReleaseCapture = winapifunc(user32, nullcheck,
    'BOOL ReleaseCapture();')

RemoveMenu = winapifunc(user32, nullcheck,
    'WINBOOL RemoveMenu(HMENU hMenu, UINT uPosition, UINT uFlags);')

RegisterClassEx = winapifunc(user32, nullcheck,
    'ATOM RegisterClassExW(WNDCLASSEXW* wc);')

RegisterWindowMessage = winapifunc(user32, None,
    'UINT RegisterWindowMessageW(LPCWSTR lpString);')

ReplyMessage = winapifunc(user32, None,
    'WINBOOL ReplyMessage(LRESULT lResult);')

SendMessage = winapifunc(user32, None,
    'LRESULT SendMessageW(HWND hWnd, UINT Msg, WPARAM wParam, LPARAM lParam);')

SetFocus = winapifunc(user32, None,
    'HWND SetFocus(HWND hWnd);')

SetActiveWindow = winapifunc(user32, None,
    'HWND SetActiveWindow(HWND hWnd);')

SetCapture = winapifunc(user32, None,
    'HWND SetCapture(HWND hWnd);')

SetClassLong = winapifunc(user32, None,
    'DWORD SetClassLongW(HWND hWnd, INT nIndex, LONG dwNewLong);')

SetCursor = winapifunc(user32, None,
    'HCURSOR SetCursor(HCURSOR hCursor);')

SetCursorPos = winapifunc(user32, nullcheck,
    'WINBOOL SetCursorPos(INT X, INT Y);')

SetForegroundWindow = winapifunc(user32, nullcheck,
    'WINBOOL SetForegroundWindow(HWND hWnd);')

SetMenu = winapifunc(user32, nullcheck,
    'WINBOOL SetMenu(HWND hWnd, HMENU hMenu);')

SetMenuItemBitmaps = winapifunc(user32, nullcheck,
    'WINBOOL SetMenuItemBitmaps(HMENU hMenu, UINT uPosition, UINT uFlags, '
                           'HBITMAP hBitmapUnchecked, HBITMAP hBitmapChecked);')

SetMenuItemInfo = winapifunc(user32, nullcheck,
    'WINBOOL SetMenuItemInfoW(HMENU hmenu, UINT item, WINBOOL fByPosition, '
                             'MENUITEMINFOW* lpmii);')

SetParent = winapifunc(user32, nullcheck,
    'HWND SetParent(HWND hWndChild, HWND hWndNewParent);')

SetScrollInfo = winapifunc(user32, None,
    'INT SetScrollInfo(HWND hwnd, INT fnBar, SCROLLINFO* lpsi, BOOL fRedraw);')

SetScrollPos = winapifunc(user32, nullcheck,
    'INT SetScrollPos(HWND hWnd, INT nBar, INT nPos, WINBOOL bRedraw);')

SetScrollRange = winapifunc(user32, nullcheck,
    'WINBOOL SetScrollRange(HWND hWnd, INT nBar, INT nMinPos, INT nMaxPos, '
                           'WINBOOL bRedraw);')

SetWindowLong = winapifunc(user32, None,
    'LONG SetWindowLongW(HWND hWnd, INT nIndex, LPVOID dwNewLong);')

SetWindowPos = winapifunc(user32, nullcheck,
    'WINBOOL SetWindowPos(HWND hWnd, HWND hWndInsertAfter, INT X, INT Y, '
                         'INT cx, INT cy, UINT uFlags);')

SetWindowText = winapifunc(user32, nullcheck,
    'WINBOOL SetWindowTextW(HWND hWnd, LPCWSTR lpString);')

ShowCursor = winapifunc(user32, None,
    'INT ShowCursor(WINBOOL bShow);')

ShowScrollBar = winapifunc(user32, nullcheck,
    'WINBOOL ShowScrollBar(HWND hWnd, INT wBar, WINBOOL bShow);')

ShowWindow = winapifunc(user32, None,
    'WINBOOL ShowWindow(HWND hWnd, INT nCmdShow);')

ShowWindowAsync = winapifunc(user32, nullcheck,
    'WINBOOL ShowWindowAsync(HWND hWnd, INT nCmdShow);')

SwitchToThisWindow = winapifunc(user32, None,
    'VOID SwitchToThisWindow(HWND hwnd, WINBOOL fUnknown);')

TrackPopupMenu = winapifunc(user32, nullcheck,
    'BOOL TrackPopupMenu(HMENU hMenu, UINT uFlags, INT x, INT y, INT nReserved, HWND hWnd, RECT* prcRect);')

TranslateMessage = winapifunc(user32, None,
    'WINBOOL TranslateMessage(MSG* lpMsg);')

UnregisterClass = winapifunc(user32, nullcheck,
    'WINBOOL UnregisterClassW(LPCWSTR lpClassName, HINSTANCE hInstance);')

UpdateWindow = winapifunc(user32, nullcheck,
    'WINBOOL UpdateWindow(HWND hWnd);')

WaitMessage = winapifunc(user32, None,
    'WINBOOL WaitMessage();')

WindowFromPoint = winapifunc(user32, nullcheck,
    'HWND WindowFromPoint(POINT Point);')
