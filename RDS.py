import boto3
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize AWS RDS connection
rds_client = boto3.client('rds-data', region_name='us-east-2')
database_name = 'car_data_db'
db_cluster_arn = 'your-rds-cluster-arn'
db_credentials_secrets_store_arn = 'your-secret-store-arn'

# Query RDS
def execute_rds_query(sql, parameters=None):
    response = rds_client.execute_statement(
        resourceArn=db_cluster_arn,
        secretArn=db_credentials_secrets_store_arn,
        database=database_name,
        sql=sql,
        parameters=parameters or []
    )
    return response

@app.route('/insert-car-data', methods=['POST'])
def insert_car_data():
    data = request.json
    sql = """
        INSERT INTO car_data (car_model, year, price, auction_date)
        VALUES (:car_model, :year, :price, :auction_date)
    """
    parameters = [
        {'name': 'car_model', 'value': {'stringValue': data['car_model']}},
        {'name': 'year', 'value': {'stringValue': data['year']}},
        {'name': 'price', 'value': {'stringValue': data['price']}},
        {'name': 'auction_date', 'value': {'stringValue': data['auction_date']}}
    ]
    execute_rds_query(sql, parameters)
    return jsonify({"message": "Data inserted successfully"}), 200

@app.route('/get-car-data', methods=['GET'])
def get_car_data():
    car_model = request.args.get('car_model')
    sql = "SELECT * FROM car_data WHERE car_model = :car_model"
    parameters = [{'name': 'car_model', 'value': {'stringValue': car_model}}]
    response = execute_rds_query(sql, parameters)
    return jsonify(response['records'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
