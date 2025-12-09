# Windows calendar creator

This is a simple family calendar PDF creator program for Windows.

## Usage

You need a Windows computer with Microsoft Print to PDF and Python 3 installed.

Configure the parameters in `calendar.ini`.

Replace the month pictures, front cover picture, and back page picture with ones you like, with exactly the same filenames.
All pictures need to have 8.5x11 aspect ratio if you don't want them to be distorted in the output.

Add your family birthdays and anniversaries to `birthdays.txt`.

Add your family's deceased to `deaths.txt`.

Put photo credits in `picture-credits.txt`.

In File Explorer, right-click in the project folder and select *Open in Terminal*
(or open Windows Terminal and run `cd C:\path\to\project\folder`).
Then run `python calendar.py` to run the calendar generator program.

A dialog will pop up asking you to where to save the file. Enter a filename and click Save.

The calendar will take a bit to be generated. Look for the file you saved for the PDF calendar.

If you want to speed up the generation while perfecting layout, set the `Skip-bitmaps` setting in `calendar.ini` to `true`.

If you want to prepare the calendar for commercial printing,
the `add-bleed-with-pdfbooklet.ini` file is a configuration for
[PDFBooklet](https://github.com/Averell7/PdfBooklet) for adding a bleed area around all the pages.

# License

MIT License; use it however you like but keep the license file with it.
