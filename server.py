import socketserver, random, re

from init import Game
from bot import callBot

class GameServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.old_timeout = self.request.gettimeout()
        self.new_timeout = 60
        self.request.settimeout(self.new_timeout)

    def handle(self):
        gameInstance = Game()

        isPlayFirst = random.choice([True, False])
        if isPlayFirst:
            gameInstance.setNextTurn(callBot(gameInstance.getInfo()))

        try:
            while not gameInstance.checkGameOver():
                self.request.sendall(bytes(gameInstance.getInfo(), "ASCII"))

                try:
                    temp = self.request.recv(8)
                    ret = str(temp, "ASCII")
                except:
                    self.request.sendall(bytes("ERROR: INVALID ASCII STRING ~ " + repr(temp), "ASCII"))
                    return
                if ret != "NULL" and re.fullmatch("\w\d", ret) is None:
                    self.request.sendall(bytes("ERROR: INVALID INPUT ~ " + repr(ret), "ASCII"))
                    return
                if not gameInstance.setNextTurn(ret):
                    self.request.sendall(bytes("ERROR: INVALID MOVE ~ " + repr(ret), "ASCII"))
                    return

                if not gameInstance.checkGameOver():
                    gameInstance.setNextTurn(callBot(gameInstance.getInfo()))

            self.request.sendall(bytes(gameInstance.getFinalResult(), "ASCII"))
        except:
            return

    def finish(self):
        self.request.settimeout(self.old_timeout)

if __name__ == "__main__":
    HOST, PORT = "", 14003

    with socketserver.TCPServer((HOST, PORT), GameServerHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
