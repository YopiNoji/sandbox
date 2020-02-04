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

import urllib.parse
import boto3
import zipfile
import os.path
import random, string
from boto3.dynamodb.types import TypeDeserializer
from datetime import datetime

s3 = boto3.resource('s3')
s3_cli = boto3.client('s3')
bucket_name = 'photoruction-test'

def lambda_handler(event, context):
    try:
        for value in event['Records']:
            data = deserialize(value['dynamodb']['NewImage'])
            if data['request_paths'] and data['status'] == 0:
                print('data is OK')
                s3_file_paths = data['request_paths']
                update = {}
                update['status'] = 1
                update['upload_path'] = archive_s3_files(s3_file_paths)
                update_dynamodb(data, update)
            else:
                print('Illegal data')
    except Exception as e:
        print(e)
        print('ERROR in lambda_handler')
        update = {}
        update['status'] = 9
        update['upload_path'] = None
        update_dynamodb(data, update)
        raise e
    finally:
        print('Lambda ')
        return True

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
        upload_path = 'TEST/%s.zip' % randomname(5)
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.upload_file(zip_path, upload_path)
    except Exception as e:
        print(e)
        print('ERROR in archive_s3_files')
        raise e
    finally:
        print('upload_path')
        print(upload_path)
        return upload_path
    
    # Dictに変換する関数
def deserialize(image):
    deserializer = TypeDeserializer()
    d = {}
    for key in image:
        d[key] = deserializer.deserialize(image[key])
    return d
    
    # ランダム文字列生成関数
def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    # DynamoDB更新関数
def update_dynamodb(key, update):
    response = ''
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dynamoDB = boto3.resource("dynamodb")
        table_name = "dev_S3_archive"
        dynamotable = dynamoDB.Table(table_name)
        response = dynamotable.update_item(
            Key={
                'id': key["id"],
                'division': key["division"]
            },
            # 更新式　set 更新したい値 = :更新内容
            UpdateExpression="set #st = :status, result_path=:result_path, updated_at=:updated_at",
            # 予約語はエスケープする
        	ExpressionAttributeNames={
        		'#st': 'status'
        	},
            # 更新内容を記述
            ExpressionAttributeValues={
                ':status': update['status'],
                ':result_path': update['upload_path'],
                ':updated_at': date
            })
    except Exception as e:
        print('ERROR in update_dynamodb')
        print(key)
        print(update)
        print(e)
        raise e
    finally:
        return response