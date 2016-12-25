# fantasy_scraper

A python script to calculate Kicker and D/ST regular season point totals for NFL.com's Fantasy Football.

Requirements:
- python 2.7
- selenium webdriver
- chromedriver or phantomjs (binaries only)
- beautifulsoup 4

Usage:
1. Enter your NFL.com account credentials as USERNAME/PASSWORD variables
2. Change for loop range to match your league's team count
3. run 'python fantasy_scraper.py'
4. output is a csv in [Team #, K Totals, D/ST Totals] format
