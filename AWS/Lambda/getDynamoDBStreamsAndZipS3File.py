import urllib.parse
import boto3
import zipfile
import os.path
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer

# DynamoDB
# Table:dev_S3_archive
# PartitionKey:id(str)
# SortKey:division(num)
# Other:
#     status(bool)
#     notification_type(num)
#     request_paths(list)
#     result_path(str)
#     created_at(str)
#     updated_at(str)

s3 = boto3.resource('s3')
s3_cli = boto3.client('s3')
bucket_name = 'photoruction-test'

def lambda_handler(event, context):
    print(event)
    try:
        image = event['Records'][0]['dynamodb']['NewImage']
        item = deserialize(image)
        if item['request_paths']:
            s3_file_paths = item['request_paths']
            upload_path = archive_s3_files(s3_file_paths)
            update_dynamodb(item, upload_path)
        print('--END--')
    except Exception as e:
        print(e)
        raise e
    else:
        print('finish (no error)')
    finally:
        print('all finish')
        return {
            "status": "ok"
        }

    # S3ファイルのZIP化関数
def archive_s3_files(s3_file_paths):
    upload_path = ''
    try:
        zip_path = '/tmp/%s.zip' % 'image'
        zf = zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED)
        for s3_file_path in s3_file_paths:
            basename = os.path.basename(s3_file_path)
            tmp_file = os.path.join('/tmp/', basename)
            response = s3_cli.get_object(Bucket=bucket_name, Key=s3_file_path)
            bodystr = response['Body'].read()
            zf.writestr(os.path.basename(s3_file_path), bodystr)
        zf.close()
        upload_path = 'TEST/%s.zip' % 'image'
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.upload_file(zip_path, upload_path)
    except Exception as e:
        print(e)
        raise e
    finally:
        return upload_path
    
    # Dictに変換する関数
def deserialize(image):
    deserializer = TypeDeserializer()
    d = {}
    for key in image:
        d[key] = deserializer.deserialize(image[key])
    return d

    # DynamoDB更新関数
def update_dynamodb(item, upload_path):
    response = ''
    try:
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        dynamoDB = boto3.resource("dynamodb")
        table_name = "dev_S3_archive"
        dynamotable = dynamoDB.Table(table_name)
        response = dynamotable.update_item(
            Key={
                'id': item["id"],
                'division': item["division"]
            },
            # 更新式　set 更新したい値 = :更新内容
            UpdateExpression="set #st = :status, result_path=:result_path, updated_at=:updated_at",
            # 予約語はエスケープする
        	ExpressionAttributeNames={
        		'#st': 'status'
        	},
            # 更新内容を記述
            ExpressionAttributeValues={
                ':status': True,
                ':result_path': upload_path,
                ':updated_at': date
            })
        print(response)
    except Exception as e:
        print(e)
        raise e
    finally:
        return response