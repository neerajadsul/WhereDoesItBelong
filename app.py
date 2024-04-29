import logging
import os

from flask import Flask, request
from prediction import Prediction

app = Flask(__name__)

prediction = Prediction()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logfilepath = os.path.join(os.getenv('HOME'), '.gptlog', 'app.log')
logging.basicConfig(filename=logfilepath, level=logging.DEBUG)


@app.route('/classify', methods=['POST'])
def classify():
    data = request.data.decode()
    result = prediction.predict(data)
    result = prediction.format_result_from_plain(result)
    return result

if __name__ == "__main__":
    app.run(port=8000, debug=True)