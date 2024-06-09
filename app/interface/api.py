import typing as t
from app.interface import common
from app.pyside6.threads import RequestThread


class RequestProxy(RequestThread):
    def __init__(self, api: t.Union[str] = '', method: t.Union[str] = 'GET',
                 params: t.Dict[str, str] = None, data: t.Union[t.Dict, bytes] = None,
                 headers: t.Dict[str, str] = common.headers, cookies: t.Dict[str, str] = common.cookies,
                 parent=None):
        super().__init__(api, method, params, data, headers, cookies, parent)
