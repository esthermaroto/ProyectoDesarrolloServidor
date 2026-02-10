from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models import Accommodation, db

acomodation_bp = Blueprint('acomodation', __name__, template_folder='../templates')

# =========================
# INDEX
# =========================
@acomodation_bp.route('/acomodation')
def index():
    accommodations = Accommodation.query.all()
    return render_template('acomodationIndex.html', accommodations=accommodations)


# =========================
# CREATE
# =========================
@acomodation_bp.route('/acomodation/create', methods=['GET', 'POST'])
def create():

    if "user_id" not in session:
        flash('Debes iniciar sesión')
        return redirect(url_for('login'))

    if session.get("role") not in ["company", "admin"]:
        flash('No tienes permisos')
        return redirect(url_for('acomodation.index'))

    if request.method == 'POST':
        accommodation = Accommodation(
            name=request.form['name'],
            address=request.form['address'],
            phoneNumber=request.form['phoneNumber'],
            web=request.form['web'],
            stars_quality=request.form['stars_quality'],
            description=request.form['description'],
            type=request.form['type'],
            id_company=session["user_id"]
        )

        db.session.add(accommodation)
        db.session.commit()
        return redirect(url_for('acomodation.index'))
    
    return render_template('acomodationCreate.html')


# =========================
# SHOW
# =========================
@acomodation_bp.route('/acomodation/show/<int:id>', methods=['GET'])
def show(id):
    accommodation = Accommodation.query.get_or_404(id)
    return render_template('acomodationShow.html', accommodation=accommodation)


# =========================
# DELETE
# =========================
@acomodation_bp.route('/acomodation/delete/<int:id>', methods=['POST'])
def delete(id):

    if "user_id" not in session:
        flash('Debes iniciar sesión')
        return redirect(url_for('login'))

    accommodation = Accommodation.query.get_or_404(id)

    if session["user_id"] != accommodation.id_company and session.get("role") != "ADMIN":
        flash('No tienes permiso')
        return redirect(url_for('acomodation.index'))

    db.session.delete(accommodation)
    db.session.commit()
    return redirect(url_for('acomodation.index'))


# =========================
# EDIT
# =========================
@acomodation_bp.route('/acomodation/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    if "user_id" not in session:
        flash('Debes iniciar sesión')
        return redirect(url_for('login'))

    accommodation = Accommodation.query.get_or_404(id)

    if session["user_id"] != accommodation.id_company and session.get("role") != "ADMIN":
        flash('No tienes permiso')
        return redirect(url_for('acomodation.index'))

    if request.method == 'POST':
        accommodation.name = request.form['name']
        accommodation.address = request.form['address']
        accommodation.phoneNumber = request.form['phoneNumber']
        accommodation.web = request.form['web']
        accommodation.stars_quality = request.form['stars_quality']
        accommodation.description = request.form['description']
        accommodation.type = request.form['type']

        db.session.commit()
        return redirect(url_for('acomodation.index'))

    return render_template('acomodationEdit.html', accommodation=accommodation)