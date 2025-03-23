# Flask-VQA-Interface (Version 2)

A web-based Visual Question Answering (VQA) interface built using Flask. This project allows users to upload an image, ask a question about its content, and receive an AI-generated answer along with a confidence score. Version 2 enhances the result display with additional information sourced from Wikipedia, fact websites, and YouTube videos for a more interactive and informative user experience.

## Features:
- **Image Upload:** Users can upload any image in standard formats (e.g., JPEG, PNG, GIF).
- **Question Submission:** Users can ask a question about the uploaded image through a simple interface.
- **AI-Powered Answers:** Utilizes a pre-trained Visual Question Answering model from the Hugging Face Transformers library.
- **Confidence Score:** Displays a confidence score showing the model's certainty.
- **Enhanced Results Display (New in v2):**
    - **Wikipedia Info:** Shows summarized content about the answer.
    - **Interesting Facts:** Extracts 4-5 facts from reliable fact websites.
    - **Video Embeds:** Embeds relevant YouTube videos (educational/documentary style).
    - **Source Links:** Provides links to the sources for further exploration.
- **User-Friendly Interface:** Clean and responsive interface with enhanced styling in result display (new result.html and result.css).

## Getting Started:
Clone the repository, install the required dependencies, and run the Flask app locally to start using the VQA interface.

## Dependencies:
- Flask
- Transformers
- Pillow
- requests
- BeautifulSoup4

## Usage:
1. Upload an image.
2. Ask a question related to the image.
3. Receive an answer and confidence score from the model.

## Installation:
```bash
git clone https://github.com/yourusername/VQA-Insight.git
cd VQA-Insight
python app.py
