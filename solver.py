def find_empty(board):

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    
    return None

def print_board(board):
    
    for row in range(len(board)):
        if row % 3 == 0 and row != 0:
            print("----------------------")

        for col in range(len(board[0])):
            if col % 3 == 0 and col != 0:
                print("|", end=" ")
            
            print(board[row][col], end=" ")
        
        print()

def solve(board):

    empty = find_empty(board)

    if empty == None:
        return True
    
    for i in range(1, 10):

        if valid_move(empty[0], empty[1], i, board):
            board[empty[0]][empty[1]] = i
            if solve(board):
                return True
            
            board[empty[0]][empty[1]] = 0
        
    return False
        
def valid_move(row, col, num, board):

    for i in range(len(board)):
        if i != row and board[i][col] == num:
            return False
    
    for i in range(len(board[0])):
        if i != col and board[row][i] == num:
            return False

    x = (col // 3)*3
    y = (row // 3)*3

    for i in range(y, y+3):
        for j in range(x, x+3):
            if board[i][j] == num and i != row and j != col:
                return False
    return True