# 导包
from bs4 import BeautifulSoup
# 定义html

file = """
<html> 
    <head>
        <title>黑马程序员</title>
    </head> 
    <body>
        <p id="test01">软件测试</p>
        <p id="test02">2020年</p>
        <a href="/api.html">接口测试</a>
        <a href="/web.html">Web自动化测试</a> 
        <a href="/app.html">APP自动化测试</a>
    </body>
</html>
"""

# 获取soup对象
soup = BeautifulSoup(file, "html.parser")
# 1、使用soup对象提取html 获取标签代码
print(soup.title)
# 2、获取标签名称
print(soup.title.name)
# 3、获取标签文本
print(soup.title.string)
# 4、获取属性
print(soup.p.get("id"))
# 5、获取所有的相同标签
print(soup.find_all("p"))
# 扩展 获取第二个p标签的文本值 2020年
print(soup.find_all("p")[1].string)
print(soup.find_all("p")[1].get("id"))