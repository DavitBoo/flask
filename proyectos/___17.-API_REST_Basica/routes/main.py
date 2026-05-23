from flask import Blueprint, render_template
from models import Post

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)
