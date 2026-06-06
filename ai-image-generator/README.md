# AI Image Generator

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red?logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E%203-orange?logo=openai)
![License](https://img.shields.io/badge/License-MIT-yellow)

A powerful AI image generation tool built with Streamlit and OpenAI's DALL-E 3. Create stunning images from text descriptions with an intuitive web interface.

## Features

- Text-to-image generation using DALL-E 3
- Multiple image size options (1024x1024, 1024x1792, 1792x1024)
- Quality selection (standard / HD)
- Image download functionality
- Generation history with expandable previews
- Clean, responsive Streamlit interface
- Input validation and error handling

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Backend language |
| Streamlit | Web interface framework |
| OpenAI DALL-E 3 | Image generation API |
| Pillow | Image processing |
| Requests | HTTP image downloads |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/ai-image-generator.git
cd ai-image-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter a descriptive prompt in the text area
2. Select your desired image size and quality
3. Click "Generate Image"
4. View the generated image and download if desired
5. Browse previous generations in the history section

## Project Structure

```
ai-image-generator/
├── app.py              # Streamlit main application
├── generator.py        # ImageGenerator class
├── config.py           # Configuration management
├── utils.py            # Utility functions
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Screenshots

> Screenshots will be added after deployment.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is part of my development portfolio.
