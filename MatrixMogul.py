import numpy as np
import pygame as pg
from DynamicTextInput import PromptInputBox, TextInputBox 

pg.init()
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
element_count = 0
rows = 0
cols = 0
pg.display.set_caption("Matrix Mogul")
screen = pg.display.set_mode((1000, 600))
screen.fill(white)

font = pg.font.SysFont('times new roman', 20)
user_text1 = ''
user_text2 = ''
Promt_text1 = "Enter the number of rows: "
Promt_text2 = "Enter the number of columns: "
output_text = "3"
error_text = "Please enter valid numbers and make sure you have an input for rows and columns."
input_rect = pg.Rect(1, 1, 400, 500)
user_textrect1 = pg.Rect(220, 1, 100, 25)
user_textrect2 = pg.Rect(245, 25, 100, 25)
Promt_textrect1 = pg.Rect(1, 1, 140, 25)
Promt_textrect2 = pg.Rect(1, 25, 140, 25)
output_rect = pg.Rect(403, 1, 400, 500)
error_rect = pg.Rect(1, 550, 100,  25)

running = True
active1 = False
active2 = False
display_error = False

CONVERSION_ERROR_EVENT = pg.USEREVENT + 1
RENDERING_COUNT_CHANGED_EVENT = pg.USEREVENT + 2


#Matrix Defenitions
def is_row_echelon_form(matrix):
    if not matrix.any():
        return False
    
    prev_leading_col = -1
 
    for i in range(rows):
        leading_col_found = False
        for j in range(cols):
            if matrix[i, j] != 0:
                if j <= prev_leading_col:
                    return False
                prev_leading_col = j
                leading_col_found = True
                break
        if not leading_col_found and any(matrix[i, j] != 0 for j in range(cols)):
            return False
    return True


def find_nonzero_row(matrix, pivot_row, j):
    
    for i in range(pivot_row, rows):
        if matrix[i, j] != 0:
            return i
    return None
 
# Swapping rows so that we can have our non zero row on the top of the matrix
def swap_rows(matrix, row1, row2):
    matrix[[row1, row2]] = matrix[[row2, row1]]
 
def make_pivot_one(matrix, pivot_row, j):
    pivot_element = matrix[pivot_row, j]
    matrix[pivot_row] //= pivot_element
    # print(pivot_element)
 
def eliminate_below(matrix, pivot_row, j):
    
    pivot_element = matrix[pivot_row, j]
    for i in range(pivot_row + 1, rows):
        factor = matrix[i, j]
        matrix[i] -= factor * matrix[pivot_row]
 
# Implementing above functions
def row_echelon_form(matrix):
    
    pivot_row = 0
# this will run for number of column times. If matrix has 3 columns this loop will run for 3 times
    for j in range(cols):
        nonzero_row = find_nonzero_row(matrix, pivot_row, j)
        if nonzero_row is not None:
            swap_rows(matrix, pivot_row, nonzero_row)
            make_pivot_one(matrix, pivot_row, j)
            eliminate_below(matrix, pivot_row, j)
            pivot_row += 1
    return matrix


def first_input(event):
    global active1
    global user_text1
    if event.type == pg.MOUSEBUTTONDOWN:
        if user_textrect1.collidepoint(event.pos):
            active1 = True
        else:
            active1 = False   
    
    if event.type == pg.KEYDOWN:
        if active1 == True:    
            if event.key == pg.K_BACKSPACE:
                user_text1 = user_text1[:-1]
            else:
                user_text1 += event.unicode

def second_input(event):
    global active2
    global user_text2
    if event.type == pg.MOUSEBUTTONDOWN:
        if user_textrect2.collidepoint(event.pos):
            active2 = True
        else:
            active2 = False   
    
    if event.type == pg.KEYDOWN:
        if active2 == True:    
            if event.key == pg.K_BACKSPACE:
                user_text2 = user_text2[:-1]
            else:
                user_text2 += event.unicode

def full_inputs():
    global display_error
    global user_num1
    global user_num2
    global element_count
    global rows
    global cols
    try: 
        user_num1 = int(user_text1)
        user_num2 = int(user_text2)
        display_error = False
        element_count = user_num1 * user_num2
        rows = user_num1
        cols = user_num2
        pg.event.post(pg.event.Event(RENDERING_COUNT_CHANGED_EVENT))
    except ValueError:
        display_error = True

        # Trigger the custom event for conversion errors
        #pg.event.post(pg.event.Event(CONVERSION_ERROR_EVENT))


def compute_matrix():
    global rows, cols
    # Initialize an empty NumPy array with zeros
    matrix = np.zeros((rows, cols), dtype=int)

    # Get the elements of the matrix from the user.
    for i in range(rows):
        for j in range(cols):
            element = int((i, j))
            matrix[i, j] = element


    for i in matrix:
        for element in i:
            print(element, end=" ")
        print()
    result = row_echelon_form(matrix)

prompt_input_boxes = []
text_input_boxes = []

# game loop
while running:


    # Clear the screen
    screen.fill(white)

    # Render the text
    text_surface1 = font.render(user_text1, True, black)
    text_surface2 = font.render(user_text2, True, black)
    promt_surface1 = font.render(Promt_text1, True, black)
    promt_surface2 = font.render(Promt_text2, True, black)
    
    output_surface = font.render(output_text, True, black)
    pg.draw.rect(screen, black, input_rect, 3)
    pg.draw.rect(screen, black, output_rect, 3)
    screen.blit(promt_surface1, (Promt_textrect1.x +5, Promt_textrect1.y +5))
    screen.blit(promt_surface2, (Promt_textrect2.x +5, Promt_textrect2.y +5))
    screen.blit(text_surface1, (user_textrect1.x + 5, user_textrect1.y +5))
    screen.blit(text_surface2, (user_textrect2.x + 5, user_textrect2.y +5))
    
    screen.blit(output_surface, (output_rect.x + 5, output_rect.y + 5))


    if display_error == True:
        error_surface = font.render(error_text, True, black)
        screen.blit(error_surface, (error_rect.x +5, error_rect.y +5))

    

    # Check for QUIT event outside the event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Handle events for existing input boxes
        for box in text_input_boxes:
            box.handle_event(event)
        
        first_input(event)
        second_input(event)
        
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            full_inputs()  
            for _ in range(element_count):
                    new_prompt_box = PromptInputBox(1, 50 , 200, 25, rows, cols)
                    new_text_box = TextInputBox(180, 50 + len(text_input_boxes) * 25, 200, 25)
                    
                    prompt_input_boxes.append(new_prompt_box)
                    text_input_boxes.append(new_text_box)

    # Update and render existing input boxes
    for box in prompt_input_boxes:
        box.update()
        box.render(screen)                

    for box in text_input_boxes:
        box.update()
        box.render(screen)
     
            
    # Update the display
    pg.display.flip()

    pg.time.delay(10)

pg.quit()


# Initialize an empty NumPy array with zeros
matrix = np.zeros((rows, cols), dtype=int)

# Get the elements of the matrix from the user.
for i in range(rows):
    for j in range(cols):
        element = int(input("Enter element (%d, %d): " % (i, j)))
        matrix[i, j] = element


for i in matrix:
    for element in i:
        print(element, end=" ")
    print()
result = row_echelon_form(matrix)

if is_row_echelon_form(result):
    print("In REF")
else:
    print("Not in REF--------------->")





