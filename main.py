from flask import Flask, redirect, render_template, request, Response, url_for
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from datetime import date
from io import BytesIO
import barcode
import random
import qrcode
import base64
import yt_dlp
import io
import os

app = Flask(__name__)

@app.route('/down')
def download():
    url = request.form.get('url')
    download_video(url)
    return render_template('index.html', url = url)

@app.route('/git')
def redirection_google():
    return redirect('https://github.com/randriamalala5')
    
@app.route('/mail')
def redirection_mail():
    return redirect('http://randriamalalaandrefelix@gmail.com')

@app.route('/in')
def redirection_linkedin():
    return redirect('http://www.linkedin.com/in/randriamalala-andré-félix-b32851248')

@app.route('/')
def accueil():
    #d = date.today().isoformat()
    phqr = random.choice(['Entrez le texte à générer ici.',"Votre texte s'il vous plait.",'Veillez saisir votre texte ici.'])
    phbc = random.choice(['Entrez le texte à générer ici.',"Votre texte s'il vous plait.",'Veillez saisir votre texte ici.'])
    return render_template('index.html',placeholder_bc = phbc,placeholder_qr = phqr)

@app.route('/qrcodegen', methods=['GET', 'POST'])
def qrcodegen():
    qr_code_data = None  # Variable pour stocker le QR Code
    phqr = random.choice(['Entrez le texte à générer ici.',"Votre texte s'il vous plait.",'Veillez saisir votre texte ici.'])
    phbc = random.choice(['Entrez le texte à générer ici.',"Votre texte s'il vous plait.",'Veillez saisir votre texte ici.'])
    if request.method == 'POST':
        text = request.form.get('char')
        if text:
            # Générer un QR Code pour le texte saisi
            qr = qrcode.QRCode(
                version=1,
                error_correction = qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            # Convertir le QR Code en image binaire
            img = qr.make_image(fill_color="black", back_color="white")
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            # Encoder l'image en base64 pour l'afficher dans HTML
            qr_code_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return render_template('index.html', qr_code_data=qr_code_data,placeholder_bc = phbc,placeholder_qr = phqr, texte_saisi_qr = text)
    
@app.route('/barcodegen', methods=['GET', 'POST'])
def barcodegen():
    bar_code_data = None
    phqr = random.choice(['Entrez le texte à générer ici.',"Votre texte s'il vous plait.",'Veillez saisir votre texte ici.'])
    phbc = random.choice(['Entrez le texte à générer ici.',"Votre texte s'il vous plait.",'Veillez saisir votre texte ici.'])
    if request.method == 'POST':
        text = request.form.get('char_bar')
        if text:            
            # Générer un QR Code pour le texte saisi
            code128 = barcode.get(
                "code128",
                text,
                writer = ImageWriter())
            buffer = io.BytesIO()
            code128.write(buffer)
            image = Image.open(buffer)
            bar_code_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return render_template('index.html', bar_code_data = bar_code_data, placeholder_bc = phbc, placeholder_qr = phqr, texte_saisi_bc = text)


def download_video(url):
    ydl_opts = {
        'outtmpl': 'video_downloaded.%(ext)s',  # Nom du fichier de sortie
        'noplaylist': True,  # Ne pas télécharger des playlists, juste la vidéo
        'quiet': False,  # Afficher des logs pour le suivi
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host = '192.168.137.1', port = 5000, debug=True)
