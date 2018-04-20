import boto
import boto.s3
import sys
import os.path

from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAJAA3SIB4TH6KZXDA'
AWS_SECRET_ACCESS_KEY = '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'

# bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


# bucket = conn.create_bucket(bucket_name,
#     location=boto.s3.connection.Location.DEFAULT)

bucket_name = "zestlmedia"
bucket = conn.get_bucket(bucket_name)


testfile = "/Users/sujoychakravarty/Dropbox/Zestl-share/Deployment/Sanskriti/DataWagholi/teachers photo/ritika bajaj.jpg"

sourceDir = "/Users/sujoychakravarty/Dropbox/Zestl-Deployment/Sanskriti/DataWagholi/sep15images/"
# /Users/sujoychakravarty/Dropbox/Zestl-share/Deployment/Sanskriti/DataWagholi/

destDir = ''


uploadFileNames = []
for (sourceDir, dirname, filename) in os.walk(sourceDir):
    uploadFileNames.extend(filename)
    break

for filename in uploadFileNames:

    sourcepath = os.path.join(sourceDir + filename)
    destpath = os.path.join(destDir, filename)
    print 'Uploading %s to Amazon S3 bucket %s' %(filename, bucket_name)



    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()


    k = Key(bucket)
    k.key = filename
    k.set_contents_from_filename(sourcepath, cb=percent_cb, num_cb=10)
    k.set_metadata('Content-Type', 'image/jpeg')
    k.set_acl('public-read')
    url = k.generate_url(expires_in=0, query_auth=False)
    print url