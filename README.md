## 项目：BB-Top-100

> 采集哔哩哔哩 Top100 视频的弹幕、点赞、投币、转发等数据量，从而进行简单数据分析的 PySide6 项目。

## 一、环境部署

1. 安装 `poetry`：
    ```bash
    pip install poetry==1.8.2 -i "https://mirrors.cloud.tencent.com/pypi/simple/"
    ```

2. 安装项目依赖：
    ```bash
    poetry lock
    poetry install
    ```

## 二、快速开发

使用 `poetry` 运行项目：
```bash
poetry run python .\manage.py
```

- **重点文件**
  - app.interface.common.py：配置文件，存储常用的全局变量、界面以及饼图等颜色字体配置等
  - app.pyside6.threads.py：常用线程，特别是预加载线程，负责提前检查环境、数据
  - app.pyside6.main_graph.py：存储内容页的五个图像（弹幕文字云、饼图、柱状图、折线图等）

## 三、可执行程序

1. 使用 `PyInstaller` 打包项目：
    ```bash
    pyinstaller .\main.spec
    ```

2. 复制 `assets` 目录到打包输出目录：
    ```bash
    cp .\assets\ .\dist\bilibili-data\ -r
    ```
