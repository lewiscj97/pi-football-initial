#!/usr/bin/python

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import datetime

import time


class Scraper:
    def __init__(self):
        self.link = "https://www.bbc.co.uk/sport/football/scores-fixtures"
        self.browser = webdriver.Chrome('/Users/lewisjones/PycharmProjects/Bits/chromedriver')
        self.block = ""
        self.matches = []

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
        home_team = []
        away_team = []

        for match in matches:
            """
            Names
            """
            if "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport" in str(match):
                team_name = match.find_all('span',
                                           class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
                team_names.append(team_name)

            elif "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft" in str(match):
                team_name = match.find_all('span',
                                           class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
                team_names.append(team_name)

        # Names
        for x in range(len(team_names)):
            home_team.append(team_names[x][0].text)
            away_team.append(team_names[x][1].text)

        print(home_team)
        print(away_team)

    def get_scores(self, matches):
        home_scores = []
        away_scores = []
        home_score = []
        away_score = []
        yet_to_start = []

        for match in range(len(matches)):
            """
            Scores
            """
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

        # Scores
        # Home
        for x in range(len(home_scores)):
            home_score.append(home_scores[x][0].text)

        # Away
        for x in range(len(away_scores)):
            away_score.append(away_scores[x][0].text)

        print(home_score)
        print(away_score)
        # print(yet_to_start)

    def get_times(self, matches):
        times = []
        time_list = []

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
            time_list.append(time[0].text)

        print(time_list)


s = Scraper()
s1 = s.open_pages()
blocks = s.get_match_blocks(s1)
prem_block = s.identify_block(blocks, "French Ligue 1")
matches = s.find_all_matches(prem_block)
s.get_team_names(matches)
s.get_scores(matches)
s.get_times(matches)
