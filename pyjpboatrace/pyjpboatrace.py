import datetime
from logging import Logger, getLogger
from typing import Any, Dict, Optional, Union

from selenium import webdriver

from . import operator, scraper
from .drivers import create_httpget_driver
from .user_information import UserInformation
from .validator import validate_date, validate_race, validate_stadium


class PyJPBoatrace(object):
    """Python-based Japanese Boatrace Tools Class

    Attributes:
        Stadiums (scraper.StadiumsScraper)
        Races (scraper.RacesScraper)
        RaceInfo (scraper.RaceInfoScraper)
        JustBeforeInfo (scraper.JustBeforeInfoScraper)
        WinPlaceshowOdds (scraper.WinPlaceshowOddsScraper)
        QuinellaplaceOdds (scraper.QuinellaplaceOddsScraper)
        ExactaQuinellaOdds (scraper.ExactaQuinellaOddsScraper)
        TrioOdds (scraper.TrioOddsScraper)
        TrifectaOdds (scraper.TrifectaOddsScraper)
        Result (scraper.ResultScraper)

        Bet (operator.BettingOperator)
        Depost (operator.DepositOperator)
        Withdraw (operator.WithdrawOperator)
        BettingLimitCheck (operator.BettingLimitCheckOperator)

    """

    def __init__(
        self,
        driver: Union[
            webdriver.remote.webdriver.WebDriver, None
        ] = create_httpget_driver(),
        user_information: Optional[UserInformation] = None,
        close_driver_when_closing_pyjpboatrace: bool = True,
        logger: Logger = getLogger(__name__),
    ):
        """Python-based Japanese Boatrace Tools Class

        Args:
            driver (Union[webdriver.remote.webdriver.WebDriver, None], optional): webdriver.
                Defaults to create_httpget_driver().
                If None is given, requests is used.
            user_information (Optional[UserInformation], optional): user information. Defaults to None.  # noqa
            close_driver_when_closing_pyjpboatrace (bool, optional): If True, close driver when calling self.close(). Defaults to True.  # noqa
            logger (Logger, optional): logger. Defaults to getLogger(__name__).  # noqa
        """
        self.__driver = driver
        self.__user_information = user_information
        self.__close_driver_when_closing_pyjpboatrace = (
            close_driver_when_closing_pyjpboatrace  # noqa
        )
        self.__logger = logger

        self.Stadiums = scraper.StadiumsScraper(driver)
        self.Races = scraper.RacesScraper(driver)
        self.RaceInfo = scraper.RaceInfoScraper(driver)
        self.JustBeforeInfo = scraper.JustBeforeInfoScraper(driver)
        self.WinPlaceshowOdds = scraper.WinPlaceshowOddsScraper(driver)
        self.QuinellaplaceOdds = scraper.QuinellaplaceOddsScraper(driver)
        self.ExactaQuinellaOdds = scraper.ExactaQuinellaOddsScraper(driver)
        self.TrioOdds = scraper.TrioOddsScraper(driver)
        self.TrifectaOdds = scraper.TrifectaOddsScraper(driver)
        self.Result = scraper.ResultScraper(driver)

        self.Bet = operator.BettingOperator(user_information, driver)
        self.Depost = operator.DepositOperator(user_information, driver)
        self.Withdraw = operator.WithdrawOperator(user_information, driver)
        self.BettingLimitCheck = operator.BettingLimitCheckOperator(
            user_information, driver
        )  # noqa

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.__driver and self.__close_driver_when_closing_pyjpboatrace:
            self.__driver.close()
            self.__logger.info("Closed the driver")

    def get_stadiums(self, d: datetime.date) -> Dict[str, Any]:
        """Get stadiums where races are held on the given day.

        Args:
            d (datetime.date): race date

        Raises:
            ValueError: Occurred when invalid date given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        return self.Stadiums.get(d)

    def get_12races(self, d: datetime.date, stadium: int) -> Dict[str, Any]:
        """Get 12 races held in the given stadium on the given date.

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        return self.Races.get(d, stadium)

    def get_race_info(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:  # noqa
        """Get race information.

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.RaceInfo.get(d, stadium, race)

    def get_odds_win_placeshow(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get win/placeshow odds

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.WinPlaceshowOdds.get(d, stadium, race)

    def get_odds_quinellaplace(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get quinellaplace odds

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.QuinellaplaceOdds.get(d, stadium, race)

    def get_odds_exacta_quinella(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get exacta/quinella odds

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.ExactaQuinellaOdds.get(d, stadium, race)

    def get_odds_trifecta(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get trifecta odds

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.TrifectaOdds.get(d, stadium, race)

    def get_odds_trio(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get trio odds

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.TrioOdds.get(d, stadium, race)

    def get_just_before_info(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get just-before race information

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.JustBeforeInfo.get(d, stadium, race)

    def get_race_result(
        self, d: datetime.date, stadium: int, race: int
    ) -> Dict[str, Any]:
        """Get race result.

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.
            race (int): race no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return self.Result.get(d, stadium, race)

    def deposit(self, num_of_thousands_yen: int) -> None:
        """To deposit money.

        Args:
            depo_amt_unit_thousands_yen (int): the amount of deposit.

        Raises:
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
        """
        # deposit
        self.Depost.do(
            num_of_thousands_yen,
        )

    def get_bet_limit(self) -> int:
        """To check the amount of money deposited.

        Raises:
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.

        Returns:
            int: the amount of deposited money
        """
        # get bet limit
        return self.BettingLimitCheck.do()

    def withdraw(self) -> None:
        """To withdraw deposit.

        Raises:
            ZeroDepositException:
                Occurred when no deposit.
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
        """
        # withdraw
        self.Withdraw.do()

    def bet(
        self,
        stadium: int,
        race: int,
        trifecta_betting_dict: Dict[str, int] = {},
        trio_betting_dict: Dict[str, int] = {},
        exacta_betting_dict: Dict[str, int] = {},
        quinella_betting_dict: Dict[str, int] = {},
        quinellaplace_betting_dict: Dict[str, int] = {},
        win_betting_dict: Dict[str, int] = {},
        placeshow_betting_dict: Dict[str, int] = {},
    ) -> bool:
        """To bet money on the race.

        Args:
            stadium (int): stadium no.
            race (int): race no.
            trifecta_betting_dict (Dict[str, int], optional):
                Betting dictionary for trifecta.
                Defaults to {}.
                e.g. {"1-2-3": 100, }
            trio_betting_dict (Dict[str, int], optional):
                Betting dictionary for trio.
                Defaults to {}.
                e.g. {"1=2=3": 100, }
            exacta_betting_dict (Dict[str, int], optional):
                Betting dictionary for exacta.
                Defaults to {}.
                e.g. {"1-2": 100, }
            quinella_betting_dict (Dict[str, int], optional):
                Betting dictionary for quinella.
                Defaults to {}.
                e.g. {"1=2": 100, }
            quinellaplace_betting_dict (Dict[str, int], optional):
                Betting dictionary for quinellaplace.
                Defaults to {}.
                e.g. {"1=3": 100, }
            win_betting_dict (Dict[str, int], optional):
                Betting dictionary for win.
                Defaults to {}.
                e.g. {"1": 100, }
            placeshow_betting_dict (Dict[str, int], optional):
                Betting dictionary for placeshow.
                Defaults to {}.
                e.g. {"1": 100, }

        Raises:
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
            ZeroDepositException:
                Occurred when no deposit.
            InactiveStadium:
                Occurred when stadium no. is valid but no races are there.
            InactiveRace:
                Occurred when race no. is valid but the race is probabily over.
            InsufficientDepositException:
                Occurred when the sum of your bet is greater than deposit.

        Returns:
            bool: whether betting is succeeded

        NOTE:
            betdict keys:
                'win',
                'placeshow',
                'exacta',
                'quinella',
                'quinellaplace',
                'trifecta',
                'trio',

        TODO: to create the data structure for betting dict.
        """
        # create bet dict
        betdict = {
            "trifecta": trifecta_betting_dict,
            "trio": trio_betting_dict,
            "exacta": exacta_betting_dict,
            "quinella": quinella_betting_dict,
            "quinellaplace": quinellaplace_betting_dict,
            "win": win_betting_dict,
            "placeshow": placeshow_betting_dict,
        }

        # bet
        return self.Bet.do(stadium=stadium, race=race, betdict=betdict)
