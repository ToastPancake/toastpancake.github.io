# -*- coding: utf-8 -*-
# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub
# For downloading the image.
import tempfile

# For drawing onto the image.
from PIL import Image
from PIL import ImageOps

from flask import Flask, render_template, request, jsonify
import base64




def download_and_resize_image(url, new_width=256, new_height=256,
                              display=False):
  # imgdata = base64.b64decode(url)
  _, filename = tempfile.mkstemp(suffix=".jpg")
  pil_image = Image.open(url)
  pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.LANCZOS)
  pil_image_rgb = pil_image.convert("RGB")
  pil_image_rgb.save(filename, format="JPEG", quality=90)
  return filename
# Check available GPU devices.

# By Heiko Gorski, Source: https://commons.wikimedia.org/wiki/File:Naxos_Taverna.jpg
# image_url = "chair.jpg"  #@param
# downloaded_image_path = download_and_resize_image(image_url, 1280, 856, True)

"""Pick an object detection module and apply on the downloaded image. Modules:
* **FasterRCNN+InceptionResNet V2**: high accuracy,
* **ssd+mobilenet V2**: small and fast.
"""

module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]

detector = hub.load(module_handle).signatures['default']

def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

def run_detector(detector, path):
  img = load_img(path)

  converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
  result = detector(converted_img)

  result = {key:value.numpy() for key,value in result.items()}
  word = str(result["detection_class_entities"][0])[1:]
  return word
  
#  print(re.search(r'\d+', mass).group())

"""### More images
Perform inference on some additional images with time tracking.

"""

def detect_img(image_url):
  image_path = download_and_resize_image(image_url, 640, 480)
  return run_detector(detector, image_path)

detect_img("./templates/plant.jpg")

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template('./index.html')

@app.route('/scan', methods=['GET','POST'])
def scan():
  url = request.args.get('value')
  word = detect_img("./templates/plant.jpg")
  result = {"output" : word}
  result = {str(key): value for key, value in result.items()}
  return word
  


if __name__ == '__main__':
  app.run()
  
#  detect_img(downloaded_image_path)
