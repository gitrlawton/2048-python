import pygame
import random
import math

# Initialize the pygame features
pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

# How large a tile is going to be.
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
# Speed at which the tiles will move (move velocity).
MOVE_VEL = 20

# Create a pygame window.
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]
    
    def __init__(self, value, row, col):
        self.value = value         # 2, 4, 8, etc.
        self.row = row             # row number of the grid.
        self.col = col             # column number of the grid.
        self.x = col * RECT_WIDTH  # starting x-coordinate for drawing the tile.
        self.y = row * RECT_HEIGHT # starting y-coordinate for drawing the tile.
        
    # Getter   
    def get_color(self):
        # Get the index of the color the tile currently is.
        color_index = int(math.log2(self.value)) - 1
        # Retrieve the color from the list of colors using the index.
        color = self.COLORS[color_index]
        
        return color
    
    # Method draws the tile on the screen.
    def draw(self, window):
        # Draw the tile.
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
        
        # Set the text to be drawn on top of the tile.
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        # Set the position to draw the text at.
        x_position = self.x + (RECT_WIDTH / 2 - text.get_width() / 2)
        y_position = self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)
        # Draw the number at that position.
        window.blit(text, (x_position, y_position))
    
    # Method sets the position of the tile in the grid.
    # Look at the current x and y position of the tile, then update the row and
    # column based on that position.
    def set_position(self, ceiling = False):
        # If we're rounding up...
        if ceiling:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        # Otherwise, round down.
        else:
            self.row = math.floo(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)
            
            
            
    
    # Method moves the tile.
    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    
    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
    
    # Draw window border.
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

# Function that draws the game board.
def draw(window, tiles):
    # Paint the window the background color.
    window.fill(BACKGROUND_COLOR)
    
    # Draw each of the tiles.
    for tile in tiles.values():
        tile.draw(window)
    
    # Draw the grid.
    draw_grid(window)
    # Update window.
    pygame.display.update()
    
def get_random_pos(tiles):
    row = None
    col = None
    
    # Until we find a random row-col position that does not yet have a tile 
    # in it...
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        
        if f"{row}{col}" not in tiles:
            break
        
    return (row, col)
        
def move_tiles(window, tiles, clock, direction):
    updated = True
    # The tiles that already had a merge operation done, that way we don't
    # allow them to merge again.
    blocks = set()
    
    if direction == "left":
        # Sort the tiles by their column.  Since the tiles are being held in a
        # dictionary, they are not in any particular order.  We want to create
        # a list to hold the order of the row's tiles.
        # Note: lambda is an anonymous function. It is equivalent to
        # def func(x):
        #   return x.col
        sort_function = lambda x: x.col
        # The order to sort in.
        reverse = False
        # How much to move each tile by per each frame. -MOVE_VEL means a -x,
        # which means move the tile to the left. 0 means do not move up or down.
        delta = (-MOVE_VEL, 0)
        # Check if tile to move has reached the left boundary of the playing 
        # field.
        boundary_check = lambda tile: tile.col == 0
        # Get next tile, so we know if we will be merging with it or blocked
        # by it per game rules.  Returns None if no next tile.
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        # Check whether or not we should merge the tile, based on the movement
        # of it (ie. have we moved the tile far enough to where it looks like it 
        # is completely inside the other tile?)
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        # Check if there is a tile next to the current tile, but it cannot merge
        # with it.
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        # Whether or not we should round up or down when dtermining the post-move 
        # tile location.
        ceiling = True
    elif direction == "right":
        sort_function = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceiling = False
    elif direction == "up":
        sort_function = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL 
        ceiling = True
    elif direction == "down":
        sort_function = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceiling = False
    
    # Updated means we have a change on the playing board we need to make happen.
    while updated:
        clock.tick(FPS)
        # Reset updated back to False.
        updated = False
        # Sort the tiles.
        sorted_tiles = sorted(tiles.values(), key = sort_function, reverse = reverse)
        
        for i, tile in enumerate(sorted_tiles):
            # If we're at the boundary of the grid, do nothing.
            if boundary_check(tile):
                pass
            
            next_tile = get_next_tile(tile)
            # If there's no tile next to the current tile, move it by delta.
            if not next_tile:
                tile.move(delta)
            # Else, there is a next tile.  If tile and next tile have the same 
            # value...
            elif (tile.value == next_tile.value 
                  and tile not in blocks # ...and tile hasn't just merged...
                  and next_tile not in blocks # ...and next_tile hasn't either...
                  ):
                # Check if a merge is in process.
                if merge_check(tile, next_tile):
                    # Keep moving the tile.
                    tile.move(delta)
                # Otherwise, merge has completed.
                else:
                    # Multiply the value of the tile we merged with by 2.
                    next_tile.value *= 2
                    # Pop the tile that disappeared because of the merge.
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            # Else, there is a next tile, but the value is not the same as the
            # current tile...
            elif move_check(tile, next_tile):
                # Move the current tile until we reach the board of the next
                # tile.
                tile.move(delta)
            # Otherwise, do nothing.
            else:
                continue
            
            # If we reach this line of code, it's because a tile moved (and thus
            # the game board updated.)  True will allow the while loop to
            # iterate another time.
            updated = True
            
            # Update the current tile's row and column.  If we're moving to the
            # left, ceiling will be True.  To the right, ceiling will be False.
            tile.set_pos(ceiling)
        
        # Adjust the dictionary of tiles to account for any removed tiles due to
        # merging.
        update_tiles(window, tiles, sorted_tiles)
        
    # Check what should happen next after our current move.
    return end_move(tiles)

