#------------------------------------------------------------#
#-----------Instagram Automatic Post Generator Bot-----------#
#------------------------------------------------------------#
#--Usage example: AI Generated Artworks of Baku, Azerbaijan--#
#------------------------------------------------------------#

# Import artists database
import artists

# Import scheduling library and time
import schedule
import time as tm

# Instagram Interaction API integration
from instagrapi import Client
from instagrapi.types import Location
import config

# Requests library imports
import requests # request img from web
import shutil # save img locally

# Open AI API integration
import openai
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

# EDIT YOUR CITY OF CHOICE HERE
city = "Baku, Azerbaijan"


artists_list = artists.famous_painters

# ChatGPT generated post description
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "user", "content" : prompt}
        ]
    )
    post_description = response['choices'][0]["message"]["content"]
    return post_description




# DALL-E generated post image
def generate_image(prompt):
    image = openai.Image.create(
        prompt = prompt,
        n = 1,
        size = "256x256"
    )
    return image["data"][0]["url"]



# Function to save image from URL
def save_image_from_url(url, file_name):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', file_name)
    else:
        print('Image Couldn\'t be retrieved')

    return file_name


# Function to post on instagram
def instagram_upload_post(image, description):
    # Post upload
    media = cl.photo_upload(
        path = image,
        caption = description
    )

def main():
    global artist_number
    artist_name = artists_list[artist_number]

    image_prompt = city + " if it was drawn by " + artist_name + " in artist's signature style"
    text_prompt = "What would " + artist_name + " like about " + city + " and what would inspire him to draw the city?"

    image = save_image_from_url(generate_image(image_prompt), artist_name.replace(" ", "_") + ".jpg")
    text = generate_text(text_prompt)

    print(text)
    print(image)

    instagram_upload_post(image, text)

    print("Upload successful")
    artist_number += 1


# Login to Instagram account
cl = Client()
cl.login(config.username, config.password)

artist_number = 0

# Post 1 image every day
main()
schedule.every(1).days.do(main)
while True:
     schedule.run_pending()
     tm.sleep(1)




