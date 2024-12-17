# 使用 Python 3.10 的官方映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製所有檔案到容器內
COPY . /app

# 安裝必要的套件
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 8080 埠供 Flask 使用
EXPOSE 8080

# 啟動 Flask 應用程式
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
