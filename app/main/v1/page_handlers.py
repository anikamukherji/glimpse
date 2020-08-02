from __future__ import absolute_import

from flask import Blueprint

from main import db

pages = Blueprint("pages", __name__)


@pages.route("/")
def index():
    return "Index"


@pages.route("/profile")
def profile():
    return "Profile"
