# 1. 使用 python 3.9 映像
FROM python:3.9-slim

# 安裝系統依賴，包括 pkg-config 和 MySQL 開發庫
RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. 設置工作目錄
WORKDIR /app

# 3. 複製本地的 requirements.txt 並安裝依賴
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r /app/requirements.txt

# 4. 複製專案檔案
COPY ./backend /app

# 5. 允許 Django 的埠
EXPOSE 8000
