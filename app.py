
import os
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FULL_NAME = os.getenv("FULL_NAME", "Farzaliyev Bulud")
GROUP_NAME = os.getenv("GROUP_NAME", "Computer engineering")

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Student Document Upload</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f4f8;
            padding: 40px 15px;
        }
        .card {
            max-width: 500px;
            margin: auto;
            padding: 30px;
            background: white;
            border-radius: 12px;
        }
        h1 {
            color: #1769aa;
        }
        .info {
            background: #eaf4ff;
            padding: 15px;
            line-height: 2;
            border-radius: 8px;
        }
        input, button {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            margin-top: 15px;
        }
        button {
            background: #1769aa;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Student Document Upload</h1>

        <div class="info">
            <b>Full Name:</b> {{ full_name }}<br>
            <b>Group:</b> {{ group_name }}
        </div>

        <h3>Upload your document</h3>
        <p>Allowed files: PDF, DOC, DOCX, TXT (maximum 10 MB).</p>

        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="document"
                   accept=".pdf,.doc,.docx,.txt" required>
            <button type="submit">Upload Document</button>
        </form>

        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        file = request.files.get("document")

        if not file or not file.filename:
            message = "Please select a file."
        else:
            filename = secure_filename(file.filename)
            extension = (
                filename.rsplit(".", 1)[-1].lower()
                if "." in filename else ""
            )

            if not filename or extension not in ALLOWED_EXTENSIONS:
                message = "File type not allowed."
            else:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                message = f"Successfully uploaded: {filename}"

    return render_template_string(
        HTML,
        full_name=FULL_NAME,
        group_name=GROUP_NAME,
        message=message
    )


@app.errorhandler(413)
def file_too_large(error):
    return "File is too large. Maximum size is 10 MB.", 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
