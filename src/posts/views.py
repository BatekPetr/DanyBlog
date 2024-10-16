import os
from flask import Blueprint, current_app, render_template, redirect, request, url_for, jsonify, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from src.posts.models import Post
from src.utils.decorators import check_is_approved
from model import db


# Defining a blueprint
posts_bp = Blueprint('posts', __name__, template_folder='../templates')


# Přidání nového příspěvku
@posts_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
@check_is_approved
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
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))
                image_filenames.append(file_name)

        # Uložení příspěvku do databáze
        new_post = Post(title=title, content=content, images=image_filenames)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({'success': True})

    return render_template('posts/add_post.html', post=None, edit=False)


@posts_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@check_is_approved
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
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))
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
        return redirect(url_for('posts.post_detail', post_id=post.id))

    return render_template('posts/add_post.html', post=post, edit=True)


# Funkce pro odstranění příspěvku
@posts_bp.route('/delete_post/<int:post_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
@check_is_approved
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Odstranění obrázku ze složky uploads, pokud existuje
    if post.images:
        for image in post.images:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
            if os.path.exists(image_path):
                os.remove(image_path)

    # Odstranění příspěvku z databáze
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('core.index'))


@posts_bp.route('/delete_image/<int:post_id>/<image_name>', methods=['POST'])
@login_required
@check_is_approved
def delete_image(post_id, image_name):
    post = Post.query.get_or_404(post_id)

    # Odstraň obrázek ze seznamu obrázků (pokud existuje)
    if image_name in post.images:
        post.images.remove(image_name)

        # Ulož změny do databáze
        db.session.commit()

        # Odstraň obrázek ze souborového systému
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)
        if os.path.exists(image_path):
            os.remove(image_path)

        flash('Obrázek byl úspěšně odstraněn.', 'success')
    else:
        flash('Obrázek nebyl nalezen.', 'danger')

    # Přesměrování zpět na detail příspěvku
    return redirect(url_for('posts.post_detail', post_id=post_id))


@posts_bp.route('/post/<int:post_id>')
@login_required
@check_is_approved
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_detail.html', post=post,
                           image=os.path.join('uploads/', post.images[0]))
