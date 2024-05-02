from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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
        new_martyr = Martyr(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            # ... [Add other fields as per your form] ...
        )
        db.session.add(new_martyr)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('insert.html')

# Route to update a martyr's details
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    martyr_to_update = Martyr.query.get_or_404(id)
    if request.method == 'POST':
        martyr_to_update.first_name = request.form['first_name']
        martyr_to_update.last_name = request.form['last_name']
        # ... [Update other fields as per your form] ...
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

from datetime import date


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)