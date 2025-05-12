# 🇰🇿 Kazakhstan Constitution AI Assistant

An intelligent assistant that helps users understand and navigate the Constitution of the Republic of Kazakhstan. The application uses natural language processing to answer questions about the constitution and provides relevant context from the document.

## 🌟 Features

- **Document Processing**: Upload and process PDF documents of the Constitution
- **Intelligent Chat**: Ask questions in natural language about the Constitution
- **Context-Aware Responses**: Get answers with relevant citations and context
- **Multi-language Support**: Ask questions in different languages
- **Local Processing**: Runs entirely on your machine, no API keys required

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Language Model**: Facebook OPT-350M (local)
- **Document Processing**: PyPDF, ChromaDB
- **Vector Store**: ChromaDB for document embeddings
- **Dependencies**: See requirements.txt

## 📋 Prerequisites

- Python 3.8 or higher
- 4GB+ RAM recommended
- 1GB+ free disk space

## 🚀 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided URL (usually http://localhost:8501)

3. Upload PDF documents of the Constitution

4. Start asking questions about the Constitution

## 📁 Project Structure

```
.
├── app.py              # Main application file
├── utils.py           # Utility functions and document processing
├── requirements.txt   # Project dependencies
├── .env              # Environment variables (create from .env.example)
├── temp/             # Temporary storage for uploaded files
└── chroma_db/        # Vector store database
```

## 🔧 Configuration

The application uses a local language model and doesn't require API keys. However, you can configure various parameters in the code:

- Model parameters (temperature, max_length, etc.)
- Document chunking settings
- Vector store configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit for the web framework
- Hugging Face for the language model
- ChromaDB for vector storage
- PyPDF for PDF processing

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.

## 🔄 Updates

- Latest update: [Current Date]
- Version: 1.0.0
- Changes: Initial release 