# Function to check what should happen next after our current move.
def end_move(tiles):
    if len(tiles) == 16:
        # There are 16 tiles in the dictionary, meaning the board is completely 
        # filled (ie. we lose.)
        return "lost"

    # Since we didn't lose, add a new tile to the screen.
    # Generate a random row/col position for the new tile to add.
    row, col = get_random_pos(tiles)
    # Create the new tile at that position and add it to the dictionary of tiles.
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    
    return "continue"

# Function to update the dictionary of tiles to account for any removed tiles 
# due to merging.  Sorted_tiles holds all the tiles that currently exist.
def update_tiles(window, tiles, sorted_tiles):
    # Clear the dictionary of tiles.
    tiles.clear()
    # For each tile, assign it to a row-col string key in the dictionary.
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    
    # Redraw the game board.
    draw(window, tiles)     

# Function to generate two initial tiles to start our game.   
def generate_tiles():
    # Create empty dictionary for tiles.
    tiles = {}
    # Execute loop 2 times.
    for _ in range(2):
        # generate random row and column for tile to be placed at.
        row, col = get_random_pos(tiles)
        # Add tile to the dictionary using the string version of its row/col 
        # for the key and the Tile object as the value.
        tiles[f"{row}{col}"] = Tile(2, row, col)
        
    return tiles

def main(window):
    clock = pygame.time.Clock()
    run = True
    
    # Tiles is a dictionary of tiles.  The keys are two-digit strings 
    # representing the row and column. Example: "00" is row 0 col 0 and 
    # "20" is row 2 col 0.  generate_tiles() generates two random tiles to
    # start our game.
    tiles = generate_tiles()
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            # If user quit...
            if event.type == pygame.QUIT:
                run = False
                break
            
            # If a key was pressed...
            if event.type == pygame.KEYDOWN:
                # ...if that key was the left arrow...
                if event.key == pygame.K_LEFT:
                    # ...move to the left.
                    move_tiles(window, tiles, clock, "left")
                # ...if that key was the right arrow...
                if event.key == pygame.K_RIGHT:
                    # ...move to the right.
                    move_tiles(window, tiles, clock, "right")
                # ...if that key was the up arrow...
                if event.key == pygame.K_UP:
                    # ...move up.
                    move_tiles(window, tiles, clock, "up")
                # ...if that key was the down arrow...
                if event.key == pygame.K_DOWN:
                    # ...move down.
                    move_tiles(window, tiles, clock, "down")
            
        # Draw the tiles on the window.
        draw(window, tiles)
    
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)