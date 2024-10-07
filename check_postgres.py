from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Replace 'username', 'password', 'hostname', 'port', 'database' with your PostgreSQL details
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@127.0.0.1:5432/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/check_db')
def check_db_connection():
    try:
        # Establish a connection and execute a simple query using the connection
        with db.engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        return "PostgreSQL connection is working."
    except OperationalError:
        return "Failed to connect to PostgreSQL."

if __name__ == '__main__':
    app.run(debug=True)