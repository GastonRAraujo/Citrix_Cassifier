import os
import requests  # to sent GET requests
from PIL import Image
from io import BytesIO

# Crate an aimation while running----------------
import itertools
import threading
import time
import sys

done = False
# here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

# ------------------------------------------



# The User-Agent request header contains a characteristic string
# that allows the network protocol peers to identify the application type,
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


SAVE_FOLDER = 'processed_images'

# crate list of categories
fruits = ['lemon', 'orange', 'tangerine', 'grapefruit']


def main():
    print("Let's save some fruits from the internet... \n")

    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    for index, data in enumerate(fruits):

        # crate folder for each category
        data_folder = SAVE_FOLDER + '/' + data
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)

        # filename where links from imageNet are saved
        file = 'links/' + data + ".txt"
        f = open(file, "r")
        links = f.read()
        f.close()

        # save links as list of array
        links = links.replace(" ", "")  # clean white spaces
        links = links.split("\n")       # links separated in lines

        download_images(links, data, data_folder)


def save_processed_image(response, image_number, SAVE_FOLDER2):
    try:
        image = Image.open(BytesIO(response.content))
        imageResized = image.resize((128,128), resample=Image.ANTIALIAS)

        # SAVE_DIR EXAMPLE: processed_images/fruit/fruitXXXX.jpg
        SAVE_DIR = SAVE_FOLDER2 + str(image_number) + ".jpg"
        imageResized.convert('RGB').save(SAVE_DIR, 'JPEG', quality=90)

    except:
        print("\rERROR OPENNING IMAGE")
        image_number += -1

    return image_number


def download_images(f, data, data_folder):
    count_pictures = 0
    print("Start saving pictures of " + data + "s...")
    print("Number of links:", len(f))

    for i, url in enumerate(f):
        # get extension for file (last 3 char from link)

        # Your connection can get lost for the many times you
        # request data from the same server
        # request has a reconnect function but is faster to continue
        # and loose some pictures

        try:
            page = requests.get(url)
            # check no error to prevent empty pictures
            if page.status_code != requests.codes.ok:
                continue
        except:
            print("\rConnection refused by the server...")
            continue

        # file directory
        imagename = data_folder + '/' + data
        # Writing file
        count_pictures = save_processed_image(page, count_pictures, imagename)

        count_pictures += 1

    print("\r {} Saved pictures of {}s".format(count_pictures, data))
    print('Done \n')


if __name__ == '__main__':
    main()
    time.sleep(10)
    done = True
