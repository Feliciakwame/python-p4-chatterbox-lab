from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(Message.updated_at).all()
        response = [message.to_dict() for message in messages]
        return make_response(jsonify(response), 200)

    elif request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        if not data.get("body") or not data.get("username"):
            return make_response({"error": "Missing required fields"}, 400)

        message = Message(**data)
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 201)


@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if message is None:
        return make_response({"error": "Message not found"}, 404)

    if request.method == "GET":
        return make_response(message.to_dict(), 200)

    elif request.method == "PATCH":
        data = request.get_json() if request.is_json else request.form
        for key, value in data.items():
            setattr(message, key, value)

        db.session.commit()
        return make_response(message.to_dict(), 200)

    elif request.method == "DELETE":
        print(f"Before delete: {message.id}, {message.body}")  # Debug print
        db.session.delete(message)
        db.session.commit()

        # Check if it's deleted
        deleted_message = db.session.get(Message, id)
        if deleted_message is None:
            print(f"After delete:None(Successfully deleted)")
            return make_response({"message": "Message deleted successfully"}, 200)
        else:
            print(f"After delete: {deleted_message.id}")
            return make_response({"error": "Failed to delete message"})
    return make_response({"error": "Invalid request method"}, 400)


if __name__ == "__main__":
    app.run(port=5555)
