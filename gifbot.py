import os
import giphypop
import json
import requests
import config

MAX_IMAGE_SIZE = 3072 * 1024
giphy = giphypop.Giphy(api_key=config.giphy['key'])

class Element(object):

    __acceptable_keys = ['title', 'item_url', 'image_url', 'subtitle']
    def __init__(self, **kwargs):
        for key in self.__acceptable_keys:
            setattr(self, key, kwargs.get(key))

    def to_json(self):
        data = {}
        for key in self.__acceptable_keys:
            data[key] = getattr(self, key)
        return json.dumps(data)

def get_gif_filename(text):
    images = [i for i in giphy.search(text, limit=20) if i.filesize < MAX_IMAGE_SIZE]
    if not images or images is []:
        return None
    print images
    image = images[0]
    print "image is ", image
    filename = 'images/%s.%s' % (text.replace(' ', '_'), image.type)
    print filename, "  FILENAME ", " URL ", image.media_url
    f = open(filename, 'wb')
    f.write(requests.get(image.media_url).content)
    f.close()
    return filename

def send_generic_message(recipient_id, elements):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements
                    }
                }
            }
        }
        result = requests.post(base_url, json=payload).json()
        return result

def send_gif_url(recipient_id, text):
    images = [i for i in giphy.search(text, limit=20) if i.filesize < MAX_IMAGE_SIZE]
    if not images or images is []:
        return None
    image = images[0]
    elements = []
    element = Element(title="test", image_url=image.media_url, subtitle="subtitle", item_url=image.media_url)
    elements.append(element)
    send_generic_message(recipient_id, elements)
    print filename, "  FILENAME ", " URL ", image.media_url
    #return image.media_url

if not os.path.exists('images/'):
    os.makedirs('images/')

def main():
    inp = raw_input("Enter text: ")
    get_gif_filename(inp)

if __name__ == "__main__":
    main()
