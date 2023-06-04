My first readmeimport win32print
import win32ui
import win32gui

def print_receipt(image_filename):
    try:
        # Open the image file
        image = win32ui.CreateBitmap()
        image.LoadImage(image_filename)

        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()

        # Create a printer DC
        printer_dc = win32print.OpenPrinter(printer_name)
        dc = win32print.GetPrinter(printer_dc)["pDevMode"]["Specs"]["DeviceName"]
        dc = win32gui.CreateDC(dc)

        # Start the printing process
        dc.StartDoc("Receipt")
        dc.StartPage()

        # Print the image
        dc.BitBlt((0, 0), (image.GetWidth(), image.GetHeight()), image, (0, 0), win32con.SRCCOPY)

        # End the printing process
        dc.EndPage()
        dc.EndDoc()

        # Cleanup
        dc.DeleteDC()
        win32print.ClosePrinter(printer_dc)

        messagebox.showinfo("Print Receipt", "Receipt sent to printer successfully!")
    except Exception as e:
        messagebox.showerror("Print Receipt", f"Failed to send receipt to printer! Error: {str(e)}")
