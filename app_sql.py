from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()

# 初始化 Flask 應用
app = Flask(__name__)

# MySQL 資料庫配置
username = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db_name = os.getenv("MYSQL_DB")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 定義資料表模型 (需與 MySQL 資料表結構一致)
class ContentData(db.Model):
    __tablename__ = 'content_data'
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Available_Globally = db.Column(db.Boolean)
    Release_Date = db.Column(db.Date)
    Hours_Viewed = db.Column(db.Integer)
    Language_Indicator = db.Column(db.String(50))
    Content_Type = db.Column(db.String(100))

# 主頁面路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('index-2.html')

# 圖表資料的 API 路由
@app.route('/chart-data')
def generate_chart():
    # 從資料庫讀取數據
    results = db.session.query(
        ContentData.Content_Type,
        db.func.sum(ContentData.Hours_Viewed)
    ).group_by(ContentData.Content_Type).all()
    
    # 組裝 JSON 格式，確保 values 是數字
    data = {
        'labels': [row[0] for row in results],
        'values': [float(row[1]) for row in results]  # 強制轉換為數字
    }
    return jsonify(data)

@app.route('/chart-data-2')
def generate_chart_2():
    # 讀取並轉換資料庫中的日期和觀看數據
    results = db.session.query(
        db.func.month(ContentData.Release_Date).label('month'),
        db.func.sum(ContentData.Hours_Viewed).label('total_hours'),
        db.func.count(ContentData.id).label('total_releases')
    ).group_by('month').all()

    months = list(range(1, 13))
    monthly_hours = {row[0]: row[1] for row in results}
    monthly_releases = {row[0]: row[2] for row in results}

    # 返回資料
    data = {
        "months": months,
        "monthly_releases": [monthly_releases.get(m, 0) for m in months],
        "monthly_viewership": [monthly_hours.get(m, 0) for m in months]
    }
    return jsonify(data)

@app.route('/datatable')
def datatable():
    # 從資料庫取得觀看數據前 10 名
    top_10 = ContentData.query.order_by(ContentData.Hours_Viewed.desc()).limit(10).all()

    # 組裝資料
    data = [
        {
            "Title": row.Title,
            "Hours Viewed": row.Hours_Viewed,
            "Language Indicator": row.Language_Indicator,
            "Content Type": row.Content_Type,
            "Release Date": row.Release_Date
        }
        for row in top_10
    ]
    return jsonify(data)

@app.route('/language_pie_data')
def language_pie_data():
    # 計算每個語言的總觀看時數
    results = db.session.query(ContentData.Language_Indicator, db.func.sum(ContentData.Hours_Viewed)).group_by(ContentData.Language_Indicator).order_by(db.func.sum(ContentData.Hours_Viewed).desc()).all()

    # 組裝 JSON 格式
    data = {
        "labels": [row[0] for row in results],
        "values": [round(float(row[1]) / 1e9, 2) for row in results]  # 轉換為 Billion
    }
    return jsonify(data)

@app.route('/release-month')
def release_month_bar():
    # 讀取資料庫中的發布月份和觀看時數
    results = db.session.query(
        db.func.month(ContentData.Release_Date).label('month'),
        db.func.sum(ContentData.Hours_Viewed).label('total_hours'),
        db.func.count(ContentData.id).label('release_count')
    ).group_by('month').all()

    # 確保所有月份都有數據
    months = list(range(1, 13))
    monthly_hours = {row[0]: row[1] for row in results}
    monthly_releases = {row[0]: row[2] for row in results}

    data = {
        "months": months,
        "values": [round(monthly_hours.get(m, 0), 2) for m in months],
        "monthly_releases": [monthly_releases.get(m, 0) for m in months]
    }
    return jsonify(data)

@app.route('/release-weekly')
def release_weekly():
    # 讀取每周的發布數量和觀看時數
    results = db.session.query(
        db.func.dayname(ContentData.Release_Date).label('weekday'),
        db.func.count(ContentData.id).label('release_count'),
        db.func.sum(ContentData.Hours_Viewed).label('total_hours')
    ).group_by('weekday').all()

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_data = {row[0]: (row[1], float(row[2])) for row in results}

    data = {
        "weekdays": weekdays,
        "releases": [weekly_data.get(day, (0, 0))[0] for day in weekdays],
        "viewership": [round(weekly_data.get(day, (0, 0))[1] / 1e9, 2) for day in weekdays]  # 以 "B" 為單位
    }
    return jsonify(data)

@app.route('/holiday_release')
def holiday_release():
    # 重要節日
    important_dates = [
        dt(2023, 1, 1),  # 新年
        dt(2023, 2, 14),  # 情人節
        dt(2023, 10, 31),  # 萬聖節
        dt(2023, 12, 25)   # 聖誕節
    ]

    # 查詢假期前後 3 天內的影片
    date_ranges = [date + timedelta(days=i) for date in important_dates for i in range(-3, 4)]
    holiday_releases = ContentData.query.filter(ContentData.Release_Date.in_(date_ranges)).all()

    total_releases = ContentData.query.count()

    data = {
        "holiday_release_count": len(holiday_releases),
        "non_holiday_release_count": total_releases - len(holiday_releases),
        "holiday_releases": [
            {
                "Title": row.Title,
                "Release Date": row.Release_Date,
                "Hours Viewed": row.Hours_Viewed,
                "Content Type": row.Content_Type
            } for row in holiday_releases
        ]
    }
    return jsonify(data)

# 啟動 Flask 應用
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))  # 預設為 8080
    app.run(host='0.0.0.0', port=port)
