import random
import curses
import time

def create_food(screen_height, screen_width,snake):
  food = None
  first_time = None
   while food is None:
      new_food = [
        random.randint(2, screen_height - 2),
        random.randint(2, screen_width - 2)
      ]
      food = new_food if new_food not in snake else None
  

screen = curses.initscr()

curses.curs_set(0)

screen_height, screen_width = screen.getmaxyx()

window = curses.newwin(screen_height, screen_width, 0, 0)

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

window.bkgd(curses.color_pair(1))

window.attron(curses.color_pair(3))
window.border()
window.attroff(curses.color_pair(3))

window.keypad(1)

vel = 100
window.timeout(vel)

score = 0
window.addstr(0, screen_height // 4, "SCORE {}".format(score),
              curses.color_pair(3))

#First position of snake head
head_x = screen_width // 4
head_y = screen_height // 2
snake = [[head_y, head_x], [head_y, head_x - 1], [head_y, head_x - 2]]

#First position of food
food = [screen_height // 2, screen_width // 2]
window.addch(food[0], food[1], curses.ACS_PI)

start_time = time.time()
max_time = 5

#Fisrt motion
key = curses.KEY_RIGHT

while True:
  next_key = window.getch()
  key = key if next_key == -1 else next_key

  if snake[0][0] in [0, screen_height] or snake[0][1] in [
      0, screen_width
  ] or snake[0] in snake[1:]:
    curses.endwin()
    print("Game Over")
    quit()

  new_head = [snake[0][0], snake[0][1]]
  if key == curses.KEY_DOWN:
    new_head[0] += 1
  if key == curses.KEY_UP:
    new_head[0] -= 1
  if key == curses.KEY_RIGHT:
    new_head[1] += 1
  if key == curses.KEY_LEFT:
    new_head[1] -= 1

  snake.insert(0, new_head)

  if snake[0] == food:
    food = None
    window.timeout(int(vel * 0.95))

    score += 10
    window.addstr(0, screen_height // 4, "SCORE {}".format(score),
                  curses.color_pair(1))

    food_age = time.time() - start_time

    if food_age > max_time:
      food = None
      start_time = None

    while food is None:
      new_food = [
        random.randint(2, screen_height - 2),
        random.randint(2, screen_width - 2)
      ]
      food = new_food if new_food not in snake else None

    window.addch(food[0], food[1], curses.ACS_PI)
    start_time = time.time()
  else:
    tail = snake.pop()
    window.addch(tail[0], tail[1], ' ')

  window.addch(snake[0][0], snake[0][1], curses.ACS_BLOCK)
