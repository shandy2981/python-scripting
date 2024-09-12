import argparse
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

s3 = boto3.client('s3')

def list_buckets_or_files(bucket=None):
    try:
        if bucket:
            objects = s3.list_objects_v2(Bucket=bucket)
            if 'Contents' in objects:
                for obj in objects['Contents']:
                    print(f"{obj['Key']}")
            else:
                print(f"No files found in bucket: {bucket}")
        else:
            response = s3.list_buckets()
            print("Buckets in your account:")
            for b in response['Buckets']:
                print(f"{b['Name']}")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")

def upload_file(file_path, bucket_name):
    try:
        file_name = file_path.split('/')[-1]
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"File {file_name} uploaded to bucket {bucket_name}.")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")

def download_file(file_name, bucket_name, destination_path):
    try:
        s3.download_file(bucket_name, file_name, destination_path)
        print(f"File {file_name} downloaded from bucket {bucket_name} to {destination_path}.")
    except FileNotFoundError:
        print(f"Error: Destination path {destination_path} not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")

def main():
    parser = argparse.ArgumentParser(description="A simple S3 Bucket Manager")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List S3 buckets or contents of a bucket")
    list_parser.add_argument("--bucket", type=str, help="Name of the bucket to list files from")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a file to an S3 bucket")
    upload_parser.add_argument("file_path", type=str, help="Path to the file to upload")
    upload_parser.add_argument("bucket_name", type=str, help="Name of the bucket to upload the file to")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download a file from an S3 bucket")
    download_parser.add_argument("file_name", type=str, help="Name of the file to download")
    download_parser.add_argument("bucket_name", type=str, help="Name of the bucket to download the file from")
    download_parser.add_argument("destination_path", type=str, help="Path to save the downloaded file")

    args = parser.parse_args()

    if args.command == "list":
        list_buckets_or_files(args.bucket)
    elif args.command == "upload":
        upload_file(args.file_path, args.bucket_name)
    elif args.command == "download":
        download_file(args.file_name, args.bucket_name, args.destination_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()