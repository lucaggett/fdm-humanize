import logging
import os
import flask

try:
    from .humanize import analyse_file
except ImportError:
    from humanize import analyse_file

app = flask.Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/upload', methods=['POST'])
def upload_file():
    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            return 'No file part in the request'
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        # save the file to the desired location
        # generate the filename based on the current time
        try:
            file.save(os.path.join('uploaded_files', file.filename))
        except FileNotFoundError:
            return 'The uploaded file could not be saved'
        else:
            # redirect to files/<filename> to display the file
            return flask.redirect(flask.url_for('show_file_analysis', filename=file.filename))



@app.route('/files')
def list_files():
    files = os.listdir('uploaded_files')
    return flask.render_template('list_files.html', files=files)

@app.route('/files/<filename>')
def show_file_analysis(filename):
    # perform analysis on file
    faults, msgs, ne = analyse_file(filename)
    return flask.render_template('file_analysis.html', filename=filename, faulty_parts=faults, num_errors=ne, messages=msgs)



@app.route('/')
def main_page():
    return flask.render_template('main_page.html')


if __name__ == '__main__':
    app.run()
