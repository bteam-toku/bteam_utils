from abc import ABC, abstractmethod

class AbstractProhibitReplacer(ABC):
    """ 禁則置換抽象クラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {}
    _RESERVED_WORDS: dict[str, str] = {}

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self):
        pass
    
    def __del__(self):
        pass

    #
    # publicメソッド
    #
    @abstractmethod
    def replace(self, text: str) -> str:
        """ 禁則文字列を置換する抽象メソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        pass
    
    #
    # protectedメソッド
    #
    @abstractmethod
    def _replace_prohibit_characters(self, text: str) -> str:
        """ 禁則文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        pass

    @abstractmethod    
    def _replace_reserved_words(self, text: str) -> str:
        """ 予約語を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        pass

    @abstractmethod    
    def _replace_csv_splitter(self, text: str) -> str:
        """ CSV区切り文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        pass

    @abstractmethod    
    def _truncate_max_length(self, text: str, max_length: int) -> str:
        """ 最大長を超過した場合に切り詰めるメソッド
        Args:
            text (str): 置換対象文字列
            max_length (int): 最大長
        Returns:
            str: 置換後文字列
        """
        pass