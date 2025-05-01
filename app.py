from flask import Flask, request, jsonify, render_template_string
import boto3
import json
import uuid

app = Flask(__name__)

# ARN do ponto de acesso
BUCKET_ACCESS_POINT_ARN = 'arn:aws:s3:us-east-1:381492243096:accesspoint/acesso-public'

# Criar o cliente boto3 (não precisa mudar o endpoint manualmente, boto3 entende Access Point se usar o ARN)
s3 = boto3.client('s3')

# Página HTML
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Enviar Pedido</title>
</head>
<body>
    <h1>Formulário de Envio de Pedido</h1>
    <form action="/submit" method="post">
        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>ID do Pedido:</label><br>
        <input type="text" name="order_id" required><br><br>

        <label>Detalhes do Pedido:</label><br>
        <textarea name="details" rows="6" cols="40" required></textarea><br><br>

        <input type="submit" value="Enviar Pedido">
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def form():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Captura os dados do formulário
        order = {
            "email": request.form.get('email'),
            "order_id": request.form.get('order_id'),
            "details": request.form.get('details')
        }

        print("Dados recebidos:", order)

        # Nome único para o arquivo dentro do bucket
        file_name = f"orders/{uuid.uuid4()}.json"

        # Salvar no S3 através do Access Point
        s3.put_object(
            Bucket=BUCKET_ACCESS_POINT_ARN,
            Key=file_name,
            Body=json.dumps(order, ensure_ascii=False),
            ContentType='application/json'
        )

        return '''
            <h2>Pedido enviado com sucesso!</h2>
            <a href="/">Voltar ao formulário</a>
        '''

    except Exception as e:
        print("Erro:", str(e))
        return f"<h2>Erro: {str(e)}</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
