from flask import Flask, request
from prediction import predict

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.data.decode()
    result = predict(data)
    return result

if __name__ == "__main__":
    app.run(port=8000, debug=True)