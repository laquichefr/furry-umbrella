import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

thumb_size=300,300
main_size=1024,1024

s3 = boto3.client('s3')

def resize_thumb_image(image_path, resized_path):
	with Image.open(image_path) as image:
		image.thumbnail(thumb_size,Image.ANTIALIAS)
		image.save(resized_path)

def resize_main_image(image_path, resized_path):
	with Image.open(image_path) as image:
		image.thumbnail(main_size,Image.ANTIALIAS)
		image.save(resized_path)

def lambda_handler(event, context):
	# TODO implement
	for record in event['Records']:
		key = unquote_plus(record['s3']['object']['key'])
		dest_bucket = key.split('!')[0]
		tmpkey = key.split('!')[1]
		bucket = record['s3']['bucket']['name']
		download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
		s3.download_file(bucket, key, download_path)
		s3.upload_file(download_path, dest_bucket, Key='images/'+tmpkey)
		print('upload_mainfile done')
		upload_thumb_path = '/tmp/thumbnail_{}'.format(tmpkey)
		upload_main_path = '/tmp/{}'.format(tmpkey)
		print('key',key,'dest_bucket',dest_bucket,'tmpkey',tmpkey,'download_path',download_path,'upload_thumb_path',upload_thumb_path,'upload_main_path',upload_main_path)
		print("picsize",os.path.getsize(download_path))
		if os.path.getsize(download_path)>50000:
			print('resizing...')
			resize_main_image(download_path, upload_main_path)
			print('main resize done','new size:',os.path.getsize(upload_main_path))
			s3.upload_file(upload_main_path, dest_bucket, Key='images/'+tmpkey)
			print('upload_mainfile done')
			resize_thumb_image(download_path, upload_thumb_path)
			print('thumb resize done','new size:',os.path.getsize(upload_thumb_path))
			s3.upload_file(upload_thumb_path, dest_bucket, Key='thumbnails/thumbnail_'+tmpkey)
			print('upload_thumbfile done')
		else:
			print('only generate thumb!!! size less than 50ko')
			resize_thumb_image(download_path, upload_thumb_path)
			print('thumb resize done','new size:',os.path.getsize(upload_thumb_path))
			s3.upload_file(upload_thumb_path, dest_bucket, Key='thumbnails/thumbnail_'+tmpkey)
			print('upload_thumbfile done')
		s3.delete_object(Bucket=bucket,Key=key)

