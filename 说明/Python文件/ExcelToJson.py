# 文件名：ExcelToJson.py
import pandas as pd
import json

# 两个路径自定义
ExcelPath = 'C:\\Users\\Lzy\\Desktop\\IDEA.xlsx'
JsonPath = 'IDEA_ShortCut.json'

# 读取 Excel 文件 openpyxl 需要pip安装一下
df = pd.read_excel(ExcelPath, engine='openpyxl')

# 将 DataFrame 转换为 JSON
json_data = df.to_json(orient='records', force_ascii=False)

# 格式化 JSON 数据
formatted_json_data = json.dumps(json.loads(json_data), indent=4, ensure_ascii=False)

# 将格式化后的 JSON 数据写入文件
with open(JsonPath, 'w', encoding='utf-8') as f:
    f.write(formatted_json_data)
