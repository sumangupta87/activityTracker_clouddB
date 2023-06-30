from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 

import os
from datetime import datetime
import pytz
import urllib.parse 

# Configure Database URI: 
params = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:appdbserver431.database.windows.net,1433;Database=appdB;Uid=SumanSQL;Pwd={Welcome@12345};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")

# Init app
app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
# Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
#app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# To create db, run following commands from terminal,
# >>> python
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) 
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    started = db.Column(db.DateTime, default = datetime.now(pytz.timezone('Asia/Kolkata')))
    #duration = db.Column(db.Integer, default = 0 )

    def __repr__(self):
        return '<Task %r>' % self.id

#with app.app_context():
#    db.create_all()

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_owner = request.form['name']
        new_task = Todo(content=task_content,name=task_owner)
 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


# pip3 freeze > requirements.txt

if __name__ == '__main__':
    app.run(debug=True)
