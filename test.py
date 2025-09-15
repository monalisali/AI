import requests
import datetime
import boto3
from botocore.client import Config
import os
#import requests_async

def get_baidu_response():
    # 百度首页URL  
    url = "https://www.baidu.com"
    today = datetime.date.today().strftime("%Y%m%d")
    
    try:
        # 发送GET请求
        response = requests.get(url)
        
        # 检查请求是否成功
        response.raise_for_status()  # 如果响应状态码不是200，会抛出HTTPError异常
        
        # 设置正确的编码，避免中文乱码
        response.encoding = response.apparent_encoding
        
        # 打印返回内容
        print("百度返回的内容如下：\n")
        print(response.text)
        
        return response.text
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP请求错误: {e}")
    except requests.exceptions.ConnectionError:
        print("连接错误，请检查网络连接")
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")

#上传文件到RustFS站点
def upload_to_rustfs(
    local_file_path,
    rustfs_endpoint,
    access_key,
    secret_key,
    bucket_name,
    remote_directory
):
    """
    向RustFS的指定bucket和目录上传文件
    
    参数:
        local_file_path: 本地文件路径
        rustfs_endpoint: RustFS的API端点
        access_key: 访问密钥
        secret_key: 密钥
        bucket_name: 目标bucket名称
        remote_directory: 目标目录路径（如 'data/logs/'）
    """
    # 确保远程目录以斜杠结尾
    if not remote_directory.endswith('/'):
        remote_directory += '/'
    
    # 获取本地文件名
    file_name = os.path.basename(local_file_path)
    
    # 构建远程文件路径
    remote_file_path = f"{remote_directory}{file_name}"
    
    try:
        # 创建RustFS客户端
        s3 = boto3.client(
            's3',
            endpoint_url=rustfs_endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4')
        )
        
        # 上传文件
        s3.upload_file(
            Filename=local_file_path,
            Bucket=bucket_name,
            Key=remote_file_path
        )
        
        print(f"文件 {local_file_path} 已成功上传到 {bucket_name}/{remote_file_path}")
        return True
        
    except Exception as e:
        print(f"上传失败: {str(e)}")
        return False

"""
async def download(args: Args) -> Output:
    params = args.params
    url = params['input']
    url = 'https://lf6-appstore-sign.oceancloudapi.com/ocean-cloud-tos/7fe45502-d5f2-4b54-9cf9-746952a90c4a.md?lk3s=edeb9e45&x-expires=1757565385&x-signature=2GMM8avAz9gJWt%2FzMGKRAtjw0as%3D'
    save_path = r'C:\D\download'
    #save_path = params['C:\\D\\download']

    try:
        response = await requests_async.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        ret: Output = {
            "key0": f"File downloaded successfully to {save_path}",
            "key1": [url],
            "key2": {
                "key21": "Download completed"
            }
        }
    except Exception as e:
        ret: Output = {
            "key0": f"Download failed: {str(e)}",
            "key1": [url],
            "key2": {
                "key21": "Download error"
            }
        }
    
    return ret
"""
def printString():
    print("this is test print")

upload_to_rustfs("C:\D\mock.txt","http://10.158.15.248:9000","rustfsadmin","g74tU%Gk0*nU","test-bucket","test/")
#download()
#get_baidu_response()


 