import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import boto3

def lambda_handler(event, context):
    # Obter informações do evento S3
    s3_event = event['Records'][0]['s3']
    bucket_name = s3_event['bucket']['name']
    object_key = s3_event['object']['key']

    # Criar cliente S3
    s3_client = boto3.client('s3')

    # Baixar o arquivo do pedido
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    order_data = response['Body'].read().decode('utf-8')

    # Parse do JSON do pedido
    order = json.loads(order_data)
    customer_email = order['email']
    order_id = order['order_id']
    order_details = order['details']


    # Construir os detalhes em HTML
    item_rows = ""
    total_price = 0
    for item in order_details:
        item_rows += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #dddddd;">{item['name']}</td>
                <td style="padding: 8px; border: 1px solid #dddddd; text-align: right;">R$ {item['price']:.2f}</td>
            </tr>
        """
        total_price += item['price']

    # Agora o corpo do e-mail em HTML
    email_subject = f"Confirmação do Pedido #{order_id}"
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #4CAF50;">Pedido Recebido com Sucesso!</h2>
        <p>Olá,</p>
        <p>Seu pedido <strong>#{order_id}</strong> foi recebido com sucesso. Confira os detalhes abaixo:</p>

        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 8px; border: 1px solid #dddddd; text-align: left;">Produto</th>
                    <th style="padding: 8px; border: 1px solid #dddddd; text-align: right;">Preço</th>
                </tr>
            </thead>
            <tbody>
                {item_rows}
                <tr style="background-color: #f9f9f9;">
                    <td style="padding: 8px; border: 1px solid #dddddd; text-align: right;"><strong>Total:</strong></td>
                    <td style="padding: 8px; border: 1px solid #dddddd; text-align: right;"><strong>R$ {total_price:.2f}</strong></td>
                </tr>
            </tbody>
        </table>

        <p style="margin-top: 30px;">Agradecemos a sua compra! Em breve você receberá novas atualizações sobre o envio.</p>
        <p>Atenciosamente,<br><strong>Yuri Pierri Veiga - 22150750</strong><br><strong>Ednardo Luz - 22150551</strong><br><strong>Luisa Guimarães - 22150454</strong><br><strong>Marco Tonho - 22252445</strong><br><strong>Matheus Barcelos de Carvalho - 22350575</strong></p>
    </body>
    </html>
    """

    # Enviar e-mail usando SendGrid
    message = Mail(
        from_email=os.environ['SOURCE_EMAIL'],
        to_emails=customer_email,
        subject=email_subject,
        html_content=email_body
    )
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))  # Ajuste para imprimir a exceção corretamente

    return {
        'statusCode': 200,
        'body': json.dumps('E-mail de confirmação enviado com sucesso!')
    }
