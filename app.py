import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#crates an app that is named under the name of our file 'app' for us
app = Flask(__name__)

#connect SQLAlchemy to our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://andrespuentes@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#links sqlalchemy to our flask app
db = SQLAlchemy(app)

#we define migrate and pass the app and the database, we can now start using the Flask-Migrate commands
migrate = Migrate(app, db)



class Todo(db.Model):
    #we define the table name:
    __tablename__ = 'todos'

    #we define our table structure:
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)#we define the ForeignKey and the constraints in the Child, the string is the name and column of the Parent table

    #we dine our repr function, repr is a sqlalchemy function that let us know what our datbase contains
    def __repr__(self):
        return f'<Todo {self.id} {self.description} >'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)#We define the relationship, this is defined in the Parent class


#executes all the past config
#with migrations we dont use create.all anymore
#db.create_all()

@app.route('/')
def index():
    return redirect(url_for('get_lists_todos', list_id = 1))


#route that listens to the root folder
@app.route('/lists/<list_id>')
def get_lists_todos(list_id):
    #jinja templating solution in flask: allows to embed non-html content to html files
    #render_template will go and look for the 'index.html' file in a templates folder inside the root folder

    lists = TodoList.query.order_by('id').all()
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    
    return render_template('index.html',lists=lists, todos=todos)

    #return render_template('index.html', data=Todo.query.filter_by(list_id=list_id).order_by('id').all())

#we define the route and add an aurgument with the methos that the form will use
#this is our controller
@app.route('/create', methods=['POST'])
def create():
    #we add a second argument as a fallback in case there is no data
    #description = request.form.get('description', '')

    #as the ajax request sends a json object, we use a different method here called get_json, as we sent an object we receive a dictionary with a key 'description'
    error = False
    body = {}
    try:
        #from the AJAX request we get the json object
        description = request.get_json()['description']
        print(description)
        new_todo = Todo(description=description)
        db.session.add(new_todo)
        db.session.commit()
        #we add the description to the body so we keep it there in case everything works fine, we need to do this because we can't read from the new_todo object after it is commited, it will expire and we will get an error
        body['description'] = new_todo.description
    except:
        error = True
        db.session.rollback()
        #we need to import sys so we wil get the info of the exception back
        print(sys.exc_info())
    finally:
        db.session.close()
        
    if not error:
        #everything looks good so we return the body as JSON -- 
        return jsonify(body)

    #we can import redirect and url_for so in this case the site is redirected to index and the news entries will be shown
    
    #I comment this out as I am not redirectitng anymore, we are now using an ajax request
    #return redirect(url_for('index'))

    #we remove this as it will be returned inside the try block
    #return jsonify({
    #    'description': new_todo.description
    #})

#in this route we added <todo_id> this let's us use that part as it is returned inside the function
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed'] 
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
        body.completed = completed
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for('index'))



@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    body = {}
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        body['respuesta'] = 'done!'
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify(body)

    
