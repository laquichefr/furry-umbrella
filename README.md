# AWS LAMBDA images resizer
  Create a TO_PROCESS S3 Bucket that will receive images to be processed.  
  Create multiples Buckets that will receive processed images.  
  Create the Lambda function with lambda_function.py  
  For automated execute this function, add a createObject trigger from S3 Bucket you just created in Lambda options.  
  Test:  
  	Rename image with the name of the receiver Bucket before Uploading image  
    (ex: rename butterfly.webp to MYBUCKET3!butterfly.webp will go to MYBUCKET3 after being processed DONT FORGET THE "!" SEPARATOR or modify code to choose another one )  
    Upload MYBUCKET3!butterfly.webp to the TO_PROCESS Bucket.  
    LAMBDA detect a new object is created in TO_PROCESS Bucket and execute the lambda_function.py.
    After a few seconds check MYBUCKET3 Bucket.  
    You will see 2 resized files images/butterfly.webp and thumbnails/thumbnail_butterfly.webp.  
    MYBUCKET3!butterfly.webp is deleted from TO_PROCESS Bucket after being processed.  
