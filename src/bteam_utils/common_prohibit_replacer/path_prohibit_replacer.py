from .base_prohibit_replacer import BaseProhibitReplacer

class PathProhibitReplacer(BaseProhibitReplacer):
    """ パスの禁則文字と予約語を置換するクラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '\\': '＼',
        '/': '／',
        ':': '：',
        '*': '＊',
        '?': '？',
        '"': '＂',
        '<': '＜',
        '>': '＞',
        '|': '｜',
    }
    _RESERVED_WORDS: dict[str, str] = {
        'CON': '_con_',
        'PRN': '_prn_',
        'AUX': '_aux_',
        'NUL': '_nul_',
        'COM1': '_com1_',
        'COM2': '_com2_',
        'COM3': '_com3_',
        'COM4': '_com4_',
        'COM5': '_com5_',
        'COM6': '_com6_',
        'COM7': '_com7_',
        'COM8': '_com8_',
        'COM9': '_com9_',
        'LPT1': '_lpt1_',
        'LPT2': '_lpt2_',
        'LPT3': '_lpt3_',
        'LPT4': '_lpt4_',
        'LPT5': '_lpt5_',
        'LPT6': '_lpt6_',
        'LPT7': '_lpt7_',
        'LPT8': '_lpt8_',
        'LPT9': '_lpt9_',
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
        # 末尾のドットとスペースを置換する
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
        while text.endswith('.') or text.endswith(' '):
            if text.endswith(' '):
                text = text[:-1] + '＿'
            elif text.endswith('.'):
                text = text[:-1] + '．'
        return text 