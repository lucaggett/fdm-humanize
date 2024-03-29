import logging
import os
import flask

try:
    from fdm_humanize.humanize import analyse_file
except ImportError:
    from humanize import analyse_file


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# DEBUGGING:
# Print the current working directory

# print the contents of the current directory and subdirectories
def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "./uploaded_files"
    app.config["EXTRACTED_FOLDER"] = "./extracted"

    @app.route("/")
    def index():
        return flask.render_template("index.html")

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
                file.save(os.path.join('./uploaded_files', file.filename))
            except FileNotFoundError:
                return 'The uploaded file could not be saved'
            else:
                # redirect to files/<filename> to display the file
                return flask.redirect(flask.url_for('show_file_analysis', filename=file.filename))

    @app.route('/files')
    def list_files():
        files = os.listdir('./uploaded_files')
        return flask.render_template('list_files.html', files=files)

    @app.route('/files/<filename>')
    def show_file_analysis(filename):
        # perform analysis on file
        faults, msgs, ne, summary = analyse_file(filename)
        print(summary)
        return flask.render_template('file_analysis.html', filename=filename, faulty_parts=faults, num_errors=ne,
                                     messages=msgs, summary=summary)

    return app

if __name__ == '__main__':
    create_app().run()
