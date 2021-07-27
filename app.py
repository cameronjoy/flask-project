from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(20))
    todo = db.relationship('Todo', backref='owner')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        current_user = request.form['user']
        exists = db.session.query(User.id).filter_by(username=current_user).first() is not None
        if exists == False:
            new_user = User(username=current_user)

            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template('index.html', current_user=current_user)
            except:
                print('error!')
        else:
            return render_template('index.html', current_user=current_user)

    else:
        return render_template('login.html',)
        




@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)


        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            print('error!')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)