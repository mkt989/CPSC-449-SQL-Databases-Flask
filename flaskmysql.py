from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

#sourcing the environment variables from the .env file
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
            return {
                "id": self.id,
                "username": self.username,
            }

@app.route('/add_users', methods=['POST'])
def add_users():
    try:
        # Begin a transaction
        db.session.begin()

        # Create multiple user instances
        user1 = User(username='user1')
        user2 = User(username='user2')
        user3 = User(username='user3')

        # Add them to the session
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        # Commit the transaction
        db.session.commit()

        return 'Users added successfully!', 201

    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        return f'An error occurred: {str(e)}', 500

    finally:
        # Optional: cleanup (not necessary in this context)
        db.session.remove()

@app.route('/users/query', methods=['GET'])
def get_users_query():
    sql = text('SELECT id, username FROM user')
    result = db.session.execute(sql)
    users_list = [{"id": row[0], "username": row[1]} for row in result]
    return jsonify(users_list)

@app.route('/users/model', methods=['GET'])
def get_users_model():
    users = User.query.all()  # Fetch all users
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list), 200 

@app.route('/users/where', methods=['GET'])
def get_users_new():
    users = db.session.scalars(db.select(User).where(User.username=='user1')).all()  # ORM way to query all users
    users_list = [user.to_dict() for user in users]  # Convert each User object to a dictionary
    return jsonify(users_list)

@app.route('/users/fetchall', methods=['GET'])
def get_users_fetchall():
    users = db.session.scalars(db.select(User)).fetchall()  # ORM way to query all users
    users_list = [user.to_dict() for user in users]  # Convert each User object to a dictionary
    return jsonify(users_list)

@app.route('/users/fetchmany', methods=['GET'])
def get_users_fetchmany():
    users = db.session.scalars(db.select(User)).fetchmany(2)  # ORM way to query all users
    users_list = [user.to_dict() for user in users]  # Convert each User object to a dictionary
    return jsonify(users_list)

@app.route('/users/fetchone/<username>', methods=['GET'])
def get_user_fetch_one(username):
    sql = text('SELECT id, username FROM user')
    row = db.session.execute(sql).fetchone()
    users_list = {"id": row[0], "username": row[1]}
    return jsonify(users_list)

@app.route('/users/<username>', methods=['GET'])
def get_users_username(username):
    user = db.session.scalars(db.select(User).where(User.username==username)).one()  # ORM way to query all users
    users_list = user.to_dict() # Convert each User object to a dictionary
    return jsonify(users_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)