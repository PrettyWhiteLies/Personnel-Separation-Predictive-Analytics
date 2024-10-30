from flask import Blueprint, request, jsonify
from utils import preprocess_model


predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/', methods=['POST'])
def predict_route():
    data = request.get_json(force=True)
    input_data = data['input']

    #processed_data = preprocess_data(input_data)


    predictions = preprocess_model.predict_model(input_data)


    return jsonify({'predictions': predictions.tolist()})
