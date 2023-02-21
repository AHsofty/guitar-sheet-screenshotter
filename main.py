import threading
from Image import ImageHandler
import time
import keyboard
from PDF import PdfMaker
import GlobalVariables

image = ImageHandler()

pdf_creator = PdfMaker("images")

image.clear_images()


def stop_listener():
    while True:
        if keyboard.is_pressed("q") or GlobalVariables.run is False:
            print("Getting stop signal")
            GlobalVariables.run = False
            break


thread = threading.Thread(target=stop_listener)
thread.start()

time.sleep(1)
print("STARTING")

while GlobalVariables.run:
    image.save_image()
    time.sleep(0.5)

if image.clean_images_at_end:
    image.clean_images()

if image.auto_convert_to_pdf:
    print("Creating a PDF file....")
    pdf_creator.create_pdf()

print("Done, exiting, thanks for using me:)")
exit()
