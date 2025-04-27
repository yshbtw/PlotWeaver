CUSTOM_CSS = """
    <style>
    /* Dark theme colors */
    :root {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #b3b3b3;
        --accent: #4f39fa;
        --accent-hover: #6d5cfb;
        --border: #404040;
    }

    /* Main container styling */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background: linear-gradient(to bottom, var(--bg-primary) 0%, #151515 100%);
        color: var(--text-primary);
    }

    /* Header styling */
    .main-header {
        text-align: center;
        color: var(--accent);
        padding: 2rem 0;
        background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }

    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 0 0 10px rgba(79, 57, 250, 0.3);
    }

    .sub-header {
        font-size: 1.2rem;
        color: var(--text-secondary);
        text-align: center;
        margin: 1rem 0 2rem;
        font-weight: 300;
    }

    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
        color: white;
        padding: 0.75rem 0;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(79, 57, 250, 0.4);
    }

    /* Story container styling */
    .story-container {
        background-color: var(--bg-secondary);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        color: var(--text-primary);
    }

    .story-container:hover {
        box-shadow: 0 4px 12px rgba(79, 57, 250, 0.2);
        border-color: var(--accent);
    }

    /* Input fields styling */
    .stTextArea>div>div {
        border-radius: 8px;
        border-color: var(--border);
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        transition: all 0.3s ease;
    }

    .stTextArea>div>div:focus-within {
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent);
    }

    /* Slider styling */
    .stSlider>div>div>div {
        background-color: var(--accent);
    }

    /* Tab styling */
    .stTabs>div>div {
        gap: 1rem;
    }

    .stTabs>div>div>button {
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        font-weight: 500;
        color: var(--text-secondary);
        background-color: var(--bg-secondary);
    }

    .stTabs>div>div>button:hover {
        background-color: rgba(79, 57, 250, 0.1);
        color: var(--text-primary);
    }

    .stTabs>div>div>button[data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--accent);
        color: white;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: var(--bg-secondary);
        border: 1px solid var(--border);
        padding: 1rem;
        font-weight: 500;
        color: var(--text-primary);
    }

    .streamlit-expanderHeader:hover {
        background-color: #333333;
        border-color: var(--accent);
    }

    /* Spinner styling */
    .stSpinner>div {
        border-color: var(--accent);
    }

    /* Warning message styling */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
    }

    /* Select box styling */
    .stSelectbox>div>div {
        background-color: var(--bg-secondary);
        border-color: var(--border);
        color: var(--text-primary);
    }

    .stSelectbox>div>div:hover {
        border-color: var(--accent);
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent);
    }
    </style>
"""