from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from werkzeug.utils import secure_filename

import os
app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

db = SQLAlchemy(app)



class Martyr(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # شناسه یکتا برای هر شهید
    first_name = db.Column(db.String(50), nullable=False)  # نام شهید
    last_name = db.Column(db.String(50), nullable=False)  # نام خانوادگی شهید
    birth_date = db.Column(db.Date)  # تاریخ تولد شهید
    birth_place = db.Column(db.String(100))  # محل تولد شهید
    burial_place = db.Column(db.String(100))  # محل دفن شهید
    martyrdom_date = db.Column(db.Date)  # تاریخ شهادت شهید
    martyrdom_place = db.Column(db.String(100))  # محل شهادت شهید
    achievements = db.Column(db.Text)  # اثرات و دستاوردهای شهید
    will = db.Column(db.Text)  # وصیت‌نامه شهید
    biography = db.Column(db.Text)  # زندگی‌نامه شهید
    photos = db.Column(db.String(1000))  # لیست مسیر عکس‌ها
    main_photo = db.Column(db.String(100))  # مسیر تصویر شاخص
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

@app.route('/')
def home():
    martyrs = Martyr.query.all()
    return render_template("home.html", martyrs=martyrs)

# Route to add a new martyr
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # Convert string dates to Python date objects
        birth_date_str = request.form['birth_date']
        martyrdom_date_str = request.form['martyrdom_date']
        birth_date = datetime.strptime(birth_date_str, '%B %d, %Y').date() if birth_date_str else None
        martyrdom_date = datetime.strptime(martyrdom_date_str, '%B %d, %Y').date() if martyrdom_date_str else None

        new_martyr = Martyr(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            birth_date=birth_date,
            birth_place=request.form['birth_place'],
            burial_place=request.form['burial_place'],
            martyrdom_date=martyrdom_date,
            martyrdom_place=request.form['martyrdom_place'],
            achievements=request.form['achievements'],
            will=request.form['will'],
            biography=request.form['biography'],
            photos=request.form['photos'],
            main_photo=request.form['main_photo']
        )
        file = request.files['main_photo_file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_martyr.main_photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        db.session.add(new_martyr)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('insert.html')


# Route to update a martyr's details
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

# ... your existing code ...

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    martyr_to_update = Martyr.query.get_or_404(id)
    if request.method == 'POST':
        martyr_to_update.first_name = request.form['first_name']
        martyr_to_update.last_name = request.form['last_name']
        # Convert string dates to Python date objects
        birth_date_str = request.form['birth_date']
        martyrdom_date_str = request.form['martyrdom_date']
        martyr_to_update.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        martyr_to_update.martyrdom_date = datetime.strptime(martyrdom_date_str, '%Y-%m-%d').date() if martyrdom_date_str else None
        martyr_to_update.birth_place = request.form['birth_place']
        martyr_to_update.burial_place = request.form['burial_place']
        martyr_to_update.martyrdom_place = request.form['martyrdom_place']
        martyr_to_update.achievements = request.form['achievements']
        martyr_to_update.will = request.form['will']
        martyr_to_update.biography = request.form['biography']
        martyr_to_update.photos = request.form['photos']
        martyr_to_update.main_photo = request.form['main_photo']
        # Handle file upload for main_photo
        file = request.files.get('main_photo_file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            martyr_to_update.main_photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html', martyr=martyr_to_update)

# Route to delete a martyr
@app.route('/delete/<int:id>')
def delete(id):
    martyr_to_delete = Martyr.query.get_or_404(id)
    db.session.delete(martyr_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/martyr/<int:id>')
def martyr_details(id):
    martyr = Martyr.query.get_or_404(id)
    return render_template('martyr_details.html', martyr=martyr)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)