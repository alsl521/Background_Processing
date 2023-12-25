class Result:
    """
    表示操作结果的类。

    Attributes:
        code (int): 结果代码。
        msg (str): 结果消息。
        data (any): 结果数据。

    """

    def __init__(self, code=None, msg=None, data=None):
        """
        初始化操作结果。

        Args:
            code (int, optional): 结果代码。默认为None。
            msg (str, optional): 结果消息。默认为None。
            data (any, optional): 结果数据。默认为None。

        """
        self.code = code
        self.msg = msg
        self.data = data

    def to_dict(self):
        """
        将结果转换为字典形式。

        Returns:
            dict: 结果的字典表示。

        """
        return {
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        }

    @classmethod
    def success(cls, data=None):
        """
        创建成功的结果对象。

        Args:
            data (any, optional): 结果数据。默认为None。

        Returns:
            Result: 成功的结果对象。

        """
        result = cls()
        result.code = 1
        result.data = data
        return result

    @classmethod
    def error(cls, msg=None):
        """
        创建失败的结果对象。

        Args:
            msg (str, optional): 结果消息。默认为None。

        Returns:
            Result: 失败的结果对象。

        """
        result = cls()
        result.code = 0
        result.msg = msg
        return result
