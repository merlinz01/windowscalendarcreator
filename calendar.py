import os, datetime, configparser

import wingui
from wingui.gdiplus import GdiPlus, Bitmap
def main():
    cfg = configparser.RawConfigParser()
    cfg.read('calendar.ini')

    OUTPUT_BITMAPS = not cfg.getboolean('General', 'Skip-bitmaps')
    MONTHS = (
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December')
    WEEKDAYS = (
       'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

    dm = wingui.types.alloc('DEVMODE')
    dm.dmSize = dm.sizeof()
    dm.dmFields = wingui.const.DM_ORIENTATION
    dm.dmOrientation = wingui.const.DMORIENT_LANDSCAPE
    dc = wingui.DC.Create('WINSPOOL', 'Microsoft Print to PDF', dm.ref())
    dc.SetMapMode(wingui.const.MM_HIENGLISH)
    dc.StartDoc('Calendar')
    dc.SetBkMode(transparent=True)

    birthdays = open('birthdays.txt').read()
    birthdays = (l.split(' ', 1)
                 for l in birthdays.splitlines(False)
                 if l.lstrip() and l.lstrip()[0] != '#')
    birthdays = [(*d.split('/'), n.strip()) for d, n in birthdays]
    birthdays = [(int(m), int(d), int(y), n) for m, d, y, n in birthdays]
    birthdays.sort(key=lambda v: (v[0], v[1]), reverse=True)

    class in_page:
        def __init__(self, dc):
            self.dc = dc
            self.pageno = 0
        def __enter__(self):
            self.dc.StartPage()
            self.pageno += 1
            print('Printing page', self.pageno)
        def __exit__(self, exc, val, tb):
            self.dc.EndPage()
            return False
    page = in_page(dc)

    def text_left(dc, x, y, text):
        dc.DrawText2(x, -y, 11000, 0, text,
                    (wingui.const.DT_LEFT
                     |wingui.const.DT_NOCLIP
                     |wingui.const.DT_WORDBREAK
                     |wingui.const.DT_NOPREFIX))
    def text_center(dc, x, y, text):
        dc.DrawText2(x-11000, -y, 22000, 0, text,
                    (wingui.const.DT_CENTER
                     |wingui.const.DT_NOCLIP
                     |wingui.const.DT_WORDBREAK
                     |wingui.const.DT_NOPREFIX))
    def bitmap(dc, l, t, r, b, bmpfn):
        bmpfn = os.path.realpath(bmpfn)
        # Load bitmap file
        with GdiPlus():
            gpb = Bitmap.FromFile(bmpfn)
            bmp = gpb.GetHBITMAP()
            #gpb.Free()
            gpb.Dispose()
        # Create DC for bitmap
        bmpdc = wingui.DC.CreateCompatible(dc.hdc)
        # Select bitmap into its DC
        old = bmpdc.SelectObject(bmp)
        # Paint the bitmap
        bl, bt, br, bb = bmpdc.GetClipBox()
        dc.StretchBlt(
            l, -t, r-l, -(b-t), bmpdc.hdc, bl, bt, br-bl, bb-bt, wingui.const.SRCCOPY)
        # Free up stuff
        bmpdc.SelectObject(old)
        bmpdc.Delete()
        wingui.gdi32.DeleteObject(bmp)

    def set_font(dc, docpart):
        font = cfg.get('Fonts', docpart)
        name, height, *other = font.split(',')
        other = tuple(o.strip() for o in other)
        if ':' in height:
            height, width = height.split(':', 1)
            width = int(width.strip())
        else: width = 0
        height = int(height.strip())
        dc.SetFont(name=name.strip(),
                   height=height,
                   width=width,
                   underline=('underline' in other),
                   weight=(wingui.const.FW_BOLD
                         if 'bold' in other
                         else wingui.const.FW_NORMAL))
        return height

    def get_layout(docpart):
        return (int(x.strip()) for x in cfg.get('Layout', docpart).split(','))

    def get_color(docpart, section='Fill-colors'):
        return int(cfg.get(section, docpart), 16)

    def set_pen(dc, docpart):
        width, color = cfg.get('Lines', docpart).split(',')
        dc.SetPen(width=int(width.strip()), color=int(color.strip(), 16))

    ################################################################################
    #   Front Cover
    ################################################################################
    with page:
        bmpfn = 'front-cover.jpg'
        if OUTPUT_BITMAPS and os.path.isfile(bmpfn):
            l, t, r, b = get_layout('Front-cover-image')
            bitmap(dc, l, t, r, b, bmpfn)
        set_font(dc, 'Front-cover')
        dc.SetTextColor(get_color('Front-cover'))
        x, y = get_layout('Front-cover-text')
        text_center(dc, x, y, cfg.get('General', 'Front-cover-text').format(
            year=cfg.get('General', 'Year'), nl='\n'))
        x, y = get_layout('Front-cover-year')
        text_center(dc, x, y, cfg.get('General', 'Year'))
    #dc.EndPage(); dc.EndDoc(); exit()
    ################################################################################
    #   Month Pages
    ################################################################################
    one_day = datetime.timedelta(days=1)
    cellwidth, cellheight = get_layout('Grid-cell')
    grid_x, grid_y = get_layout('Grid')
    weekday_y, = get_layout('Weekdays')
    bd_format = cfg.get('General', 'Birthday-format')
    def weekday(date):
        return date.isoweekday() % 7
    try: quotes = open('quotes.txt').readlines()
    except FileNotFoundError: quotes = None

    for month_n, month in enumerate(MONTHS, start=1):
        # Picture Page
        with page:
            bmpfn = '%i %s.jpg' % (month_n, month)
            if OUTPUT_BITMAPS and os.path.isfile(bmpfn):
                l, t, r, b = get_layout('Month-image')
                bitmap(dc, l, t, r, b, bmpfn)
        # Calendar Page
        with page:
            # Box
            set_pen(dc, 'Box-outline')
            dc.SetBrush(color=get_color('Box-color', month))
            l, t, r, b = get_layout('Box')
            dc.Rectangle(l, -t, r, -b)
            # Month & year
            set_font(dc, 'Month')
            dc.SetTextColor(get_color('Month'))
            x, y = get_layout('Month')
            text_left(dc, x, y, month)
            dc.SetTextColor(get_color('Year'))
            set_font(dc, 'Year')
            text_left(dc, 500, 860, cfg.get('General', 'Year'))
            # Quote
            #if quotes:
            dc.SetTextColor(get_color('Quote'))
            set_font(dc, 'Quote')
            l, t, r, b = get_layout('Quote')
            dc.DrawText(l, -t, r, -b,
                        #quotes[month_n-1],
                        cfg.get(month, 'Quote'),
                ( wingui.const.DT_LEFT
                 |wingui.const.DT_WORDBREAK
                 |wingui.const.DT_NOPREFIX))
            # Days of the week
            dc.SetTextColor(get_color('Weekdays'))
            set_font(dc, 'Weekdays')
            x = cellwidth//2 + grid_x
            for day in WEEKDAYS:
                # Day Number
                text_center(dc, x, weekday_y, day)
                x += cellwidth
            # Grid
            set_pen(dc, 'Grid')
            for x in range(grid_x, grid_x+cellwidth*8, cellwidth):
                dc.MoveTo(x, -grid_y)
                dc.LineTo(x, -grid_y-cellheight*6)
            for y in range(grid_y, grid_y+cellheight*7, cellheight):
                dc.MoveTo(grid_x, -y)
                dc.LineTo(grid_x+cellwidth*7, -y)
            # Days
            date = datetime.date(cfg.getint('General', 'Year'), month_n, 1)
            week = 0
            while True:
                wd = weekday(date)
                X = wd*cellwidth + grid_x
                Y = week*cellheight + grid_y
                # Day Number
                dc.SetTextColor(get_color('Day'))
                set_font(dc, 'Day')
                x, y = get_layout('Day')
                text_left(dc, X+x, Y+y, str(date.day))
                # Birthdays
                x, y = get_layout('Birthday')
                Y += cellheight-y
                while birthdays and birthdays[-1][:2] == (date.month, date.day):
                    month, day, year, name = birthdays.pop(-1)
                    dc.SetTextColor(get_color(
                        'Anniversary' if '&' in name else 'Birthday'))
                    height = set_font(dc, 'Anniversary' if '&' in name else 'Birthday')
                    Y -= height
                    text_left(dc, X+x, Y, bd_format.format(
                        name=name, year=year, shortyear=f'{year%100:0>2}',
                        month=month, day=day))
                if wd == 6: week += 1
                date += one_day
                if date.month != month_n: break
    ################################################################################
    #   Last Page (Deaths)
    ################################################################################
    with page:
        bmpfn = 'in-memory.jpg'
        if OUTPUT_BITMAPS and os.path.isfile(bmpfn):
            l, t, r, b = get_layout('Deaths-image')
            bitmap(dc, l, t, r, b, bmpfn)
        try: deaths = open('deaths.txt').read()
        except FileNotFoundError: pass
        else:
            set_font(dc, 'Deaths-title')
            dc.SetTextColor(get_color('Deaths-title'))
            x, y = get_layout('Deaths-title')
            text_center(dc, x, y, cfg.get('General', 'Deaths-title'))
            set_font(dc, 'Deaths')
            dc.SetTextColor(get_color('Deaths'))
            x, y = get_layout('Deaths')
            text_left(dc, x, y, deaths)
    ################################################################################
    #   Inside Back Cover (Addresses)
    ################################################################################
    with page:
        try: addresses = open('addresses.txt')
        except FileNotFoundError: pass
        else:
            set_font(dc, 'Addresses-title')
            dc.SetTextColor(get_color('Addresses-title'))
            x, y = get_layout('Addresses-title')
            text_center(dc, x, y, cfg.get('General', 'Addresses-title'))
            x, y = get_layout('Addresses')
            ys = y
            xincr, maxy = get_layout('Addresses-wrap')
            for line in addresses:
                if line.startswith('@comment:'): continue
                if line.startswith('@'):
                    fontname, line = line.split(':', 1)
                    fontname = 'Addresses-'+fontname[1:]
                else: fontname = 'Addresses'
                line = line.rstrip('\r\n')
                dc.SetTextColor(get_color(fontname))
                height = set_font(dc, fontname)
                if line: text_left(dc, x, y, line)
                y += height
                if y > maxy:
                    x += xincr
                    y = ys
                
    ################################################################################
    #   Back Cover (Picture Credits)
    ################################################################################
    with page:
        set_font(dc, 'Credits-title')
        dc.SetTextColor(get_color('Credits-title'))
        x, y = get_layout('Credits-title')
        text_left(dc, x, y, cfg.get('General', 'Credits-title'))
        set_font(dc, 'Credits')
        dc.SetTextColor(get_color('Credits'))
        x, y = get_layout('Credits')
        try: text_left(dc, x, y, open('picture-credits.txt').read())
        except FileNotFoundError: pass
    print('Outputting...')
    dc.EndDoc()
    dc.Delete()
    #time.sleep(9 if OUTPUT_BITMAPS else 2)
    #while print(os.stat('calendar.pdf').st_size) == None:
    #    time.sleep(0.5)
    #os.startfile('calendar.pdf')
    print('Done')
if __name__ == '__main__':
    main()
 # type: ignore