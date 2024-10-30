# 使用官方 Python 3.9 作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录中的内容复制到工作目录中
COPY . .

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口 5000 供 Flask 使用
EXPOSE 5000

# 运行 Flask 应用程序
CMD ["python", "./run.py"]
