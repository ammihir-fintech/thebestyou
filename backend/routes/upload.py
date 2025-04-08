import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import base64
import openai
upload_bp = Blueprint("upload", __name__)
import json
from dotenv import load_dotenv
load_dotenv()
# Set the folder where uploaded files will be saved
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


api_key = os.getenv('API_KEY')
client = openai.OpenAI(api_key=api_key)

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def encode_image(image_path):
    """Encodes an image to base64 format for API input."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def get_profile_analysis(prompt=None, image_paths=None):
    """Sends either text or image input to OpenAI's API and returns a response."""
    messages = [{
        "role": "system",
        "content": "Here is my dating profile, including text and photos. Analyze the following aspects and provide the output in JSON format: "
                   "1. Vibe: What vibe am I coming across as based on my profile text and photos? "
                   "2. Target Audience: What type of person am I likely attracting with this profile? "
                   "3. Overall Score: Rate my profile on a scale of 1-10. "
                   "4. Photo Score: Rate my photos on a scale of 1-10 (consider factors like lighting, composition, and authenticity). "
                   "5. Prompt Quality: Rate the quality of my profile text/prompts on a scale of 1-10. "
                   "6. Improvement Suggestions: Provide specific suggestions to improve my profile text and photos. For the photos, focus on aspects like lighting, composition, background, and authenticity. "
                   "7. Bio Score: Rate my bio on a scale of 1-10. "
                   "Return the output in the following JSON format: "
                   "{ "
                   "  'vibe': 'Your vibe based on text and photos', "
                   "  'target_audience': 'Type of person you're likely attracting', "
                   "  'overall_score': X, "
                   "  'photo_score': X, "
                   "  'prompt_quality': X, "
                   "  'improvement_suggestions': { "
                   "    'text': 'Suggestions for improving your profile text', "
                   "    'photos': 'Specific suggestions for improving your photos, focusing on lighting, composition, background, and authenticity' "
                   "  } "
                   "}"}]

    if prompt:
        messages.append({"role": "user", "content": prompt})

    if image_paths:
        for image_path in image_paths:
            base64_image = encode_image(image_path)
            if base64_image:
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "This is one of the images from my dating profile."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                })
            else:
                return "Error: Failed to encode image."

    try:
        response = client.chat.completions.create(
            model="gpt-4.5-preview-2025-02-27",  # Use the correct model for image analysis
            messages=messages,
            max_tokens=500  # Adjust as needed
        )
        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        return f"API Error: {str(e)}"


@upload_bp.route("/image", methods=["POST"])
def upload_photo():
    print("Received upload request")
    print("Request files:", request.files)
    
    try:
        if "files" not in request.files:
            print("No 'files' in request.files. Keys found:", request.files.keys())
            return jsonify({"error": "No files part"}), 400

        files = request.files.getlist("files")
        print(f"Number of files received: {len(files)}")
        
        if not files:
            return jsonify({"error": "No selected files"}), 400

        uploaded_files = []
        for file in files:
            print(f"Processing file: {file.filename}")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    file.save(file_path)
                    uploaded_files.append({
                        "filename": filename,
                        "path": file_path
                    })
                    print(f"Successfully saved file: {filename} to {file_path}")
                except Exception as e:
                    print(f"Error saving file {filename}: {str(e)}")
                    return jsonify({"error": f"Failed to save file {filename}: {str(e)}"}), 500

        if not uploaded_files:
            return jsonify({"error": "No valid files uploaded"}), 400

        print(f"Successfully uploaded {len(uploaded_files)} files")

        image_paths = [file['path'] for file in uploaded_files]
        #analysis_result = chatbot(image_paths=image_paths)
        analysis_result = get_profile_analysis(image_paths=image_paths)
        #print(type(analysis_result))
        analysis_result_dict = json.loads(analysis_result)
        analysis_result_json = json.dumps(analysis_result_dict)
        print(type(analysis_result_json))
        print(f"Image Analysis Response: {analysis_result_json}")
        print(f"**********END*********")

        return jsonify({
            "message": f"Successfully uploaded {len(uploaded_files)} files", 
            "files": uploaded_files,
            "analysis_result": analysis_result_json
        }), 201
        
    except Exception as e:
        print(f"Unexpected error in upload_photo: {str(e)}")
        return jsonify({"error": str(e)}), 500
