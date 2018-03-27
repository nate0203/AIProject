'''
	Nathan Ly
	AI project for MiniCamelot Game.
'''
import Tkinter
from Tkinter import *
import timeit
import time

# Board class, shows position of pieces on the board
class Board(Tkinter.Frame):
	# create the actual board and positions of pieces
	def __init__(self, parent):
		Tkinter.Frame.__init__(self, parent)
		game.title("Mini Camelot")
		self.cv = Canvas(game, width=335, height=560)
		self.cv.pack()

		for j in range(0, 14):
			for i in range(0, 8):
				self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Tan", tags="square")
				if j == 0 or j == 13:
					if i <= 2 or i >= 5:
						self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Red", tags="sqaure")
				if j == 1 or j == 12:
					if i <= 1 or i >= 6:
						self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Red", tags="square")
				if j == 2 or j == 11:
					if i <= 0 or i >= 7:
						self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Red", tags="square")

		for i in black_pieces:
			self.cv.create_rectangle(i[1]*40, i[0]*40, (i[1]+1)*40, (i[0]+1)*40, fill="Black")

		for i in white_pieces:
			self.cv.create_rectangle(i[1]*40, i[0]*40, (i[1]+1)*40, (i[0]+1)*40, fill="White")

	# shows the current configuration of the board
	def Draw(self):
		for j in range(0, 14):
			for i in range(0, 8):
				self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Tan", tags="square")
				if j == 0 or j == 13:
					if i <= 2 or i >= 5:
						self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Red", tags="sqaure")
				if j == 1 or j == 12:
					if i <= 1 or i >= 6:
						self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Red", tags="square")
				if j == 2 or j == 11:
					if i <= 0 or i >= 7:
						self.cv.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, fill="Red", tags="square")

		# draw black pieces (computer)
		for i in black_pieces:
			self.cv.create_rectangle(i[1]*40, i[0]*40, (i[1]+1)*40, (i[0]+1)*40, fill="Black")

		# draw white pieces
		for i in white_pieces:
			self.cv.create_rectangle(i[1]*40, i[0]*40, (i[1]+1)*40, (i[0]+1)*40, fill="White")


# check if location of a piece is valid (on game board, not overlapping another piece)
# return -1 if invalid board location, 0 if a piece is there, 1 if valid
def location(position, otherPiece):
	# checks if location is on game board
	if position[0] < 0 or position[0] > 13 or position[1] < 0 or position[1] > 7:
		return -1
	if position[0] == 0 or position[0] == 13:
		if position[1] < 3 or position[1] > 4:
			return -1
	if position[0] == 1 or position[0] == 12:
		if position[1] < 2 or position[1] > 5:
			return -1
	if position[0] == 2 or position[0] == 11:
		if position[1] < 1 or position[1] > 6:
			return -1

	# checks if piece is not on top of another piece
	if position in otherPiece:
		return 0
	return 1


# finds all regular moves including cantering moves, does not include capturing moves
# return array of possible locations to move to (includes cantering moves)
def Move(position, current_pieces, other_pieces):
	possible = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			# skips current position
			if i == 0 and j == 0:
				continue

			new_location = (position[0]+i, position[1]+j)
			
			# check if location valid (same color piece is not on new location and valid game board)
			if location(new_location, current_pieces) == 1 and location(new_location, other_pieces) == 1:
				# no piece currently there, append to move list
				possible.append(new_location)
			else:
				# check if oppnnent piece is there
				if location(new_location, other_pieces) == 0:
					continue

				# own pieces are there, cantering move
				canter_x = 0
				canter_y = 0

				if i == -1:
					canter_x = i - 1
				if i == 1:
					canter_x = i + 1

				if j == -1:
					canter_y = j - 1
				if j == 1:
					canter_y = j + 1

				# check if new location from cantering move, append if valid location
				new_location = (position[0] + canter_x, position[1] + canter_y)
				if location(new_location, current_pieces) == 1 and location(new_location, other_pieces) == 1:
					possible.append(new_location)
	return possible


