import requests
import datetime
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

#download()
#get_baidu_response()


 