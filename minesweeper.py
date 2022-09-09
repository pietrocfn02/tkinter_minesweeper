#!/usr/bin/python3
import tkinter as tk
import random

class Static:

    EASY   :str = 'EASY'
    MEDIUM :str = 'MEDIUM'
    HARD   :str = 'HARD'

    EMPTY  :int = 0
    BOMB   :int = 9

    NOT_PLAYED :int = -1
    FLAGGED    :int = 99


    RESOURCES_FOLDER :str = 'minesweeper_res'


    def load_images(self):
        

        self.NOT_PLAYED_IMAGE = tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/E.png')
        self.FLAG_IMAGE = tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/F.png')
        self.BOMB_IMAGE = tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/B.png')
        self.NUMBER_IMAGES = [tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/0.png'), tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/1.png'), 
            tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/2.png'), tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/3.png'), 
            tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/4.png'), tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/5.png'),
            tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/6.png'), tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/7.png'),
            tk.PhotoImage(file=Static.RESOURCES_FOLDER+'/8.png')]
   


    def char_to_image(self, char:str) -> tk.PhotoImage:

        if char == 'F':
            return self.FLAG_IMAGE

        if char == '*':
            return self.BOMB_IMAGE
        
        if char == '_':
            return self.NOT_PLAYED_IMAGE

        
        if char.isdigit():
            x:int = int(char)
            if x >= 0 and x < len(self.NUMBER_IMAGES):
                return self.NUMBER_IMAGES[x]
            
        return self.NOT_PLAYED_IMAGE



    NEIGHBORS = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1], [1,0], [1,1]]


    def main():

        m = Minesweeper(Static.EASY)

        root = tk.Tk()
        root.configure(bg="#8a2424")
        root.resizable(False, False)
        root.title("MINESWEEPER")

        root.overrideredirect(False)

        
        app = Application(master=root, game=m)
        app.mainloop()
        
        #next_move = random.randint(0, m.config.x*m.config.y-1)
        #while (m.play(next_move//m.config.y, next_move%m.config.y)[0] and not m.is_win()):
        #    print(m)
        #    next_move = random.randint(0, m.config.x*m.config.y-1)
        #print(m)
    

class Pair:

    def __init__(self,i,j):
        self.i = i
        self.j = j

class Config:
    
    def __init__(self, diff:str):
        
        if diff == Static.EASY:
            self.x = 10
            self.y = 10
            self.bombs = 10

    
    


    

