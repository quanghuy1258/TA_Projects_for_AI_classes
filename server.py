import socketserver, random, re

from init import Game
from bot import callBot

class GameServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        gameInstance = Game()

        isPlayFirst = random.choice([True, False])
        if isPlayFirst:
            gameInstance.setNextTurn(callBot(gameInstance.getInfo()))
            if gameInstance.checkGameOver():
                self.request.sendall(bytes(gameInstance.getFinalResult(), "ASCII"))

        while not gameInstance.checkGameOver():
            self.request.sendall(bytes(gameInstance.getInfo(), "ASCII"))

            ret = str(self.request.recv(8), "ASCII")
            if ret != "NULL" and re.fullmatch("\w\d", ret) is None:
                self.request.sendall(bytes("ERROR INPUT: " + ret, "ASCII"))
                return
            gameInstance.setNextTurn(ret)

            if not gameInstance.checkGameOver():
                gameInstance.setNextTurn(callBot(gameInstance.getInfo()))

        self.request.sendall(bytes(gameInstance.getFinalResult(), "ASCII"))

if __name__ == "__main__":
    HOST, PORT = "", 14003

    with socketserver.TCPServer((HOST, PORT), GameServerHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
