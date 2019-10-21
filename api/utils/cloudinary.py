from os import environ

from cloudinary import config, uploader

config(
    cloud_name = environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = environ.get('CLOUDINARY_API_KEY'),
    api_secret = environ.get('CLOUDINARY_API_SECRET')
)

def upload_images(files):
    return [ uploader.upload(file, folder="grupo_camporota") for file in files ]
    