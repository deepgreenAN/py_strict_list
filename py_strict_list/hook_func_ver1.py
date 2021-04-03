class HookFunc():
    """
    後から追加可能なコーラブル
    """
    def __init__(self):
        self._func_list = []
    
    def add(self, func):
        if callable(func):
            self._func_list.append(func)
    
    def __call__(self):
        for func in self._func_list:
            func()  # 引数の無い関数の実行
    
    @property
    def func_list(self):
        return self._func_list


if __name__ == "__main__":
    pass