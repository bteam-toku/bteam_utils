class CommonProgress:
    """共通進捗表示クラス
    """
    # protected members
    _total: int = 0  # 総数
    _current: int = 0  # 現在数
    _task_msg: str = ""  # タスクメッセージ
    _status_msg: str = ""  # 状態メッセージ
    _display_type: int = 0  # 表示タイプ

    #
    # constructor / destructor
    #
    def __init__(self, total: int, task_msg: str = "", status_msg: str = "", display_type: int = 0) -> None:
        """コンストラクタ
        Args:
            total (int): 総数
            task_msg (str): タスクメッセージ
            status_msg (str): 状態メッセージ
            display_type (int): 表示タイプ (0:タイプ01)
        """
        self._total = total
        self._current = 0
        self._display_type = display_type
        self.update(current=0, task_msg=task_msg, status_msg=status_msg)

    #
    # public methods
    #
    def update(self,  current: int = -1, task_msg:str = "", status_msg:str = "") -> None:
        """進捗情報更新
        Args:
            current (int): 現在数（指定なしの場合は自動インクリメント）
            task_msg (str): タスクメッセージ
            status_msg (str): 状態メッセージ
        """
        # 情報更新
        self._current = current if current >= 0 else (self._current + 1)
        self._task_msg = task_msg if task_msg else self._task_msg
        self._status_msg = status_msg if status_msg else self._status_msg
        # 表示更新
        self.display()
    
    def complete(self, status_msg: str = "Completed") -> None:
        """進捗完了処理
        Args:
            status_msg (str): 状態メッセージ
        """
        # 最終更新
        self.update(current=self._total, status_msg=status_msg)
        # 改行表示(完了時)
        print()

    def display(self) -> None:
        """進捗表示
        """
        # 表示タイプによる分岐
        match self._display_type:
            case 0:
                self._show_type01()
            case _:
                pass

    #
    # protected methods
    #
    def _show_type01(self):
        """タイプ01の進捗表示

        表示形式は以下の通り
        [#########################-------------------------] 50% | Task Message : Status Message
        """
        # 進捗率計算
        ratio = int((self._current / self._total) * 100) if self._total > 0 else 100
        # 表示ブロック数計算
        display_block_num = 50
        current_block = int((ratio * display_block_num) / 100)
        # 進捗表示
        display_bar = '[' + '#' * current_block + '-' * (display_block_num - current_block) + ']'
        display_output = f"\r{display_bar} {ratio:3}% | {self._task_msg} : {self._status_msg}"
        print(f"{display_output[:150]:<150}", end="", flush=True)

