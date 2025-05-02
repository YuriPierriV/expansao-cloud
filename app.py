from flask import Flask, request, jsonify, render_template, redirect, url_for
import boto3
import json
import uuid
from datetime import datetime
import psycopg2

app = Flask(__name__)

# ARN do ponto de acesso
BUCKET_ACCESS_POINT_ARN = 'arn:aws:s3:us-east-1:381492243096:accesspoint/acesso-public'

# Cliente S3
s3 = boto3.client('s3')

# Configurações do Banco de Dados
DB_CONFIG = {
    "host": "database-2.cluster-cpwk8e8yo28t.us-east-1.rds.amazonaws.com",
    "database": "migration",  # Banco migration que você criou
    "user": "postgres",       # Usuário correto
    "password": "senhaadmin",
    "port": 5432
}

def get_products_from_db():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT product_id, name, description, price, stock_quantity, created_at
            FROM products
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()

        products = []
        for row in rows:
            products.append({
                "product_id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4],
                "created_at": row[5].strftime('%Y-%m-%d %H:%M:%S')
            })

        return products

    except Exception as e:
        print("Erro ao buscar produtos:", e)
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()

def add_product_to_db(name, description, price, stock_quantity):
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products (name, description, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """, (name, description, price, stock_quantity))

        connection.commit()

    except Exception as e:
        print("Erro ao adicionar produto:", e)
        raise

    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/', methods=['GET'])
def catalog():
    products = get_products_from_db()
    return render_template('catalog.html', products=products)

@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        name = data['name']
        description = data['description']
        price = float(data['price'])
        stock_quantity = int(data['stock_quantity'])

        add_product_to_db(name, description, price, stock_quantity)

        return jsonify({"message": "Produto adicionado com sucesso!"}), 201

    except Exception as e:
        print("Erro ao adicionar produto:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/submit', methods=['POST'])
def submit():
    try:
        order_data = request.get_json()
        print("Pedido recebido:", order_data)

        # Processar cada item comprado
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        for item in order_data['details']:
            product_id = item['product_id']
            quantity = 1  # Estamos considerando que o botão "Adicionar" é para 1 unidade

            # Primeiro, verifica se tem estoque
            cursor.execute("SELECT stock_quantity FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
            if result is None:
                raise Exception(f"Produto ID {product_id} não encontrado.")
            current_stock = result[0]
            if current_stock <= 0:
                raise Exception(f"Produto ID {product_id} está fora de estoque.")

            # Atualizar diminuindo o estoque
            cursor.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE product_id = %s
            """, (quantity, product_id))

        connection.commit()
        cursor.close()
        connection.close()

        # Agora salvar o pedido no S3
        file_name = f"orders/{uuid.uuid4()}.json"
        s3.put_object(
            Bucket=BUCKET_ACCESS_POINT_ARN,
            Key=file_name,
            Body=json.dumps(order_data, ensure_ascii=False),
            ContentType='application/json'
        )

        return jsonify({"message": "Pedido enviado e estoque atualizado com sucesso!"})

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
