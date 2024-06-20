import os

from flask import Flask, request, jsonify, send_file
from tasks import process_image

app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER='/data/uploads/',
    GENERATED_FOLDER='/data/generated/',
)


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    task = process_image.apply_async(args=[filename])
    return jsonify({'task_id': task.id}), 202


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_image.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state, 'progress': 0}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'progress': task.info.get('progress', 100)}
        if 'video_url' in task.info:
            response['video_url'] = task.info['video_url']
    else:
        response = {'state': task.state, 'progress': 0}

    return jsonify(response)


@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_file(os.path.join(app.config['GENERATED_FOLDER'], filename))


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
    app.run(port=8080, host="0.0.0.0", debug=False)
