FROM node:20-alpine

WORKDIR /app

# 复制package文件
COPY package*.json ./
RUN npm install

# 复制源码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动
CMD ["npm", "run", "dev"]
