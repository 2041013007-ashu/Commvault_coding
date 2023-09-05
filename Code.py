import boto3
import os

os.environ['ACCESS_KEY_ID'] = 'AKIARAQCHDAP3N4CB6T4'
os.environ['SECRET_ACCESS_KEY'] = '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'

session = boto3.Session(region_name='us-west-1', 
                  aws_access_key_id=os.environ.get('ACCESS_KEY_ID'), 
                  aws_secret_access_key=os.environ.get('SECRET_ACCESS_KEY'))

ec2 = session.resource('ec2')
s3 = session.resource('s3')
ec2.create_instances(
    ImageId='ami-03f2f5212f24db70a',
    InstanceType='t2.micro',
    KeyName='my-new-key-pair',
    MinCount=1,
    MaxCount=1,
)

s3.create_bucket(Bucket='my-first-bucket-1801', CreateBucketConfiguration={
        'LocationConstraint': 'us-west-1'})

from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    email = input("Enter email: ")
    filename = input("Enter filename: ")

    if not email or not filename:
        print("Both email and filename are required.")
    else:
        # Combine email and filename to create S3 object name
        object_name = f"{email}_{filename}"

        # Get the local file path to upload
        file_path = input("Enter the local file path to upload: ")

        if not os.path.exists(file_path):
            print("File not found.")
        else:
            # Upload the file to S3
            upload_to_s3(file_path, 'my-first-bucket-1801', object_name, s3)
            
def upload_to_s3(file_path, bucket_name, object_name, s3):
    try:
        # Upload the file to S3
        bucket = s3.Bucket(bucket_name)
        bucket.upload_file(file_path, object_name)

        print(f"File '{object_name}' uploaded successfully to '{bucket_name}'.")

    except Exception as e:
        print(f"Error uploading file: {e}")

@app.route('/search', methods=['POST'])
def search():
    email = request.form['email']
    search_query = request.form['search_query']
    results = [key for key in os.listdir() if email in key and search_query in key]
    return render_template('results.html', results=results)

@app.route('/download/<path:file_key>')
def download(file_key):
    return file_key

if __name__ == '__main__':
    app.run(debug=True)
