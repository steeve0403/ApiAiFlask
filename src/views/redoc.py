from flask import Blueprint, render_template

redoc_bp = Blueprint('redoc', __name__)

@redoc_bp.route('/redoc', methods=['GET'])
def redoc():
    """
    Display the ReDoc documentation page.
    """
    spec_url = 'swagger.json'
    return render_template('redoc.html', spec_url=spec_url)

