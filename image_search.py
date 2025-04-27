import requests
import os
from serpapi import GoogleSearch

SERPAPI_KEY = "b0be7f39e32131926b121590db314d0e55109248fa8fe096c708c7518a31ec7a"

def fetch_google_images(query, num_images=4):
    search = GoogleSearch({
        "q": query,
        "tbm": "isch",
        "num": num_images,
        "api_key": SERPAPI_KEY
    })
    results = search.get_dict()
    images = results.get("images_results", [])
    
    if not images:
        return []

    return [img["original"] for img in images[:num_images]]

def download_images(image_urls, folder="downloaded_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    downloaded_paths = []
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(folder, f"image_{i+1}.jpg")
                with open(image_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                downloaded_paths.append(image_path)
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
    
    return downloaded_paths