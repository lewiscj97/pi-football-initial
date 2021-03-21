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
        # print("link found")
        self.browser.close()
        return soup

    def get_match_blocks(self, soup):
        match_blocks = soup.find_all('div', class_='qa-match-block')
        # print(match_blocks)
        return match_blocks

    def identify_block(self, all_blocks, league):
        for block in all_blocks:
            if block.h3.text.strip() == league:
                self.block = block
        return self.block

    def find_all_matches(self, container):
        self.matches = container.find_all('li', class_='gs-o-list-ui__item gs-u-pb-')
        return self.matches

    def get_scores(self, matches):
        team_names = []
        home_scores = []
        away_scores = []
        home_team = []
        away_team = []
        home_score = []
        away_score = []
        time = []

        for match in matches:
            """
            Names
            """
            team_name = match.find_all('span',
                                       class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
            team_names.append(team_name)

            """
            Scores
            """
            home_scores.append(match.find_all('span',
                                              class_="sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport"))
            away_scores.append(match.find_all('span',
                                              class_="sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--live-sport"))

        # Names
        for x in range(len(team_names)):
            home_team.append(team_names[x][0].text)
            away_team.append(team_names[x][1].text)

        # Scores
        # Home
        for x in range(len(home_scores)):
            home_score.append(home_scores[x][0].text)

        # Away
        for x in range(len(away_scores)):
            away_score.append(away_scores[x][0].text)

        # print(home_team)
        # print(home_score)
        # print(away_team)
        # print(away_score)


s = Scraper()
s1 = s.open_pages()
blocks = s.get_match_blocks(s1)
prem_block = s.identify_block(blocks, "Scottish Premiership")
matches = s.find_all_matches(prem_block)
s.get_scores(matches)

