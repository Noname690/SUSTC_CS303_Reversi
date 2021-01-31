COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self,chessboard):
        self.candidate_list = self.find_choice(chessboard, self.color)
        alpha = -99999
        beta = 99999
        a = self.search(self.color,chessboard,1,alpha,beta,2)
        if a is not None:
            self.candidate_list.append(a)
        a = self.search(self.color, chessboard, 1, alpha, beta, 3)
        if a is not None:
            self.candidate_list.append(a)
        a = self.search(self.color, chessboard, 1, alpha, beta, 4)
        if a is not None:
            self.candidate_list.append(a)
        a = self.search(self.color, chessboard, 1, alpha, beta, 6)
        if a is not None:
            self.candidate_list.append(a)

    def search(self,color,board,deep,alpha,beta,t):
        if deep == t:
            choice = self.find_choice(board,self.color)
            un_choice = self.find_choice(board,-self.color)
            return self.assess(board)+(len(choice)-len(un_choice))*220
        else:
            if deep%2==1:
                choice = self.find_choice(board,color)
                if len(choice)!=0:
                    a = -99999
                    b = 0
                    for i in range(0,len(choice)):
                        newboard = self.find_change(board,color,choice[i])
                        n = self.search(-color,newboard,deep+1,alpha,beta,t)
                        if n is not None:
                            if n>a:
                                a = n
                                b = i
                            if a>=beta:
                                if deep==1:
                                    return choice[i]
                                return a
                            alpha = max(alpha,a)
                    if deep==1:
                        return choice[b]
                    return a
            else:
                choice = self.find_choice(board,color)
                if len(choice)!=0:
                    a = 99999
                    b = 0
                    for i in range(0,len(choice)):
                        newboard = self.find_change(board,color,choice[i])
                        n = self.search(-color,newboard,deep+1,alpha,beta,t)
                        if n is not None:
                            if n<a:
                                a = n
                                b = i
                            if a<=alpha:
                                if deep==1:
                                    return choice[i]
                                return a
                            beta = min(beta,a)
                    if deep==1:
                            return choice[b]
                    return a
    # def search(self,color,board,deep,alpha,beta):
    #     if deep==5:
    #         return [self.assess(board),[-1,-1]]
    #     else:
    #         grade = []
    #         choice = self.find_choice(board,color)
    #         if len(choice)!=0:
    #             for i in range(0,len(choice)):
    #                 newboard = self.find_change(board,color,choice[i])
    #                 a = self.search(-color,newboard,deep+1,alpha,beta)
    #                 if a is not None:
    #                     if deep%2==1 and color==1:
    #                         if a[0]>beta:
    #                             return [a[0],choice[i]]
    #                         alpha = max(alpha,a[0])
    #                     if deep%2==0 and color==-1:
    #                         if a[0]>beta:
    #                             return [a[0],choice[i]]
    #                         alpha = max(alpha,a[0])
    #                     if deep%2==1 and color==-1:
    #                         if a[0]<alpha:
    #                             return [a[0],choice[i]]
    #                         beta = min(beta,a[0])
    #                     if deep%2==0 and color==1:
    #                         if a[0]<alpha:
    #                             return [a[0],choice[i]]
    #                         beta = min(beta,a[0])
    #                     grade.append(a[0])

    def find_change(self,chessboard,color,choice):
            change = chessboard.copy()
            x = choice[0]
            y = choice[1]
            if x > 1 and chessboard[x - 1][y] == -color:  # 向上
                x_temp = x - 2
                while x_temp >= 0:
                    if chessboard[x_temp][y] == 0:
                        break
                    if chessboard[x_temp][y] == color:
                        while x_temp<x:
                            x_temp = x_temp + 1
                            change[x_temp][y]=color
                        break
                    x_temp = x_temp - 1
            if x < self.chessboard_size - 2 and chessboard[x + 1][y] == -color:  # 向下
                x_temp = x + 2
                while x_temp <= self.chessboard_size - 1:
                    if chessboard[x_temp][y] == 0:
                        break
                    if chessboard[x_temp][y] == color:
                        while x_temp > x:
                            x_temp = x_temp - 1
                            change[x_temp][y] = color
                        break
                    x_temp = x_temp + 1
            if y > 1 and chessboard[x][y - 1] == -color:  # 向左
                y_temp = y - 2
                while y_temp >= 0:
                    if chessboard[x][y_temp] == 0:
                        break
                    if chessboard[x][y_temp] == color:
                        while y_temp < y:
                            y_temp = y_temp + 1
                            change[x][y_temp] = color
                        break
                    y_temp = y_temp - 1
            if y < self.chessboard_size - 2 and chessboard[x][y + 1] == -color:  # 向右
                y_temp = y + 2
                while y_temp <= self.chessboard_size - 1:
                    if chessboard[x][y_temp] == 0:
                        break
                    if chessboard[x][y_temp] == color:
                        while y_temp > y:
                            y_temp = y_temp - 1
                            change[x][y_temp] = color
                        break
                    y_temp = y_temp + 1
            if x > 1 and y > 1 and chessboard[x - 1][y - 1] == -color:  # 向左上
                x_temp = x - 2
                y_temp = y - 2
                while x_temp >= 0 and y_temp >= 0:
                    if chessboard[x_temp][y_temp] == 0:
                        break
                    if chessboard[x_temp][y_temp] == color:
                        while y_temp < y:
                            x_temp = x_temp + 1
                            y_temp = y_temp + 1
                            change[x_temp][y_temp] = color
                        break
                    x_temp = x_temp - 1
                    y_temp = y_temp - 1
            if x > 1 and y < self.chessboard_size - 2 and chessboard[x - 1][y + 1] == -color:  # 向右上
                x_temp = x - 2
                y_temp = y + 2
                while x_temp >= 0 and y_temp <= self.chessboard_size - 1:
                    if chessboard[x_temp][y_temp] == 0:
                        break
                    if chessboard[x_temp][y_temp] == color:
                        while y_temp > y:
                            x_temp = x_temp + 1
                            y_temp = y_temp - 1
                            change[x_temp][y_temp] = color
                        break
                    x_temp = x_temp - 1
                    y_temp = y_temp + 1
            if x < self.chessboard_size - 2 and y > 1 and chessboard[x + 1][y - 1] == -color:  # 向左下
                x_temp = x + 2
                y_temp = y - 2
                while x_temp <= self.chessboard_size - 1 and x_temp >= 0:
                    if chessboard[x_temp][y_temp] == 0:
                        break
                    if chessboard[x_temp][y_temp] == color:
                        while y_temp < y:
                            x_temp = x_temp - 1
                            y_temp = y_temp + 1
                            change[x_temp][y_temp] = color
                        break
                    x_temp = x_temp + 1
                    y_temp = y_temp - 1
            if x < self.chessboard_size - 2 and y < self.chessboard_size - 2 and chessboard[x + 1][
                y + 1] == -color:  # 向右下
                x_temp = x + 2
                y_temp = y + 2
                while x_temp <= self.chessboard_size - 1 and y_temp <= self.chessboard_size - 1:
                    if chessboard[x_temp][y_temp] == 0:
                        break
                    if chessboard[x_temp][y_temp] == color:
                        while y_temp > y:
                            x_temp = x_temp - 1
                            y_temp = y_temp - 1
                            change[x_temp][y_temp] = color
                        break
                    x_temp = x_temp + 1
                    y_temp = y_temp + 1
            return change


    def find_choice(self, chessboard, color):
        choice=[]
        i = 0
        j = 0
        while i < self.chessboard_size:
            j = 0
            while j < self.chessboard_size:
                ij = 0
                if chessboard[i][j] == 0:
                    if i > 1 and chessboard[i - 1][j] == -color and ij == 0:  #向上
                        i_temp = i - 2
                        while i_temp >= 0:
                            if chessboard[i_temp][j] == 0:
                                break
                            if chessboard[i_temp][j] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp - 1
                    if i < self.chessboard_size - 2 and chessboard[i + 1][j] == -color and ij == 0: #向下
                        i_temp = i + 2
                        while i_temp <= self.chessboard_size - 1:
                            if chessboard[i_temp][j] == 0:
                                break
                            if chessboard[i_temp][j] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp + 1
                    if j > 1 and chessboard[i][j - 1] == -color and ij == 0: #向左
                        j_temp = j - 2
                        while j_temp >= 0:
                            if chessboard[i][j_temp] == 0:
                                break
                            if chessboard[i][j_temp] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            j_temp = j_temp - 1
                    if j < self.chessboard_size - 2 and chessboard[i][j + 1] == -color and ij == 0: #向右
                        j_temp = j + 2
                        while j_temp <= self.chessboard_size - 1:
                            if chessboard[i][j_temp] == 0:
                                break
                            if chessboard[i][j_temp] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            j_temp = j_temp + 1
                    if i > 1 and j > 1 and chessboard[i - 1][j - 1] == -color and ij == 0: #向左上
                        i_temp = i - 2
                        j_temp = j - 2
                        while i_temp >= 0 and j_temp >= 0:
                            if chessboard[i_temp][j_temp] == 0:
                                break
                            if chessboard[i_temp][j_temp] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp - 1
                            j_temp = j_temp - 1
                    if i > 1 and j < self.chessboard_size - 2 and chessboard[i - 1][j + 1] == -color and ij == 0:#向右上
                        i_temp = i - 2
                        j_temp = j + 2
                        while i_temp >= 0 and j_temp <= self.chessboard_size - 1:
                            if chessboard[i_temp][j_temp] == 0:
                                break
                            if chessboard[i_temp][j_temp] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp - 1
                            j_temp = j_temp + 1
                    if i < self.chessboard_size - 2 and j > 1 and chessboard[i + 1][j - 1] == -color and ij == 0:#向左下
                        i_temp = i + 2
                        j_temp = j - 2
                        while i_temp <= self.chessboard_size - 1 and j_temp >= 0:
                            if chessboard[i_temp][j_temp] == 0:
                                break
                            if chessboard[i_temp][j_temp] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp + 1
                            j_temp = j_temp - 1
                    if i < self.chessboard_size - 2 and j < self.chessboard_size - 2 and chessboard[i + 1][
                        j + 1] == -color and ij == 0: #向右下
                        i_temp = i + 2
                        j_temp = j + 2
                        while i_temp <= self.chessboard_size - 1 and j_temp <= self.chessboard_size - 1:
                            if chessboard[i_temp][j_temp] == 0:
                                break
                            if chessboard[i_temp][j_temp] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp + 1
                            j_temp = j_temp + 1
                j = j + 1
            i = i + 1
        return choice

    def assess(self,board):
        assess = [[2000,-60 ,  300, 200, 200,  300,  -60,  2000],
                  [-60 ,-400 ,   1,  1,  1,   1,  -400,   -60],
                  [300  ,   1,  10,  5,  5,  10,    1,    300],
                  [200  ,   1,   5,  3,  3,   5,    1,    200],
                  [200  ,   1,   5,  3,  3,   5,    1,    200],
                  [300  ,   1,  10,  5,  5,  10,    1,    300],
                  [-60 , -400,   1,  1,  1,   1,  -400,   -60],
                  [2000, -60,  300, 200, 200,  300,  -60,  2000]]
        status = 0
        for i in range(0,8):
            for j in range(0,8):
                if board[i][j]!=0:
                    status = status+1
        if board[0][0]!=0:
            if board[0][1] == board[0][0]:
                assess[0][1] = 400
            if board[1][0] == board[0][0]:
                assess[1][0] = 400
            if board[0][1] == board[0][0] and board[1][0]==board[0][0] and board[1][1]==board[0][0]:
                assess[1][1] = 100
        if board[0][7]!=0:
            if board[0][6] == board[0][7]:
                assess[0][6] = 400
            if board[1][7] == board[0][7]:
                assess[1][7] = 400
            if board[0][6] == board[0][7] and board[1][7]==board[0][7] and board[1][6]==board[0][7]:
                assess[1][6] = 100
        if board[7][0]!=0:
            if board[6][0] == board[7][0]:
                assess[6][0] = 400
            if board[7][1] == board[7][0]:
                assess[7][1] = 400
            if board[6][0] == board[7][0] and board[7][1]==board[7][0] and board[6][1]==board[7][0]:
                assess[6][1] = 100
        if board[7][7]!=0:
            if board[6][7] == board[7][7]:
                assess[6][7] = 400
            if board[7][6] == board[7][7]:
                assess[7][6] = 400
            if board[7][6] == board[7][7] and board[6][7]==board[7][7] and board[6][6]==board[7][7]:
                assess[6][6] = 100
        if status>60:
            assess = [[500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500],
                      [500, 500, 500, 500, 500, 500, 500, 500]]

        sum = 0
        for i in range(0,8):
            for j in range(0,8):
              sum = sum + assess[i][j]*board[i][j]
        if self.color==-1:
            sum = -sum
        return sum