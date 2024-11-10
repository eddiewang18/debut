# 1. 使用 Node.js 16 映像
FROM node:16-alpine

# 2. 設置工作目錄
WORKDIR /app

# 3. 安裝依賴
COPY ./frontend/package.json ./
RUN npm install
RUN npm install axios
# 4. 複製前端代碼
COPY ./frontend ./

# 5. 編譯 Vue 應用
RUN npm run build

# 6. 使用靜態文件服務器
CMD ["npm", "run", "serve"]