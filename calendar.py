import configparser
import ctypes
import datetime
import os
from ctypes import (
    Structure,
    byref,
    c_int,
    c_short,
    c_uint,
    c_ulong,
    c_ushort,
    c_void_p,
    c_wchar,
    c_wchar_p,
    sizeof,
    wintypes,
)

# Load Windows DLLs
gdi32 = ctypes.windll.gdi32
user32 = ctypes.windll.user32
winspool = ctypes.WinDLL("winspool.drv")
gdiplus = ctypes.windll.gdiplus

# Windows constants
DM_ORIENTATION = 0x00000001
DMORIENT_LANDSCAPE = 2
MM_HIENGLISH = 5
TRANSPARENT = 1
OPAQUE = 2

# DrawText flags
DT_LEFT = 0x00000000
DT_CENTER = 0x00000001
DT_NOCLIP = 0x00000100
DT_WORDBREAK = 0x00000010
DT_NOPREFIX = 0x00000800

# Font weights
FW_NORMAL = 400
FW_BOLD = 700

# Pen styles
PS_SOLID = 0

# Brush styles
BS_SOLID = 0

# Raster operations
SRCCOPY = 0x00CC0020

# GDI object types
OBJ_PEN = 1
OBJ_BRUSH = 2
OBJ_FONT = 3


