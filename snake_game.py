#!/usr/bin/env python3
"""
משחק הנחש הקלאסי - Snake Game
שימוש במקשי החיצים להזיז את הנחש
אכול את התפוחים האדומים וגדל!
"""

import curses
import random
import time
from collections import deque

class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.height, self.width = screen.getmaxyx()
        self.window = curses.newwin(self.height, self.width, 0, 0)
        self.window.keypad(1)
        self.window.timeout(100)

        # צבעים
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # נחש
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # תפוח
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # ניקוד
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # מסגרת

        self.snake = deque([[self.height//2, self.width//2]])
        self.food = self.create_food()
        self.direction = curses.KEY_RIGHT
        self.score = 0
        self.game_over = False

    def create_food(self):
        """יוצר תפוח במקום אקראי"""
        while True:
            food = [random.randint(1, self.height-2), random.randint(1, self.width-2)]
            if food not in self.snake:
                return food

    def draw_border(self):
        """מצייר מסגרת סביב המשחק"""
        self.window.attron(curses.color_pair(4))
        for i in range(self.width):
            self.window.addch(0, i, '═')
            self.window.addch(self.height-1, i, '═')
        for i in range(self.height):
            self.window.addch(i, 0, '║')
            self.window.addch(i, self.width-1, '║')
        self.window.addch(0, 0, '╔')
        self.window.addch(0, self.width-1, '╗')
        self.window.addch(self.height-1, 0, '╚')
        self.window.addch(self.height-1, self.width-1, '╝')
        self.window.attroff(curses.color_pair(4))

    def draw_snake(self):
        """מצייר את הנחש"""
        for i, segment in enumerate(self.snake):
            if i == 0:
                # ראש הנחש
                self.window.addstr(segment[0], segment[1], '●',
                                 curses.color_pair(1) | curses.A_BOLD)
            else:
                # גוף הנחש
                self.window.addstr(segment[0], segment[1], '○',
                                 curses.color_pair(1))

    def draw_food(self):
        """מצייר את התפוח"""
        self.window.addstr(self.food[0], self.food[1], '◆',
                          curses.color_pair(2) | curses.A_BOLD)

    def draw_score(self):
        """מציג את הניקוד"""
        score_text = f" ניקוד: {self.score} "
        self.window.addstr(0, (self.width - len(score_text)) // 2, score_text,
                          curses.color_pair(3) | curses.A_BOLD)

    def move(self):
        """מזיז את הנחש"""
        head = self.snake[0].copy()

        # מחשב מיקום חדש לראש
        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1

        # בדיקת התנגשות בקירות
        if (head[0] <= 0 or head[0] >= self.height-1 or
            head[1] <= 0 or head[1] >= self.width-1):
            self.game_over = True
            return

        # בדיקת התנגשות בעצמו
        if head in self.snake:
            self.game_over = True
            return

        # הוספת הראש החדש
        self.snake.appendleft(head)

        # בדיקה אם אכל תפוח
        if head == self.food:
            self.score += 10
            self.food = self.create_food()
            # הנחש גדל - לא מסירים את הזנב
        else:
            # הנחש לא גדל - מסירים את הזנב
            self.snake.pop()

    def run(self):
        """לולאת המשחק הראשית"""
        while not self.game_over:
            self.window.clear()
            self.draw_border()
            self.draw_snake()
            self.draw_food()
            self.draw_score()
            self.window.refresh()

            # קבלת קלט מהמשתמש
            key = self.window.getch()

            # שינוי כיוון (אי אפשר לחזור לאחור)
            if key == curses.KEY_UP and self.direction != curses.KEY_DOWN:
                self.direction = key
            elif key == curses.KEY_DOWN and self.direction != curses.KEY_UP:
                self.direction = key
            elif key == curses.KEY_LEFT and self.direction != curses.KEY_RIGHT:
                self.direction = key
            elif key == curses.KEY_RIGHT and self.direction != curses.KEY_LEFT:
                self.direction = key
            elif key == ord('q') or key == ord('Q'):
                break

            # הזז את הנחש
            self.move()

            # מהירות המשחק גדלה עם הניקוד
            self.window.timeout(max(50, 100 - self.score))

        # מסך סיום
        self.show_game_over()

    def show_game_over(self):
        """מציג מסך סיום משחק"""
        self.window.clear()
        msg = "!משחק נגמר"
        score_msg = f"{self.score} :הניקוד הסופי"
        restart_msg = "לחץ על מקש כלשהו לסגירה..."

        self.window.addstr(self.height//2 - 1, (self.width - len(msg))//2,
                          msg, curses.color_pair(2) | curses.A_BOLD)
        self.window.addstr(self.height//2 + 1, (self.width - len(score_msg))//2,
                          score_msg, curses.color_pair(3) | curses.A_BOLD)
        self.window.addstr(self.height//2 + 3, (self.width - len(restart_msg))//2,
                          restart_msg)

        self.window.timeout(-1)
        self.window.getch()

def main(stdscr):
    """פונקציה ראשית"""
    curses.curs_set(0)  # הסתר סמן
    game = SnakeGame(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)
