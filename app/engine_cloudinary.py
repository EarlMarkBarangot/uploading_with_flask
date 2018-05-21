import os
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

cloudinary.config( 
  cloud_name = 'silverly', 
  api_key = '393882568386968', 
  api_secret = 'RlS1MEq2NDzByGKDuVobeRTCYvY'
)

options = {"resource_type":"video"}

#d = upload("theflask.jpg", **options)
d = upload('rer.jpg')
print d
#pipeshelf = cloudinary.CloudinaryImage("theflask.jpg")