# Structures
class RECT(Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class DOCINFO(Structure):
    _fields_ = [
        ("cbSize", c_int),
        ("lpszDocName", c_wchar_p),
        ("lpszOutput", c_wchar_p),
        ("lpszDatatype", c_wchar_p),
        ("fwType", wintypes.DWORD),
    ]


class DEVMODE(Structure):
    _fields_ = [
        ("dmDeviceName", c_wchar * 32),
        ("dmSpecVersion", c_ushort),
        ("dmDriverVersion", c_ushort),
        ("dmSize", c_ushort),
        ("dmDriverExtra", c_ushort),
        ("dmFields", c_ulong),
        ("dmOrientation", c_short),
        ("dmPaperSize", c_short),
        ("dmPaperLength", c_short),
        ("dmPaperWidth", c_short),
        ("dmScale", c_short),
        ("dmCopies", c_short),
        ("dmDefaultSource", c_short),
        ("dmPrintQuality", c_short),
        ("dmColor", c_short),
        ("dmDuplex", c_short),
        ("dmYResolution", c_short),
        ("dmTTOption", c_short),
        ("dmCollate", c_short),
        ("dmFormName", c_wchar * 32),
        ("dmLogPixels", c_ushort),
        ("dmBitsPerPel", c_ulong),
        ("dmPelsWidth", c_ulong),
        ("dmPelsHeight", c_ulong),
        ("dmDisplayFlags", c_ulong),
        ("dmDisplayFrequency", c_ulong),
        ("dmICMMethod", c_ulong),
        ("dmICMIntent", c_ulong),
        ("dmMediaType", c_ulong),
        ("dmDitherType", c_ulong),
        ("dmReserved1", c_ulong),
        ("dmReserved2", c_ulong),
        ("dmPanningWidth", c_ulong),
        ("dmPanningHeight", c_ulong),
        ("dmICMFlags", c_ulong),
        ("dmNup", c_ulong),
        ("dmDisplayOrientation", c_ulong),
        ("dmDisplayFixedOutput", c_ulong),
    ]


class GdiplusStartupInput(Structure):
    _fields_ = [
        ("GdiplusVersion", c_uint),
        ("DebugEventCallback", c_void_p),
        ("SuppressBackgroundThread", wintypes.BOOL),
        ("SuppressExternalCodecs", wintypes.BOOL),
    ]


class DC:
    def __init__(self, hdc):
        self.hdc = hdc
        self._objects = []

    @staticmethod
    def Create(driver, device, devmode=None):
        hdc = gdi32.CreateDCW(driver, device, None, devmode)
        if not hdc:
            raise ctypes.WinError()
        return DC(hdc)

    @staticmethod
    def CreateCompatible(hdc):
        new_hdc = gdi32.CreateCompatibleDC(hdc)
        if not new_hdc:
            raise ctypes.WinError()
        return DC(new_hdc)

    def SetMapMode(self, mode):
        gdi32.SetMapMode(self.hdc, mode)

    def StartDoc(self, doc_name):
        di = DOCINFO()
        di.cbSize = sizeof(DOCINFO)
        di.lpszDocName = doc_name
        di.lpszOutput = None
        di.lpszDatatype = None
        di.fwType = 0
        result = gdi32.StartDocW(self.hdc, byref(di))
        if result <= 0:
            raise ctypes.WinError()

    def EndDoc(self):
        gdi32.EndDoc(self.hdc)

    def StartPage(self):
        gdi32.StartPage(self.hdc)

    def EndPage(self):
        gdi32.EndPage(self.hdc)

    def SetBkMode(self, transparent=False):
        gdi32.SetBkMode(self.hdc, TRANSPARENT if transparent else OPAQUE)

    def SetTextColor(self, color):
        gdi32.SetTextColor(self.hdc, color)

    def DrawText(self, left, top, right, bottom, text, flags):
        rect = RECT(left, top, right, bottom)
        user32.DrawTextW(self.hdc, text, -1, byref(rect), flags)

    def DrawText2(self, left, top, width, height, text, flags):
        rect = RECT(left, top, left + width, top + height)
        user32.DrawTextW(self.hdc, text, -1, byref(rect), flags)

    def SetFont(self, name, height, width=0, underline=False, weight=FW_NORMAL):
        hfont = gdi32.CreateFontW(
            height,
            width,
            0,  # escapement
            0,  # orientation
            weight,
            0,  # italic
            1 if underline else 0,
            0,  # strikeout
            1,  # charset (DEFAULT_CHARSET)
            0,  # output precision
            0,  # clip precision
            0,  # quality
            0,  # pitch and family
            name,
        )
        if not hfont:
            raise ctypes.WinError()
        old = gdi32.SelectObject(self.hdc, hfont)
        if old:
            self._objects.append(old)
        return hfont

    def SetPen(self, width, color):
        hpen = gdi32.CreatePen(PS_SOLID, width, color)
        if not hpen:
            raise ctypes.WinError()
        old = gdi32.SelectObject(self.hdc, hpen)
        if old:
            self._objects.append(old)
        return hpen

    def SetBrush(self, color):
        hbrush = gdi32.CreateSolidBrush(color)
        if not hbrush:
            raise ctypes.WinError()
        old = gdi32.SelectObject(self.hdc, hbrush)
        if old:
            self._objects.append(old)
        return hbrush

    def Rectangle(self, left, top, right, bottom):
        gdi32.Rectangle(self.hdc, left, top, right, bottom)

    def MoveTo(self, x, y):
        gdi32.MoveToEx(self.hdc, x, y, None)

    def LineTo(self, x, y):
        gdi32.LineTo(self.hdc, x, y)

    def SelectObject(self, obj):
        if isinstance(obj, int):
            obj = c_void_p(obj)
        old = gdi32.SelectObject(self.hdc, obj)
        if not old:
            raise ctypes.WinError()
        return old

    def GetClipBox(self):
        rect = RECT()
        gdi32.GetClipBox(self.hdc, byref(rect))
        return (rect.left, rect.top, rect.right, rect.bottom)

    def StretchBlt(
        self, x, y, width, height, src_dc, src_x, src_y, src_width, src_height, rop
    ):
        gdi32.StretchBlt(
            self.hdc,
            x,
            y,
            width,
            height,
            src_dc,
            src_x,
            src_y,
            src_width,
            src_height,
            rop,
        )

    def Delete(self):
        if self.hdc:
            gdi32.DeleteDC(self.hdc)
            self.hdc = None


def gdiplus_startup():
    gdiplustartupinput = GdiplusStartupInput()
    gdiplustartupinput.GdiplusVersion = 1
    gdiplustartupinput.DebugEventCallback = None
    gdiplustartupinput.SuppressBackgroundThread = False
    gdiplustartupinput.SuppressExternalCodecs = False

    token = c_void_p()
    status = gdiplus.GdiplusStartup(byref(token), byref(gdiplustartupinput), None)
    if status != 0:
        raise RuntimeError(f"GdiplusStartup failed with status {status}")
    return token


def gdiplus_shutdown(token):
    gdiplus.GdiplusShutdown(token)


class Bitmap:
    def __init__(self, gpbitmap):
        self.gpbitmap = gpbitmap
        self.gdiplus = ctypes.windll.gdiplus

    @staticmethod
    def FromFile(filename):
        gdiplus = ctypes.windll.gdiplus
        gpbitmap = c_void_p()
        status = gdiplus.GdipCreateBitmapFromFile(filename, byref(gpbitmap))
        if status != 0:
            raise RuntimeError(f"GdipCreateBitmapFromFile failed with status {status}")
        return Bitmap(gpbitmap)

    def GetHBITMAP(self):
        hbitmap = c_void_p()
        status = self.gdiplus.GdipCreateHBITMAPFromBitmap(
            self.gpbitmap, byref(hbitmap), 0
        )
        if status != 0:
            raise RuntimeError(
                f"GdipCreateHBITMAPFromBitmap failed with status {status}"
            )
        return hbitmap.value

    def Dispose(self):
        if self.gpbitmap:
            self.gdiplus.GdipDisposeImage(self.gpbitmap)
            self.gpbitmap = None


def main():
    cfg = configparser.RawConfigParser()
    cfg.read("calendar.ini")

    OUTPUT_BITMAPS = not cfg.getboolean("General", "Skip-bitmaps")
    MONTHS = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )
    WEEKDAYS = (
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    )

    dm = DEVMODE()
    dm.dmSize = sizeof(DEVMODE)
    dm.dmFields = DM_ORIENTATION
    dm.dmOrientation = DMORIENT_LANDSCAPE
    dc = DC.Create("WINSPOOL", "Microsoft Print to PDF", byref(dm))
    dc.SetMapMode(MM_HIENGLISH)
    dc.StartDoc("Calendar")
    dc.SetBkMode(transparent=True)

    birthdays = open("birthdays.txt").read()
    birthdays = (
        ln.split(" ", 1)
        for ln in birthdays.splitlines(False)
        if ln.lstrip() and ln.lstrip()[0] != "#"
    )
    birthdays = [(*d.split("/"), n.strip()) for d, n in birthdays]
    birthdays = [(int(m), int(d), int(y), n) for m, d, y, n in birthdays]
    birthdays.sort(key=lambda v: (v[0], v[1]), reverse=True)

    class in_page:
        def __init__(self, dc):
            self.dc = dc
            self.pageno = 0

        def __enter__(self):
            self.dc.StartPage()
            self.pageno += 1
            print("Printing page", self.pageno)

        def __exit__(self, exc, val, tb):
            self.dc.EndPage()
            return False

    page = in_page(dc)

    def text_left(dc, x, y, text):
        dc.DrawText2(
            x,
            -y,
            11000,
            0,
            text,
            (DT_LEFT | DT_NOCLIP | DT_WORDBREAK | DT_NOPREFIX),
        )

    def text_center(dc, x, y, text):
        dc.DrawText2(
            x - 11000,
            -y,
            22000,
            0,
            text,
            (DT_CENTER | DT_NOCLIP | DT_WORDBREAK | DT_NOPREFIX),
        )

    def bitmap(dc, left, top, right, bottom, bmpfn):
        bmpfn = os.path.realpath(bmpfn)
        # Load bitmap file
        gdiplus_token = gdiplus_startup()
        gpb = Bitmap.FromFile(bmpfn)
        bmp = gpb.GetHBITMAP()
        gpb.Dispose()
        gdiplus_shutdown(gdiplus_token)
        # Create DC for bitmap
        bmpdc = DC.CreateCompatible(dc.hdc)
        # Select bitmap into its DC
        old = bmpdc.SelectObject(bmp)
        # Paint the bitmap
        bl, bt, br, bb = bmpdc.GetClipBox()
        dc.StretchBlt(
            left,
            -top,
            right - left,
            -(bottom - top),
            bmpdc.hdc,
            bl,
            bt,
            br - bl,
            bb - bt,
            SRCCOPY,
        )
        # Free up stuff
        bmpdc.SelectObject(old)
        bmpdc.Delete()
        gdi32.DeleteObject(c_void_p(bmp))

    def set_font(dc, docpart):
        font = cfg.get("Fonts", docpart)
        name, height, *other = font.split(",")
        other = tuple(o.strip() for o in other)
        if ":" in height:
            height, width = height.split(":", 1)
            width = int(width.strip())
        else:
            width = 0
        height = int(height.strip())
        dc.SetFont(
            name=name.strip(),
            height=height,
            width=width,
            underline=("underline" in other),
            weight=(FW_BOLD if "bold" in other else FW_NORMAL),
        )
        return height

    def get_layout(docpart):
        return (int(x.strip()) for x in cfg.get("Layout", docpart).split(","))

    def get_color(docpart, section="Fill-colors"):
        return int(cfg.get(section, docpart), 16)

    def set_pen(dc, docpart):
        width, color = cfg.get("Lines", docpart).split(",")
        dc.SetPen(width=int(width.strip()), color=int(color.strip(), 16))

    ################################################################################
    #   Front Cover
    ################################################################################
    with page:
        bmpfn = "front-cover.jpg"
        if OUTPUT_BITMAPS and os.path.isfile(bmpfn):
            L, t, r, b = get_layout("Front-cover-image")
            bitmap(dc, L, t, r, b, bmpfn)
        set_font(dc, "Front-cover")
        dc.SetTextColor(get_color("Front-cover"))
        x, y = get_layout("Front-cover-text")
        text_center(
            dc,
            x,
            y,
            cfg.get("General", "Front-cover-text").format(
                year=cfg.get("General", "Year"), nl="\n"
            ),
        )
        x, y = get_layout("Front-cover-year")
        text_center(dc, x, y, cfg.get("General", "Year"))
    # dc.EndPage(); dc.EndDoc(); exit()
    ################################################################################
    #   Month Pages
    ################################################################################
    one_day = datetime.timedelta(days=1)
    cellwidth, cellheight = get_layout("Grid-cell")
    grid_x, grid_y = get_layout("Grid")
    (weekday_y,) = get_layout("Weekdays")
    bd_format = cfg.get("General", "Birthday-format")

    def weekday(date):
        return date.isoweekday() % 7

    for month_n, month in enumerate(MONTHS, start=1):
        # Picture Page
        with page:
            bmpfn = "%i %s.jpg" % (month_n, month)
            if OUTPUT_BITMAPS and os.path.isfile(bmpfn):
                L, t, r, b = get_layout("Month-image")
                bitmap(dc, L, t, r, b, bmpfn)
        # Calendar Page
        with page:
            # Box
            set_pen(dc, "Box-outline")
            dc.SetBrush(color=get_color("Box-color", month))
            L, t, r, b = get_layout("Box")
            dc.Rectangle(L, -t, r, -b)
            # Month & year
            set_font(dc, "Month")
            dc.SetTextColor(get_color("Month"))
            x, y = get_layout("Month")
            text_left(dc, x, y, month)
            dc.SetTextColor(get_color("Year"))
            set_font(dc, "Year")
            text_left(dc, 500, 860, cfg.get("General", "Year"))
            # Quote
            dc.SetTextColor(get_color("Quote"))
            set_font(dc, "Quote")
            L, t, r, b = get_layout("Quote")
            dc.DrawText(
                L,
                -t,
                r,
                -b,
                cfg.get(month, "Quote"),
                (DT_LEFT | DT_WORDBREAK | DT_NOPREFIX),
            )
            # Days of the week
            dc.SetTextColor(get_color("Weekdays"))
            set_font(dc, "Weekdays")
            x = cellwidth // 2 + grid_x
            for day in WEEKDAYS:
                # Day Number
                text_center(dc, x, weekday_y, day)
                x += cellwidth
            # Grid
            set_pen(dc, "Grid")
            for x in range(grid_x, grid_x + cellwidth * 8, cellwidth):
                dc.MoveTo(x, -grid_y)
                dc.LineTo(x, -grid_y - cellheight * 6)
            for y in range(grid_y, grid_y + cellheight * 7, cellheight):
                dc.MoveTo(grid_x, -y)
                dc.LineTo(grid_x + cellwidth * 7, -y)
            # Days
            date = datetime.date(cfg.getint("General", "Year"), month_n, 1)
            week = 0
            while True:
                wd = weekday(date)
                X = wd * cellwidth + grid_x
                Y = week * cellheight + grid_y
                # Day Number
                dc.SetTextColor(get_color("Day"))
                set_font(dc, "Day")
                x, y = get_layout("Day")
                text_left(dc, X + x, Y + y, str(date.day))
                # Birthdays
                x, y = get_layout("Birthday")
                Y += cellheight - y
                while birthdays and birthdays[-1][:2] == (date.month, date.day):
                    month, day, year, name = birthdays.pop(-1)
                    dc.SetTextColor(
                        get_color("Anniversary" if "&" in name else "Birthday")
                    )
                    height = set_font(dc, "Anniversary" if "&" in name else "Birthday")
                    Y -= height
                    text_left(
                        dc,
                        X + x,
                        Y,
                        bd_format.format(
                            name=name,
                            year=year,
                            shortyear=f"{year % 100:0>2}",
                            month=month,
                            day=day,
                        ),
                    )
                if wd == 6:
                    week += 1
                date += one_day
                if date.month != month_n:
                    break
    ################################################################################
    #   Last Page (Deaths)
    ################################################################################
    with page:
        bmpfn = "in-memory.jpg"
        if OUTPUT_BITMAPS and os.path.isfile(bmpfn):
            L, t, r, b = get_layout("Deaths-image")
            bitmap(dc, L, t, r, b, bmpfn)
        try:
            deaths = open("deaths.txt").read()
        except FileNotFoundError:
            pass
        else:
            set_font(dc, "Deaths-title")
            dc.SetTextColor(get_color("Deaths-title"))
            x, y = get_layout("Deaths-title")
            text_center(dc, x, y, cfg.get("General", "Deaths-title"))
            set_font(dc, "Deaths")
            dc.SetTextColor(get_color("Deaths"))
            x, y = get_layout("Deaths")
            text_left(dc, x, y, deaths)
    ################################################################################
    #   Inside Back Cover (Addresses)
    ################################################################################
    with page:
        try:
            addresses = open("addresses.txt")
        except FileNotFoundError:
            pass
        else:
            set_font(dc, "Addresses-title")
            dc.SetTextColor(get_color("Addresses-title"))
            x, y = get_layout("Addresses-title")
            text_center(dc, x, y, cfg.get("General", "Addresses-title"))
            x, y = get_layout("Addresses")
            ys = y
            xincr, maxy = get_layout("Addresses-wrap")
            for line in addresses:
                if line.startswith("@comment:"):
                    continue
                if line.startswith("@"):
                    fontname, line = line.split(":", 1)
                    fontname = "Addresses-" + fontname[1:]
                else:
                    fontname = "Addresses"
                line = line.rstrip("\r\n")
                dc.SetTextColor(get_color(fontname))
                height = set_font(dc, fontname)
                if line:
                    text_left(dc, x, y, line)
                y += height
                if y > maxy:
                    x += xincr
                    y = ys

    ################################################################################
    #   Back Cover (Picture Credits)
    ################################################################################
    with page:
        set_font(dc, "Credits-title")
        dc.SetTextColor(get_color("Credits-title"))
        x, y = get_layout("Credits-title")
        text_left(dc, x, y, cfg.get("General", "Credits-title"))
        set_font(dc, "Credits")
        dc.SetTextColor(get_color("Credits"))
        x, y = get_layout("Credits")
        try:
            text_left(dc, x, y, open("picture-credits.txt").read())
        except FileNotFoundError:
            pass
    print("Outputting...")
    dc.EndDoc()
    dc.Delete()
    print("Done")


if __name__ == "__main__":
    main()
