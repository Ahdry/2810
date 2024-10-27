from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

@app.route('/register', methods=['POST'])
def register_users():
    data = request.json
    count = data.get('count', 0)

    if not isinstance(count, int) or count <= 0:
        return jsonify({'error': 'Count must be a positive integer'}), 400

    start_time = time.time()

    for i in range(count):
        username = f"user_{i+1}"
        new_user = User(username=username)
        db.session.add(new_user)

    db.session.commit()
    end_time = time.time()

    return jsonify({
        'message': f'{count} users registered successfully',
        'time_taken': end_time - start_time
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    db.create_all()  # Создаёт таблицы базы данных
    app.run(debug=True)