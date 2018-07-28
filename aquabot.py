#!/usr/bin/env python

# Standard Python libraries.
import json
import logging
import os
import time

# Third party Python libraries.
# import requests
from botocore.vendored import requests
from bs4 import BeautifulSoup
from TwitterAPI import TwitterAPI

# Custom Python libraries.


# Setup logging
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
rootLogger = logging.getLogger()


class Aquifer:
    """Main Aquifer class."""

    def __init__(self):
        """Initialize Aquifer class."""
        self.url = "https://data.edwardsaquifer.org/j-17.php"
        self.retrieve_twitter_creds()

    def run(self):
        """Retrieve water levels and post to Twitter."""
        today_water_level, yesterday_water_level, ten_day_average = self.fetch_levels()
        message = "The J-17 Bexar aquifer level is {}. Yesterday, it was {} and the 10-day average is {}".format(
            today_water_level, yesterday_water_level, ten_day_average
        )
        message = "The J-17 Bexar aquifer level is {}.  Yesterday, it was {} and the 10-day average is {}.".format(
            today_water_level, yesterday_water_level, ten_day_average
        )

        # Update Twitter.
        self.post_tweet(message)

    def fetch_levels(self):
        """Retrieve water levels from edwardsaquifer.org site."""
        rootLogger.info("[*] Fetching water levels...")

        headers = {"User-Agent": "Edwards Aquifer Bot - Follow on Twitter: @edwardsaquabot"}

        response = requests.get(self.url, headers=headers, verify=True, timeout=60)
        if response.status_code != 200:
            rootLogger.error(
                "HTTP status code: {} -- unsuccessfully retrieved: {}".format(response.status_code, self.url)
            )
            return

        # Use beautiful soup to grab the levels...works, maybe not the best though.
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table")[1]

        # Today's Reading.
        column = table.find_all("td")[0]
        today_water_level = column.find("span").contents[0].strip()

        # Yesterday's Reading.
        column = table.find_all("td")[2]
        yesterday_water_level = column.find("span").contents[0].strip()

        # 10 Day Average Reading.
        column = table.find_all("td")[4]
        ten_day_average = column.find("span").contents[0].strip()

        return today_water_level, yesterday_water_level, ten_day_average

    def retrieve_twitter_creds(self):
        with open("twitter_creds.json", "r") as json_file:
            self.twitter_creds = json.loads(json_file.read())

    def post_tweet(self, message):
        """Tweet message to Twitter."""
        twitter = TwitterAPI(
            # os.environ["consumerKey"],
            # os.environ["consumerSecret"],
            # os.environ["accessToken"],
            # os.environ["accessTokenSecret"],
            self.twitter_creds["consumerKey"],
            self.twitter_creds["consumerSecret"],
            self.twitter_creds["accessToken"],
            self.twitter_creds["accessTokenSecret"],
        )

        request = twitter.request("statuses/update", {"status": message})

        status_code = request.status_code
        if status_code == 200:
            rootLogger.info("Successfully tweeted: {}".format(message))
        else:
            rootLogger.error("HTTP status code: {} -- unsuccessfully tweeted: {}".format(status_code, message))


def log_timestamp():
    """Retrieve a pre-formated datetimestamp."""
    now = time.localtime()
    timestamp = time.strftime("%Y%m%d_%H%M%S", now)
    return timestamp


def lambda_handler(event, context):
    """AWS Lambda wrapper function."""
    try:
        aq = Aquifer()
        aq.run()

        return "Completed"

    except (Exception, KeyboardInterrupt) as e:
        return "Error occurred"
