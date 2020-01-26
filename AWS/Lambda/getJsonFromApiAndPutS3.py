import boto3
import urllib
import json
import sys
import codecs
import base64
from datetime import datetime

# s3object取得
s3r = boto3.resource('s3') 
s3c = boto3.client('s3')

# ベースURL
base_url = 'https://stg.www.yoshinoya.com/'

# URLリスト
urllist = [
    base_url + 'json_service',
    base_url + 'json_menu_category'
    ]

# Basic認証の情報
user = 'admin'
password = 'password'

# Basic認証用の文字列を作成.
basic_user_and_pasword = base64.b64encode('{}:{}'.format(user, password).encode('utf-8'))

# メイン関数
def lambda_handler(event, context):

    bucket = 'json2upload'    # S3バケット名を指定

    for url in urllist:
        file_contents = dataGet(url)  # 保存するファイルの内容
        filehead = url.replace(base_url,'')
        key = filehead + '.json'  # S3に保存するファイル名
        obj = s3r.Object(bucket,key)
        obj.put( Body=file_contents, ContentType="application/json" ) # S3更新

    return "Success to upload JSON on S3"

# webAPIからJSONの形式の文字列の結果をもらう
def dataGet(url):

    try:
        # Basic認証付きの、GETリクエストの作成
        request = urllib.request.Request(url, headers={"Authorization": "Basic " + basic_user_and_pasword.decode('utf-8')})
        with urllib.request.urlopen(request) as res:
            api_contents = res.read()
        # # Basic認証なしの場合はこちらを使う
        # readObj = urllib.request.urlopen(url)  # 読み込むオブジェクトの作成
        # api_contents = readObj.read()   # webAPIからのJSONを取得
        # api_contents = ','.join(api_contents.decode('utf-8').split('\n')) #string型に変換
    except:
        print("some error in process to get API data")
    finally:
        return api_contents