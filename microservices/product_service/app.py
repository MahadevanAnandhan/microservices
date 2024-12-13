from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    connection = mysql.connector.connect(
        host='database_service',  # Change to your database host
        user='user',              # Your database user
        password='password',      # Your database password
        database='dbname'        # Your database name
    )
    return connection

@app.route('/products', methods=['GET'])
def get_products():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.json.get('name')
    price = request.json.get('price')
    quantity = request.json.get('quantity')

    if not all([name, price, quantity]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
