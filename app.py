from flask import Flask, request, jsonify, render_template
import boto3
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# ARN do ponto de acesso
BUCKET_ACCESS_POINT_ARN = 'arn:aws:s3:us-east-1:381492243096:accesspoint/acesso-public'

# Cliente S3
s3 = boto3.client('s3')

# Simulando a lista de produtos (poderia vir de banco futuramente)
PRODUCTS = [
    {
        "product_id": "1",
        "name": "Notebook Gamer",
        "description": "Notebook potente para jogos pesados.",
        "price": 4500.00,
        "stock_quantity": 10,
        "created_at": str(datetime.now())
    },
    {
        "product_id": "2",
        "name": "Mouse Sem Fio",
        "description": "Mouse wireless com bateria durável.",
        "price": 150.00,
        "stock_quantity": 50,
        "created_at": str(datetime.now())
    },
    {
        "product_id": "3",
        "name": "Teclado Mecânico",
        "description": "Teclado mecânico RGB para alta performance.",
        "price": 350.00,
        "stock_quantity": 30,
        "created_at": str(datetime.now())
    }
]

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html', products=PRODUCTS)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        order_data = request.get_json()
        print("Pedido recebido:", order_data)

        file_name = f"orders/{uuid.uuid4()}.json"

        s3.put_object(
            Bucket=BUCKET_ACCESS_POINT_ARN,
            Key=file_name,
            Body=json.dumps(order_data, ensure_ascii=False),
            ContentType='application/json'
        )

        return jsonify({"message": "Pedido enviado com sucesso!"})

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
