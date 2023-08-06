import json
import requests
from mcwrapper import exceptions

class Hypixel:
    "Hypixel Stats. Takes a username and api key"
    def __init__(self, username : str, apikey : str):
        self.username = username
        self.apikey = apikey


    def stats(self):
        data = requests.get(f"https://api.hypixel.net/player?key={self.apikey}&name={self.username}").json()
        if "player" not in data:
            raise exceptions.NotFound("Either api key invalid or player name invalid!")


            
        self.firstLogin = data["player"]["firstLogin"]
        self.lastLogin = data["player"]["lastLogin"]
        self.namehistory = data["player"]["knownAliases"]
        self.display = data["player"]["displayname"]



                

class Bedwars:
    "Bedwars Stats. Takes a username and api key"
    def __init__(self, username : str, apikey : str):
        self.username = username
        self.apikey = apikey

    def stats(self):
        data = requests.get(f"https://api.hypixel.net/player?key={self.apikey}&name={self.username}").json()
        if "player" not in data:
            raise exceptions.NotFound("Either api key invalid or player name invalid!")


        self.display = data["player"]["displayname"]
        self.wins = data["player"]["achievements"]["bedwars_wins"]
        self.level = data["player"]["achievements"]["bedwars_level"]
        self.deaths = data["player"]["stats"]["Bedwars"]["deaths_bedwars"]
        self.kills = data["player"]["stats"]["Bedwars"]["kills_bedwars"]
        self.coins = data["player"]["stats"]["Bedwars"]["coins"]
        self.beds_lost = data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"]
        self.beds_destroyed = data["player"]["stats"]["Bedwars"]["beds_broken_bedwars"]
        self.final_kills = data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
        self.final_deaths = data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
        self.winstreak = data["player"]["stats"]["Bedwars"]["winstreak"]
        self.losses = data["player"]["stats"]["Bedwars"]["losses_bedwars"]




class Skywars:
    "Skywars Stats. Takes a username and api key"
    def __init__(self, username : str, apikey : str):
        self.username = username
        self.apikey = apikey

    def stats(self):
        data = requests.get(f"https://api.hypixel.net/player?key={self.apikey}&name={self.username}").json()
        if "player" not in data:
            raise exceptions.NotFound("Either api key invalid or player name invalid!")

    
        
        self.display = data["player"]["displayname"]
        self.coins = data["player"]["stats"]["SkyWars"]["coins"]
        self.kills = data["player"]["stats"]["SkyWars"]["kills"]
        self.deaths = data["player"]["stats"]["SkyWars"]["deaths"]
        self.wins = data["player"]["stats"]["SkyWars"]["wins"]
        self.losses = data["player"]["stats"]["SkyWars"]["losses"]
        self.winstreak = data["player"]["stats"]["SkyWars"]["win_streak"]
        self.souls = data["player"]["stats"]["SkyWars"]["souls"]
        self.heads = data["player"]["stats"]["SkyWars"]["heads"]


