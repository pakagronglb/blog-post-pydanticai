# Blog Post Summarizer | Pydantic AI

A powerful application that uses AI to automatically summarize blog posts and articles. This tool helps users quickly extract key information from lengthy content, saving time while maintaining comprehension of essential points.

## Features

- **Automated Summarization**: Convert long-form content into concise, readable summaries
- **Pydantic AI Integration**: Leverages Pydantic AI for structured data extraction and processing
- **Customizable Summary Length**: Adjust the level of detail in your summaries
- **User-Friendly Interface**: Simple and intuitive design for ease of use
- **Fast Processing**: Quick turnaround times for content analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/pakagronglb/blog-post-pydanticai.git
cd blog-post-pydanticai

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python app.py
```

## Project Structure

```
blog-post-summarizer/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── utils.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Dependencies

- Python 3.8+
- PydanticAI
- FastAPI/Flask
- Other dependencies listed in requirements.txt

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys and configuration settings

```
API_KEY=your_api_key_here
MODEL_NAME=gpt-4
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project was inspired by and follows the tutorial from [Jie Jenn](https://youtu.be/Ix_nt4Fi3ls)
- Thanks to the PydanticAI team for their excellent library
- All contributors who have helped improve this project

## Contact

Pakagrong Lebel - [@pakagronglb](https://twitter.com/pakagronglb) - pakagronglebel@gmail.com

Project Link: [https://github.com/pakagronglb/blog-post-summarizer](https://github.com/pakagronglb/blog-post-pydanticai)
