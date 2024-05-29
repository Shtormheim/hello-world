import random


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы игрового поля!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли по этой клетке!"

class BoardWrongShipException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
       return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            tek_x = self.bow.x
            tek_y = self.bow.y

            if self.orientation == "horizontal":
                tek_x += i
            elif self.orientation == "vertical":
                tek_y += i

            ship_dots.append(Dot(tek_x, tek_y))

        return ship_dots

    def hit(self, shot):
        if shot in self.dots():
            self.lives -= 1
            return True
        return False

    def is_sunk(self):
        return self.lives == 0

class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.field = [["~"] * size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.count = 0

    def add_ship(self, ship):
        for d in ship.dots():
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots():
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.count += 1

    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots():
            for dx, dy in near:
                tek = Dot(d.x + dx, d.y + dy)
                if not(self.out(tek)) and tek not in self.busy:
                    if verb:
                        self.field[tek.x][tek.y] = "."
                    self.busy.append(tek)

    def __str__(self):
        res = ""
        res += " | 0 | 1 | 2 | 3 | 4 | 5 | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1 - 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "~")
        return res

    def out(self, d):
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        for ship in self.ships:
            if d in ship.dots():
                ship.lives -= 1
                self.field[d.x][d.y] = "x"
                if ship.lives == 0:
                    self.count -= 1
                    self.contour(ship, verb=True)
                    print("Корабль взорван!")
                    return True
                else:
                    print("Вы попали по кораблю!")
                    return True
            if ship.is_sunk():
                self.contour(ship, verb=True)

        self.field[d.x][d.y] = "0"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(random.randint(0, self.enemy_board.size - 1), random.randint(0, self.enemy_board.size - 1))
        print(f"Ход компьютера: {d.x + 1} {d.y +1}")
        return d

class User(Player):
    def ask(self):
        while True:
            try:
                coords = input("Ваш ход (формат: x y): ").split()
                if len(coords) != 2:
                    raise ValueError("Введите две координаты")
                x, y = map(int, coords)
                if not (0 <= x < self.enemy_board.size and 0 <= y < self.enemy_board.size):
                    raise ValueError("Неверный диапазон координат")
                return Dot(x, y)
            except ValueError as e:
                print(e)

class Game():
    def __init__(self, size = 6):
        self.size = size
        self.user_board = self.random_board()
        self.ai_board = self.random_board()
        if self.ai_board:
            self.ai_board.hid = True

        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def random_board(self):
        board = Board(size=self.size)
        attempts = 0
        placed_ships = 0
        ships_to_place = [3, 2, 2, 1, 1, 1, 1]

        for ship_size in ships_to_place:
            while True:
                attempts += 1
                if attempts > 2000:
                    return self.random_board()
                bow = Dot(random.randint(0, self.size - 1), random.randint(0, self.size - 1))
                orientation = random.choice(['horizontal', 'vertical'])
                ship = Ship(bow, ship_size, orientation)
                try:
                    board.add_ship(ship)
                    board.contour(ship)
                    placed_ships += 1
                    break
                except BoardWrongShipException:
                    pass

        if placed_ships == len(ships_to_place):
            return board
        else:
            return self.random_board()


    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Формат ввода: x y (где x - номер строки, а y - номер столбца)" )

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.user.own_board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.user.enemy_board)

            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.own_board.count == 0:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user.own_board.count == 0:
                print("-" * 20)
                print("Компьютер выиграл!")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()