# check for list of capturing moves
# returns array of altering indexs of new location and captured pieces
def Capture(position, current_pieces, other_pieces):
	possible = []
	for i in range(-1, 2):
		for j in range(-1, 2):
			# check if opponent pieces are on the new location
			new_location = (position[0] + i, position[1] + j)
			if location(new_location, other_pieces) == 0:
				# calculate the new location after capturing

				capture_x = 0
				capture_y = 0

				if i == -1:
					capture_x = -2
				elif i == 1:
					capture_x = 2

				if j == -1:
					capture_y = -2
				elif j == 1:
					capture_y = 2

				# check if new location is valid (no other piece there, is still on game board)
				captured_piece = new_location
				new_location = (position[0] + capture_x, position[1] + capture_y)
				if location(new_location, current_pieces) == 1 and location(new_location, other_pieces) == 1:
					# append new location and the piece that was captured to be removed
					possible.append(new_location)
					possible.append(captured_piece)
	return possible


# check if a player has won, computer/AI has won, or draw
# return 0 as draw, 1 as computer win, or -1 as computer lose
def TerminalStateWin(player_pieces, AI_pieces):
	# Draw
	if len(player_pieces) <= 1 and len(AI_pieces) <= 1:
		return 0

	# Player wins by capturing all computer pieces
	if len(player_pieces) >= 2 and len(AI_pieces) == 0:
		return -1

	# AI/computer wins by capturing all player pieces
	if len(AI_pieces) >= 2 and len(white_pieces) == 0:
		return 1

	# Player captures computer's castles
	w_win1 = (13, 3)
	w_win2 = (13, 4)
	if w_win1 in player_pieces and w_win2 in player_pieces:
		return -1

	# Computer/AI captures player's castle
	b_win1 = (0, 3)
	b_win2 = (0, 4)
	if b_win1 in AI_pieces and b_win2 in AI_pieces:
		return 1


# evaluation function for current state of the board
def UtilityValue(player, AI):
	score = 0

	# checks if a castle has been captured
	in03 = False
	in04 = False
	for i in AI:
		if i == (0, 3):
			in03 = True
			score += 100
		if i == (0, 4):
			in03 = True
			score += 100


	# captured castles or having 2 pieces left
	if AI[0] == 2 or in03 or in04:
		# find closest piece to last castle for win
		closest = 13
		index = 0
		for i in range(len(AI)):
			if AI[i] == (0, 3) or AI[i] == (0, 4):
				continue
			if in03:
				distance = max(AI[i][0], abs(AI[i][1] - 4))
			if in04:
				distance = max(AI[i][0], abs(AI[i][1] - 3))
			if distance < closest:
				closest = distance
				index = i

		# return score of how close the piece is to the player's castle
		if in03:
			score += max(13 - AI[index][0], abs(4-AI[index][1]))
		if in04:
			score += max(13 - AI[index][0], abs(3-AI[index][1]))
	else:
		# evaluate distance to other's castle, wants to gain better position with pieces
		for i in player:
			score -= max(i[0], max(abs(4 - i[1]), abs(3 - i[1])))
		for i in AI:
			score += max(13 - i[0], max(abs(4-i[1]), abs(3 - i[1])))
	return score


# max is computer's decision
# returns an array of v value, configuration of player pieces, configuration of computer pieces
def MaxValue(player, AI, alpha, beta, timer, depth_count):
	global node_counter
	global max_prune_counter
	global max_depth


	# increase node count and check depth count
	node_counter += 1
	if max_depth < depth_count:
		max_depth = depth_count


	# check if current configuration of the board is the end (Draw, Win, or Lose)
	if TerminalStateWin(player, AI) == -1:
		return [min_util, player, AI]
	if TerminalStateWin(player, AI) == 1:
		return [max_util, player, AI]
	if TerminalStateWin(player, AI) == 0:
		return [0, player, AI]


	# check if difficulty depth is reached
	if depth_count == 0:
		return [UtilityValue(player, AI), player, AI]


	# set v and other variables to help find new board configurations
	v = min_util
	current_position = AI[:]
	other_position = player[:]
	capture_possible = False
	timer_copy = timer


	# check for capturing moves
	for i in range(0, len(AI)):
		capture_moves = Capture(AI[i], AI, player)

		# check if capturing moves are available
		if len(capture_moves) > 0:
			# capture moves available, bool variable stops from checking for non-capturing moves
			capture_possible = True

			# gets values of new location after capturing
			possible_moves = capture_moves[::2]


			# go through capturing moves and runs MinValue function
			for j in range(0, len(possible_moves)):
				# makes a copy of current board configuration
				start = timeit.default_timer()
				current_tmp = AI[:]
				other_tmp = player[:]

				# finds index of new location to get piece that was captured and removes that from copy of current board config
				index = capture_moves.index(possible_moves[j])
				other_tmp.remove(capture_moves[index + 1])

				current_tmp[i] = possible_moves[j]
				stop = timeit.default_timer()
				timer_copy += stop - start

				# runs MinValue function with new board configuration after capturing
				k = MinValue(other_tmp, current_tmp, alpha, beta, timer_copy, depth_count - 1)


				# pruning and other work
				if k[0] > v:
					v = k[0]
					current_position = current_tmp[:]
					other_position = other_tmp[:]
				if v >= beta:
					max_prune_counter += 1
					return [v, other_tmp, current_tmp]
				if alpha < v:
					alpha = v


	# check for other moves if capturing moves were not available
	if not capture_possible:
		# check possible moves for each piece for new board configuration
		for i in range(0, len(AI)):
			# get array of possible locations to move to
			possible_moves = Move(AI[i], AI, player)

			# consider new board configurations for MinValue function
			for j in range(0, len(possible_moves)):
				# copy of current board configuration
				start = timeit.default_timer()
				current_tmp = AI[:]
				other_tmp = player[:]


				# new board configuration of MinValue function
				current_tmp[i] = possible_moves[j]
				stop = timeit.default_timer()
				timer_copy += stop - start

				k = MinValue(player, current_tmp, alpha, beta, timer_copy, depth_count -1)#+ 1)


				# pruning and other work
				if k[0] > v:
					v = k[0]
					current_position = current_tmp[:]
				if v >= beta:
					max_prune_counter += 1
					return [v, other_tmp, current_tmp]
				if alpha < v:
					alpha = v

	# return board configuration
	if current_position == AI:
		current_position = current_tmp
	return [v, other_position, current_position]


