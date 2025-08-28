from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
