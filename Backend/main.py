from websocket import *
from Classes import *


def main():

	print(game.running)

	#Start Websocket server
	asyncio.run(startWSS())


if __name__ == "__main__":
	main()