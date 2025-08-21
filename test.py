import requests



def get_baidu_response():
    # 百度首页URL
    url = "https://www.baidu.com"
    
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


get_baidu_response()


 