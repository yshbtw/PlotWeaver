from groq import Groq
from datetime import datetime
from config import GROQ_API_KEY, MODEL_NAME, GENRE_TEMPLATES
from database import stories_collection

class StoryGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME
        self.genre_templates = GENRE_TEMPLATES

    def generate_story(self, prompt, genre=None, max_length=500, temperature=0.8):
        if genre and genre in self.genre_templates:
            prompt = self.genre_templates[genre].format(context=prompt)
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a creative story writer. Write a story about {max_length} words long."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            temperature=temperature,
        )
        
        return chat_completion.choices[0].message.content

    def save_story(self, prompt, genre, story, max_length, temperature):
        """Save generated story to MongoDB if available"""
        if stories_collection is not None:
            story_doc = {
                'prompt': prompt,
                'genre': genre,
                'story': story,
                'max_length': max_length,
                'temperature': temperature,
                'created_at': datetime.utcnow()
            }
            return stories_collection.insert_one(story_doc)
        return None

    def get_story_history(self, limit=10):
        """Retrieve story history from MongoDB if available"""
        if stories_collection is not None:
            return list(stories_collection.find().sort('created_at', -1).limit(limit))
        return [] 

    def delete_story(self, story_id):
        """Delete a story from MongoDB by its ID"""
        if stories_collection is not None:
            try:
                result = stories_collection.delete_one({"_id": story_id})
                return result.deleted_count > 0
            except Exception as e:
                print(f"Error deleting story: {str(e)}")
                return False
        return False