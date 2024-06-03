# Windows calendar creator

This is a simple family calendar PDF creator program for Windows.

## Usage

Configure the parameters in `calendar.ini`.

Replace the month pictures, front cover picture, and back page picture with ones you like, with exactly the same filenames.

Add your family birthdays and anniversaries to `birthdays.txt`.

Add your family's deceased to `deaths.txt`.

Put photo credits in `picture-credits.txt`.

Run `calendar.py` on a Windows device that has Microsoft Print to PDF.

A dialog will pop up asking you to where to save the file. Enter a filename and click Save.

The calendar will take a bit to be generated. Look for the file you saved for the PDF calendar.

If you want to prepare the calendar for commercial printing, the `add-bleed-with-pdfbooklet.ini` file is a configuration for [PDFBooklet](https://github.com/Averell7/PdfBooklet) for adding a bleed area around all the pages.

# License

MIT License; use it however you like but keep the license file with it.