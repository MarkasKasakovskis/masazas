from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)


db = SQLAlchemy(app)

massage_prices = {
    'Klasikinis masažas': 40,
    'Karštu akmenų masažas':39,
    'Masažas bioenerginiu masažuokliu': 20
}



class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    massage = db.Column(db.String(50))
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    day = db.Column(db.String(10))  
    time = db.Column(db.String(5))


def create_app():
    admin = Admin(app)
    admin.add_view(ModelView(Submission, db.session))

    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/massage-info')
    def massage_info():
        return render_template('massage_info.html')

    @app.route('/about-massage-therapist')
    def about_massage_therapist():
        return render_template('about_massage_therapist.html')

    @app.route('/registration')
    def registration():
        return render_template('registration.html')

    @app.route('/start')
    def start():
        return render_template('index.html')

    @app.route('/submit', methods=['POST'])
    def submit():
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            day = request.form['day']
            time = request.form['time']
            selected_massage = request.form['massage']

        
        existing_submission = Submission.query.filter_by(day=day, time=time).first()
        if existing_submission:
            flash("Šis laikas jau užimtas. Pasirinkite kita jums patogu laiką.")
            return redirect(url_for('home'))

        
        price = massage_prices.get(selected_massage, 0)  

        
        submission = Submission(
            massage=selected_massage,
            name=name,
            phone=phone,
            day=day,
            time=time
        )

        db.session.add(submission)
        db.session.commit()

        return f"Jusu pasirinktas masažas: {selected_massage}<br>Kaina: {price}€<br>Vardas: {name}<br>Telefonas: {phone}<br>Diena: {day}<br>Laikas: {time}<br>Adresas: Kaunas, Parko g.1"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_app()
    app.run(debug=True)
