# guitar-sheet-screenshotter

This scripts attempts to screenshot all of the images of a guitar tab when watching a guitar tab youtube video.
You can put the video on and let the script do it's thing while you lay back and watch.


# NOTES 
This script will likely not immidiately work for you. Please read the settings section for more info

# Setting configuration
The settings file is stored under settings.json. I am planning on adding more customization in the future to make things easier for the user.

  - `bbox-check-dimensions`; this setting is an array that contains the area you want to screenshot, which usually is the guitar tab itself. Right now you have to mess around with the values to get the right size however I do have an area selector feature planned for in the future.
  - `pixel-check-end-screen`; This option can be set to `true` or `false`. This option is used to enable/disable the feature that checks if a certain pixel is  black and ends the script if the condition is met. This is supposed to detect whether the video has ended so it can automatically end the script for you. Do note that this feature doesn't work correctly yet as it was made to suite my liking. I am planning on expending this option but for now it is probably better to set this option to `false`.
  - `pixel-check-end-screen-coords`; These are the x and y coordinates used for the `pixel-check-end-screen` option. This won't be used if you've turned off `pixel-check-end-screen` (you can't leave these values empty though because it'll still throw an error)
  - `detect-end-screen-by-value`; This option can be set to `true` or `false`. This option attempts to detect whether a video has ended or not by checking how different the newest screenshot is compared to the last. If the difference is very big it'll assume the end screen has come up and end the script. More cutomization features for this option are still coming. It is reccomended to keep this on `true` unless you notice the script is stopping when it isn't suppose dot be.
  - `auto-convert-to-pdf`; Can be set to `true` or `false`. This option automatically puts the images in a pdf file. It is reccomended to keep this setting on `true`
  - `clean-images-at-end`; Can be set to `true` or `false`. This option attempts to clean up the images by changing colours that aren't black to white. It is reccomended to set this option to `true` unless the images look distorted or weird or anything like that.
  
