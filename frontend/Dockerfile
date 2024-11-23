# 使用 Node.js 16 Alpine 基礎映像
FROM node:16-alpine

# 設置工作目錄
WORKDIR /app

# 複製專案檔案到容器
COPY ./frontend/package*.json ./

# 安裝依賴
RUN npm install

COPY ./frontend ./
# 啟動 Vite 開發伺服器
CMD ["npm", "run", "dev"]
