from flask import Flask, jsonify, request
from flask_cors import CORS
import aws_handler  # קובץ לניהול AWS

app = Flask(__name__)
CORS(app)  # מאפשר ל-Frontend לגשת ל-Backend

@app.route('/api/instances', methods=['GET'])
def get_instances():
    instances = aws_handler.list_ec2_instances()
    return jsonify(instances)

@app.route('/api/start-instance', methods=['POST'])
def start_instance():
    data = request.json
    instance_id = data.get('instance_id')
    aws_handler.start_ec2_instance(instance_id)
    return jsonify({"message": f"Instance {instance_id} started!"})

if __name__ == '__main__':
    app.run(debug=True)
