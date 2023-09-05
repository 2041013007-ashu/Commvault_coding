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
    email = request.form['email']
    filename = request.form['filename']
    s3_key = f"{email}_{filename}"
    with open(s3_key, 'w') as f:
        f.write("This is the content of the file.")
    return redirect(url_for('index'))

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