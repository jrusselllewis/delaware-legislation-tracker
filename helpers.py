import boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html


class S3Helper:
  def __init__(self, bucket_name):
    self.BUCKET = bucket_name
    self.s3 = boto3.resource('s3')

  def upload_file(self, source_path, dest_path):
    print(' - uploading file %s > %s' % (source_path, dest_path))
    data = open(source_path, 'r')
    self.s3.Bucket(self.BUCKET).put_object(Key=dest_path, Body=data)

  def write_file(self, data, dest_path):
    print(' - writing data to s3://%s/%s' % (self.BUCKET, dest_path))
    return self.s3.Bucket(self.BUCKET).put_object(Key=dest_path, Body=data)

  def list_files(self, filter):
    files = []
    bucket = self.s3.Bucket(self.BUCKET)
    for file in bucket.objects.filter(Prefix=filter):
      files.append(file.key)
    return files

  def get_file_content(self, key):
    obj = self.s3.Object(self.BUCKET, key)
    return(obj.get()['Body'].read().decode('utf-8'))
    