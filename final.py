import os
import csv
import numpy as np
import pandas as pd


class Handle_Single_CSV():
    def __init__(self, data):
        self.data = data

    # 转置
    def transposition(self):
        data_values = self.data.values
        index1 = list(self.data.keys())
        data1 = list(map(list, zip(*data_values)))
        data_get = pd.DataFrame(data1, index=index1)
        return data_get

    # 首列 变为 列索引
    def change_columns(self):
        arr = np.array(self.data)
        list_columns = arr.tolist()
        columns = list_columns[0]
        self.data.columns = columns
        self.data.drop([0], inplace=True)


def handle_csv_txt(title):

    names = locals()

    # 删除文本前两行
    with open(f"C:\\Desktop\\rose导出数据\\{title}.txt", mode='r', encoding='utf-8') as f1:
        line = f1.readlines()  # 读取文件
        for i in range(0, 2):
            line = line[1:]  # 只读取第一行之后的内容
            f2 = open(f"C:\\Desktop\\rose(changed)\\{title}.txt", mode='w', encoding='utf-8')  # 以写入的形式打开txt文件
            f2.writelines(line)  # 将修改后的文本内容写入
            f2.close()  # 关闭文件
    f1.close()

    # 分割左列题头创建csv文件
    csv_file = open(f"C:\\Desktop\\csv\\{title}.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)
    f = open(f"C:\\Desktop\\rose(changed)\\{title}.txt", 'r', encoding='utf-8')
    list_1 = [
        "PT", "AU", "AF", "TI", "SO", "LA", "DT", "DE", "ID", "AB", "C1", "C3", "EM", "OI",
        "FU", "FX", "NR", "TC", "Z9", "U1", "U2", "PU", "PI", "PA", "SN", "EI", "J9", "JI",
        "PD", "PY", "VL", "AR", "DI", "PG", "WC", "WE", "SC", "GA", "UT", "OA", "DA", "ER"
    ]
    for line in f.read().splitlines():
        csvrow = line.split(maxsplit=1)
        if csvrow:  # 判断是否空行
            if np.isin(csvrow[0], list_1):  # 判断是否存在题头
                writer.writerow(csvrow)  # 照常写入
            else:
                writer.writerow(["", line])  # 以0为题头，将内容写入第二列
        else:
            writer.writerow(["\n"])
    f.close()
    csv_file.close()

    # 同题头下不同行内容整合至同行

    # 使第一行不再是索引
    """反例：data = pd.read_csv("C:\\Desktop\\rose1-500.csv", encoding="utf-8")"""
    data = pd.read_csv(f"C:\\Desktop\\csv\\{title}.csv", header=None, index_col=None, encoding="utf-8")
    chance = True
    j = 0
    while chance:
        chance = False
        for i in range(j, len(data.index)):
            if pd.isna(data.loc[i, 0]):
                data.loc[i - 1, 1] = str(data.loc[i - 1, 1]) + str(data.loc[i, 1])
                data.drop([i], inplace=True)
                data.reset_index(drop=True, inplace=True)
                chance = True
                j = i
                break
            else:
                continue

    # 分割csv文件，获得各篇论文的具体内容
    sign = []
    for i in range(0, len(data.index)):
        if data.loc[i, 0] == "PT":
            sign.append(i)
    for j in range(0, len(sign) - 1):
        names["df" + str(j)] = data[sign[j]: sign[j + 1]]
    names["df" + str(len(sign) - 1)] = data[sign[len(sign) - 1]:]
    data.to_csv(f"C:\\Desktop\\csv\\{title}.csv", index=False, header=False, encoding="utf-8")

    for m in range(0, len(sign)):
        handle_single_csv = Handle_Single_CSV(names.get("df" + str(m)))
        names["data" + str(m)] = handle_single_csv.transposition()
        handle_single_csv = Handle_Single_CSV(names.get("data" + str(m)))
        handle_single_csv.change_columns()

        if m == 0:
            data = names.get("data" + str(m))
        else:
            data = pd.concat([data, names.get("data" + str(m))], join="outer")

    data.reset_index(drop=True, inplace=True)
    data = pd.DataFrame(np.insert(data.values, 0, values=list(data.columns), axis=0))

    data.to_csv(f"C:\\Desktop\\df\\{title}.csv", index=False, header=False, encoding="utf-8")


# 整文件只需提供原始txt文本数据的文件夹
file = os.listdir("C:\\Desktop\\rose导出数据")
for file1 in file:
    title = file1.split(".", 1)[0]
    print(title)
    handle_csv_txt(title)


"""
文件需原始txt文本数据的文件夹，进行如上拆分获得title操作后，调用handle_csv_txt函数，即获得文件夹df中的csv文件直接导入数据库即可
"""