# MinValue function for player's 
def MinValue(player, AI, alpha, beta, timer, depth_count):
	global node_counter
	global min_prune_counter
	global max_depth

	# update node counter
	node_counter += 1
	if max_depth < depth_count:
		max_depth = depth_count


	# check if end has been reached
	if TerminalStateWin(player, AI) == -1:
		return [min_util, player, AI]
	if TerminalStateWin(player, AI) == 1:
		return [max_util, player, AI]
	if TerminalStateWin(player, AI) == 0:
		return [0, player, AI]


	# check if depth limit has been reached
	if depth_count == 0:
		return [UtilityValue(player, AI), player, AI]


	# max util value and copy of current board configuration
	v = max_util
	current_position = player[:]
	other_position = AI[:]
	capture_possible = False
	timer_copy = timer
	current_tmp = player[:]
	other_tmp = AI[:]


	# check if capturing moves are available for all pieces
	for i in range(0, len(player)):
		capture_moves = Capture(player[i], player, AI)

		if len(capture_moves) > 0:
			# capturing moves available, no longer check for possible moves (cantering/regular)
			capture_possible = True

			# get new locations after capturing
			possible_moves = capture_moves[::2]


			# go through list of possible capturing moves for new board configuration
			for j in range(0, len(possible_moves)):
				# copy of current board configuration
				start = timeit.default_timer()
				current_tmp = player[:]
				other_tmp = AI[:]


				# index of possible location from capture_moves function, remove captured piece and apply new board configuration
				index = capture_moves.index(possible_moves[j])
				other_tmp.remove(capture_moves[index + 1])
				current_tmp[i] = possible_moves[j]


				stop = timeit.default_timer()
				timer_copy += stop - start
				k = MaxValue(current_tmp, other_tmp, alpha, beta, timer_copy, depth_count -1)# 1)
				
				# pruning and other work
				if k[0] < v:
					v = k[0]
					current_position = current_tmp[:]
					other_position = other_tmp[:]
				if v <= alpha:
					min_prune_counter += 1
					return [v, current_tmp, other_tmp]
				if beta > v:
					beta = v


	# check if capturing moves were possible
	if not capture_possible:
		for i in range(0, len(player)):
			# get current piece's possible moves
			possible_moves = Move(player[i], player, AI)


			# apply new locations to current board config
			for j in range(0, len(possible_moves)):
				# copy of current board config
				start = timeit.default_timer()
				current_tmp = player[:]
				other_tmp = AI[:]

				# new board config after moving/cantering
				current_tmp[i] = possible_moves[j]
				stop = timeit.default_timer()
				timer_copy += stop - start

				k = MaxValue(current_tmp, other_tmp, alpha, beta, timer_copy, depth_count - 1)#+ 1)
				
				# pruning and other work
				if k[0] < v:
					v = k[0]
					current_position = current_tmp[:]
				if v <= alpha:
					min_prune_counter += 1
					return [v, current_tmp, other_tmp]
				if beta > v:
					beta = v

	# return board config
	if current_position == player:
		current_position = current_tmp
	return [v, current_position, other_position]


