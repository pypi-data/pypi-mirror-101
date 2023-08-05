#encoding:utf-8
class Rclone:
    '''模拟Rclone软件的类'''
    def __init__(self):
        self.__version = 'rclone 15.4.0'

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self,value):
        self.__version = value


if __name__ == '__main__':
    print(Rclone().version)