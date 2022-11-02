import base64
import boto3
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from textwrap import wrap
from datetime import datetime

def lambdaFunction(json):

    image = base64.b64decode(json['base64_image'])
    page = Canvas("report.pdf", pagesize=A4)

    body = json['body']
    pdf_image = ImageReader(io.BytesIO(image))

    page.drawString(30, 800,'Fecha: ' + str(datetime.now()).split('.')[0])
    page.drawString(220, 800,'Reporte de Emergencia')
    page.drawString(100, 750,'ID: ' + str(body['id']))
    page.drawString(100, 730,'Location: ' + body['location'])
    page.drawString(100, 710,'Type: ' + body['type'])
    page.drawString(340, 750,'Latitud: ' + str(body['lat']))
    page.drawString(340, 730,'Longitud: ' + str(body['lon']))
    page.drawString(340, 710,'Level: ' + str(body['level']))
    page.drawString(100, 690,'Message: ')
    
    msg = page.beginText()
    msg.setTextOrigin(155, 690)
    wraped_text = "\n".join(wrap( body['message'], 80))
    msg.textLines(wraped_text)
    page.drawText(msg)

    page.drawImage(pdf_image, 50, 300)

    page.save()

    client = boto3.client("s3",
        aws_access_key_id='AKIAUNIYQCLUG3BNRNOA',
        aws_secret_access_key= '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'
    )
    client.upload_file('report.pdf', "smartinformes", 'emergencie_report_ID-'+str(body['id'])+'.pdf', ExtraArgs={'ACL':'public-read'})
    return 'https://smartinformes.s3.amazonaws.com/'+'emergencie_report_ID-'+str(body['id'])+'.pdf'
