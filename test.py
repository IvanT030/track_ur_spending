import re

text = "項目：住院，醫療，2020年7月6日，20000。，其他，2020年7月6日，6000。項目：應酬，其他，2020年7月5日"

# 使用 split 將文本分割成不同的段落
paragraphs = text.split('。')

# 定義正規表達式模式
pattern = re.compile(r'(?:項目：)?([^，]+)，([^，]+)，(\d{4})年(\d+)月(\d+)日，(\d+)')

# 定義存放結果的列表
list1 = []  # 有缺少的段落
list2 = []  # 沒有缺少的段落

# 使用正規表達式檢查每段
for paragraph in paragraphs:
    if paragraph:  # 確保不處理空的段落
        match = pattern.match(paragraph)
        if match and len(match.groups()) == 6:
            list2.append(match.groups())
        elif "項目：" in paragraph:
            list1.append(paragraph)

# 列印結果
print("有缺少的段落:", list1)
print("沒有缺少的段落:", list2)

print(list1[0][4])