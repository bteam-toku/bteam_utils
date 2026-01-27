from .base_prohibit_replacer import BaseProhibitReplacer

class TeamsProhibitReplacer(BaseProhibitReplacer):
    """ Teamsの禁則文字を置換するクラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '~': '～',
        '#': '＃',
        '%': '％',
        '&': '＆',
        '*': '＊',
        ':': '：',
        '<': '＜',
        '>': '＞',
        '?': '？',
        '/': '／',
        '\\': '￥',
        '{': '｛',
        '}': '｝',
        '|': '｜',
        '\"': '＂',
    }
    _RESERVED_WORDS: dict[str, str] = {
        'General': '_general_',
        'Files': '_files_',
        'forms': '_forms_',
        'Documents': '_documents_',
        '一般': '_general_',
    }

    #
    # publicメソッドのoverride
    #
    def replace(self, text: str, is_csv: bool = False, is_truncate: bool = True) -> str:
        """ 禁則文字と予約語を置換するメソッド
        Args:
            text (str): 置換対象文字列
            is_csv (bool): CSV出力用かどうか(デフォルト: False)
            is_truncate (bool): 最大長で切り詰めるかどうか(デフォルト: True)
        Returns:
            str: 置換後文字列
        """
        # 親クラスの置換処理を実行
        text = super().replace(text)
        # 末尾のドットを置換する
        text = self._replace_trailing_dots(text)
        # CSV出力用にカンマを置換
        if is_csv:
            text = self._replace_csv_splitter(text)
        # 最大長を超過している場合は切り詰める
        if is_truncate:
            text = self._truncate_max_length(text, max_length=255)
        return text
    
    #
    # protectedメソッド
    #
    def _replace_trailing_dots(self, text: str) -> str:
        """ 末尾のドットを置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        while text.endswith('.'):
            text = text[:-1] + '．'
        return text 