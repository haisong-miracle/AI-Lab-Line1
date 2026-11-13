# mdcheck 容器镜像
# 构建: docker build -t mdcheck .
# 运行: docker run --rm -v /宿主机目录:/data mdcheck
FROM python:3.10-slim

WORKDIR /app

# 先复制依赖清单（当前为空，保留分层缓存习惯），再复制源码
COPY requirements.txt ./
COPY main.py ./
COPY mdcheck/ ./mdcheck/

# 工具只依赖 Python 标准库，无需 pip install；
#ENTRYPOINT 固定为工具本体，CMD 提供默认参数（扫描挂载进来的 /data）
ENTRYPOINT ["python", "main.py"]
CMD ["--dir", "/data", "--quiet"]
