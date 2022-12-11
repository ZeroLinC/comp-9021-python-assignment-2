class FriezeError(Exception):
    pass

class Frieze:
    
    def __init__(self,filename):
        self.matrix = []
        self.filename = filename.split('.')[0]
        length = 0
        height = 0
        with open(filename) as file:
            for line in file:
                if line.isspace():
                    continue
                new = [int(x) for x in line.split()]
                for item in new:
                    if item <0 or item >15:
                        raise FriezeError('Incorrect input.')
                if len(new) < 5 or len(new) > 51:
                    raise FriezeError('Incorrect input.')
                if length == 0:
                    length = len(new)
                if length != 0:
                    if len(new) != length:
                        raise FriezeError('Incorrect input.')
                height += 1
                self.matrix.append(new)
        self.length = length
        self.height = height
        if height < 3 or height > 17:
            raise FriezeError('Incorrect input.')
        if self.matrix[0][length-1] != 0 or \
            (self.matrix[height-1][length-1] != 0 and self.matrix[height-1][length-1] != 1):
            raise FriezeError('Input does not represent a frieze.')
        for i in range(0,length-1):
            if self.matrix[0][i] != 4 and self.matrix[0][i] != 12:
                raise FriezeError('Input does not represent a frieze.')
            if self.matrix[height-1][i] != 4 and self.matrix[height-1][i] != 5\
                and self.matrix[height-1][i] != 6 and self.matrix[height-1][i] != 7:
                    raise FriezeError('Input does not represent a frieze.')
        for i in range(0,height-1):
            upper = [8,9,10,11,12,13,14,15]
            below = [2,3,6,7,10,11,14,15]
            for j in range(0,length):
                if self.matrix[i][j] in upper:
                    if self.matrix[i+1][j] in below:
                        raise FriezeError('Input does not represent a frieze.')
        # check if there is a period except consider last column
        period = [i for i in range(2,int(length/2)+1)]
        for x in range(height):
            for y in range(length-max(period)-1):
                if len(period) == 0:
                    raise FriezeError('Input does not represent a frieze.')
                new_period = []
                for i in period:
                    yes = 1
                    for t in range(1,int(length/i)):
                        if y+i*t < length-1:
                            if self.matrix[x][y] != self.matrix[x][y+i*t]:
                                yes = 0
                    if yes == 1:
                        new_period.append(i)
                period = new_period
        min_period = min(period)
        # adding consideration of last column
        for i in range(height):
            if self.matrix[i][length-1] == 0:
                if self.matrix[i][length-1-min_period] not in [0,2,4,6,8,10,12,14]:
                    raise FriezeError('Input does not represent a frieze.')
            if self.matrix[i][length-1] == 1:
                if self.matrix[i][length-1-min_period] not in [1,3,5,7,9,11,13,15]:
                    raise FriezeError('Input does not represent a frieze.')
        self.period = min_period
                    
    def is_vertical_reflection(self):
        for i in range(self.length - self.period + 1):
            yes1 = 1
            for k in range(self.height):
                for j in range(i,int(i+self.period)):
                    #print(i,k,j)
                    if self.matrix[k][j] % 2 == 1 and self.matrix[k][2*i+self.period-j-1] % 2 != 1:
                        yes1 = 0
                    if int(self.matrix[k][j]%4/2) == 1 and int(self.matrix[k-1][2*i+self.period-j-1-1]/8) != 1:
                        yes1 = 0
                    if int(self.matrix[k][j]%8/4) == 1 and int(self.matrix[k][2*i+self.period-j-1-1]%8/4) != 1:
                        yes1 = 0
                    if int(self.matrix[k][j]/8) == 1 and int(self.matrix[k+1][2*i+self.period-j-1-1]%4/2) != 1:
                        yes1 = 0
            if yes1 == 1:
                return 1
        for i in range(self.length - self.period):
            yes2 = 1
            for k in range(self.height):
                for j in range(i,int(i+self.period)):
                    #print(i,k,j)
                    if self.matrix[k][j] % 2 == 1 and self.matrix[k][2*i+self.period-j] % 2 != 1:
                        yes2 = 0
                    if int(self.matrix[k][j]%4/2) == 1 and int(self.matrix[k-1][2*i+self.period-j-1]/8) != 1:
                        yes2 = 0
                    if int(self.matrix[k][j]%8/4) == 1 and int(self.matrix[k][2*i+self.period-j-1]%8/4) != 1:
                        yes2 = 0
                    if int(self.matrix[k][j]/8) == 1 and int(self.matrix[k+1][2*i+self.period-j-1]%4/2) != 1:
                        yes2 = 0
                if self.period % 2 == 1:
                    if self.matrix[k][i+int(self.period/2)]%2 == 1 and self.matrix[k][i+int(self.period/2)+1]%2 != 1:
                        yes2 = 0
                    if int(self.matrix[k][i+int(self.period/2)]%4/2) == 1 and int(self.matrix[k][i+int(self.period/2)]/8) == 1:
                        yes2 = 0
            if yes2 == 1:
                return 1
        return 0
    
    def is_horizontal_reflection(self):
        yes = 1
        for j in range(self.length):
            for k in range(int(self.height)):
                if self.matrix[k][j]%2 == 1 and self.matrix[self.height-k][j]%2 != 1:
                    yes = 0
                if int(self.matrix[k][j]%4/2) == 1 and int(self.matrix[self.height-k-1][j]/8) != 1:
                    yes = 0
                if int(self.matrix[k][j]%8/4) == 1 and int(self.matrix[self.height-k-1][j]%8/4) != 1:
                    yes = 0
                if int(self.matrix[k][j]/8) == 1 and int(self.matrix[self.height-k-1][j]%4/2) != 1:
                    yes = 0
        if yes == 1:
            return 1
        return 0
    
    def is_rotation(self):
        for i in range(self.length - self.period):
            yes = 1
            for k in range(self.height):
                for j in range(i,int(i+self.period)):
                    if self.matrix[k][j]%2 == 1 and self.matrix[self.height-k][2*i+self.period-j]%2 != 1:
                        yes = 0
                    if int(self.matrix[k][j]%4/2) == 1 and int(self.matrix[self.height-k][2*i+self.period-j-1]%4/2) != 1:
                        yes = 0
                    if int(self.matrix[k][j]%8/4) == 1 and int(self.matrix[self.height-k-1][2*i+self.period-j-1]%8/4) != 1:
                        yes = 0
                    if int(self.matrix[k][j]/8) == 1 and int(self.matrix[self.height-k-1-1][2*i+self.period-j-1]/8) != 1:
                        yes = 0
            if yes == 1:
                return 1
        return 0
    
    def is_glided_horizontal_reflection(self):
        sub = -1
        for i in range(1,self.period):
            yes1 = 1
            for j in range(self.length-i-1):
                for k in range(int(self.height/2)):
                    if self.matrix[k][j]%2 == 1 and self.matrix[self.height-k][j+i]%2 != 1:
                        yes1 = 0
                    if int(self.matrix[k][j]%4/2) == 1 and int(self.matrix[self.height-k-1][j+i]/8) != 1:
                        yes1 = 0
                    if int(self.matrix[k][j]%8/4) == 1 and int(self.matrix[self.height-k-1][j+i]%8/4) != 1:
                        yes1 = 0
                    if int(self.matrix[k][j]/8) == 1 and int(self.matrix[self.height-k-1][j+i]%4/2) != 1:
                        yes1 = 0
            
            if yes1 == 1:
                sub = i
        if sub == -1:
            return 0
        i = sub
        yes2 = 1
        for j in range(i,self.length-1):
            for k in range(int(self.height/2)+1,self.height):
                if self.matrix[k][j]%2 == 1 and self.matrix[self.height-k][j-i]%2 != 1:
                    yes2 = 0
                if int(self.matrix[k][j]%4/2) == 1 and int(self.matrix[self.height-k-1][j-i]/8) != 1:
                    yes2 = 0
                if int(self.matrix[k][j]%8/4) == 1 and int(self.matrix[self.height-k-1][j-i]%8/4) != 1:
                    yes2 = 0
                if int(self.matrix[k][j]/8) == 1 and int(self.matrix[self.height-k-1][j-i]%4/2) != 1:
                    yes2 = 0
        if yes2 == 1:
            return 1
        return 0
    
    def analyse(self):
        print(f'Pattern is a frieze of period {self.period} that is invariant under translation',end = '')
        if Frieze.is_vertical_reflection(self) and Frieze.is_horizontal_reflection(self):
            print(',\n        horizontal and vertical reflections, and rotation',end = '')
        elif Frieze.is_vertical_reflection(self) and Frieze.is_glided_horizontal_reflection(self):
            print(',\n        glided horizontal and vertical reflections, and rotation',end = '')
        elif Frieze.is_vertical_reflection(self):
            print('\n        and vertical reflection',end = '')
        elif Frieze.is_horizontal_reflection(self):
            print('\n        and horizontal reflection',end = '')
        elif Frieze.is_glided_horizontal_reflection(self):
            print('\n        and glided horizontal reflection',end = '')
        elif Frieze.is_rotation(self):
            print('\n        and rotation',end = '')
        print(' only.')
    
    def draw_N_to_S(self,i,j):
        if j == self.height:
            return j
        if self.matrix[j][i] % 2 == 1:
            return Frieze.draw_N_to_S(self,i, j+1)
        if self.matrix[j][i] % 2 != 1:
            return j
        
    def draw_NW_to_SE(self,i,j):
        if self.matrix[i][j] >= 8:
            return Frieze.draw_NW_to_SE(self,i+1,j+1)
        if self.matrix[i][j] < 8:
            return (i,j)
    
    def draw_W_to_E(self,i,j):
        if int(self.matrix[i][j]%8/4) == 1:
            return Frieze.draw_W_to_E(self,i,j+1)
        if int(self.matrix[i][j]%8/4) != 1:
            return j
    
    def draw_SW_to_NE(self,i,j):
        if int(self.matrix[i][j]%4/2) == 1:
            return Frieze.draw_SW_to_NE(self,i-1, j+1)
        if int(self.matrix[i][j]%4/2) != 1:
            return (i,j)
    
    def display(self):
        with open(self.filename + '.tex', 'w') as tex_file:
            print('\\documentclass[10pt]{article}\n'
              '\\usepackage{tikz}\n'
              '\\usepackage[margin=0cm]{geometry}\n'
              '\\pagestyle{empty}\n'
              '\n'
              '\\begin{document}\n'
              '\n'
              '\\vspace*{\\fill}\n'
              '\\begin{center}\n'
              '\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]', file=tex_file
             )
            # N to S
            print('% North to South lines', file=tex_file)
            visited =[]
            for i in range(self.length):
                j = 0
                while j < self.height:
                    n = Frieze.draw_N_to_S(self,i,j+1)
                    if n - 1 != j:
                        print(f'    \\draw ({i},{j}) -- ({i},{n-1});', file=tex_file)
                        j = n
                    else:
                        j += 1
            
            # NW to SE
            print('% North-West to South-East lines', file=tex_file)
            visited = []
            for i in range(self.height):
                for j in range(self.length):
                    if (i,j) not in visited and self.matrix[i][j] >= 8:
                        (x,y) = Frieze.draw_NW_to_SE(self,i+1,j+1)
                        print(f'    \\draw ({j},{i}) -- ({y},{x});', file=tex_file)
                        i1 = i
                        j1 = j
                        while i1 < x and j1 < y:
                            visited.append((i1,j1))
                            i1 += 1
                            j1 += 1
            
            # W to E
            print('% West to East lines', file=tex_file)
            visited = []
            for i in range(self.height):
                for j in range(self.length):
                    if (i,j) not in visited and int(self.matrix[i][j]%8/4) == 1:
                        n = Frieze.draw_W_to_E(self,i,j+1)
                        print(f'    \\draw ({j},{i}) -- ({n},{i});', file=tex_file)
                        j1 = j
                        while j1 < n:
                            visited.append((i,j1))
                            j1 += 1
            
            # SW to NE
            print('% South-West to North-East lines', file=tex_file)
            for i in range(self.height):
                for j in range(self.length):
                    if int(self.matrix[i][j]%4/2) == 1 and \
                        (i == self.height-1 or j == 0 or int(self.matrix[i+1][j-1]%4/2) != 1):
                        (x,y) = Frieze.draw_SW_to_NE(self, i-1, j+1)
                        print(f'    \\draw ({j},{i}) -- ({y},{x});', file=tex_file)
                        
                            
    
            print('\\end{tikzpicture}\n'
             '\\end{center}\n'
             '\\vspace*{\\fill}\n\n'
             '\\end{document}', file=tex_file
            )
