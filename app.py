from flask import Flask, render_template, jsonify
import pandas as pd
import os

# 初始化 Flask 應用
app = Flask(__name__)

# 主頁面路由
@app.route('/')
def index():
    return render_template('index.html')  # 確保你的 index.html 位於 templates 資料夾中

@app.route('/analysis')
def analysis():
    return render_template('index-2.html')  # 確保你的 index.html 位於 templates 資料夾中

# 圖表資料的 API 路由
@app.route('/chart-data')
def generate_chart():
    # 提供資料
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')  # 確保 dataset 資料夾和 CSV 文件存在
    df = pd.read_csv(dataset_path)

    # 數據處理
    df['Hours Viewed'] = df['Hours Viewed'].replace(',', '', regex=True).astype(float)
    content_type_viewership = df.groupby('Content Type')['Hours Viewed'].sum()

    # 返回 JSON 格式的資料
    data = {
        'labels': content_type_viewership.index.tolist(),
        'values': content_type_viewership.values.tolist()
    }
    return jsonify(data)

@app.route('/chart-data-2')
def generate_chart_2():
    # 提供資料
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')  # 確保 dataset 資料夾和 CSV 文件存在
    df = pd.read_csv(dataset_path)

    # 數據處理
    df['Hours Viewed'] = df['Hours Viewed'].replace(',', '', regex=True).astype(float)

    # 計算每月數據
    df['Release Month'] = pd.to_datetime(df['Release Date']).dt.month  # 假設有 Release Date 欄位
    monthly_releases = df['Release Month'].value_counts().sort_index()
    monthly_viewership = df.groupby('Release Month')['Hours Viewed'].sum()

    # 將資料轉換為 Python 的內建型態
    data = {
        "months": list(range(1, 13)),
        "monthly_releases": [int(monthly_releases.get(i, 0)) for i in range(1, 13)],  # 確保是 Python int
        "monthly_viewership": [float(monthly_viewership.get(i, 0)) for i in range(1, 13)]  # 確保是 Python float
    }
    return jsonify(data)


@app.route('/datatable')
def datatable():
    # 提供資料
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')  # 確保 dataset 資料夾和 CSV 文件存在
    df = pd.read_csv(dataset_path)
    
    # 確保 'Hours Viewed' 為數字類型
    df['Hours Viewed'] = df ['Hours Viewed'].replace(',','',regex=True).astype(float)
    
    # 選取 'Hours Viewed' 前 10 名
    top_10_titles = df.nlargest(10, 'Hours Viewed')

    # 篩選需要的欄位
    top_10_titles = top_10_titles[['Title', 'Hours Viewed', 'Language Indicator', 'Content Type', 'Release Date']]
    
    # 將 DataFrame 轉換為列表形式
    data = top_10_titles.to_dict('records')
    return jsonify(data)

@app.route('/language_pie_data')
def language_pie_data():
    # 提供資料
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')  # 確保 dataset 資料夾和 CSV 文件存在
    df = pd.read_csv(dataset_path)

    # 確保 'Hours Viewed' 為數字類型
    df['Hours Viewed'] = df['Hours Viewed'].replace(',', '', regex=True).astype(float)

    # 計算每個語言的總觀看時數
    language_viewership = df.groupby('Language Indicator')['Hours Viewed'].sum().reset_index()
    language_viewership = language_viewership.sort_values(by='Hours Viewed', ascending=False)

    # 轉換為前端需要的格式
    data = {
        "labels": language_viewership['Language Indicator'].tolist(),
        "values": language_viewership['Hours Viewed'].tolist()
    }
    return jsonify(data)

@app.route('/release-month')
def release_month_bar():
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')
    df = pd.read_csv(dataset_path)

    # 將 Release Date 轉換為 datetime
    df['Release Date'] = pd.to_datetime(df['Release Date'])
    df['Release Month'] = df['Release Date'].dt.month

    # 清理數據：確保 'Hours Viewed' 為數字
    df['Hours Viewed'] = (
        df['Hours Viewed']
        .replace(',', '', regex=True)  # 去掉逗號
        .fillna(0)  # 填充空值為 0
        .astype(float)  # 轉換為浮點數
    )

    # 分組統計
    monthly_viewership = df.groupby('Release Month')['Hours Viewed'].sum()
    monthly_releases = df.groupby('Release Month').size()

    # 確保所有月份都有數據，即使為 0
    months = list(range(1, 13))
    viewership_values = [round(monthly_viewership.get(month, 0), 2) for month in months]
    release_values = [int(monthly_releases.get(month, 0)) for month in months]

    # 返回 JSON 數據
    data = {
        "months": months,  # [1, 2, ..., 12]
        "values": viewership_values,  # 總觀看時數
        "monthly_releases": release_values  # 每月發布數量
    }
    return jsonify(data)


@app.route('/release-weekly')
def release_weekly():
    # 模擬數據讀取，替換為你的 CSV 文件路徑
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')
    df = pd.read_csv(dataset_path)

    # 數據處理：將 Release Date 轉換為 Weekday
    df['Release Date'] = pd.to_datetime(df['Release Date'])
    df['Weekday'] = df['Release Date'].dt.day_name()

    # 每周發佈數量和觀看時數
    weekday_releases = df['Weekday'].value_counts().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    df['Hours Viewed'] = (
        df['Hours Viewed']
        .replace(',', '', regex=True)
        .astype(float)
    )
    weekday_viewership = df.groupby('Weekday')['Hours Viewed'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    # 返回 JSON 數據
    data = {
        "weekdays": weekday_releases.index.tolist(),
        "releases": weekday_releases.values.tolist(),
        "viewership": [round(v / 1e9, 2) for v in weekday_viewership.values]  # 以 "B" 為單位
    }
    return jsonify(data)

# 重要節日
important_dates = pd.to_datetime([
    '2023-01-01',  # 新年
    '2023-02-14',  # 情人節
    '2023-10-31',  # 萬聖節
    '2023-12-25'   # 聖誕節
])

@app.route('/holiday_release')
def holiday_release():
    dataset_path = os.path.join('dataset', 'netflix_content_2023.csv')
    df = pd.read_csv(dataset_path)

    # 將 Release Date 轉換為 datetime
    df['Release Date'] = pd.to_datetime(df['Release Date'])

    # 篩選假期前後 3 天的影片發布
    holiday_releases = df[df['Release Date'].apply(
        lambda x: any((x - date).days in range(-3, 4) for date in important_dates)
    )]

    # 假期影片數量
    holiday_release_count = len(holiday_releases)
    # 總影片數量
    total_release_count = len(df)

    # 返回 JSON 格式數據
    data = {
        "holiday_release_count": holiday_release_count,
        "non_holiday_release_count": total_release_count - holiday_release_count,
        "holiday_releases": holiday_releases.to_dict('records')  # 假期影片的詳細數據
    }
    return jsonify(data)

# 啟動 Flask 應用
if __name__ == '__main__':
    app.run(debug=True)





