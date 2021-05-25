import csv
import os

import settings
sheets_path = os.path.join(settings.BASE_PATH, "sheets1.csv")
save_csvFile1 = open(sheets_path, "w", encoding="utf-8", newline='')
save_csvFile = csv.writer(save_csvFile1)


def read_user_settings():
    """
    通过本地表格文件读取用户设定
    :return:
    """
    csvFile = open(settings.SHEET_PATH, "r", encoding="utf-8")
    reader = csv.reader(csvFile)
    reader = list(reader)
    csvFile.close()
    csvFile = open(settings.SHEET_PATH, "w", encoding="utf-8", newline='')
    save_csvFile = csv.writer(csvFile)
    user_settings = {}
    # 迭代所有的行

    for row in reader:
        if "T" in row[0]:
            tool_num = row[0]
            model = row[1]
            val1 = row[2]
            val2 = row[3]
            is_newTool = row[4]
            if is_newTool == "1":
                row[4] = "0"

            user_settings[tool_num] = {
                "model": model,
                "var1": val1,
                "var2": val2,
                "is_newTool": is_newTool,
            }
        save_csvFile.writerow(row)
    csvFile.close()
    return user_settings
print(read_user_settings())