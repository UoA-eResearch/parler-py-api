from re import sub
from Parler import Parler
import json
import requests
import string, random


class AuthSession(Parler):

    """
    Functions for logging in - which require initialization
    """

    def login(self, identifier: str, password: str) -> dict:

        data = json.dumps(
            {"identifier": identifier, "password": password, "device_id": ""}
        )
        response = self.post(
            "/functions/sessions/authentication/login/login.php", data=data
        )
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.login(identifier=identifier, password=password)
        return response.json()

    """
    Functions that require authentication but are non-signed-user facing
    """

    """
    :param limit: limit
    :param cursor: string to id the next items
    """

    def feed(
        self,
        hide_echoes: bool = False,
        cursor: int = 1,
        subscriptions_only: bool = False,
    ) -> dict:
        files = {
            "page": (None, cursor),
            "hide_echoes": (None, hide_echoes),
            "subscriptions_only": (None, subscriptions_only),
        }
        response = self.post("pages/feed.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.feed(
                hide_echoes=hide_echoes,
                cursor=cursor,
                subscriptions_only=subscriptions_only,
            )
        return response.json()

    """
    :param searchtag: search term
    """

    def users(self, searchtag: str = "") -> dict:
        files = {"s": (None, searchtag), "type": (None, "user")}
        response = self.post("pages/search-results.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.users(searchtag=searchtag)
        return response.json()

    """
    :param searchtag: Hashtag to search
    """

    def hashtags(self, searchtag="") -> dict:
        files = {"s": (None, searchtag), "type": (None, "hashtags")}
        response = self.post("pages/search-results.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.users(searchtag=searchtag)
        return response.json()

    def followers(self, creator_id, limit=10, cursor="") -> dict:
        raise self.NotSupportedException

    """
    :param username: username
    :param cursor: cursor
    """

    def following(self, username: str = "", cursor: int = 1) -> dict:
        files = {
            "page": (None, cursor),
            "user": (None, username),
        }
        response = self.post("pages/feed.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.following(cursor=cursor, username=username)
        return response.json()

    """
    :param post_id: post id
    :param cursor: cursor
    """

    def comments(self, post_id: str = "", cursor: int = 0) -> dict:
        params = {
            "post_id": post_id,
            "page": cursor,
        }
        response = self.get("functions/post_comments.php", params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.comments(post_id=post_id, cursor=cursor)
        return response.json()

    """
    Functions that require authentication for interfacing with the current signed in user
    """

    """
    :param username: username
    """

    def follow_user(self, username) -> dict:
        return self.UnimplementedException

    """
    :param item_type: type of created items to list ("post" or "comment")
    :param username: username to get posts or comments
    :param limit: limit
    :param cursor: string to id the next items
    """

    def created_items(self, item_type="post", username="", limit=10, cursor="") -> dict:
        return self.UnimplementedException

    """
    :param item_type: type of item to delete ("post" or "comment")
    :param id: id of item to delete
    """

    def delete_item(self, item_type, id):
        return self.UnimplementedException

    """
    :param limit: limit
    :param cursor: string to id the next items
    """

    def notifications(self, limit=10, cursor="") -> dict:
        return self.UnimplementedException