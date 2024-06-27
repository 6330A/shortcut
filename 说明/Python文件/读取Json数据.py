import json

# 使用 Python 读取 JSON 文件，并解析其中的信息
with open('shortcut.json', 'r',  encoding='utf-8') as file:
    data = json.load(file)

# 输出读取到的信息
print(data)

