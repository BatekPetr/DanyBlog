from flask import Blueprint, render_template
from flask_login import login_required

# App package imports
from src.posts.models import Post
from src.utils.decorators import check_is_approved

core_bp = Blueprint("core", __name__, template_folder='../templates', static_folder='../static')


# Hlavní stránka - zobrazení formuláře pro přidání příspěvku
@core_bp.route("/")
@login_required
@check_is_approved
def index():
    posts = Post.query.all()  # Načtení všech příspěvků z databáze
    return render_template('core/index.html', posts=posts, heading_image='DanyTravels.jpg')