from flask import Blueprint, render_template

editor_bp = Blueprint('editor', __name__)

@editor_bp.route('/editor')
def editor():
    return render_template('editor.html')