# computer uses alpha-beta search to get better board configuration at a few moves ahead
def AI():
	global player_win
	global game_over
	global AI_win
	global white_pieces
	global black_pieces

	# check if player won
	win1 = (13, 3)
	win2 = (13, 4)
	if (win1 in white_pieces and win2 in white_pieces) or len(black_pieces) == 0:
		player_win = True
		game_over = True
		return


	# check if player lost
	lose1 = (0, 3)
	lose2 = (0, 4)
	if (lose1 in black_pieces and lose2 in black_pieces) or len(white_pieces) == 0:
		AI_win = True
		game_over = True
		return

	# check for tie
	if len(white_pieces) < 2 and len(black_pieces) < 2:
		AI_win = True
		player_win = True
		game_over = True
		return

	# reset variables on info about alpha-beta pruning
	global node_counter
	global max_prune_counter
	global min_prune_counter
	global max_depth
	global difficulty
	node_counter = 0
	max_prune_counter = 0
	min_prune_counter = 0
	max_depth = 0


	depth = 0
	start = timeit.default_timer()
	k = MaxValue(white_pieces, black_pieces, min_util, max_util, 0, difficulty)
	stop = timeit.default_timer()


	# get black piece that had moved
	index = -1
	for i in range(0, len(black_pieces)):
		if black_pieces[i] != k[2][i]:
			index = i
			break


	# print new info about board configuration and set the new board configuration
	prev = str(black_pieces[index])
	new = str(k[2][index])
	white_pieces = k[1]
	black_pieces = k[2]
	print "\n============================================\n"
	print "Computer's Turn"
	print "Max Depth: " + str(max_depth)
	print "Number of Nodes Generated: " + str(node_counter)
	print "Number of Prunes in Max: " + str(max_prune_counter)
	print "Number of Prunes in Min: " + str(min_prune_counter)
	print "Computer Move: " + prev + " to " + new
	print "\n============================================"

# human move
def Human():
	global player_win
	global game_over
	global AI_win
	global white_pieces
	global black_pieces
	moveDone = False
	pieceChoice = False
	moveChoice = False
	index_piece = 0
	possible_choices = []


	# check if player won
	win1 = (13, 3)
	win2 = (13, 4)
	if (win1 in white_pieces and win2 in white_pieces) or len(black_pieces) == 0:
		player_win = True
		game_over = True
		return

	# check if player lost
	lose1 = (0, 3)
	lose2 = (0, 4)
	if (lose1 in black_pieces and lose2 in black_pieces) or len(white_pieces) == 0:
		AI_win = True
		game_over = True
		return

	# check for draw
	if len(white_pieces) < 2 and len(black_pieces) < 2:
		AI_win = True
		player_win = True
		game_over = True
		return

	print "Current Positions - Pick a piece by number and pick a move"
	print "Remember you are forced to capture if possible"


	# check if capturing moves for a piece was possible
	for i in range(0, len(white_pieces)):
		capture_moves = Capture(white_pieces[i], white_pieces, black_pieces)
		if len(capture_moves) > 0:
			possible_choices.append(white_pieces[i])


	# no capturing moves available, then pieces can be moved
	if len(possible_choices) == 0:
		possible_choices = white_pieces


	# have user pick a valid piece that can be moved 
	while not moveDone:
		# choose a piece to move
		print "\n------   Possible Pieces to Move   ------"
		for i in range(0, len(possible_choices)):
			print str(i+1) + ")\t" + str(possible_choices[i])
		while not pieceChoice:
			pick = -1
			while pick < 1 or pick > len(possible_choices):
				try:
					pick = int(raw_input("Choice: "))
					pieceChoice = True
				except:
					continue

		possible_moves = []
		capture_moves = Capture(possible_choices[pick-1], possible_choices, black_pieces)


		# choice is checked if it has capturing moves
		if len(capture_moves) > 0:
			# get capturing moves and new possible locations
			possible_moves = capture_moves[::2]
			print "\n-----   Possible Locations   -----"
			for i in range(0, len(possible_moves)):
				print str(i+1) + ")\t" + str(possible_moves[i])

			# user picks the location to move to and which piece is captured
			move_pick = -1
			while move_pick < 1 or move_pick > len(possible_moves) or move_pick !='b' or move_pick != 'B':
				print "Current Piece:\t" + str(possible_choices[pick - 1])
				move_pick = raw_input("Choose a number or press B to choose a different piece: ")
				try:
					mp = int(move_pick)
					if mp < 1 or mp > len(possible_moves):
						continue
					moveDone = True
					index = white_pieces.index(possible_choices[pick - 1])
					prev = str(white_pieces[index])
					new = str(possible_moves[mp - 1])
					white_pieces[index] = possible_moves[mp - 1]
					index = capture_moves.index(possible_moves[mp - 1])
					black_pieces.remove(capture_moves[index + 1])
					print "Move: " + prev + " to " + new
					break
				except:
					if move_pick == 'b' or move_pick == 'B':
						pieceChoice = False
						break
		else:
			# user's choice is moved (cantering or regular)
			print "\n-----   Possible Locations   -----"
			possible_moves = Move(possible_choices[pick - 1], possible_choices, black_pieces)
			for i in range(0, len(possible_moves)):
				print str(i+1) + ")\t" + str(possible_moves[i])


			# valid user choice in list of possible moves
			move_pick = -1
			while move_pick < 0 or move_pick > len(possible_moves) or move_pick != 'b' or move_pick != 'B':
				move_pick = raw_input("Choose a number or press B to choose a different piece: ")
				try:
					mp = int(move_pick)
					if mp < 1 or mp > len(possible_moves):
						continue
					moveDone = True
					index = white_pieces.index(possible_choices[pick-1])
					prev = str(white_pieces[index])
					new = str(possible_moves[mp - 1])
					white_pieces[index] = possible_moves[mp - 1]
					print "Move: " + prev + " to " + new
					break
				except:
					if move_pick == 'b' or move_pick == 'B':
						pieceChoice = False
						break


