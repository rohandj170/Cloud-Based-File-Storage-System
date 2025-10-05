from flask import Flask, request
import boto3
import os

app = Flask(__name__)

# Configure AWS S3
S3_BUCKET_NAME = "cloud170"
S3_REGION = "ap-southeast-2"
s3 = boto3.client("s3", region_name=S3_REGION)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file:
            try:
                s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
                return 'File uploaded successfully!'
            except Exception as e:
                return f'Error uploading file: {e}'

    # HTML upload form
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
    .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }

        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .upload-area {
 border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9ff;
        }

        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f2ff;
        }

        .upload-area.dragover {
            border-color: #764ba2;
            background: #e8ebff;
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 50px;
            margin-bottom: 15px;
        }

        .upload-text {
            color: #667eea;
            font-size: 18px;
            font-weight: 600;
 margin-bottom: 5px;
        }

        .upload-hint {
            color: #999;
            font-size: 14px;
        }

        #fileInput {
            display: none;
        }

        .upload-btn {
            margin-top: 20px;
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
  .upload-btn:hover {
            transform: translateY(-2px);
        }

        .upload-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .selected-file {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9ff;
            border-radius: 10px;
            display: none;
        }

        .selected-file.show {
            display: block;
        }

        .file-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .file-icon {
            font-size: 30px;
        }

        .file-details {
            flex: 1;
        }

        .file-name {
            color: #333;
            font-weight: 600;
            word-break: break-all;
            margin-bottom: 5px;
        }

        .file-size {
            color: #999;
            font-size: 14px;
        }
 .status-message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            display: none;
        }

        .status-message.show {
            display: block;
        }

        .status-message.success {
            background: #d4edda;
            color: #155724;
        }

        .status-message.error {
            background: #f8d7da;
            color: #721c24;
        }

        .status-message.loading {
            background: #d1ecf1;
            color: #0c5460;
        }
    </style>
</head>
<body>
<div class="container">
        <h1>📁 File Upload</h1>
        <p class="subtitle">Choose a file to upload</p>

        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">☁️</div>
            <div class="upload-text">Click to select file</div>
            <div class="upload-hint">or drag and drop here</div>
        </div>

        <input type="file" id="fileInput">

        <div class="selected-file" id="selectedFile">
            <div class="file-info">
                <div class="file-icon" id="fileIcon">📎</div>
 <div class="file-details">
                    <div class="file-name" id="fileName">No file selected</div>
                    <div class="file-size" id="fileSize">0 KB</div>
                </div>
            </div>
        </div>

        <button class="upload-btn" id="uploadBtn" disabled>Upload File</button>

        <div class="status-message" id="statusMessage"></div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const selectedFileDiv = document.getElementById('selectedFile');
        const uploadBtn = document.getElementById('uploadBtn');
        const statusMessage = document.getElementById('statusMessage');
        let selectedFile = null;

        // Click to select file
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // File input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                handleFile(e.dataTransfer.files[0]);
            }
        });

        function handleFile(file) {
            selectedFile = file;
            displayFileInfo(file);
 uploadBtn.disabled = false;
            hideStatus();
        }

        function displayFileInfo(file) {
            const fileIcon = getFileIcon(file.name);
            const fileSize = formatFileSize(file.size);

            document.getElementById('fileIcon').textContent = fileIcon;
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('fileSize').textContent = fileSize;
            selectedFileDiv.classList.add('show');
        }

        function getFileIcon(filename) {
            const ext = filename.split('.').pop().toLowerCase();
            const iconMap = {
                'pdf': '📄',
                'doc': '📝',
                'docx': '📝',
                'txt': '📝',
                'jpg': '🖼️',
                'jpeg': '🖼️',
                'png': '🖼️',
                'gif': '🖼️',
                'mp4': '🎬',
                'mp3': '🎵',
                'zip': '📦',
                'rar': '📦'
            };
            return iconMap[ext] || '📎';
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
        }

        function showStatus(message, type) {
            statusMessage.textContent = message;
            statusMessage.className = 'status-message show ' + type;
        }

        function hideStatus() {
            statusMessage.className = 'status-message';
        }

        // Upload button click - Connect this to your backend
 uploadBtn.addEventListener('click', async () => {
            if (!selectedFile) return;

            const formData = new FormData();
            formData.append('file', selectedFile);

            uploadBtn.disabled = true;
            showStatus('Uploading...', 'loading');

            try {
                // Backend endpoint
                const response = await fetch('http://3.107.172.111:5000', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    showStatus('File uploaded successfully!', 'success');
                    // Reset after 2 seconds
                    setTimeout(() => {
                        resetForm();
                    }, 2000);
                } else {
                    showStatus('Upload failed. Please try again.', 'error');
                    uploadBtn.disabled = false;
                }
            } catch (error) {
                showStatus('Error: ' + error.message, 'error');
                uploadBtn.disabled = false;
            }
        });

        function resetForm() {
            selectedFile = null;
            fileInput.value = '';
            selectedFileDiv.classList.remove('show');
            uploadBtn.disabled = true;
            hideStatus();
        }
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



