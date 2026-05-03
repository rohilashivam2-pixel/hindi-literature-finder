# 📚 Hindi Literature Finder

A Streamlit web app powered by Claude AI that discovers the top 10 Hindi literature books in any genre.

## Features

✨ **Real-time LLM-Powered Search** - Uses Claude AI to fetch current and accurate book information
📖 **All Genres Supported** - Novel, Poetry, Short Story, Drama, Essay, Autobiography, and more
📝 **Rich Descriptions** - Get detailed information about each book
🎨 **Beautiful UI** - Purple gradient cards with smooth animations
🔄 **Dynamic Content** - Generates responses based on user input

## Prerequisites

- Python 3.8+
- Anthropic API Key (get from [console.anthropic.com](https://console.anthropic.com))

## Installation

1. Clone the repository:
```bash
git clone git@github.com:rohilashivam2-pixel/hindi-literature-finder.git
cd hindi-literature-finder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Enter your Anthropic API Key in the sidebar

4. Enter a Hindi literature genre (e.g., "Novel", "Poetry", "Drama", etc.)

5. Click "Search Books" to get recommendations

## How It Works

1. User inputs a genre
2. The app sends a prompt to Claude API
3. Claude returns top 10 books with details
4. Results are displayed in two formats:
   - Raw LLM response (for accuracy verification)
   - Formatted cards (for better readability)

## Supported Genres

- Novel (Upanyas)
- Poetry (Kavita)
- Short Story (Laghu Katha)
- Drama (Natya/Natak)
- Essay (Nibandh)
- Autobiography (Atmakahani)
- Science Fiction
- Historical Fiction
- Romance
- Mystery
- Children's Literature

## API Key Setup

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Generate an API key
4. Copy and paste it in the Streamlit sidebar

## Technology Stack

- **Frontend**: Streamlit
- **AI**: Claude 3.5 Sonnet (Anthropic)
- **Language**: Python

## License

MIT
