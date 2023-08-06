import re

from bs4 import BeautifulSoup


class HowLongToBeatParser:
    found_games_pattern = re.compile(r"We Found (\d+) Games")
    recent_games_pattern = re.compile(r"(\d+) Recently (?:Updated|Added) Games")

    @classmethod
    def parse_game_list(cls, html: str):
        soup = BeautifulSoup(html, "html.parser")

        pages = {}
        for match_string, pattern in {
            ("We Found", cls.found_games_pattern),
            ("Recently Updated Games", cls.recent_games_pattern),
            ("Recently Added Games", cls.recent_games_pattern),
        }:
            games_found_h3 = soup.select_one(f'h3:-soup-contains("{match_string}")')
            if games_found_h3:
                games_found_matches = pattern.findall(games_found_h3.text)
                if len(games_found_matches) == 1:
                    pages["games_found"] = int(games_found_matches[0])

        games = []
        games_list = soup.select("div.search_list_details")
        for game_item in games_list:
            game_name = game_item.h3.a.text.strip()
            game_id = int(game_item.h3.a.get("href").split("id=")[-1])
            game = {"name": game_name, "id": game_id}

            game["times"] = {}
            details_block = game_item.select_one("div.search_list_details_block")
            tidbits = details_block.select("div[class^=search_list_tidbit]")
            current_label = None
            for tidbit in tidbits:
                if current_label:
                    content = tidbit.text.strip()
                    accuracy = 0
                    for block_class in tidbit.get("class"):
                        if block_class.startswith("time_"):
                            accuracy = int(block_class.split("_")[-1])
                    game["times"][current_label] = {
                        "content": content,
                        "accuracy": accuracy,
                    }
                    current_label = None
                else:
                    current_label = tidbit.text.strip()
            games.append(game)

        bottom_h2 = soup.find("h2")
        if bottom_h2:
            bottom_spans = soup.find("h2").find_all("span")
            page = 1
            for span in bottom_spans:
                if "back_blue" in span.get("class") and span.text != "":
                    page = int(span.text)
            pages["page"] = page
            pages["total_pages"] = int(bottom_spans[-1].text)

        return {
            "data": games,
            "pages": pages,
        }