class Minesweeper:

    def neighbors_increment_near_bombs(self,i, j):
        for k in range(len(Static.NEIGHBORS)):
            tmp_i = i+Static.NEIGHBORS[k][0]
            tmp_j = j+Static.NEIGHBORS[k][1]
            if tmp_i >= 0 and tmp_i < len(self.grid) and tmp_j >= 0 and tmp_j < len(self.grid[i]):
                if self.grid[tmp_i][tmp_j] != Static.BOMB:
                    self.grid[tmp_i][tmp_j]+=1

    
    def __init__(self,diff:str):    
        self.config = Config(diff)
        self.grid = [[Static.EMPTY for _ in range(self.config.y)]for _ in range(self.config.x)]
        self.played = [[Static.NOT_PLAYED for _ in range (self.config.y)]for _ in range(self.config.x)]
        self.init = False
        

    def place_bombs(self, first_i, first_j):
        placed_bombs:int = 0

        while placed_bombs < self.config.bombs:
            next_bomb = random.randint(0, self.config.x*self.config.y-1)
            if self.grid[next_bomb//self.config.y][next_bomb%self.config.y] != Static.BOMB and not (next_bomb//self.config.y == first_i and next_bomb%self.config.y == first_j):
                self.grid[next_bomb//self.config.y][next_bomb%self.config.y] = Static.BOMB
                self.neighbors_increment_near_bombs(next_bomb//self.config.y, next_bomb%self.config.y)
                placed_bombs+=1

        self.init = True


    def as_char(self, i, j):
        if self.played[i][j] == Static.FLAGGED:
            return 'F'
        if self.played[i][j] == Static.BOMB:
            return '*'
        if self.played[i][j] == Static.NOT_PLAYED:
            return '_'

        return str(self.played[i][j])


    def reveal(self):
        for i in range (len(self.grid)):
            for j in range (len(self.grid[i])):
                if self.grid[i][j] == Static.BOMB:
                    self.played[i][j] = Static.BOMB
                else:
                    self.played[i][j] = self.grid[i][j]


    def flag(self, i, j):

        if self.played[i][j] == Static.NOT_PLAYED:
            self.played[i][j] = Static.FLAGGED
        
        if self.played[i][j] == Static.FLAGGED:
            self.played[i][j] == Static.NOT_PLAYED




    def play(self, i, j, direct=True):


        if not self.init:
            self.place_bombs(i,j)
        
        if not self.played[i][j] == Static.FLAGGED:
            self.played[i][j] = self.grid[i][j]
        elif self.played[i][j] == Static.FLAGGED and not direct:
            self.played[i][j] = self.grid[i][j]
        
        if self.grid[i][j] == Static.BOMB:
            self.played[i][j] = Static.BOMB
            return False, self.played[i][j]
        
        zeros = []
        if self.played[i][j] == 0:
            zeros.append(Pair(i,j))

        for zero in zeros:
            for k in range(len(Static.NEIGHBORS)):
                tmp_i = zero.i+Static.NEIGHBORS[k][0]
                tmp_j = zero.j+Static.NEIGHBORS[k][1]
                if tmp_i >= 0 and tmp_i < len(self.grid) and tmp_j >= 0 and tmp_j < len(self.grid[i]):
                    if self.played[tmp_i][tmp_j] == Static.NOT_PLAYED or self.played[tmp_i][tmp_j] == Static.FLAGGED:
                        self.play(tmp_i, tmp_j, False)

        return True, self.played



    def flag(self, i, j):
        print (f"i: {i}")
        print (f"j: {j}")
        if self.played[i][j] == Static.NOT_PLAYED:
            self.played[i][j] = Static.FLAGGED
        elif self.played[i][j] == Static.FLAGGED:
            self.played[i][j] = Static.NOT_PLAYED

        return self.played[i][j]


    def __str__(self):
        return_value = ''
        for i in range (self.config.x):
            for j in range (self.config.y):
                if self.played[i][j] == Static.NOT_PLAYED:
                    return_value+='_ '
                elif self.played[i][j] == Static.FLAGGED:
                    return_value+='F '
                else:
                    return_value+=str(self.played[i][j])+' '
            return_value+='\n'
        return return_value

    def is_win(self):
        counter = 0
        for i in range (len(self.played)):
            for j in range(len(self.played[i])):
                if self.played[i][j] == Static.NOT_PLAYED or self.played[i][j] == Static.FLAGGED:
                    counter+=1
        if counter > self.config.bombs:
            return False
        
        return True
    

class Application(tk.Frame):




    def new_game(self):
        self.master.destroy
        m = Minesweeper(Static.EASY)
        self.game = m
        self.in_game = True
        
        self.init_buttons()


    def on_flag(self,i,j):

        self.game.flag(i,j)
        self.buttons[i][j].configure(image=self.static.char_to_image(self.game.as_char(i,j)))

    def on_play_button(self,i,j):

        if self.in_game:

            result = self.game.play(i,j)
            if result[0]:
                if self.game.is_win():
                    self.in_game = False
                    self.game.reveal()
                    self.message["text"] = "You win!"
                    self.message.config(fg="red", bg="#8a2424", font=("Courier", 14))
                    self.message.grid(row=len(self.game.played)+3, column = len(self.game.played)//2 -5, columnspan=11)
            else:
                self.in_game = False
                self.game.reveal()
                self.message["text"] = "Oh, no! You got the bomb!"
                self.message.config(fg="red", bg="#8a2424", font=("Courier", 14))
                self.message.grid(row=len(self.game.played)+3, column = len(self.game.played)//2 -5, columnspan=11)

            if self.in_game:
                self.message["text"] = f"Played {i} {j}"
                self.message.config(fg="red", bg="#8a2424", font=("Courier", 14))
                self.message.grid(row=len(self.game.played)+3, column = len(self.game.played)//2 -5, columnspan=11)
            
            
            for i in range(len(self.game.played)):
                for j in range(len(self.game.played[i])):
                    self.buttons[i][j].configure(image=self.static.char_to_image(self.game.as_char(i,j)))
                    self.buttons[i][j].grid(row = i+2, column = j+1)
                            
            

    def init_buttons(self):
        self.buttons = [[tk.Button(master=self.master , borderwidth=0) for _ in range (len(self.game.played[0]))] for _ in range (len(self.game.played))]
        for i in range(len(self.game.played)):
            for j in range(len(self.game.played[i])):
                self.buttons[i][j] = tk.Button(self.master, fg="white", command = lambda i=i, j=j : self.on_play_button(i, j), borderwidth=0)
                self.buttons[i][j].bind("<Button-2>", func=  lambda event=0, j=j, i=i :  self.on_flag(i,j)) 
                self.buttons[i][j].bind("<Button-3>", func=  lambda event=0, j=j, i=i :  self.on_flag(i,j)) 
                #self.buttons[i][j].configure(bg="#8a2424")
                #self.buttons[i][j].config(text=self.game.as_char(i,j))
                self.buttons[i][j].configure(image=self.static.NOT_PLAYED_IMAGE)
                self.buttons[i][j].grid(row = i+2, column = j+1)

        self.message["text"] = "You can do it :)"
        self.message.config(fg="red", bg="#8a2424", font=("Courier", 14))
        self.message.grid(row=len(self.game.played)+3, column = len(self.game.played)//2 -5, columnspan=11)




    def __init__(self, master=None, game:Minesweeper=Minesweeper(Static.EASY)):
        super().__init__(master)
        self.master = master
        self.game = game
        self.in_game = True
        self.message = ''
        
        self.static = Static()
        self.static.load_images()
        
        self.create_widgets()
        self.init_buttons()


        

    def create_widgets(self):
        self.zero = tk.Label(self.master, text = "")
        self.zero.config(fg="red", bg="#8a2424", font=("Courier", 14))
        self.zero.grid(row=0, column = len(self.game.played)//2 -5, columnspan=11)
        self.title = tk.Label(self.master, text = "Minesweeper")
        self.title.config(fg="red", bg="#8a2424", font=("Courier", 14))
        self.title.grid(row=1, column = len(self.game.played)//2 -5, columnspan=11)
        self.zero = tk.Label(self.master, text = "")
        self.zero.config(fg="red", bg="#8a2424", font=("Courier", 14))
        self.zero.grid(row=len(self.game.played)+2, column = len(self.game.played)//2 -5, columnspan=11)
        self.message = tk.Label(self.master, text = "You can do it :)")
        self.message.config(fg="red", bg="#8a2424", font=("Courier", 14))
        self.message.grid(row=len(self.game.played)+3, column = len(self.game.played)//2 -5, columnspan=11)
        self.quit = tk.Button(text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.configure(bg="#8a2424")
        self.quit.grid(row=len(self.game.played)+4, column = len(self.game.played)//2 -2, columnspan=2)


        self.new = tk.Button(text="NEW", fg="red",
                              command=self.new_game)
        self.new.configure(bg="#8a2424")
        self.new.grid(row=len(self.game.played)+4, column = len(self.game.played)//2 +2, columnspan=2)
        self.zero = tk.Label(self.master, text = "")
        self.zero.config(fg="red", bg="#8a2424", font=("Courier", 14))
        self.zero.grid(row=len(self.game.played)+5, column = len(self.game.played)//2 -5, columnspan=11)



if __name__ == "__main__":
    Static.main()
