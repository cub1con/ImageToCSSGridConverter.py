
# ImageToCSSGridConverter.py

A small python script which is able to convert RGBA images to a HTML and CSS file using the css ``display: grid`` property.

It's best use case are small images up to 256x256px.

It removes fully transparent pixels.

Some facts with the provided ``magala.png`` 6000x4000px picture:
- It's reasonable slow: Takes ~110 seconds to process (not so save to disk!)
- It's kinda big: Needs about 1.4 GB of disk space
- Omnomnom Ram: Eats up to 6.0GB of RAM
- I can't load the processed file in Google Chrome
- Tested on an Ryzen 3700X with 16GB 3200MHZ RAM

There is room to improve, like generating classes for colors which are used often to get the used disk space down.

The idea and provided example images are by: **[@Feuerfrosch on Twitter](https://twitter.com/Feuerfrosch_art)**

# How to use
You need Python 3.

- Clone the repo
- Open ImageToCSSGridConverter.Py
- Choose your image
    - Using your own image
        - Place your image in the ImageToCSSGridConverter.py folder
        - Replace string in ``main.py`` with your file name
            - ``imgName = "magala.png"``
    - Using the provided image
        - Do literally nothing
- Run python3 main.py
- Profit
