#!/usr/bin/env python
# -*-coding:UTF-8 -*

from flask import Flask, render_template, request, send_file, jsonify, Response
import os

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

fileseq = filefolder = awb = metering = ev = exposure = sharpness = brightness = contrast = saturation = iso = imxfix = quality = raw = width = height = hflip = vflip = timelapse_active = False
tlFolderRoot = "/media/usb/"

@app.after_request
def add_header(Response):
    Response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    Response.headers['Cache-Control'] = 'no-cache, no-store, max-age=0'
    Response.headers['Pragma'] = 'no-cache'
    return Response

@app.route('/')
def acceuil():
    return render_template('index.html')

@app.route('/takepicture', methods=['GET', 'POST'])
def takepicture():
    action = False
    if request.method == 'GET':
        fileseq = request.args.get('fileseq')
        filefolder = request.args.get('filefolder')
        awb = request.args.get('awb')
        metering = request.args.get('metering')
        ev = request.args.get('ev')
        exposure = request.args.get('exposure')
        sharpness = request.args.get('sharpness')
        brightness = request.args.get('brightness')
        contrast = request.args.get('contrast')
        saturation = request.args.get('saturation')
        iso = request.args.get('iso')
        imxfx = request.args.get('imxfx')
        quality = request.args.get('quality')
        raw = request.args.get('raw')
        width = request.args.get('width')
        height = request.args.get('height')
        hflip = request.args.get('hflip')
        vflip = request.args.get('vflip')
        timelapse_active = request.args.get('timelapse_active')
        timelapse = request.args.get('timelapse')
        timeout = request.args.get('timeout')
        action = True
                 
    if request.method == 'POST':
        fileseq = request.form['fileseq']
        filefolder = request.form['filefolder']
        awb = request.form['awb']
        metering = request.form['metering']
        ev = request.form['ev']
        exposure = request.form['exposure']
        sharpness = request.form['sharpness']
        brightness = request.form['brightness']
        contrast = request.form['contrast']
        saturation = request.form['saturation']
        iso = request.form['iso']
        imxfx = request.form['imxfx']
        quality = request.form['quality']
        raw = request.form.getlist('raw')
        width = request.form['width']
        height = request.form['height']
        hflip = request.form.getlist('hflip')
        vflip = request.form.getlist('vflip')
        timelapse_active = request.form.getlist('timelapse_active')
        timelapse = request.form['timelapse']
        timeout = request.form['timeout']
        action = True        

    if action == True:
        command = "raspistill"
        command += " --awb '" + str(awb) + "'" # Define WB
        command += " --metering '" + str(metering) + "'" # Define Metering Mode
        command += " --ev " + str(ev) # Define the Exposure Adjustment
        command += " --exposure '" + str(exposure) + "'" # Define Exposure Mode
        command += " --sharpness " + str(sharpness) # Define Image Sharpness
        command += " --brightness " + str(brightness) # Define Image Brightness
        command += " --contrast " + str(contrast) # Define Image Contrast
        command += " --saturation " + str(saturation) # Define Image Saturation
        command += " --ISO " + str(iso) # Define Image ISO            
        command += " --imxfx '" + str(imxfx) + "'" # Define Image Effect
        command += " --quality " + str(quality) # Define Image Quality
        command += " --width " + str(width) # Define output image width
        command += " --height " + str(height) # Define output image height
        command += " -n"
        
        if hflip == "1":
            command += " --hflip"

        if vflip == "1":
            command += " --vflip"

        if raw == "1":
            command += " --raw"

        # TimeLapse parameter
        # 1 minute = 3600000 microsecondes
        # 1 seconde = 1000 microsecondes
        if timelapse_active == "1":
            #folder = tlFolderRoot + "images/timelapse/" + str(filefolder)
            folder = "images/timelapse/" + str(filefolder)
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            # temps entre deux prises de vue
            # valeur en seconde à convertir en microsecondes
            timelapse = int(timelapse) * 1000
            command += " --timelapse " + str(timelapse)
            
            # durée du timelapse
            # valeur en minutes à convertir en microsecondes
            timeout = int(timeout) * 360000
            command += " --timeout " + str(timeout)
            
            command += " --output " + folder + "/" + fileseq + "\%05d.jpg"

            os.system(command)
            return render_template('takepicture.html')
        else:
            if filefolder:
                folder = "images/" + str(filefolder)
                if not os.path.exists(folder):
                    os.makedirs(folder)
            else:
                folder = "images"
                if not os.path.exists(folder):
                    os.makedirs(folder)

            if os.path.isfile(folder + "/" + str(fileseq) + ".jpg"):
                print("suppression de " + folder + "/" + str(fileseq) + ".jpg")
                
            command += " --output '" + folder + "/" + str(fileseq) + ".jpg'"

            os.system(command)
            return jsonify(fileFolder=str(filefolder), filePicture=str(fileseq) + ".jpg")
            #return render_template('takepicture.html', fileFolder=str(filefolder), filePicture=str(fileseq) + ".jpg")    
    else:
        return render_template('index.html')

@app.route('/images/<fileFolder>/<filePicture>')
def images(fileFolder, filePicture):
    return send_file("images/" + fileFolder + "/" + filePicture, "image/jpg"), 200

if __name__== '__main__' :
    app.run(host="0.0.0.0", debug=False)