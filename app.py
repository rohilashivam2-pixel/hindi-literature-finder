import streamlit as st
import anthropic
import json
import re

# Page configuration
st.set_page_config(
    page_title="Hindi Literature Finder",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .book-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .book-rank {
        display: inline-block;
        background: rgba(255, 255, 255, 0.3);
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        margin-right: 10px;
    }
    .book-title {
        font-size: 1.3em;
        font-weight: bold;
        margin: 10px 0 5px 0;
    }
    .book-author {
        font-size: 1.1em;
        opacity: 0.9;
        margin: 5px 0;
    }
    .book-year {
        font-size: 0.9em;
        opacity: 0.8;
        margin: 5px 0;
    }
    .book-description {
        font-size: 0.95em;
        margin-top: 10px;
        line-height: 1.5;
    }
    .header-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "books_data" not in st.session_state:
    st.session_state.books_data = None
if "genre" not in st.session_state:
    st.session_state.genre = None

# Sidebar
st.sidebar.title("⚙️ Configuration")
api_key = st.secrets.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("❌ API key not configured. Please contact the app owner.")
    st.stop()

if api_key:
    st.session_state.api_key = api_key

st.sidebar.markdown("---")
st.sidebar.markdown("""
    ### About This App
    Discover top 10 Hindi literature books.
    
    **How to use:**
    1. Select or type a genre
    2. Click "Search Books"
    3. Explore the recommendations
""")

# Main content
st.markdown("""
    <div class="header-gradient">
        <h1>📚 Hindi Literature Finder</h1>
        <p>Discover Top 10 Books in Any Genre</p>
    </div>
""", unsafe_allow_html=True)

# Genre input
col1, col2 = st.columns([3, 1])

with col1:
    genre = st.text_input(
        "Enter a Hindi Literature Genre",
        placeholder="e.g., Novel, Poetry, Short Story, Drama, Essay, etc."
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# Parse LLM response
def parse_books_response(response_text):
    books = []
    lines = response_text.split('\n')
    current_book = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_book:
                books.append(current_book)
                current_book = {}
            continue
        
        if re.match(r'^\d+\.', line):
            if current_book:
                books.append(current_book)
            title = re.sub(r'^\d+\.\s*', '', line)
            current_book = {'title': title, 'description': ''}
        elif ':' in line and current_book:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if 'author' in key:
                current_book['author'] = value
            elif 'year' in key or 'published' in key:
                current_book['year'] = value
            elif 'description' in key or 'summary' in key:
                current_book['description'] = value
        elif current_book:
            current_book['description'] += ' ' + line
    
    if current_book:
        books.append(current_book)
    
    return books[:10]

# Call API
def get_books(genre: str, api_key: str):
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""You are an expert in Hindi literature. Provide the top 10 books in the "{genre}" genre of Hindi literature.

For each book, provide:
1. Book Title
   Author: [Author Name]
   Year: [Publication Year]
   Description: [2-3 line description]

Make sure to:
- Include only authentic Hindi literature books
- Provide accurate author names and publication years
- Give meaningful descriptions
- Order by importance/popularity"""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

# Search logic
if search_button:
    if not api_key:
        st.error("❌ Please enter your API Key")
    elif not genre.strip():
        st.error("❌ Please enter a genre")
    else:
        try:
            with st.spinner("Searching..."):
                response = get_books(genre, api_key)
                st.session_state.books_data = response
        except anthropic.APIError as e:
            st.error(f"❌ API Error: {str(e)}")

# Display results
if st.session_state.books_data:
    st.markdown("---")
    st.markdown(f"## 📖 Top 10 Books - **{genre}**")
    
    st.info("**Results:**")
    st.markdown(st.session_state.books_data)
    
    st.markdown("---")
    with st.expander("View as Cards", expanded=True):
        books = parse_books_response(st.session_state.books_data)
        
        for idx, book in enumerate(books, 1):
            title = book.get('title', 'Unknown').strip()
            author = book.get('author', 'Unknown').strip()
            year = book.get('year', 'N/A').strip()
            description = book.get('description', '').strip()
            
            st.markdown(f"""
                <div class="book-card">
                    <span class="book-rank">#{idx}</span>
                    <div class="book-title">{title}</div>
                    <div class="book-author">✍️ {author}</div>
                    <div class="book-year">📅 {year}</div>
                    <div class="book-description">{description}</div>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Hindi Literature Finder</p>", unsafe_allow_html=True)
