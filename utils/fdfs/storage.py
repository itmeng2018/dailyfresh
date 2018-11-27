from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    '''FastDFS文件存储类'''

    def __init__(self, client_conf=None, fdfs_url=None):
        '''
        :param client_conf: 如果不指定, 默认调用setting文件
        :param fdfs_url: 如果不指定, 默认调用setting文件
        '''
        self.clint_conf = settings.FDFS_CLIENT_CONF if client_conf is None else client_conf
        self.fdfs_url = settings.FDFS_URL if fdfs_url is None else fdfs_url

    def _open(self, name, mode='rb'):
        '''
        打开文件时使用
        :param name: 打开文件的名字
        :param mode: 打开文件的模式
        :return:
        '''
        pass

    def _save(self, name, content):
        '''
        保存文件时使用
        :param name: 所选择上传文件的名字
        :param content: 包含上传文件内容的File对象
        :return: 返回的被保存文件的ID
        '''

        # 创建一个Fdfs_client的对象
        client = Fdfs_client(self.clint_conf)

        # 上传文件到FastDFS系统中
        result = client.upload_by_buffer(content.read())
        '''
        上传文件到FastDFS返回的是内容(dict):
        {
            'Group name': group_name,
            'Remote file_id': remote_file_id,
            'Status': 'Upload successed.',
            'Local file name': '',
            'Uploaded size': upload_size,
            'Storage IP': storage_ip
        }
        '''

        if result.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到FastDFS失败')

        # 获取返回的文件ID
        file_name = result.get('Remote file_id')

        return file_name

    def exists(self, name):
        '''
        Django判断文件名是否可用
        :param name:
        :return: False: 表示文件名永远可用
        '''
        return False

    def url(self, name):
        '''
        Django返回访问文件的url路径
        :param name:
        :return: 访问文件的url路径
        '''
        return self.fdfs_url + name
