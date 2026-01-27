from .base_prohibit_replacer import BaseProhibitReplacer

class RedmineProhibitReplacer(BaseProhibitReplacer):
    """ Redmineの禁則文字を置換するクラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '#': '＃',
    }

    #
    # publicメソッドのoverride
    #
    def replace(self, text: str, is_csv: bool = False, is_truncate: bool = True) -> str:
        """ 禁則文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
            is_csv (bool): CSV出力用かどうか(デフォルト: False)
            is_truncate (bool): 最大長で切り詰めるかどうか(デフォルト: True)
        Returns:
            str: 置換後文字列
        """
        # 親クラスの置換処理を実行
        text = super().replace(text)
        # CSV出力用にカンマを置換
        if is_csv:
            text = self._replace_csv_splitter(text)
        # 最大長を超過している場合は切り詰める
        if is_truncate:
            text = self._truncate_max_length(text, max_length=255)
        # 置換後文字列を返却
        return text
