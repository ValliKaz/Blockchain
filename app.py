import streamlit as st

# Set page config first
st.set_page_config(
    page_title="Kazakhstan Constitution AI Assistant",
    page_icon="📚",
    layout="wide"
)

import os
from utils import DocumentProcessor
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize model and tokenizer
@st.cache_resource
def load_model():
    model_name = "facebook/opt-350m"  # Smaller model for local use
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Create pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )
    return pipe

# Load the model
try:
    chat = load_model()
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

def get_chat_response(prompt: str, chat_history: List[Dict[str, str]]) -> str:
    try:
        system_message = """You are an AI assistant specialized in the Constitution of the Republic of Kazakhstan. 
        Provide accurate and helpful information based on the constitution. 
        If you're unsure about something, acknowledge the limitation and suggest consulting the official document.
        Please provide responses in the same language as the question."""
        
        # Format the prompt with system message
        formatted_prompt = f"{system_message}\n\nUser: {prompt}\n\nAssistant:"
        
        # Generate response
        response = chat(formatted_prompt, max_length=512, num_return_sequences=1)[0]['generated_text']
        
        # Extract only the assistant's response
        response = response.split("Assistant:")[-1].strip()
        return response
    except Exception as e:
        error_message = str(e)
        return f"An error occurred: {error_message}. Please try again later."

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'processor' not in st.session_state:
    st.session_state.processor = DocumentProcessor()

# Title and description
st.title("🇰🇿 Kazakhstan Constitution AI Assistant")
st.markdown("""
This AI assistant can help you understand the Constitution of the Republic of Kazakhstan.
Upload PDF documents and ask questions about their content.
""")

# File upload section
st.header("📄 Upload Documents")
uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=['pdf'],
    accept_multiple_files=True
)

if uploaded_files:
    # Create a temporary directory for uploaded files
    os.makedirs("temp", exist_ok=True)
    
    # Save uploaded files
    file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join("temp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        file_paths.append(file_path)
    
    # Process documents
    with st.spinner("Processing documents..."):
        st.session_state.processor.process_documents(file_paths)
    st.success("Documents processed successfully!")

# Chat interface
st.header("💬 Chat with the Constitution")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the Constitution"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get relevant document chunks
    relevant_chunks = st.session_state.processor.query_documents(prompt)
    
    # Create context from relevant chunks
    context = "\n\n".join(relevant_chunks)
    
    # Create system message with context
    system_message = f"""You are an AI assistant specialized in the Constitution of the Republic of Kazakhstan.
    Use the following context to answer the user's question. If the answer cannot be found in the context,
    say so and provide a general response based on your knowledge.
    
    Context:
    {context}
    """
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_chat_response(prompt, st.session_state.messages)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})