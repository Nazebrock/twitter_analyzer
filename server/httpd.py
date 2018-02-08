#!/usr/bin/env python3
# -*- coding:  utf-8
import socket
import random
import json
import http.server
import socketserver
import urllib.parse
from twitter_db import TwitterDB


class HttpHandler(http.server.SimpleHTTPRequestHandler):
    """Implementation d'un handler http simple:
        - fournit des fichiers (via SimpleHTTPRequestHandler)
        - parse et execute des commandes passées via des paramètres GET"""


    def __init__(self, *args, **kwargs):
        self._session_id = None
        self.db = TwitterDB()
        super().__init__(*args, **kwargs)


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_JSON(self, json):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.encode(encoding='utf_8'))
        return

    def do_GET(self):
        """Méthode à surcharger pour répondre à une requête HTTP get"""

        #Parsing the l'URL
        parsed_url = urllib.parse.urlparse(self.path)
        #Extraction des paramètres GET sous la forme d'un dictionnaire python
        #?p1=v1&p2=v2&...&pn=vn devient { 'p1' : ['v1'], …, 'pn':['vn'] }
        #Les paramètres de même noms sont fusionnés:
        #?p=v1&p=v2  devient { 'p': [ 'v1', 'v2' ]
        parameters = urllib.parse.parse_qs(parsed_url.query)
        print ("Resource : '" + parsed_url.path+"'")
        print ("Paramètres : "+str(parameters))

        content = ""

        #Search query
        if parsed_url.path == "/search":
            print("Search Query")
            self.send_JSON('{"count": 1732, "hashtags": {"love": 1, "crazycatady": 1, "MuslimBanProtest": 10, "job": 22, "jfkprotest": 8, "MuslimBanprotest": 36, "UVA": 1, "Job": 8, "fwx": 1, "Schick": 1, "Sampdoria": 1, "StopPresidentBannon": 14, "sachabaroncohen": 1, "immigration": 5, "Contest": 2, "win": 5, "openaccess": 1, "Oregon": 1, "motorbikes": 1, "mamasporelmundo": 1, "AFP": 1, "MattRiddle": 1, "Houston": 2, "PositivityBot": 1, "MUFC": 1, "Manufacturing": 1, "contest": 3, "fuckem": 1, "Belleville": 1, "protest": 4, "UniteBlue": 1, "housing": 1, "ProtestInTheUSA": 2, "KeystoneXL": 1, "Retweet": 1, "Periscope": 3, "nobannowallsat": 1, "bbcworldwide": 1, "ban": 1, "Bahrain": 1, "fabulousnight": 1, "naked": 1, "LiveOnK2": 1, "Sales": 1, "BiggBoss10": 1, "PrimairesGauche": 1, "hamon": 1, "DC": 2, "Nurses": 1, "DeleteUber": 2, "FreeSouthernCameroon": 1, "BUEA": 1, "Bamenda": 1, "ProtestforPeaceinMiddleEast": 1, "MakeThatChange": 1, "womenintech": 1, "PodemosEnMovimiento": 1, "SuperMajority": 1, "Dulles": 2, "Chicago": 1, "dinosaurs": 1, "ChristianBlogger": 1, "divini": 1, "Indianapolis": 1, "RescindRacism": 2, "HouSuperBowl": 1, "Hounews": 1, "pbs103": 1, "savelinkas": 2, "Fox61": 1, "Bogot\u00e1SinToreo": 1, "DesMoinesProtests": 1, "Highland": 1, "free": 2, "tests": 1, "RiseUp": 1, "stoptheban": 1, "music": 1, "wholesome": 1, "USA": 1, "lifestyle": 1, "Twitler": 1, "Immigrantban": 1, "Shame": 1, "MSM": 1, "google": 1, "Oreca07": 1, "Huskers": 1, "valls": 1, "MuslimBan": 199, "dating": 1, "PhillyResistance": 12, "Clerical": 1, "BatteryPark": 15, "ForensicFavor": 1, "BocaRaton": 1, "regionsbank": 1, "eventprofs": 1, "NoMuslimBanSFO": 1, "WatchDogs2": 1, "NYC": 6, "Muslim": 1, "Eugene": 1, "CareerArc": 14, "muslimban": 6, "johnny": 2, "EvilDead": 1, "trump": 1, "PHL": 2, "IT": 1, "RantwithAnt": 1, "prizes": 3, "BogotaMejorSinToreo": 1, "SinToreoPorLaPaz": 1, "Lorton": 1, "RT": 2, "TheFlexxPistoia": 1, "quotestoliveby": 1, "problem": 1, "socialmedia": 3, "bdlprotest": 1, "RentControl": 1, "NotMyPresidentTrump": 1, "FakeWallFacts": 1, "WIN": 1, "stnews": 1, "edchat": 1, "FakeOutrage": 1, "RDU": 2, "PAXSouth": 1, "bucharest": 1, "SmallBiz": 1, "Toronto": 1, "Hamon": 1, "betisfcb": 1, "Minooka": 1, "london": 1, "phlairport": 3, "phl": 1, "greatfood": 1, "BreakingNews": 1, "BlackStars": 1, "gamedev": 1, "founders": 1, "entrepreneurs": 2, "fuckreligionanyway": 1, "Whitehouse": 1, "Fox51": 1, "MTP": 1, "NHS": 1, "GROUNDBREAKER": 1, "greece": 1, "travel": 1, "BlueTelecoms": 1, "allarewelcome": 1, "CalExit": 1, "tech": 1, "Manchester": 1, "WarmUpAndWin": 1, "kate": 1, "GBR": 1, "thankyoutrump": 1, "StLouis": 1, "anime": 1, "bbnaija": 1, "hewillnotdivide": 1, "Loveinthecity": 1, "TheResistance": 5, "HeartieArtContest": 1, "Speed": 1, "theworldsgreatest": 1, "worldsgreatestgrandpa": 1, "Dakota": 1, "LAX": 1, "Colorado": 3, "India": 1, "Jobs": 8, "ReleaseTheDetainees": 1, "nextstopCanada": 1, "commonsense": 1, "TravelBan": 3, "XboxOne": 1, "WhiteHouse": 1, "\u4f50\u5009\u7dbe\u97f3": 1, "trumpban": 2, "JFKTerminal4": 1, "Worldnews": 1, "hiring": 8, "nprtinydeskcontest": 1, "Washington": 2, "CrazyExGirlfriend": 1, "hypocrisy": 3, "MySecondChance": 3, "Hayfestival": 1, "BuildTheWall": 2, "OklahomaCity": 1, "ScienceMajorProblems": 1, "ATL": 1, "cartoon": 1, "Satire": 1, "kambala": 1, "StopTheMuslimBan": 1, "seatacprotest": 1, "SFO": 3, "news3lv": 1, "Veterans": 2, "Computers": 1, "CLT": 1, "airportprotest": 1, "Seattle": 1, "BostonMarathonBombing": 1, "IoT": 1, "Mundo": 1, "feynec": 1, "HandsOffJeruslem": 1, "Valls": 1, "WomensMarch": 3, "secureyouraccount": 1, "nowplaying": 1, "Ghana": 1, "StopHatingonTrump": 1, "France": 1, "Rog": 1, "refugees": 1, "science": 1, "CarltonSpeaks": 1, "caridadcristiana": 1, "stupid": 1, "GlobalWarming": 1, "DigiNU": 1, "couchbase": 1, "gainzzz": 1, "IllegitimatePresident": 1, "protestmakesmehungry": 1, "news": 1, "Rolex24": 1, "ForwardNotBack": 1, "Protest": 12, "SB51": 2, "NoMuslimBan": 9, "nomuslimban": 16, "noMuslimbanNewark": 7, "resist": 12, "AZ": 1, "regions": 1, "CONCOURS": 1, "MTVHottest": 1, "WorldSBK": 1, "Portimaotest": 1, "copleysquare": 8, "art": 1, "protests": 1, "jfk": 1, "Resist": 4, "Portland": 1, "daniilivanov": 1, "the": 1, "RefugeeBan": 3, "competition": 2, "WJHL": 1, "aviation": 1, "tomorrowspaper": 1, "immigrationban": 4, "antitrump": 2, "giveaways": 3, "KansasCity": 1, "MCI": 1, "succeed": 1, "washington": 1, "hopenothate": 1, "LiveCam": 1, "SkypeShows": 1, "nobannowall": 1, "Media": 1, "smallbiz": 1, "ThinkBIGSundayWithMarsha": 1, "newrelease": 1, "p2": 1, "NOTOURPRESIDENT": 1, "bailgada": 1, "Federer": 2, "Docker": 1, "roadtoSTOH": 1, "Pittsburgh": 1, "stoptrump": 1, "Datsun": 1, "saintpetersburg": 1, "DWTSME": 1, "WashingtonDC": 1, "dancedancedance": 1, "10cocktailstested": 1, "Cancer": 1, "nancy": 1, "internacional": 1, "protestify": 1, "freenfontem": 1, "AFCON2017": 1, "ProtestMiddleEastViolence": 1, "Latest": 1, "Nadal": 1, "chatbot": 1, "ElectoralCollege": 1, "digitalliteracy": 1, "JFKairport": 1, "video": 1, "goofy": 1, "alphasigma1914": 1, "savelink": 2, "savevideo": 2, "stopMuslimBan": 1, "losers": 1, "LaVerne": 1, "TrumpBan": 1, "DemocraticParty": 1, "Miami": 1, "internship": 1, "bodybuilding2": 1, "DiscoverySport": 1, "Education": 1, "Ayatollah_Qassim": 1, "TrumpPence16": 1, "animenews": 1, "crunchyroll": 1, "refugiados": 1, "seo": 1, "roostertesting": 3, "5yearswithBAEKHYUN": 1, "Hiring": 19, "MAGA": 7, "NBA": 1, "thedivahfilez": 1, "thebuzz": 1, "breakingnews": 1, "MaricopaCounty": 1, "AZSucks": 1, "Banking": 2, "VeranoMTV2016": 1, "RESIST": 2, "Trump": 9, "EndGameDynamics": 1, "Drones": 1, "travelban": 2, "Copley": 1, "climatechange": 1, "atx": 1, "RefugeesWelcome": 4, "deleteuber": 10, "Love": 1, "CharlesTown": 1, "NoBan": 5, "Royals": 1, "Atmore": 1, "AvGeek": 1, "Mooresville": 1, "RHTechJobs": 1, "facebook": 2, "Barakaldo": 1, "GraciasTit\u00e1n": 1, "BBNaija": 1, "amateur": 1, "growthmindset": 1, "united": 1, "Taureau": 1, "5yearswithbaekhyun": 2, "AffordableHousing": 1, "affordablehousing": 1, "bridgesnotwalls": 1, "Immigration": 1, "Motorgiga": 1, "Weekend": 1, "Follow": 1, "refugeesban": 1, "edtech": 1, "Paramus": 2, "GeorgeSoros": 1, "Events": 1, "FakeProtestors": 1, "rediGO": 1, "sweepstakes": 1, "HBDGrissRomero": 1, "German": 1, "CraftHour": 1, "FACTSTHATKICK": 1, "for\u00e7abar\u00e7a": 1, "ChantajeChallengeContest": 1, "SupplyChain": 1, "popefrancis": 1, "tuckcc": 1, "Harrogate": 1, "Views": 1, "tips": 1, "sportsnews": 1, "SouthernCameroon": 1, "freenkongho": 1, "ChillChaser": 1, "ceo": 1, "Ban": 1, "whiteHouseProtest": 1, "stl": 1, "clt": 1, "Stevenson": 1, "News": 1, "MakeAmericaGreatAgain": 1, "FoxNews": 1, "digitaltesting": 1, "DesMoines": 1, "political": 1, "world": 1, "tlot": 1, "contestprep": 1, "Providence": 1, "NOISundays": 1, "TrumpHotel": 1, "TrumpTrain": 2, "latestpost": 1, "marketing": 3, "NoBanNoWall": 103, "HostingCon": 5, "Chandler": 1, "yawn": 1, "teens": 1, "NFL": 1, "Jfk": 1, "DonaldTrump": 1, "JFK": 1, "SachaBaronCohen": 1, "Boston": 10, "wcvb": 2, "Healthcare": 4, "StL": 1, "Win": 3, "avgeek": 1, "antibannon": 2, "laxprotest": 1, "fetish": 1, "femdom": 1, "Skokie": 1, "failure": 1, "Hospitality": 4, "OurNY": 1, "ForzaPistoia": 1, "Milpitas": 1, "BB10GrandFinale": 1, "unityindiversity": 1, "jallikattu": 1, "manveergurjar": 1, "charobs": 1, "impeach": 1, "Giveaway": 1, "Jewelry": 1, "Undraashka_O": 1, "Capitol": 1, "Retail": 3, "f": 1, "HolocaustMemorialDay": 1, "Israel": 1, "YourNewsTweet": 1, "DWTSME_elissa": 1, "noban": 2, "lovethemall": 1, "birthday": 1, "lookbook": 1, "shopping": 1, "b3d": 1, "3d": 1, "NapoliPalermo": 1, "prototype": 1, "Canton": 1, "Cosmetology": 1, "iglesia": 1, "WeStandTogether": 2, "HereToStay": 1, "HMKBreathOfTheWildGiveaway": 1, "PhillyResists": 1, "pbs1914": 1, "Mixcloud": 2, "parttime": 1, "Detroit": 1, "Nursing": 1, "ratpack": 1, "NoWallNoBan": 2, "London": 1, "Marketing": 1, "history": 1, "cruise": 1, "AusOpen": 1, "Deleteyouruberacct": 1, "truelegends": 1, "immagrationban": 1, "Pharmaceutical": 1, "WoodcliffLake": 1, "nomuslimbancmh": 1, "NHLAllStar": 1}, "places": {"MX": 1, "IT": 1, "GB": 3, "DE": 1, "BR": 1, "US": 41, "CL": 1, "FR": 1}}')
            return
            if 'q' not in parameters:
                print("No query parameter")
                self.send_error(404, "No Query parameter (q) found")
            else:
                val = self.db.search(str(parameters['q'][0]))
                if 'hashtags' in val:
                    val['hashtags'] = dict(val['hashtags'])
                if 'places' in val:
                    val['places'] = dict(val['places'])
                val = json.dumps(dict(val))
                print("search done : "+str(val))
                self.send_JSON(val)
        else:
            super().do_GET()


class ExtensibleHttpServer(socketserver.TCPServer):
    """Serveur HTTP qui étend celui donné par défaut. 2 Améilorations
       - on configure la socket pour pouvoir redémarrer immédiatement le serveur
         si jamais on quitte le programme et on le relance (sinon   il
         faut attendre le timeout de la socket)
       - on ajoute une méthode serve_until_interrupted qui rattrape le CTRL-C dans le terminal.
"""

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def serve_until_interrupted(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()
        finally:
            self.server_close()


#Exemple d'utilisation :
#Naviguer sur http://localhost:9010 après avoir lancé le serveur et observer la console

if __name__ == "__main__":
    HTTPD = ExtensibleHttpServer(("127.0.0.1", 9010), HttpHandler)
    HTTPD.serve_until_interrupted()
