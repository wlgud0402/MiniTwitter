from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.users = {}
app.id_count = 1


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(
        app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database
    return app


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user['id'] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1

    return jsonify(new_user)


app.tweets = []


@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    if len(tweet) > 300:
        return "300자를 초과했습니다.", 400

    user_id = int(payload['id'])
    app.tweets.append({
        'user_id': user_id,
        'tweet': tweet
    })

    return '', 200

# Default JSON encoder는 set을 JSON으로 변환할 수 없다.
# 그러므로 JSON encoder를 오버라이딩 => set을 list로 변환하여 JSON으로 변환 가능하게 해야함


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder


@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonify(user)


@app.route("/unfollow", methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)

    return jsonify(user)


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })


app.run(port=5000, debug=True)
