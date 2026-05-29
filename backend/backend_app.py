from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_book_data(data):
    if "title" not in data:
        return "title is missing"
    elif "content" not in data:
        return "content is missing"
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
            return jsonify({f"Message: {new_post}"}), 400

        new_post['id'] = post_id
        POSTS.append(new_post)
        return jsonify(new_post), 201

    elif request.method == "GET":
        sort = request.args.get('sort')
        direction = request.args.get('direction')

        if not sort and not direction:
            return jsonify(POSTS), 200

        if sort == 'title' and direction == 'asc':
            sorted_list = sorted(POSTS, key=lambda post: post['title'])
            return jsonify(sorted_list), 200

        if sort == 'title' and direction == 'desc':
            sorted_list = sorted(POSTS, key=lambda post: post['title'],
                                 reverse=True)
            return jsonify(sorted_list), 200

        if sort == 'content' and direction == 'asc':
            sorted_list = sorted(POSTS, key=lambda post: post['content'])
            return jsonify(sorted_list), 200

        if sort == 'content' and direction == 'desc':
            sorted_list = sorted(POSTS, key=lambda post: post['content'],
                                 reverse=True)
            return jsonify(sorted_list), 200

        return jsonify("Message: Invalid sort fields or directions"), 400


def find_post_by_id(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=["DELETE", "PUT"])
def delete_post(id):
    if request.method == "DELETE":
        deleted_post = find_post_by_id(id)
        if not deleted_post:
            return jsonify(f"Message: Post {id} was not found"), 404

        POSTS.remove(deleted_post)
        return jsonify(
            f"message: Post with id {id} has been deleted successfully."), 200

    elif request.method == "PUT":
        post = find_post_by_id(id)
        if not post:
            return jsonify(f"Message: Post {id} was not found"), 404

        get_json = request.get_json()
        update_post = {
            "id": id,
            "title": get_json.get("title", post["title"]),
            "content": get_json.get("content", post["content"])
        }

        post.update(update_post)

        return jsonify(update_post), 200


@app.route("/api/posts/search", methods=["GET"])
def search():
    title = request.args.get('title')
    content = request.args.get('content')
    if not title or not content:
        return jsonify("Message: we need two parameters"), 404

    search_post = [post for post in POSTS
                   if title.lower() in post['title'].lower()
                   and content.lower() in post['content'].lower()]

    return jsonify(search_post), 200


@app.errorhandler(400)
def invalid_error(error):
    return jsonify({"error": "Invalid post data"}), 400


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
