import tkinter as tk
import random

class DockDialog:
    def __init__(self, parent, island_coords):
        self.top = tk.Toplevel(parent)
        self.island_coords = island_coords
        self.action = None
        
        tk.Label(self.top, text="You have docked at ({}, {}). What would you like to do?".format(*self.island_coords)).pack()
        tk.Button(self.top, text="Repair ship", command=self.choose_repair).pack()
        tk.Button(self.top, text="Refit ship", command=self.choose_refit).pack()
        tk.Button(self.top, text="Trade", command=self.choose_trade).pack()
        
    def choose_repair(self):
        self.action = 'repair'
        self.top.destroy()
        
    def choose_refit(self):
        self.action = 'refit'
        self.top.destroy()
        
    def choose_trade(self):
        self.action = 'trade'
        self.top.destroy()

class OceanMap:
    def __init__(self, master, width=800, height=800, rows=80, cols=80):
        self.master = master
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.tile_width = self.width // self.cols
        self.tile_height = self.height // self.rows
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.focus_set()
        self.ship_pos = [self.cols // 2, self.rows // 2]
        self.islands = []
        self.port_locs = {}  # dictionary of island coordinates and their port locations
        self.popup_open = False  # flag to indicate if a popup is currently open
        self.ship_health = 100  # initial ship health
        self.action = None
        self.gold = 0  # initial gold
        
        # Create AI ships
        self.ai_ships = []
        self.ai_ship_objects = []  # list of AI ships' objects on the canvas
        self.ai_ship_health = [100] * 3  # list of AI ships' health
        
        # Draw map and start AI ship movements
        self.generate_islands()  # call generate_islands function
        self.draw_map()
        self.start_ai_movements()

        self.canvas.bind("<KeyPress>", self.move_ship)
    
    def generate_islands(self):
        for i in range(10):
            island_size = random.randint(1, 5)
            island_x = random.randint(island_size, self.cols - island_size)
            island_y = random.randint(island_size, self.rows - island_size)
            port_x = random.randint(island_x-island_size+1, island_x+island_size-1)  # generate random port location on island
            port_y = random.randint(island_y-island_size+1, island_y+island_size-1)
            for j in range(-island_size, island_size+1):
                for k in range(-island_size, island_size+1):
                    if (island_x+j, island_y+k) == (port_x, port_y):
                        self.port_locs[(island_x, island_y)] = (port_x, port_y)  # add port location to dictionary
                    self.islands.append((island_x + j, island_y + k))
                        
    def draw_map(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if (i, j) == tuple(self.ship_pos):
                    self.ship = self.canvas.create_rectangle(i * self.tile_width, j                     * self.tile_height, (i + 1) * self.tile_width,
                                                             (j + 1) * self.tile_height, fill='blue')
                elif (i, j) in self.islands:
                    self.canvas.create_rectangle(i * self.tile_width, j * self.tile_height, (i + 1) * self.tile_width,
                                                 (j + 1) * self.tile_height, fill='brown')
                    if (i, j) in self.port_locs:
                        self.canvas.create_oval((self.port_locs[(i, j)][0] - 0.25) * self.tile_width,
                                                (self.port_locs[(i, j)][1] - 0.25) * self.tile_height,
                                                (self.port_locs[(i, j)][0] + 0.25) * self.tile_width,
                                                (self.port_locs[(i, j)][1] + 0.25) * self.tile_height, fill='white')
                else:
                    self.canvas.create_rectangle(i * self.tile_width, j * self.tile_height, (i + 1) * self.tile_width,
                                                 (j + 1) * self.tile_height, fill='light blue')
        self.canvas.create_text(self.ship_pos[0] * self.tile_width + self.tile_width // 2,
                                self.ship_pos[1] * self.tile_height + self.tile_height // 2, text='You', fill='white')
        for i, ship in enumerate(self.ai_ships):
            ai_ship_object = self.canvas.create_rectangle(ship[0] * self.tile_width, ship[1] * self.tile_height,
                                                           (ship[0] + 1) * self.tile_width,
                                                           (ship[1] + 1) * self.tile_height, fill='red')
            self.ai_ship_objects.append(ai_ship_object)
            self.canvas.create_text(ship[0] * self.tile_width + self.tile_width // 2,
                                    ship[1] * self.tile_height + self.tile_height // 2,
                                    text='AI Ship {}'.format(i + 1), fill='white')
    
    def start_ai_movements(self):
        for i in range(len(self.ai_ships)):
            self.move_ai_ship(i)

    def move_ai_ship(self, index):
        ai_ship_pos = self.ai_ships[index]
        new_pos = ai_ship_pos
        while new_pos == ai_ship_pos:
            new_pos = [ai_ship_pos[0] + random.randint(-1, 1), ai_ship_pos[1] + random.randint(-1, 1)]
            if new_pos[0] < 0 or new_pos[0] >= self.cols or new_pos[1] < 0 or new_pos[1] >= self.rows:
                new_pos = ai_ship_pos
            elif tuple(new_pos) in self.islands:
                new_pos = ai_ship_pos  # don't move into islands
            elif new_pos == self.ship_pos:
                self.ship_health -= 10  # damage
                print("Ship health: {}".format(self.ship_health))
                if self.ship_health <= 0:
                    print("Game over!")
                    self.master.destroy()
                new_pos = ai_ship_pos
            elif new_pos in [ship for i, ship in enumerate(self.ai_ships) if i != index]:
                self.ai_ship_health[index] -= 10  # damage AI ship
                print("AI ship health: {}".format(self.ai_ship_health))
                if self.ai_ship_health[index] <= 0:
                    print("AI ship sunk!")
                    self.canvas.delete(self.ai_ship_objects[index])
                    del self.ai_ships
                    del self.ai_ship_objects[index]
                    del self.ai_ship_health[index]
                    return
                new_pos = ai_ship_pos
        self.canvas.move(self.ai_ship_objects[index], (new_pos[0]-ai_ship_pos[0]) * self.tile_width, (new_pos[1]-ai_ship_pos[1]) * self.tile_height)
        self.ai_ships[index] = new_pos
        self.master.after(500, lambda: self.move_ai_ship(index))
    
    def move_ship(self, event):
        if self.popup_open:  # check if a popup is already open
            return

        if event.keysym == 'w':
            new_pos = [self.ship_pos[0], self.ship_pos[1] - 1]
        elif event.keysym == 'a':
            new_pos = [self.ship_pos[0] - 1, self.ship_pos[1]]
        elif event.keysym == 's':
            new_pos = [self.ship_pos[0], self.ship_pos[1] + 1]
        elif event.keysym == 'd':
            new_pos = [self.ship_pos[0] + 1, self.ship_pos[1]]
        else:
            return

        if new_pos[0] < 0 or new_pos[0] >= self.cols or new_pos[1] < 0 or new_pos[1] >= self.rows:
            return

        if tuple(new_pos) in self.islands:
            if tuple(new_pos) in self.port_locs.values():  # check if new position is on a port tile
                island_coords = [(x, y) for (x, y) in self.port_locs.keys() if self.port_locs[(x, y)] == tuple(new_pos)][
                    0]  # get island coordinates of port
                dialog = DockDialog(self.master, island_coords)
                self.master.wait_window(dialog.top)
                self.action = dialog.action
                self.popup_open = True  # set popup flag to True when popup is opened
            else:
                self.damage_ship()  # damage ship if new position is not on a port tile

        self.canvas.move(self.ship, (new_pos[0] - self.ship_pos[0]) * self.tile_width,
                          (new_pos[1] - self.ship_pos[1]) * self.tile_height)
        self.ship_pos = new_pos

    def choose_action(self, action):
        self.action = action
        self.popup_open = False  # set popup flag to False when popup is closed

    def choose_port_action(self, action):
        self.port_action = action
        self.popup_open = False  # set popup flag to False when popup is closed

    def do_port_action(self):
        if self.port_action == 'repair':
            self.ship_health = min(self.ship_health + 20, 100)  # increase ship health by 20 but not beyond 100
            print("Ship health: {}".format(self.ship_health))
        elif self.port_action == 'refit':
            self.ai_ships = []  # remove AI ships
            self.ai_ship_objects = []  # remove AI ships' objects on canvas
            self.ai_ship_health = []  # remove AI ships' health
            self.start_ai_movements()  # create new AI ships and start their movements
            print("AI ships refitted and ready to sail!")
        elif self.port_action == 'trade':
            print("You traded with the island and earned 100 gold!")
            self.gold += 100

    def damage_ship(self):
        self.ship_health -= 10
        print("Ship health: {}".format(self.ship_health))
        if self.ship_health <= 0:
            print("Game over!")
            self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    ocean_map = OceanMap(root)
    root.mainloop()
