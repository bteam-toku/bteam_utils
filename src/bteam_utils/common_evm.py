from .common_calendar import CommonCalendar
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CommonEVMInput:
    """EVM入力データクラス
    """
    status_ended:bool = False # 終了ステータスフラグ
    status_ongoing:bool = False # 作業中ステータスフラグ
    status_notyet:bool = False # 未着手ステータスフラグ
    status_onhold:bool = False # 保留ステータスフラグ
    status_reject:bool = False # 却下ステータスフラグ
    start_date:date = None # 開始日
    due_date:date = None # 期日
    actual_start_date:date = None # 実開始日
    actual_due_date:date = None # 実終了日
    done_ratio:float = float(0) # 進捗率
    estimated_hours:float = float(0) # 予定工数
    spent_hours:float = float(0) # 作業工数

class CommonEVM:
    """EVM計算クラス
    """
    # EVM基本指標
    __pv:float = float(0) # PV(計画価値)
    __ev:float = float(0) # EV(出来高)
    __ac:float = float(0) # AC(実コスト)
    # EVM管理指標
    __sv:float = float(0) # SV(スケジュール差異)
    __cv:float = float(0) # CV(コスト差異)
    __spi:float = float(0) # SPI(スケジュール効率指数)
    __cpi:float = float(0) # CPI(コスト効率指数)
    # EVM予測指標
    __bac:float = float(0) # BAC(予算総額)
    __etc:float = float(0) # ETC(残作業コスト予測)
    __eac:float = float(0) # EAC(完了時コスト予測)
    __vac:float = float(0) # VAC(完了時コスト差異)

    # 丸め桁数定義
    __round:int = 3 #　丸め桁数(FIXED)

    # 入力データ
    __input_data:CommonEVMInput = None
    __as_of_date:date = None

    # 算出データ
    __totaol_days:int = 0 # 総作業日数
    __spent_days:int = 0 # 当日作業日数

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self) -> None:
        """コンストラクタ
        """
        pass
    
    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    #
    # publicメソッド
    #
    def calculate(self) -> None:
        """EVM計算メソッド
        """
        self.__calculate()

    def set_input_data(self, input_data:CommonEVMInput, as_of_date:date, calendar:CommonCalendar) -> None:
        """EVM入力データ設定メソッド

        Args:
            input_data (CommonEVMInput): EVM入力データ
            as_of_date (date): 評価日
        """
        # 入力データ設定
        self.__input_data = input_data
        self.__as_of_date = as_of_date

        # 進捗データ計算
        # 却下ステータスは対象外
        if(self.__input_data.status_reject is False):
            # 日程計画がある場合に作業日数を計算する
            if(self.__input_data.start_date is None) or (self.__input_data.due_date is None):
                # 総作業日数
                self.__totaol_days = 0
                # 当日作業日数
                self.__spent_days = 0
            else:
                # 総作業日数
                self.__totaol_days = calendar.count_businessday(self.__input_data.start_date, self.__input_data.due_date)
                # 当日作業日数
                self.__spent_days = calendar.count_businessday(self.__input_data.start_date, self.__as_of_date)
        else:
            # 総作業日数
            self.__totaol_days = 0
            # 当日作業日数
            self.__spent_days = 0
    
    def get_pv(self) -> float:
        """PV取得メソッド

        Returns:
            float: PV値
        """
        return self.__pv
    
    def get_ev(self) -> float:
        """EV取得メソッド

        Returns:
            float: EV値
        """
        return self.__ev
    
    def get_ac(self) -> float:
        """AC取得メソッド

        Returns:
            float: AC値
        """
        return self.__ac
    
    def get_sv(self) -> float:
        """SV取得メソッド

        Returns:
            float: SV値
        """
        return self.__sv
    
    def get_cv(self) -> float:
        """CV取得メソッド

        Returns:
            float: CV値
        """
        return self.__cv
    
    def get_spi(self) -> float:
        """SPI取得メソッド

        Returns:
            float: SPI値
        """
        return self.__spi
    
    def get_cpi(self) -> float:
        """CPI取得メソッド

        Returns:
            float: CPI値
        """
        return self.__cpi
    
    def get_bac(self) -> float:
        """BAC取得メソッド

        Returns:
            float: BAC値
        """
        return self.__bac
    
    def get_etc(self) -> float:
        """ETC取得メソッド

        Returns:
            float: ETC値
        """
        return self.__etc
    
    def get_eac(self) -> float:
        """EAC取得メソッド

        Returns:
            float: EAC値
        """
        return self.__eac
    
    def get_vac(self) -> float:
        """VAC取得メソッド

        Returns:
            float: VAC値
        """
        return self.__vac

    #
    # privateメソッド(EVM)
    #
    def __calculate(self) -> None:
        """EVM計算メソッド
        """
        self.__pv = self.__calculate_pv()
        self.__ev = self.__calculate_ev()
        self.__ac = self.__calculate_ac()
        self.__sv = self.__calculate_sv()
        self.__cv = self.__calculate_cv()
        self.__spi = self.__calculate_spi()
        self.__cpi = self.__calculate_cpi()
        self.__bac = self.__calculate_bac()
        self.__etc = self.__calculate_etc()
        self.__eac = self.__calculate_eac()
        self.__vac = self.__calculate_vac()

    def __calculate_pv(self) -> float:
        """PV計算メソッド
        PV = 予定工数　×　当日作業日数　÷　総作業日数

        Returns:
            float: PV値
        """
        # 日程未計画の場合
        if(self.__input_data.start_date is None) or (self.__input_data.due_date is None):
            # PV = 0
            self.__pv = float(0)
        # 予定作業期間内(総作業日数 > 当日作業日数)の場合
        elif(self.__spent_days < self.__totaol_days):
            try:
                # PV = 予定工数　×　当日作業日数　÷　総作業日数
                self.__pv = (self.__input_data.estimated_hours * self.__spent_days) / self.__totaol_days
            except Exception:
                # PV=0
                self.__pv = float(0)
        # 予定作業期間外(総作業日数 <= 当日作業日数)の場合
        else:
            # PV = 予定工数
            self.__pv = self.__input_data.estimated_hours
        # PVを丸めて復帰
        self.__pv = round(self.__pv,self.__round)
        return self.__pv

    def __calculate_ev(self) -> float:
        """EV計算メソッド
        EV = 予定工数　×　進捗率　※終了ステータスは進捗率100%とみなす

        Returns:
            float: EV値
        """
        # 終了ステータスの場合は進捗率100%とみなす
        if(self.__input_data.status_ended == True):
            # EV = 予定工数
            self.__ev = self.__input_data.estimated_hours
        else:
            # EV = 予定工数　×　進捗率
            self.__ev = (self.__input_data.estimated_hours * self.__input_data.done_ratio) / float(100)
        # 丸めて復帰
        self.__ev = round(self.__ev,self.__round)
        return self.__ev

    def __calculate_ac(self) -> float:
        """AC計算メソッド
        AC = 作業工数

        Returns:
            float: AC値
        """
        # AC = 作業工数
        self.__ac = self.__input_data.spent_hours
        # 丸めて復帰
        self.__ac = round(self.__ac,self.__round)
        return self.__ac

    def __calculate_sv(self) -> float:
        """SV計算メソッド
        SV = EV - PV

        Returns:
            float: SV値
        """
        # SV = EV - PV
        self.__sv = self.__ev - self.__pv
        # 丸めて復帰
        self.__sv = round(self.__sv,self.__round)
        return self.__sv

    def __calculate_cv(self) -> float:
        """CV計算メソッド
        CV = EV - AC

        Returns:
            float: CV値
        """
        # CV = EV - AC
        self.__cv = self.__ev - self.__ac
        # 丸めて復帰
        self.__cv = round(self.__cv,self.__round)
        return self.__cv

    def __calculate_spi(self) -> float:
        """SPI計算メソッド
        SPI = EV ÷ PV

        Returns:
            float: SPI値
        """
        # SPI = EV ÷ PV
        try:
            self.__spi = self.__ev / self.__pv
        except:
            self.__spi = float(1)
        # 丸めて復帰
        self.__spi = round(self.__spi,self.__round)
        return self.__spi

    def __calculate_cpi(self) -> float:
        """CPI計算メソッド
        CPI = EV ÷ AC

        Returns:
            float: CPI値
        """
        # CPI = EV ÷ AC
        try:
            self.__cpi = self.__ev / self.__ac
        except:
            self.__cpi = float(1)
        # 丸めて復帰
        self.__cpi = round(self.__cpi,self.__round)
        return self.__cpi

    def __calculate_bac(self) -> float:
        """BAC計算メソッド
        BAC = 予定工数

        Returns:
            float: BAC値
        """
        # BAC = 予定工数
        self.__bac = self.__input_data.estimated_hours
        # 丸めて復帰
        self.__bac = round(self.__bac,self.__round)
        return self.__bac

    def __calculate_etc(self) -> float:
        """ETC計算メソッド
        ETC = (BAC-EV) ÷ CPI

        Returns:
            float: ETC値
        """
        # ETC = (BAC-EV) ÷ CPI
        try:
            self.__etc = (self.__bac - self.__ev) / self.__cpi
        except:
            self.__etc = float(0)
        # 丸めて復帰
        self.__etc = round(self.__etc,self.__round)
        return self.__etc

    def __calculate_eac(self) -> float:
        """EAC計算メソッド
        EAC = AC + ETC

        Returns:
            float: ETC値
        """
        # EAC = AC + ETC
        self.__eac = self.__ac + self.__etc
        # 丸めて復帰
        self.__eac = round(self.__eac,self.__round)
        return self.__eac

    def __calculate_vac(self) -> float:
        """VAC計算メソッド
        VAC = BAC - EAC

        Returns:
            float: VAC値
        """
        # VAC = BAC - EAC
        self.__vac = self.__bac - self.__eac
        # 丸めて復帰
        self.__vac = round(self.__vac,self.__round)
        return self.__vac
