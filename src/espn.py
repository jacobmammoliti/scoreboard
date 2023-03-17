import requests
from datetime import date, timedelta, datetime


class ESPN:
    def __init__(
        self,
        start_date: str = None,
        end_date: str = None,
    ) -> None:
        self.root_url = "site.api.espn.com"

        if start_date is None:
            self.start_date = self._get_today_date()
        else:
            self.start_date = start_date

        if end_date is None:
            self.end_date = self._get_today_date()
        else:
            self.end_date = end_date

    def _get_today_date(
        self,
    ) -> str:
        return (date.today() - timedelta()).strftime("%Y%m%d")

    def _fetch_data_by_url(
        self,
        url: str,
    ) -> dict:
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as err:
            return err

        return r.json()

    def get_games(self) -> list:
        url = f"http://{self.root_url}/apis/site/v2/sports/hockey/nhl/scoreboard?dates={self.start_date}-{self.end_date}"

        games = []
        data = self._fetch_data_by_url(url=url)

        for game in data["events"]:
            if game["competitions"][0]["competitors"][0]["homeAway"] == "home":
                home = game["competitions"][0]["competitors"][0]["team"]["displayName"]
                away = game["competitions"][0]["competitors"][1]["team"]["displayName"]
            else:
                home = game["competitions"][0]["competitors"][1]["team"]["displayName"]
                away = game["competitions"][0]["competitors"][0]["team"]["displayName"]

            try:
                odds_details = game["competitions"][0]["odds"][0]["details"]
                over_under = f'T{game["competitions"][0]["odds"][0]["overUnder"]}'
            except KeyError:
                odds_details = "OTB"
                over_under = ""

            current_game = Game(
                date = self.start_date,
                time = game["competitions"][0]["startDate"],
                home_name = home,
                away_name = away,
                odds_details = odds_details,
                over_under = over_under,
            )

            games.append(current_game)

        return games

class Game:
    def __init__(
        self,
        date: str = None,
        time: str = None,
        home_name: str = None,
        away_name: str = None,
        odds_details: str = None,
        over_under: str = None,
    ) -> None:
        self.date = date
        self.time = time
        self.home_name = home_name
        self.away_name = away_name
        self.odds_details = odds_details
        self.over_under = over_under

    def __str__(self) -> str:
        formatted_date = str(datetime.fromisoformat(self.time).date())
        formatted_time = str(datetime.fromisoformat(self.time).time())

        return f"{formatted_date.ljust(10)} {formatted_time.ljust(10)} {self.away_name.ljust(22)} @ {self.home_name.ljust(22)} {self.odds_details.ljust(10)} {str(self.over_under).ljust(25)}"
