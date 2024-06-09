import json
import pathlib
import typing as t
import jieba
import openpyxl
import xlsxwriter
import xml.etree.ElementTree as ET
from requests import Response, sessions, exceptions
from PySide6 import QtCore
from loguru import logger
from app.interface import common


class RequestThread(QtCore.QThread):
    success = QtCore.Signal(Response)
    failure = QtCore.Signal(Exception)
    finish = QtCore.Signal()

    def __init__(self, api: t.Union[str] = '', method: t.Union[str] = 'GET',
                 params: t.Dict[str, str] = None, data: t.Union[t.Dict, bytes] = None,
                 headers: t.Dict[str, str] = None, cookies: t.Dict[str, str] = None,
                 parent=None):
        super().__init__(parent)
        self.base_url = 'https://api.bilibili.com/x/web-interface'
        self.api = api
        self.method = method
        self.params = params or {}
        self.data = data or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.proxies = {"http": None, "https": None}

    @property
    def url(self):
        return f'{self.base_url}{self.api}'

    def set_proxy(self, proxies: t.Dict):
        self.proxies = proxies

    def send_request(self):
        kwargs = {
            'headers': self.headers,
            'params': self.params,
            'proxies': self.proxies
        }
        if isinstance(self.data, dict):
            kwargs['data'] = json.dumps(self.data).encode('utf-8')
        elif isinstance(self.data, bytes):
            kwargs['data'] = self.data
        else:
            kwargs['data'] = b''

        with sessions.Session() as session:
            return session.request(method=self.method, url=self.url, **kwargs)

    def run(self):
        try:
            response = self.send_request()
            self.success.emit(response)
        except Exception as e:
            logger.debug(f'API请求异常：{self.api}')
            logger.exception(e)
            self.failure.emit(e)

        self.finish.emit()

    def stop(self):
        try:
            self.success.disconnect()
        except RuntimeError:
            pass
        try:
            self.failure.disconnect()
        except RuntimeError:
            pass
        try:
            self.finish.disconnect()
        except RuntimeError:
            pass
        self.quit()
        self.wait()


class PreloadThread(QtCore.QThread):
    sendMessage = QtCore.Signal(str)
    sendProgress = QtCore.Signal(int)
    close = QtCore.Signal()
    runtimeError = QtCore.Signal(str)

    def __init__(self, all_execute: bool = True, work_method: t.Callable = None, parent=None):
        super().__init__(parent=parent)
        self.all_execute = all_execute
        self.work_method = work_method
        self.running = False
        self.works = {
            self.initialize: (0.1, '正在检查运行环境'),
            self.get_rank_datas: (0.4, '正在获取排行榜数据'),
            self.read_rank_datas: (0.1, '正在读取排行榜数据'),
            self.get_comments: (0.3, '正在获取弹幕内容'),
            self.read_comments: (0.1, '正在读取评论内容'),
        }
        self.total_score = 0

    def initialize(self):
        pathlib.Path(common.rank_data_path).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(common.comments_of_first_path).parent.mkdir(parents=True, exist_ok=True)

    def get_rank_datas(self):
        try:
            if not pathlib.Path(common.rank_data_path).exists():
                request_thread = RequestThread(parent=self)
                request_thread.api = "/ranking/v2"
                request_thread.method = "GET"
                request_thread.params = {
                    'rid': '0',
                    'type': 'all',
                    'web_location': '333.934',
                    'w_rid': 'f124f82521585afecf815dc6639f2f06',
                    'wts': '1717563767',
                }
                request_thread.headers = common.headers
                request_thread.cookies = common.cookies
                response = request_thread.send_request()
                datas = response.json().get('data').get('list')

                common.settings.setValue('first_cid', datas[0]['cid'])

                wb = xlsxwriter.Workbook(common.rank_data_path)
                sheet = wb.add_worksheet("Sheet1")
                for i, data in enumerate(datas):
                    stat = data['stat']
                    view = stat['view']
                    dianzhan = stat['like']
                    toubi = stat['coin']
                    shoucang = stat['favorite']
                    danmu = stat['danmaku']
                    pinglun = stat['reply']
                    zhuanfa = stat['share']

                    for j, t in enumerate([i + 1, view, dianzhan, toubi, shoucang, danmu, pinglun, zhuanfa]):
                        sheet.write(i, j, t)

                wb.close()
        except (KeyError, AttributeError, NameError, ValueError):
            raise RuntimeError('获取排行榜数据失败')

    def read_rank_datas(self):
        if pathlib.Path(common.rank_data_path).exists():
            wb = openpyxl.load_workbook(common.rank_data_path)
            common.rank_data = [value for value in wb.worksheets[0].values]
            logger.debug(f'获取排行榜数据：\n{common.rank_data[:5]}')

    def get_comments(self):
        if not pathlib.Path(common.comments_of_first_path).exists():
            request_thread = RequestThread(parent=self)
            request_thread.base_url = 'https://comment.bilibili.com'
            request_thread.api = f'/{common.settings.value("first_cid")}.xml'
            request_thread.method = "GET"
            request_thread.headers = common.headers
            request_thread.cookies = common.cookies
            response = request_thread.send_request()
            with open(common.comments_of_first_path, 'wb') as fw:
                fw.write(response.content)

    def read_comments(self):
        if pathlib.Path(common.comments_of_first_path).exists():
            tree = ET.parse(common.comments_of_first_path)
            root = tree.getroot()
            comments = root.findall('d')
            common.comments_of_first = [comment.text for comment in comments]
            logger.debug(f'获取弹幕列表：\n{common.comments_of_first[:5]}')
            common.jieba_comments = jieba.lcut(''.join(common.comments_of_first))
            logger.debug(f'获取分词后的列表：\n{common.jieba_comments[:5]}')

    def run(self):
        try:
            if self.all_execute:
                for callback, info in self.works.items():
                    score = info[0]
                    msg = info[1]
                    if self.total_score >= 100:
                        break
                    self.sendMessage.emit(f"{msg}...")
                    callback()
                    self.total_score += int(100 * score)
                    self.sendProgress.emit(self.total_score)
                    self.msleep(100)
                    logger.debug(f'预加载：{msg} (完成{self.total_score}%)')
            else:
                if not self.work_method:
                    raise RuntimeError('未指定工作方法')
                self.work_method()
                logger.debug(f'指定完成工作方法：{self.work_method.__name__}')
            self.finished.emit()
        except exceptions.ConnectionError:
            self.close.emit()
        except RuntimeError as e:
            self.runtimeError.emit(str(e))
        except Exception as e:
            logger.exception(e)
            self.close.emit()

    def stop(self):
        self.running = False
        self.wait()
