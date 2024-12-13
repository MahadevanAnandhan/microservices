from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    connection = mysql.connector.connect(
        host='database_service',  # Use the service name from docker-compose
        user='user',
        password='password',
        database='dbname'
    )
    return connection

@app.route('/orders', methods=['GET'])
def get_orders():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    user_id = request.json.get('user_id')  # Assuming you have a user reference
    
    if not all([product_id, quantity, user_id]):
        return jsonify({"error": "Missing fields"}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO orders (product_id, quantity, user_id) VALUES (%s, %s, %s)", (product_id, quantity, user_id))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Order added successfully!"}), 201

@app.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Order deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
