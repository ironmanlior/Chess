#!/usr/bin/python

import socket, threading, select, random
from Engine import Game, Status, Color
from DB import User, GameDB
from Socket import Socket
from datetime import timedelta

class Server(object):
    def __init__(self):
        self.socket = Socket()
        self.connections: dict[Socket, User] = {}
        game_types: dict[float, list[Socket]] = {}
        print(socket.gethostbyname(socket.gethostname()))
        try:
            self.socket.bind((socket.gethostbyname(socket.gethostname()), 7949))
        except socket.error as e:
            print(e)
        self.socket.listen()
        print("Server listening")

        while True:
            for conn, addr in self.socket.iter_accept():
                conn: Socket = conn
                try:
                    user: User = conn.recv()
                    game_time: float = conn.recv()
                    print(f"Connected to {user.username} at {addr}")
                    self.connections[conn] = user
                    try:
                        game_types[game_time].append(conn)
                    except KeyError as e:
                        game_types[game_time] = [conn]
                except Exception as e:
                    continue
            for game_time, players in game_types.items():
                players.sort(key=lambda player: self.connections[player].rating)
                game_types[game_time] = list(filter(lambda player: player.fileno() != -1, players))
                for player in players:
                    if player.fileno() == -1:
                        self.connections.pop(player)
                        player.close()
                while len(players) > 1:
                    gamers = sorted(players[:2], key = lambda _: random.random())
                    game_types[game_time] = players = players[2:]
                    thread = threading.Thread(target=self.run, args=(gamers, game_time))
                    thread.start()

    
    def run(self, players: list[Socket], game_time: int):
        
        game = Game(timedelta(seconds=game_time))
        for i in range(len(players)):
            players[i].send((self.connections[players[1 - i]], Color(1 - i)))
            players[i].send(game)
            players[i].setblocking(False)
        
        try:
            while True:
                for i in range(len(players)):
                    player = players[i]
                    while True:
                        socks = select.select([player], [], [], .001)[0]
                        game.check_timer()
                        for sock in players:
                            if sock.is_closed():
                                game.status = Status.resign
                                raise socket.error(game.current[int(sock != player)].name)
                        try:
                            recv = socks[0].recv()
                            if recv: game: Game = recv
                            else: continue
                            players[1 - i].send(game)
                            if game.status not in [Status.null, Status.check]:
                                raise Exception(game.current[0].name)
                        except Exception as e:
                            continue
        except Exception as e:
            score: float = .5 if game.status in [Status.draw, Status.repetition, Status.pate] else 1
            color = Color(1 - Color[f"{e}"].value)
            winner: User = self.connections.pop(players[color.value])
            losser: User = self.connections.pop(players[1 - color.value])
            try:
                for player in players:
                    player.send(color)
            except Exception as e:
                pass
        winner.end_game(losser.rating, game.k, score)
        losser.end_game(winner.rating, game.k, score)
        l = [self.connections.pop(players[i]) for i in range(2)]
        GameDB(game, l).save()
        for i in range(2):
            players[i].close()
    
if __name__ == "__main__":
    Server()
    