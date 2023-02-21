import imagehash
import pyscreenshot
from PIL import Image
import os
import shutil
import GlobalVariables
import pyautogui
import json


class ImageHandler:
    IMAGE_DIR = "images"

    def __init__(self):
        self.images_names = []
        self.image_number = 0
        self.cutoff = 10  # maximum bits that could be different between the hashes.
        self.maxValue = 25

        with open("settings.json", "r") as settings:
            data = json.load(settings)
            self.bbox = data["bbox-check-dimensions"]
            self.pixel_check_end_screen = data["pixel-check-end-screen"]
            self.pixel_check_end_screen_coords = data["pixel-check-end-screen-coords"]
            self.detect_end_screen_by_value = data["detect-end-screen-by-value"]
            self.auto_convert_to_pdf = data["auto-convert-to-pdf"]
            self.clean_images_at_end = data["clean-images-at-end"]

    def save_image(self):
        '''
        Takes a screenshot and saves the screenshot

        :return: void
        '''
        pic = pyscreenshot.grab(bbox=(self.bbox[0], self.bbox[1], self.bbox[2], self.bbox[3]))
        pic.save("new.png")
        if len(self.images_names) == 0:
            self.add_image_to_list("new.png")

        else:
            can_add = self.compare("new.png")
            if not can_add:
                self.add_image_to_list("new.png")

    def add_image_to_list(self, image_name):
        '''
        This function adds the image we've taking a screenshot of to the list of screenshots.
        It also gives the image a correct name and moves it to the images folder

        :param image_name: string
        :return: void
        '''
        os.rename(image_name, f"image_{str(self.image_number).zfill(2)}.png")
        self.images_names.append(f"image_{str(self.image_number).zfill(2)}.png")
        shutil.move(f"image_{str(self.image_number).zfill(2)}.png", "images")
        self.image_number += 1

    def compare(self, image_name):
        '''
        This function compares the newest image to the oldest image
        By doing this it detemines whether we have taken a screenshot of a new image
        or the screenshot we have just taken is the same as the previous image
        https://stackoverflow.com/a/52736785

        :param image_name: string
        :return: boolean
        '''

        # This if statement checks if a certain pixel colour on a certain pixel coordination is not black
        # , and then ends the script
        # Usually it's better to turn this off in the settings
        #   set "pixel-check-end-screen" to false in the settings.json file
        if self.pixel_check_end_screen:
            x, y = self.pixel_check_end_screen_coords[0], self.pixel_check_end_screen_coords[1]
            color = pyautogui.pixel(x, y)
            if color[0] != 255:
                print("I saw the end screen, ending it!")
                GlobalVariables.run = False
                return True  # Images aren't similar but we want to stop anyway

        hash0 = imagehash.average_hash(Image.open(image_name))
        hash1 = imagehash.average_hash(
            Image.open("images/" + self.images_names[-1]))  # We always want to compare the last image

        if hash0 - hash1 < self.cutoff:
            return True  # Images are similar
        else:
            # The self.detect_end_screen_by_value function attempts to detect whether we have seen the end screen or not
            # It does this by checking if the difference between hash0 and hash1 is bigger than self.maxValue
            # It's good to have this option turned on in the settings.json by setting "detect-end-screen-by-value" to true

            if hash0 - hash1 > self.maxValue and self.detect_end_screen_by_value:
                # A value bigger than 25 is so big we can just assume we have ended and just stop
                # Usually this won't run because of the first if statement, but you never know
                print(f"Value of {hash0 - hash1} is bigger than {self.maxValue}, ENDING PROCESS")
                GlobalVariables.run = False
                return True  # Image isn't similar, but we don't want to add anyway

            else:
                print(f"Allowing to pass with: {hash0 - hash1} > {self.cutoff}. Num: {self.image_number}")
                return False  # Images are not similar

    def clear_images(self):
        '''
        This function attempts to clean the images a little
        It does this by changing colours that aren't black to white

        :return: void
        '''
        if os.path.exists("new.png"):
            os.remove("new.png")

        if os.path.exists("name.pdf"):
            os.remove("name.pdf")

        dir_name = "images"
        test = os.listdir(dir_name)

        for item in test:
            if item.endswith(".png"):
                os.remove(os.path.join(dir_name, item))

    def clean_images(self):
        '''
        This function attempts to clean the images a little
        If your images look distorted or weird you might want to turn this function off in the settings:
            set "clean-images-at-end" to false in settings.json
        A lot of this function was written by my good old friend chatgpt, I just edited it to suite my liking

        :return: void
        '''

        # Set the directory where the images are located
        directory = 'images'

        # Iterate over each image in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.png'):
                # Open the image and convert it to RGB format
                filepath = os.path.join(directory, filename)
                img = Image.open(filepath).convert('RGB')

                # Get the width and height of the image
                width, height = img.size

                # Iterate over each pixel in the image
                for x in range(width):
                    for y in range(height):
                        # Get the color of the pixel
                        r, g, b = img.getpixel((x, y))

                        # Convert green pixels to black
                        # I don't even think this does anything
                        # if r < 150 and g == 255 and b < 150:
                        #     img.putpixel((x, y), (0, 0, 0))

                        # If the pixel isn't ~black, convert it to white
                        if r > 190 or g > 190 or b > 190:
                            img.putpixel((x, y), (255, 255, 255))

                # Save the modified image
                img.save(filepath)
