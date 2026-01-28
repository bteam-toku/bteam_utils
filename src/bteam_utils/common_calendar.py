from datetime import datetime, date
import pandas as pd
import holidays

class CommonCalendar:
    _buzzday:pd.offsets.CustomBusinessDay = None # 営業日リスト

    LIMIT_DATE = date(2020,1,1) # 検索制限日付

    def __init__(self, holiday_list:list=None) -> None:
        """コンストラクタ
        
        Args:
            holiday_list (list): 休日リスト
        """
        if holiday_list is not None:
            # カスタム休日リスト設定
            self._buzzday = pd.offsets.CustomBusinessDay(holidays=holiday_list)
        else:
            # 日本の祝日設定
            start_year = self.LIMIT_DATE.year
            years = range(start_year, datetime.now().year + 3)
            holiday_list = holidays.country_holidays('JP', years=years).keys()
            self._buzzday = pd.offsets.CustomBusinessDay(holidays=list(holiday_list))

    def __del__(self) -> None:
        pass

    def is_holiday(self, target_date:date) -> bool:
        """ 休日判定

        Args:
            target_date (datetime.date): 判定対象日
        Returns:
            bool: True=休日, Flase=営業日
        """
        return not self._buzzday.is_on_offset(target_date)

    def get_recent_weekday(self, target_date:date) -> date:
        """ 直近営業日を取得

        Args:
            target_date (datetime.date): 判定対象日
        Returns:
            datetime.date: 直近営業日の日付
        """
        return self._buzzday.rollback(target_date).date()

    def get_firstday_week(self, target_date:date) -> date:
        """ 週初日取得

        Args:
            target_date (datetime.date): 判定対象日
        Returns:
            datetime.date: 週初日の日付
        """
        return pd.Timestamp(target_date).to_period('W').start_time.date()

    def get_firstday_month(self, target_date:date) -> date:
        """ 月初日取得

        Args:
            target_date (datetime.date): 判定対象日
        Returns:
            datetime.date: 月初日の日付
        """
        return pd.Timestamp(target_date).to_period('M').start_time.date()

    def count_businessday(self, start_date:date, end_date:date) -> int:
        """ 営業日数取得

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            int: 営業日数
        """
        return len(pd.date_range(start=start_date, end=end_date, freq=self._buzzday))
    