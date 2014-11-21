import io
import sys
import json

from smoke.io.wrap import demo as io_wrp_dm
from smoke.replay import demo as rply_dm
from smoke.replay.const import Data

class Chat(object):
    def __init__(self, player, message):
        self.player = player
        self.message = message

class Player(object):
    def __init__(self, steamid, username):
        self.steamid = steamid
        self.username = username

class Game(object):
    def __init__(self, gameid, dire_players, radiant_players, chats, end_time, duration):
        self.gameid = gameid
        self.dire_players = dire_players
        self.radiant_players = radiant_players
        self.chats = chats
        self.end_time = end_time
        self.duration = duration

def parse_game(fn):
    with io.open(fn, 'rb') as infile:
        demo_io = io_wrp_dm.Wrap(infile)
        demo_io.bootstrap()

        parse = Data.UserMessages
        demo = rply_dm.Demo(demo_io, parse=parse)
        demo.bootstrap()

        msgs =  [msg for match in demo.play()
                     for msgs in match.user_messages.values()
                     for msg in msgs
                     if hasattr(msg, 'chat') and msg.chat]
        demo.finish()
        overview = demo.match.overview
    radiant = [Player(p['steam_id'], p['player_name']) for p in overview['game']['players'] if p['game_team'] == 2]
    dire = [Player(p['steam_id'], p['player_name']) for p in overview['game']['players'] if p['game_team'] == 3]
    players = {p.username: p for p in (radiant + dire)}
    chats = [Chat(players[msg.prefix], msg.text) for msg in msgs]
    return Game(overview['game']['match_id'], dire, radiant, chats, overview['game']['end_time'], overview['playback']['time'])

if __name__ == '__main__':
    filename = sys.argv[1]
    for filename in sys.argv[1:]:
        game = parse_game(filename)
        print(json.dumps(game, default = lambda o : o.__dict__, indent = 2))

