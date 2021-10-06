#!/usr/bin/python

from bs4 import BeautifulSoup
from selenium import webdriver
import time


class Scraper:

    def __init__(self):
        self.link = "https://www.bbc.co.uk/sport/football/scores-fixtures"
        # self.browser = webdriver.PhantomJS('/Users/lewisjones/PycharmProjects/Bits/phantomjs')
        self.browser = webdriver.Chrome('/Users/lewisjones/PycharmProjects/Bits/chromedriver')
        self.block = ""
        self.matches = []
        # self.home_team = []
        # self.away_team = []
        # self.home_score = []
        # self.away_score = []
        # self.time_list = []

    def open_pages(self):
        self.browser.get(self.link)
        time.sleep(1)
        content = self.browser.page_source
        soup = BeautifulSoup(content, features='html.parser')
        self.browser.close()
        return soup

    def get_match_blocks(self, soup):
        match_blocks = soup.find_all('div', class_='qa-match-block')
        return match_blocks

    def identify_block(self, all_blocks, league):
        for block in all_blocks:
            if block.h3.text.strip() == league:
                self.block = block
        return self.block

    def find_all_matches(self, container):
        self.matches = container.find_all('li', class_='gs-o-list-ui__item gs-u-pb-')
        return self.matches

    def get_team_names(self, matches):
        team_names = []

        for match in matches:
            if "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport" in str(match):
                team_name = match.find_all('span',
                                           class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
                team_names.append(team_name)

            elif "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft" in str(match):
                team_name = match.find_all('span',
                                           class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
                team_names.append(team_name)

        for x in range(len(team_names)):
            self.home_team.append(team_names[x][0].text)
            self.away_team.append(team_names[x][1].text)

    def get_scores(self, matches):
        home_scores = []
        away_scores = []
        yet_to_start = []

        for match in range(len(matches)):
            # In play
            if "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport" in str(
                    matches[match]):
                home_scores.append(matches[match].find_all('span',
                                                           class_="sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport"))
                away_scores.append(matches[match].find_all('span',
                                                           class_="sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--live-sport"))

            # Full time
            elif "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft" in str(matches[match]):
                home_scores.append(matches[match].find_all('span',
                                                           class_="sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft"))
                away_scores.append(matches[match].find_all('span',
                                                           class_="sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft"))

            # Yet to start
            elif "sp-c-fixture__number sp-c-fixture__number--time" in str(matches[match]):
                yet_to_start.append(matches[match].find_all('span',
                                                            class_="sp-c-fixture__number sp-c-fixture__number--time"))

        # Home
        for x in range(len(home_scores)):
            self.home_score.append(home_scores[x][0].text)

        # Away
        for x in range(len(away_scores)):
            self.away_score.append(away_scores[x][0].text)

    def get_times(self, matches):
        times = []

        for match in matches:
            if "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport" in str(match):
                time = match.find_all('span',
                                      class_="sp-c-fixture__status gel-brevier sp-c-fixture__status--live-sport")
                times.append(time)

            elif "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft" in str(match):
                time = match.find_all('span',
                                      class_="sp-c-fixture__status sp-c-fixture__status--ft gel-minion")
                times.append(time)

        for time in times:
            self.time_list.append(time[0].text)

    def print_results(self):
        for x in range(len(self.home_team)):
            print(f"{self.home_team[x]:>17} {self.home_score[x]} - {self.away_score[x]} {self.away_team[x]:17}\n"
                  f"{self.time_list[x]:^42}")
            print()


def main(league):
    s = Scraper()
    s1 = s.open_pages()
    blocks = s.get_match_blocks(s1)
    league_block = s.identify_block(blocks, league)
    matches = s.find_all_matches(league_block)
    print(matches)
    # s.get_team_names(matches)
    # s.get_scores(matches)
    # s.get_times(matches)
    # s.print_results()


main("UEFA Nations League")
