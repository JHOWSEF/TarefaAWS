from flask import request
from flask_restx import Namespace, Resource, fields
from .services import s3_service, sqs_service
from .worker import process_message

api = Namespace('image', description='Operações com imagens')

# Modelo apenas para documentação do Swagger
upload_model = api.model('UploadModel', {
    'file': fields.String(description='Arquivo de imagem (.png)', required=True)
})


@api.route('/upload')
class Upload(Resource):
    @api.doc(consumes=['multipart/form-data'], params={
        'file': {'description': 'Arquivo de imagem (.png)', 'in': 'formData', 'type': 'file', 'required': True}
    })
    def post(self):
        if 'file' not in request.files:
            return {'message': 'Nenhum arquivo enviado'}, 400

        file = request.files['file']
        filename = file.filename

        if not filename:
            return {'message': 'Nome de arquivo inválido'}, 400

        try:
            s3_service.upload_file('image-input', filename, file)
            sqs_service.send_message(sqs_service.QUEUE_URL_INPUT, filename)

            return {'message': f'Arquivo {filename} enviado com sucesso'}, 200

        except Exception as e:
            return {'message': f'Erro ao processar o arquivo: {str(e)}'}, 500


@api.route('/healthcheck')
class Health(Resource):
    def get(self):
        return {'status': 'ok'}, 200


@api.route('/process')
class Process(Resource):
    def post(self):
        try:
            process_message()
            return {'message': 'Processamento executado com sucesso'}, 200
        except Exception as e:
            return {'message': f'Erro no processamento: {str(e)}'}, 500
