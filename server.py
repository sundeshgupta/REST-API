from flask import Flask, request, render_template, make_response, redirect
from flask_restful import Resource, Api, reqparse
from json import dumps
from flask_jsonpify import jsonify
from werkzeug.utils import secure_filename
import os

import cv2
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import math

app = Flask(__name__)
api = Api(app)


class Root(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


class CreateCollage(Resource):
    def get(self):
        result = {'Upload an image by going to:':'/index'}
        print(result)
        return jsonify(result) # Fetches first column that is Employee ID

    def post(self):
        print("sfdsff")
        print(request.method)
        print(request.form)
        print(request.files)
        if 'file' not in request.files:
            print('No file part')
            return jsonify({'No file found':'.'})
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join('/home/sundesh/Documents/git/RestAPI/static', filename))
            img = cv2.imread('/home/sundesh/Documents/git/RestAPI/static/'+ str(filename))

            # cv2.resize()
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            width = int(img.shape[1])
            height = int(img.shape[0])
            dim = (width//20, height//20)

            faces = faceCascade.detectMultiScale(img_gray, scaleFactor=1.3, minSize = dim)

            print("Found " + str(len(faces)) + " Faces!")

            rows = int(math.sqrt(len(faces)))
            columns = math.ceil((len(faces))/rows)

            plt.figure(figsize = (8, 8))
            gs1 = gridspec.GridSpec(rows, columns)
            gs1.update(wspace=0, hspace=0)

            k = 0
            for (x, y, w, h) in faces:
                roi = img[y:y+h, x:x+w]
                b, g, r = cv2.split(roi)
                roi = cv2.merge([r, g, b])
                ax1 = plt.subplot(gs1[k])
                ax1.imshow(roi)
                ax1.set_xticklabels([])
                ax1.set_yticklabels([])
                ax1.axis('off')
                ax1.set_aspect('equal')
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                k = k+1
            plt.tight_layout()
            # plt.show()
            plt.savefig('/home/sundesh/Documents/git/RestAPI/static/faces_detected.jpg')
            plt.close()
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('output.html', faces = len(faces)), 200, headers)
        # if file:
        #     print("got it")
        # else:
        #     print("got it")
        
api.add_resource(CreateCollage, '/createCollage') # Route_1
api.add_resource(Root, '/index')

if __name__ == '__main__':
     app.run(port='8000')