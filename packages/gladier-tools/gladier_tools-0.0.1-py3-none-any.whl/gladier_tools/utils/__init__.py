from gladier import GladierBaseTool


__all__ = ['HttpsDownloadFile', 'Unzip']

from .https_download_file import *
from .unzip_file import *

HttpsDownloadFile = GladierBaseTool()
HttpsDownloadFile.flow_definition = {}
HttpsDownloadFile.funcx_functions = [
        https_download_file
    ]

UnzipFile = GladierBaseTool()
UnzipFile.flow_definition = {}
UnzipFile.funcx_functions = [
        unzip_file
    ]

