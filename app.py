from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from werkzeug.utils import secure_filename
import os

import config
import instance.config

app = Flask(__name__)

# Change configuration here
cfg = config.config["development"]

# Konfigurace databáze a cesta pro nahrávání souborů
app.config['SQLALCHEMY_DATABASE_URI'] = instance.config.SQLALCHEMY_DATABASE_URI
app.config['UPLOAD_FOLDER'] = cfg.UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializace SQLAlchemy
db = SQLAlchemy(app)


# Definice modelu pro příspěvky
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(MutableList.as_mutable(ARRAY(db.Text)), nullable=True, default=list)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


# Vytvoření databázových tabulek při prvním spuštění
with app.app_context():
    db.create_all()


# Hlavní stránka - zobrazení formuláře pro přidání příspěvku
@app.route('/')
def index():
    posts = Post.query.all()  # Načtení všech příspěvků z databáze
    return render_template('index.html', posts=posts)


# Přidání nového příspěvku
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Zpracování nahrání obrázku, pokud je přítomen
        image_filenames = []
        images = request.files.getlist('images')
        if images and images[0].filename != '':  # Zkontrolovat, zda jsou obrázky
            for image in images:
                file_name = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                image_filenames.append(file_name)

        # Uložení příspěvku do databáze
        new_post = Post(title=title, content=content, images=image_filenames)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))  # Přesměrování na domovskou stránku nebo jinou stránku

    return render_template('add_post.html', post=None, edit=False)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        # Zpracování nových obrázků
        images = request.files.getlist('images')
        if images and images[0].filename != '':  # Zkontrolovat, zda jsou obrázky
            image_filenames = []
            for image in images:
                file_name = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                image_filenames.append(file_name)
            if post.images:
                post.images += image_filenames
            else:
                post.images = image_filenames

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Error occurred: {e}')  # Zobrazí chybu v konzoli
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('add_post.html', post=post, edit=True)


# Funkce pro odstranění příspěvku
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Odstranění obrázku ze složky uploads, pokud existuje
    if post.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Odstranění příspěvku z databáze
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


if __name__ == "__main__":
    app.run(debug=cfg.DEBUG)
