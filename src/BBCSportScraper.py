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
                # print(block.h3.text.strip())
                self.block = block
        return self.block

    def find_all_matches(self, container):
        self.matches = container.find_all('li', class_='gs-o-list-ui__item gs-u-pb-')
        return self.matches

    def get_scores(self, matches):
        home_team = []
        away_team = []
        home_score = []
        away_score = []
        time = []
        team_names = []
        for match in matches:
            # home team
            team_name = match.find_all('span',
                                       class_="gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc")
            team_names.append(team_name)

        # Match 1
        # Home
        print(team_names[0][0].text)
        # Away
        print(team_names[0][1].text)

        # Match 2
        # Home
        print(team_names[1][0].text)
        # Away
        print(team_names[1][1].text)


        """
        Run this code - will see that team_names is a list, which I need to iterate through and take the text from each
        team_names[0] is home, team_names[1] is away
        Then, append these to the home_team and away_team lists
        """

s = Scraper()
s1 = s.open_pages()
blocks = s.get_match_blocks(s1)
prem_block = s.identify_block(blocks, "Russian Premier League")
matches = s.find_all_matches(prem_block)
s.get_scores(matches)
