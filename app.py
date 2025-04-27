import streamlit as st
import requests
import os
from dotenv import load_dotenv
from image_search import fetch_google_images, download_images
import time

# Load environment variables
load_dotenv()

# Must be the first Streamlit command
st.set_page_config(
    page_title="PlotWeaver",
    layout="wide",
    page_icon="📚"
)

from story_generator import StoryGenerator
from styles import CUSTOM_CSS
from config import GENRE_TEMPLATES
from database import stories_collection
from auth import auth_ui

def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>📚PlotWeaver</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create unique stories with AI-powered creativity</p>', unsafe_allow_html=True)
    
    # Authentication UI
    is_authenticated = auth_ui()
    
    if is_authenticated:
        try:
            generator = StoryGenerator()
            
            tab1, tab2, tab3 = st.tabs(["📝 Story Generator", "📚 History", "ℹ️ Guide"])
            
            with tab1:
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("### 📖 Your Story Prompt")
                    prompt = st.text_area(
                        "",
                        placeholder="Let your imagination flow...",
                        height=150
                    )
                    
                    # Create three columns for the buttons
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    
                    with btn_col1:
                        generate_story = st.button("✨ Generate Story", use_container_width=True)
                    
                    with btn_col2:
                        generate_image = st.button("🎨 Generate Image", use_container_width=True)
                        
                    with btn_col3:
                        search_images = st.button("🔍 Search Images", use_container_width=True)
                
                with col2:
                    st.markdown("### ⚙️ Story Settings")
                    genre = st.selectbox(
                        "Select Genre",
                        ["None"] + list(GENRE_TEMPLATES.keys()),
                        format_func=lambda x: f" {x}" if x != "None" else "Choose a genre..."
                    )
                    
                    max_length = st.slider(
                        "Story Length",
                        min_value=100,
                        max_value=1000,
                        value=500,
                        help="Adjust the length of your story"
                    )
                    
                    temperature = st.slider(
                        "Creativity Level",
                        min_value=0.1,
                        max_value=1.0,
                        value=0.8,
                        step=0.1,
                        help="Higher values make the output more creative but less focused"
                    )
                
                if prompt:
                    if generate_story:
                        with st.spinner("🌟 Crafting your story..."):
                            genre = None if genre == "None" else genre
                            story = generator.generate_story(
                                prompt,
                                genre=genre,
                                max_length=max_length,
                                temperature=temperature
                            )
                            generator.save_story(prompt, genre, story, max_length, temperature)
                            
                            st.markdown("### 📜 Your Generated Story")
                            st.markdown('<div class="story-container">', unsafe_allow_html=True)
                            st.write(story)
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    if generate_image:
                        with st.spinner("🎨 Creating an image for your prompt..."):
                            try:
                                response = requests.post(
                                    f"https://api.stability.ai/v2beta/stable-image/generate/core",
                                    headers={
                                        "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
                                        "accept": "image/*"
                                    },
                                    files={"none": ""},
                                    data={
                                        "prompt": prompt,
                                        "output_format": "webp",
                                    }
                                )
                                
                                if response.status_code == 200:
                                    # Save the image to a temporary file
                                    temp_dir = "temp_images"
                                    if not os.path.exists(temp_dir):
                                        os.makedirs(temp_dir)
                                    
                                    image_path = os.path.join(temp_dir, f"generated_image_{int(time.time())}.webp")
                                    with open(image_path, 'wb') as file:
                                        file.write(response.content)
                                    
                                    # Display the saved image
                                    st.markdown("### 🖼️ Generated Image")
                                    st.image(image_path, caption="Generated Image from Your Prompt", use_column_width=True)
                                else:
                                    st.error(f"Failed to generate image: {response.json()}")
                            except Exception as e:
                                st.error(f"Error generating image: {str(e)}")
                    
                    if search_images:
                        with st.spinner("🔍 Searching for images..."):
                            image_urls = fetch_google_images(prompt)
                            if image_urls:
                                downloaded_paths = download_images(image_urls)
                                if downloaded_paths:
                                    st.markdown("### 🖼️ Found Images")
                                    cols = st.columns(2)
                                    for idx, img_path in enumerate(downloaded_paths):
                                        with cols[idx % 2]:
                                            st.image(img_path, caption=f"Image {idx + 1}", use_column_width=True)
                            else:
                                st.warning("No images found for your prompt.")
                else:
                    if generate_story or generate_image or search_images:
                        st.warning("🎯 Please enter a prompt first!")
            
            with tab2:
                st.markdown("### 📚 Story History")
                if stories_collection is not None:
                    stories = generator.get_story_history()
                    if stories:
                        for idx, story in enumerate(stories):
                            with st.expander(f"Story {idx + 1} - {story['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                                st.markdown("**Prompt:**")
                                st.write(story['prompt'])
                                st.markdown("**Genre:**")
                                st.write(story['genre'] if story['genre'] else "None")
                                st.markdown("**Settings:**")
                                st.write(f"Length: {story['max_length']}, Creativity: {story['temperature']}")
                                st.markdown("**Generated Story:**")
                                st.markdown('<div class="story-container">', unsafe_allow_html=True)
                                st.write(story['story'])
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                if st.button("🗑️ Delete Story", key=f"delete_{story['_id']}", use_container_width=True):
                                    if generator.delete_story(story['_id']):
                                        st.success("Story deleted successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete story. Please try again.")
                    else:
                        st.info("No stories in history yet. Generate your first story!")
                else:
                    st.warning("History feature is currently unavailable")
            
            with tab3:
                st.markdown("""
                ### 🎨 How to Get the Best Results
                
                1. **Start with a Clear Prompt**
                   - Be specific about characters, setting, and mood
                   - Include key details you want in the story
                
                2. **Choose the Right Genre**
                   - Each genre has its own unique template
                   - Helps focus the story's direction
                
                3. **Adjust the Settings**
                   - Story Length: Longer stories allow for more detail
                   - Creativity Level: Higher values for more unique stories
                
                4. **Experiment and Iterate**
                   - Try different prompts and settings
                   - Save your favorite combinations
                """)
        
        except Exception as e:
            st.error(f"🚨 Error: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Made with ❤️</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()