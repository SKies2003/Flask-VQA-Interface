from flask import Flask, request, render_template, flash, redirect, url_for
from transformers import pipeline
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
import os
from result_handler import handle_vqa_result

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load the VQA pipeline
try:
    vqa_pipeline = pipeline("visual-question-answering")
except Exception as e:
    print("Error loading the VQA pipeline:", e)
    vqa_pipeline = None

os.makedirs('static', exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vqa', methods=['POST'])
def vqa():
    print("Received a VQA request")  # Debug

    if 'image' not in request.files or 'question' not in request.form:
        print("Missing image or question")  # Debug
        flash("Please upload an image and provide a question.")
        return redirect(url_for('index'))

    image_file = request.files['image']
    question = request.form['question']

    print(f"Image filename: {image_file.filename}")  # Debug
    print(f"Question: {question}")  # Debug

    if not image_file or not allowed_file(image_file.filename):
        print("Invalid file type")  # Debug
        flash("Invalid file type. Please upload a valid image.")
        return redirect(url_for('index'))

    filename = secure_filename(image_file.filename)
    image_path = os.path.join('static', filename)
    image_file.save(image_path)
    print(f"Saved image at: {image_path}")  # Debug

    try:
        image = Image.open(image_path).convert("RGB")
    except UnidentifiedImageError:
        print("Image could not be identified")  # Debug
        flash("The uploaded file is not a valid image.")
        os.remove(image_path)
        return redirect(url_for('index'))

    if vqa_pipeline:
        try:
            print("Calling VQA pipeline...")  # Debug
            result = vqa_pipeline(image, question, top_k=1)[0]
            print(f"VQA Result: {result}")  # Debug

            answer = result['answer']
            confidence = result['score']

            extra_info, extra_facts, source_url, info_videos, fact_videos = handle_vqa_result(answer)
        except Exception as e:
            print(f"Error during VQA processing: {e}")  # Debug
            flash(f"Error processing the image: {e}")
            return redirect(url_for('index'))
    else:
        print("VQA pipeline is not available")  # Debug
        flash("VQA pipeline is not available.")
        return redirect(url_for('index'))

    return render_template(
        'result.html',
        image_url=image_path,
        question=question,
        answer=answer,
        confidence=confidence,
        extra_info=extra_info,
        extra_facts=extra_facts,
        source_url=source_url,
        info_videos=info_videos,
        fact_videos=fact_videos
    )


if __name__ == '__main__':
    app.run(debug=True)
