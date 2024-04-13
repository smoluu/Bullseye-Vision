class Game():

  def __init__(self) -> None:

    self.running = False
    self.playerNames = []
    self.playerScores = []
    self.settings = {}



def startGame(playerNames, gameOptionScore, gameOptionIn, gameOptionOut):
  game = Game()
  game.playerNames = playerNames
  game.settings["score"] = gameOptionScore
  game.settings["in"] = gameOptionIn
  game.settings["out"] = gameOptionOut
  game.running = True
  print("Game started")

