import Parler
from Parler import with_auth as authed
import os

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)

posts_per_feed_page = 20
trending_length = 8
trending_user_length = 6

def test_get_feed():
    assert os.getenv("PARLER_USERNAME") is not None
    assert os.getenv("PARLER_PASSWORD") is not None
    au.login(
        identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
    )
    assert au.is_logged_in
    r1 = au.feed()["data"]
    r2 = au.feed(False, 2, False)["data"]
    r3 = au.feed(False, 3, False)["data"]

    assert len(r1) >= posts_per_feed_page
    assert len(r2) >= posts_per_feed_page-2
    assert len(r3) >= posts_per_feed_page-2

    # deep dive: get IDs of each post in user feed, sort alphabetically, compare against n+1

    fp1 = [x.get("primary").get("uuid") for x in r1]
    fp2 = [x.get("primary").get("uuid") for x in r2]
    fp3 = [x.get("primary").get("uuid") for x in r3]

    fp1.sort()
    fp2.sort()
    fp3.sort()

    assert fp1 != fp2
    assert fp2 != fp3

def test_trending():
    assert len(p.trending("today")["data"]) == trending_length
    assert len(p.trending("top")["data"]) == trending_length

def test_discover_feed():
    r = p.discover_feed()
    assert len(r["data"]) >= posts_per_feed_page

def test_trending_users():
    assert os.getenv("PARLER_USERNAME") is not None
    assert os.getenv("PARLER_PASSWORD") is not None
    au.login(
        identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
    )
    assert au.is_logged_in
    assert len(au.trending_users()) == trending_user_length
