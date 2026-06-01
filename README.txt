# 专注孵化器：动态存储后端版

## 技术栈
- 前端：HTML+CSS+JS
- 后端：Python Flask
- 数据库：SQLite

## 运行方式
1. 解压文件夹
2. 在 VS Code 打开该文件夹
3. 终端执行：
   pip install -r requirements.txt

4. 启动：
   python app.py

5. 浏览器打开：
   http://127.0.0.1:5000

## 说明
- 小鸡数量、累计孵蛋分钟、当前蛋进度会写入 focus_data.db
- 刷新网页后数据仍然保留
- 如果要公网链接，不能只传 HTML，需要把整个 Flask 项目部署到 Render / Railway / PythonAnywhere 等支持 Python 后端的平台
