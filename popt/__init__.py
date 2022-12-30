import random
from typing import Set

import requests

base_url = "https://api.twitter.com/2/"


def fetch(tweet_id: str, bearer_token: str) -> Set[str]:
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + bearer_token})

    likers = [liker.get("username") for liker in session.get(base_url + "tweets/" + tweet_id + "/liking_users").json().get("data", [])]
    print("likers:", ", ".join(likers))

    retweeters = [retweeter.get("username") for retweeter in session.get(base_url + "tweets/" + tweet_id + "/retweeted_by").json().get("data", [])]
    print("retweeters:", ", ".join(retweeters))

    quoters_ids = [quoter.get("author_id") for quoter in session.get(base_url + "tweets/search/recent?tweet.fields=author_id&query=url:" + tweet_id).json().get("data", [])]
    repliers_ids = [replier.get("author_id") for replier in session.get(base_url + "tweets/search/recent?tweet.fields=author_id&query=conversation_id:" + tweet_id).json().get("data", [])]
    qrs = [qr.get("username") for qr in session.get(base_url + "users?ids=" + ",".join(quoters_ids + repliers_ids)).json().get("data", [])]
    print("quoters and repliers:", ", ".join(qrs))

    return set(likers + retweeters + qrs)


def choice(tweet_id: str, usernames: Set[str]) -> str:
    pool = list(usernames)
    pool.sort()

    random.seed(tweet_id.join(pool))
    return random.choice(pool)


def main(tweet_id, bearer_token):
    print("winner:", choice(tweet_id, fetch(tweet_id, bearer_token)))
