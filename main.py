from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

massage_prices = {
    'Masazas1': 10,
    'Masazas2': 20,
    'Masazas3': 30
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
            flash("A submission with the same day and time already exists. Please choose a different day or time.")
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

        return f"Selected Massage: {selected_massage}<br>Price: ${price}<br>Name: {name}<br>Phone: {phone}<br>Day: {day}<br>Time: {time}"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_app()
    app.run(debug=True)
