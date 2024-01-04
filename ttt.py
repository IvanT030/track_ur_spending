import re

def process_data(data):
    # 使用正規表達式提取資訊
    matches = re.match(r'(\w+)，(\w+)，(\d{4}年\d{1,2}月\d{1,2}日)，(\d+)。', data)

    if matches and len(matches.groups()) == 4:
        category, classification, date, cost = matches.groups()
        year, month, day = re.findall(r'\d+', date)
        return [category, classification, year, month, day, int(cost)]
    else:
        return None

# 資料
data1 = "住院，醫療，2020年7月3日，20000。賭博，其他，2020年7月6日，6000。應酬，其他，2020年7月5日，2000。"
data2 = ""
data3 = ""

# 處理資料
result1 = process_data(data1)
result2 = process_data(data2)
result3 = process_data(data3)

# 檢查是否有缺少目錄
if None in [result1, result2, result3]:
    missing_fields = []
    for idx, result in enumerate([result1, result2, result3], start=1):
        if result is None:
            missing_fields.append(f"Data {idx} is incomplete.")
    print("\n".join(missing_fields))
else:
    # 打印結果
    result_list = [result1, result2, result3]
    print(result_list)