# player info
player_color = "White"
white1 = (4, 2)
white2 = (4, 3)
white3 = (4, 4)
white4 = (4, 5)
white5 = (5, 3)
white6 = (5, 4)
white_pieces = [white1, white2, white3, white4, white5, white6]


# AI info
AI_color = 'Black'
black1 = (8, 3)
black2 = (8, 4)
black3 = (9, 2)
black4 = (9, 3)
black5 = (9, 4)
black6 = (9, 5)
black_pieces = [black1, black2, black3, black4, black5, black6]


# maximum and minimum utility value 
max_util = 1000
min_util = -1000


# global variables for info on running alpha-beta search
node_counter = 0
max_prune_counter = 0
min_prune_counter = 0
max_depth = 0


# global variables for game
game_over = False
AI_win = False
player_win = False
first_turn = "Player"
difficulty = 5

if __name__ == "__main__":
	# player chooses to go first or second
	while True:
		choice = raw_input("Are you ready?\nF to Go First\nS to Go Second.\nQ to Quit.\n")
		if choice == 'F' or choice == 'f':
			first_turn = "Player"
			break
		if choice == 'S' or choice == 's':
			first_turn = "AI"
			break
		if choice == 'Q' or choice == 'q':
			print("Thanks for playing.")
			exit()


	# player choose a difficulty level
	# easy, depth limit of alpha-beta search is 3
	# medium, depth limit of alpha-beta search is 4
	# hard, depth limit of alpha-beta search is 5
	while True:
		print "======================================="
		choice = raw_input("Choose a difficulty level:\n1 for Easy\n2 for Medium\n3 for Hard\n")
		try:
			if int(choice) == 1:
				difficulty = 3
				break
			if int(choice) == 2:
				difficulty = 4
				break
			if int(choice) == 3:
				difficulty = 5
				break
		except:
			continue


	# create board
	game = Tkinter.Tk()
	board = Board(game)
	board.pack()

	# play game
	board.Draw()
	if first_turn == "Player":
		while not game_over:
			board.Draw()
			Human()
			board.Draw()
			raw_input("\nEnter anything to continue: ")
			AI()
			board.Draw()
	elif first_turn == "AI":
		while not game_over:
			board.Draw()
			AI()
			board.Draw()
			Human()
			board.Draw()
			raw_input("\nEnter anything to continue: ")


	# outcome of game after playing
	print "============================="
	print "============================="
	if AI_win and player_win:
		print "   Draw"
	if AI_win and not player_win:
		print "   Computer Wins!"
	if not AI_win and player_win:
		print "   You Win!"

	# keep game board open
	game.mainloop()
