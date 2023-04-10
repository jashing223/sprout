import config


def getCellsAbsolutePosition(piece):
    '''取得方塊當前所有方格的座標'''
    return [(y + piece.y, x + piece.x) for y, x in piece.getCells()]


def fixPiece(shot, piece):
    '''固定已落地的方塊，並且在main中自動切到下一個方塊'''
    piece.is_fixed = True
    for y, x in getCellsAbsolutePosition(piece):
        shot.status[y][x] = 2
        shot.color[y][x] = piece.color


### Your homework below. Enjoy :) ###9 

# 向左移動
def moveLeft(shot, piece):
    def none_out():
        for y,x in getCellsAbsolutePosition(piece):
            if x == 0 or shot.status[y][x-1] == 2:
                return False
        piece.x -= 1
    none_out()

#向右移動
def moveRight(shot, piece):
    def none_out():
        for y,x in getCellsAbsolutePosition(piece):
            if x == 9 or shot.status[y][x+1] == 2:
                return
        piece.x += 1
    none_out()

# 使方塊下落一格
def drop(shot, piece):
    def none_out():
        for y,x in getCellsAbsolutePosition(piece):
            if y >= 0:
                if y+1 == 20 or shot.status[y+1][x] == 2:
                    fixPiece(shot,piece)
                    return
        piece.y += 1
    none_out()

# 瞬間掉落
def instantDrop(shot, piece):
    def none_out():
        for y,x in getCellsAbsolutePosition(piece):
            if y >= 0:
                if y+1 == 20 or shot.status[y+1][x] == 2:
                    fixPiece(shot,piece)
                    return True
        return False
    while none_out() == False:
      piece.y += 1
    
        

# 旋轉方塊
def rotate(shot, piece):
  def check():
    piece.rotation -= 1
    for y,x in getCellsAbsolutePosition(piece):
        if x == -1:
          #print('left blocked')
          return False
        elif x == 10:
          #print('right blocked')
          return False
        elif y == 20:
          #print("down blocked")
          return False
        elif shot.status[y][x]==2 and shot.status[y][x]==2:
          #print("block blocked")
          return False
  if check() == False:
    piece.rotation += 1
    
  
# 判斷是否死掉（出局）
def isDefeat(shot, piece):
    for y,x in getCellsAbsolutePosition(piece):
      if shot.status[1][5] == 2:
        print(piece.getCells())
        return True

# 消去列
def eliminateFilledRows(shot, piece):
  step = 0
  for y in range(20):
    a = 0
    for x in range(10):
      a += shot.status[y][x]
    if a == 20:
      step += 1
      for i in range(y,0,-1):
        for x in range(10):
          shot.status[i][x] = shot.status[i-1][x]
    else:
      if step!= 0:
        shot.line_count += step
        shot.score += config.score_count[step]
        step = 0
  if step!= 0:
    shot.line_count += step
    shot.score += config.score_count[step]
    step = 0