from flask import Flask, redirect, render_template, request, Response, url_for, send_file
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

"""
# Définir le dossier de téléchargement
DOWNLOAD_FOLDER = "static/DownloadsWeb"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(url):
    #Télécharge une vidéo et retourne le chemin du fichier téléchargé.
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, 'download_by_randria_app.%(ext)s'),  # Chemin du fichier
        'noplaylist': True,  # Ne pas télécharger les playlists
        'quiet': False,  # Afficher des logs
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    
    return filename  # Retourne le chemin du fichier téléchargé

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:
            try:
                filepath = download_video(video_url)
                return send_file(filepath, as_attachment=True)
            except Exception as e:
                return f"Erreur lors du téléchargement : {e}"

    return render_template("index.html")
"""





DOWN_FOLDER = "VideosDownloader"
os.makedirs(DOWN_FOLDER, exist_ok=True)

def down_video(video_url):
    #Télécharge une vidéo depuis un lien
    options = {
        'format': 'best',
        'outtmpl': f"{DOWN_FOLDER}/%(title)s.%(ext)s",
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

@app.route("/vd", methods=["GET", "POST"])
def index_0():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:
            try:
                filepath = down_video(video_url)
                return send_file(filepath, as_attachment=True)
            except Exception as e:
                return f"Erreur lors du téléchargement : {e}"
    return render_template("index.html")

    
    
    
    
    
    
    

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



if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host = '192.168.137.1', port = 5000, debug=True)
