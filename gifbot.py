import os
import giphypop

import requests
import config

MAX_IMAGE_SIZE = 3072 * 1024
giphy = giphypop.Giphy(api_key=config.giphy['key'])

def get_gif_filename(text):
    images = [i for i in giphy.search(text, limit=20) if i.filesize < MAX_IMAGE_SIZE]
    if not images or images is []:
        return None
    print images
    image = images[0]
    print "image is ", image
    filename = 'images/%s.%s' % (text.replace(' ', '_'), image.type)
    print filename, "  FILENAME"
    f = open(filename, 'wb')
    f.write(request.get(image.media_url).content)
    f.close()
    return filename

if not os.path.exists('images/'):
    os.makedirs('images/')

def main():
    inp = raw_input("Enter text: ")
    get_gif_filename(inp)

if __name__ == "__main__":
    main()
