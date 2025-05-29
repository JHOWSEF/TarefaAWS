from flask import request
from flask_restx import Namespace, Resource
from .services import s3_service, sqs_service

ns = Namespace('image', description='Operações com imagens')

@ns.route('/upload')
class Upload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']
        filename = file.filename

        s3_service.upload_file('image-input', filename, file)
        sqs_service.send_message(sqs_service.QUEUE_URL_INPUT, filename)

        return {'message': f'{filename} uploaded successfully'}, 200

@ns.route('/healthcheck')
class Health(Resource):
    def get(self):
        return {'status': 'ok'}, 200

@ns.route('/process')
class Process(Resource):
    def post(self):
        from .worker import process_message
        process_message()
        return {'message': 'Worker executed'}, 200
