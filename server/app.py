from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict
app = Flask(__name__)
cors = CORS(app)

@app.route("/predict", methods = ["POST"])
def hello():
    try:
        if 'path' not in request.json:
            return jsonify({'msg':'No filepath specified.'}), 400
        path = request.json['path']
        if not isinstance(path, str):
            return jsonify({'msg':'Path is not a string.'}), 400
        if len(path) < 4 or path[-4:] != '.wav':
            return jsonify({'msg':'File at path is not a valid wavfile.'}), 400
        try:
            pred = predict(path)
            return jsonify({"res":pred}), 200
        except Exception as e:
            return jsonify({"msg": str(e)}), 500
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=8001)