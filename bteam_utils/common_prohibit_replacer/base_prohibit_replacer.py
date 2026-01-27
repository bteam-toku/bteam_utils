from .abstract_prohibit_replacer import AbstractProhibitReplacer

class BaseProhibitReplacer(AbstractProhibitReplacer):
    """ 禁則文字列置換基底クラス
    """
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
    def replace(self, text: str) -> str:
        """ 禁則文字と予約語を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        text = self._replace_prohibit_characters(text)
        text = self._replace_reserved_words(text)
        return text

    #
    # protectedメソッド
    #
    def _replace_prohibit_characters(self, text: str) -> str:
        """ 禁則文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        for prohibited, safe in self._PROHIBIT_CHARACTERS.items():
            text = text.replace(prohibited, safe)
        return text
    
    def _replace_reserved_words(self, text: str) -> str:
        """ 予約語を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        # 予約語を完全一致していた場合に置換する
        for reserved, safe in self._RESERVED_WORDS.items():
            if text.upper() == reserved.upper():
                text = safe
                break
        return text
    
    def _replace_csv_splitter(self, text: str) -> str:
        """ CSV区切り文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        text = text.replace(',', '，')
        return text
    
    def _truncate_max_length(self, text: str, max_length: int) -> str:
        """ 最大長を超過した場合に切り詰めるメソッド
        Args:
            text (str): 置換対象文字列
            max_length (int): 最大長
        Returns:
            str: 置換後文字列
        """
        if len(text) > max_length:
            text = text[:max_length]
        return text
