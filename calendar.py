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
DM_PAPERSIZE = 0x00000002
DM_PAPERLENGTH = 0x00000004
DM_PAPERWIDTH = 0x00000008
DMORIENT_PORTRAIT = 1
DMORIENT_LANDSCAPE = 2
MM_HIENGLISH = 5
TRANSPARENT = 1
OPAQUE = 2

# Paper size constants
DMPAPER_LETTER = 1  # 8.5 x 11 inches
DMPAPER_LEGAL = 5  # 8.5 x 14 inches
DMPAPER_TABLOID = 3  # 11 x 17 inches
DMPAPER_LEDGER = 4  # 17 x 11 inches
DMPAPER_A3 = 8  # 297 x 420 mm
DMPAPER_A4 = 9  # 210 x 297 mm
DMPAPER_A5 = 11  # 148 x 210 mm

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

    # Get orientation setting
    orientation = (
        cfg.get("General", "Orientation", fallback="Landscape").strip().upper()
    )
    is_landscape = orientation == "LANDSCAPE"
    dm.dmOrientation = DMORIENT_LANDSCAPE if is_landscape else DMORIENT_PORTRAIT
    print(f"Orientation: {'Landscape' if is_landscape else 'Portrait'}")

    # Standard paper sizes (portrait dimensions: width x height)
    paper_sizes = {
        "LETTER": (DMPAPER_LETTER, 8.5, 11.0),
        "LEGAL": (DMPAPER_LEGAL, 8.5, 14.0),
        "TABLOID": (DMPAPER_TABLOID, 11.0, 17.0),
        "LEDGER": (DMPAPER_LEDGER, 11.0, 17.0),
        "A3": (DMPAPER_A3, 11.693, 16.535),
        "A4": (DMPAPER_A4, 8.268, 11.693),
        "A5": (DMPAPER_A5, 5.827, 8.268),
    }

    if cfg.has_option("General", "Paper-size"):
        paper_size = cfg.get("General", "Paper-size").strip().upper()
        if paper_size in paper_sizes:
            dm_code, paper_width, paper_height = paper_sizes[paper_size]
            dm.dmFields |= DM_PAPERSIZE
            dm.dmPaperSize = dm_code
            print(f"Paper size: {paper_size} ({paper_width} x {paper_height} inches)")
        elif "X" in paper_size:
            width, height = paper_size.split("X")
            paper_width = float(width.strip())
            paper_height = float(height.strip())
            dm.dmFields |= DM_PAPERLENGTH | DM_PAPERWIDTH
            dm.dmPaperSize = 0  # Custom paper size
            dm.dmPaperWidth = int(paper_width * 254)
            dm.dmPaperLength = int(paper_height * 254)
            print(f"Custom paper size: {paper_width} x {paper_height} inches")
        else:
            raise ValueError(f"Unknown paper size: {paper_size}")
    else:
        # Default to Letter size
        dm.dmFields |= DM_PAPERSIZE
        dm.dmPaperSize = DMPAPER_LETTER
        paper_width = 8.5
        paper_height = 11.0
        print("Paper size not specified; defaulting to Letter.")

    page_width = int(paper_height * 1000)
    page_height = int(paper_width * 1000)
    if is_landscape:
        page_width, page_height = (
            max(page_width, page_height),
            min(page_width, page_height),
        )
    else:
        page_width, page_height = (
            min(page_width, page_height),
            max(page_width, page_height),
        )
    print(f"Page size in mils: {page_width} x {page_height}")

    printer = cfg.get("General", "Printer", fallback="Microsoft Print to PDF")
    print(f"Using printer: {printer}")
    dc = DC.Create("WINSPOOL", printer, byref(dm))
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
            page_width,
            0,
            text,
            (DT_LEFT | DT_NOCLIP | DT_WORDBREAK | DT_NOPREFIX),
        )

    def text_center(dc, x, y, text):
        dc.DrawText2(
            x - page_width,
            -y,
            page_width * 2,
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
        """Parse layout values supporting percentages, units, and absolute values.

        Percentages (e.g., "50%") are relative to page dimensions.
        Units: "0.25in", "10mm", "2.5cm"
        Absolute values (e.g., "500") are in mils (0.001 inch) as-is.
        """

        def parse_value(val, dimension_size):
            val = val.strip()
            if val.endswith("%"):
                # Percentage of page dimension
                return int(float(val[:-1]) / 100.0 * dimension_size)
            elif val.endswith("in"):
                # Inches to mils (1 inch = 1000 mils)
                return int(float(val[:-2]) * 1000)
            elif val.endswith("mm"):
                # Millimeters to mils (1 mm = 39.37 mils)
                return int(float(val[:-2]) * 39.37)
            elif val.endswith("cm"):
                # Centimeters to mils (1 cm = 393.7 mils)
                return int(float(val[:-2]) * 393.7)
            else:
                # Absolute value in mils
                return int(val)

        values = cfg.get("Layout", docpart).split(",")
        result = []
        for i, val in enumerate(values):
            # Alternate between width (even indices) and height (odd indices)
            if i % 2 == 0:
                result.append(parse_value(val, page_width))
            else:
                result.append(parse_value(val, page_height))
        return result

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

    # Calculate grid dimensions based on margins
    grid_left, grid_top, grid_right, grid_bottom = get_layout("Grid-margins")
    grid_x = grid_left
    grid_y = grid_top
    available_width = page_width - grid_left - grid_right
    available_height = page_height - grid_top - grid_bottom
    cellwidth = available_width // 7  # 7 columns (days of week)
    cellheight = available_height // 6  # 6 rows (max weeks in month)

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
            lm, t, rm, b = get_layout("Box")
            r = page_width - rm
            dc.Rectangle(lm, -t, r, -b)
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
