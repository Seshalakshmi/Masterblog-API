from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def validate_book_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True

@app.route('/api/posts', methods=['GET', 'POST'])
def get_and_add_posts():
    if request.method == 'POST':
        if not POSTS:
            post_id = 1
        else:
            post_id = POSTS[-1]['id'] + 1

        new_post = request.get_json()

        if not validate_book_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400

        new_post['id'] = post_id
        POSTS.append(new_post)
        return jsonify(new_post), 201
    return jsonify(POSTS)


def find_post_by_id(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None


@app.route('/api/posts/<id>', methods=["DELETE"])
def delete_post(post_id):
    deleted_post = find_post_by_id(post_id)
    POSTS.remove(deleted_post)

    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
