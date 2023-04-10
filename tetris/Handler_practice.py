import config

def getCellsAbsolutePosition(piece):
    '''取得方塊當前所有方格的座標'''
    return [(y + piece.y, x + piece.x) for y, x in piece.getCells()]

# 印出目前方塊的所有方格的座標
def printPiece(shot, piece):

    print('目前方塊:', getCellsAbsolutePosition(piece))

### Let's practice NOW!

def moveLeft(shot, piece):
    def none_out():
        for i in getCellsAbsolutePosition(piece):
            if i[1] == 0:
                return False
        piece.x -= 1
    none_out()

def moveRight(shot, piece):
    def none_out():
        for i in getCellsAbsolutePosition(piece):
            if i[1] == 9:
                return False
        piece.x += 1
    none_out()

def moveUp(shot, piece):
    def none_out():
        for i in getCellsAbsolutePosition(piece):
            if i[0] == 0:
                return False
        piece.y -= 1
    none_out()

def moveDown(shot, piece):
    def none_out():
        for i in getCellsAbsolutePosition(piece):
            if i[0] == 19:
                return False
        piece.y += 1
    none_out()

def printMap(shot, piece):
    print('Print Map:')
    print('---'*4)
    # here
    print('---'*4)
