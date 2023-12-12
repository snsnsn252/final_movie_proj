
# poster

base_url = "https://image.tmdb.org/t/p/w500"
poster_path = "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
full_url = base_url + poster_path

import requests

def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Image successfully downloaded:", save_path)
    else:
        print("Failed to download image")

download_image(full_url, "poster.jpg")










# trailer

import requests
import json

url = "https://api.themoviedb.org/3/movie/238/videos?language=en-US" # movie_id = 238
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZWUyMWQ4N2QzZjVhNmJhZWY3YTQ5OWU2MTFkYjZhNCIsInN1YiI6IjY1NWFhMjhjNTM4NjZlMDExYzA5Y2Q3NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Oa4VJpx6NI7zowz_Kucf9N_zc_zhwBg2Tq-PeVPx-4k"
}

response = requests.get(url, headers=headers)
data = response.json()
print(data)

# Assuming the first video in the list is the trailer
if data['results']:
    first_video = data['results'][0]
    video_key = first_video.get('key')
    video_site = first_video.get('site')

    if video_site == "YouTube":
        youtube_url = f"https://www.youtube.com/watch?v={video_key}"
        print("YouTube URL:", youtube_url)
    else:
        print("Trailer not available on YouTube.")
else:
    print("No video results found.")




# api_key

import requests

api_key = "api_key=5ee21d87d3f5a6baef7a499e611db6a4"

# url="https://api.themoviedb.org/3/genre/movie/list?api_key=5ee21d87d3f5a6baef7a499e611db6a4&language=en"
# url=f"https://api.themoviedb.org/3/genre/movie/list?{api_key}&language=en"
url=f"https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&{api_key}&release_date.lte=2023-12-10&with_genres=Comedy"

response = requests.get(url)
print(response.text)



# similarity:

import difflib

def calculate_title_similarity(title1, title2):
    similarity = difflib.SequenceMatcher(None, title1, title2).ratio()
    return similarity

# Example usage
similarity = calculate_title_similarity("Your name", "The Grand Adventure")
print(f"Similarity Score based on Titles: {similarity}")
