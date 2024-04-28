import logging

from flask import Flask, request
from prediction import Prediction

app = Flask(__name__)

prediction = Prediction()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logging.basicConfig(filename='app.log', level=logging.DEBUG)


@app.route('/classify', methods=['POST'])
def classify():
    data = request.data.decode()
    result = prediction.predict(data)
    return prediction.format_result(result)

if __name__ == "__main__":
    app.run(port=8000, debug=False)