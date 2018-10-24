from math import inf as infinity
from random import choice
import time


HUMAN = -1
COMP = +1
board = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0]
]

def get_score(state):
	if is_win(state, COMP):
		return +1
	if is_win(state, HUMAN):
		return -1
	return 0 # its a draw

def is_win(state, player):
	is_win_state = [
    	[state[0][0], state[0][1], state[0][2]],
    	[state[1][0], state[1][1], state[1][2]],
    	[state[2][0], state[2][1], state[2][2]],
    	[state[0][0], state[1][0], state[2][0]],
    	[state[0][1], state[1][1], state[2][1]],
    	[state[0][2], state[1][2], state[2][2]],
    	[state[0][0], state[1][1], state[2][2]],
    	[state[2][0], state[1][1], state[0][2]],
	]
	if [player, player, player] in is_win_state:
		return True
	else:
		return False

def game_finished(state):
	return is_win(state, HUMAN) or is_win(state, COMP)

def minimax(state, depth, player):

	if player == COMP:
		best = [-1, -1, -infinity]
	else:
		best = [-1, -1, +infinity]

	if depth == 0 or game_finished(state):
		score = get_score(state)
		return [-1, -1, score]

	for square in available_moves(state):
		x, y = square[0], square[1]
		state[x][y] = player
		score = minimax(state, depth - 1, -player)
		state[x][y] = 0
		score[0], score[1] = x, y

		if player == COMP:
			if score[2] > best[2]:
				best = score
		else:
			if score[2] < best[2]:
				best = score

	return best

def valid_move(x, y):
	if [x, y] in available_moves(board):
		return True
	else:
		return False

def put_mark(x, y, player):
	if valid_move(x, y):
		board[x][y] = player
		return True
	else:
		return False

def print_board(state, human_mark, ai_mark):
	print('----------------')
	for row in state:
		print('\n----------------')
		for square in row:
			if square == +1:
				print('|', ai_mark, '|', end="")
			elif square == -1:
				print('|', human_mark, '|', end="")
			else:
				print("|", " ", "|", end="")


def human_turn(ai_mark, human_mark):
	remaining_squares = len(available_moves(board))

	if remaining_squares == 0 or game_finished(board):
		return

	

	move = -1
	moves = {
		1: [0, 0], 2: [0, 1], 3: [0, 2],
		4: [1, 0], 5: [1, 1], 6: [1, 2],
		7: [2, 0], 8: [2, 1], 9: [2, 2],
	}

	print_board(board, human_mark, ai_mark)

	while (move < 1 or move > 9):
		move = int(input("Choose a move [1..9] "))
		coord = moves[move]
		try_place = put_mark(coord[0], coord[1], HUMAN)

		if try_place == False:
			print("Bad Move, try again")
			move = -1


def ai_turn(ai_mark, human_mark):
	remaining_squares = len(available_moves(board))

	if remaining_squares == 0 or game_finished(board):
		return

	print_board(board, human_mark, ai_mark)

	if remaining_squares == 9:
		x = choice([0, 1, 2])
		y = choice([0, 1, 2])

	else:
		move = minimax(board, remaining_squares, COMP)
		x, y = move[0], move[1]

	put_mark(x, y, COMP)
	time.sleep(1)

def available_moves(state):
	squares = []

	for x, row in enumerate(state):
		for y, square in enumerate(row):
			if square == 0:
				squares.append([x, y])
	return squares


def main():
	human_mark = ""
	ai_mark = ""
	first = "Y"

	while human_mark != "O" and human_mark != "X":
		try:
			print("")
			human_mark = input("Choose X or O: ").upper()
		except:
			exit()

	if human_mark == "X":
		ai_mark = "O"
	else:
		ai_mark = "X"

	while len(available_moves(board)) > 0 and not game_finished(board):
		if first == "N":
			ai_turn(ai_mark, human_mark)
			first = ""

		human_turn(ai_mark, human_mark)
		ai_turn(ai_mark, human_mark)

	if is_win(board, HUMAN):
		print("You Win!")
		print_board(board, human_mark, ai_mark)
	elif is_win(board, COMP):
		print("Computer Wins")
		print_board(board, human_mark, ai_mark)
	else:
		print("Draw")
		print_board(board, human_mark, ai_mark)

	exit()

if __name__=="__main__":
	main()