from flask import request
from flask_restx import Namespace, Resource
from .services import s3_service, sqs_service
from .worker import process_message

api = Namespace('image', description='Operações com imagens')

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'file',
    location='files',
    type='FileStorage',
    required=True,
    help='Arquivo de imagem (.png)'
)

@api.route('/upload')
class Upload(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']
        filename = file.filename

        if not filename:
            return {'message': 'No file selected'}, 400

        s3_service.upload_file('image-input', filename, file)
        sqs_service.send_message(sqs_service.QUEUE_URL_INPUT, filename)

        return {'message': f'{filename} uploaded successfully'}, 200

@api.route('/healthcheck')
class Health(Resource):
    def get(self):
        return {'status': 'ok'}, 200

@api.route('/process')
class Process(Resource):
    def post(self):
        from .worker import process_message
        process_message()
        return {'message': 'Worker executed'}, 200
