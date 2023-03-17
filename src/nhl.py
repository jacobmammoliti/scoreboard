import requests
from datetime import date, timedelta


class NHL:
    def __init__(
        self,
        start_date: str = None,
        end_date: str = None,
    ) -> None:
        self.root_url = "https://statsapi.web.nhl.com"

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
        return (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

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
        url = f"{self.root_url}/api/v1/schedule?&startDate={self.start_date}&endDate={self.end_date}&expand=schedule.linescore"

        games = []
        data = self._fetch_data_by_url(url=url)

        for game in data["dates"][0]["games"]:
            current_game = Game(
                self.start_date,
                game["venue"]["name"],
                game["teams"]["home"]["team"]["id"],
                game["teams"]["home"]["team"]["name"],
                game["teams"]["home"]["score"],
                game["linescore"]["teams"]["home"]["shotsOnGoal"],
                game["linescore"]["teams"]["home"]["goaliePulled"],
                game["teams"]["away"]["team"]["id"],
                game["teams"]["away"]["team"]["name"],
                game["teams"]["away"]["score"],
                game["linescore"]["teams"]["away"]["shotsOnGoal"],
                game["linescore"]["teams"]["away"]["goaliePulled"],
            )

            games.append(current_game)

        return games


class Game:
    def __init__(
        self,
        date: str = None,
        venue: str = None,
        home_id: str = None,
        home_name: str = None,
        home_score: str = None,
        home_sog: str = None,
        home_goalie_pulled: str = None,
        away_id: str = None,
        away_name: str = None,
        away_score: str = None,
        away_sog: str = None,
        away_goalie_pulled: str = None,
    ) -> None:
        self.date = date
        self.venue = venue
        self.home_id = home_id
        self.home_name = home_name
        self.home_score = home_score
        self.home_sog = home_sog
        self.home_goalie_pulled = home_goalie_pulled
        self.away_id = away_id
        self.away_name = away_name
        self.away_score = away_score
        self.away_sog = away_sog
        self.away_goalie_pulled = away_goalie_pulled

    def __str__(self) -> str:
        return f"{self.date.ljust(15)} {self.home_name.ljust(25)} {str(self.home_score)} ({str(self.home_sog)}) {str(self.away_score)} ({str(self.away_sog)}) {str(self.away_name).ljust(20)}"
