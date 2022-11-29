import pandas as pd

class Files(object):
    _count = pd.NA  # 不要直接操作这个变量，也尽量避免访问它

    @property
    def count(self):
        return Files._count

    @count.setter
    def count(self, num):
        Files._count = num