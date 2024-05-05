stol = [1, 2, 3, 4, 5, 6, 7, 8, 9]
kolvo_kletok = 3

def vivod_stola():
    print("_" * 4 * kolvo_kletok)
    for i in range(kolvo_kletok):
        print((" " * 3 + "|") * 3)
        print("", stol[i * 3], "|", stol[1 + i * 3], "|", stol[2 + i * 3], "|")
        print(("_" * 3 + "|") * 3)

def hod_igri(index, char):
    if index > 9 or index < 1 or stol[index - 1] in ("X", "O"):
        return False
    stol[index - 1] = char
    return True

def proverka_pobedi():
    pobeda = False
    pobednaya_coombination = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    )
    for pos in pobednaya_coombination:
        if stol[pos[0]] == stol[pos[1]] and stol[pos[1]] == stol[pos[2]]:
            pobeda = stol[pos[0]]
    return pobeda

def nachalo_igri():
    global pobeda
    tekushiy_igrok = "X"

    shag = 1

    vivod_stola()

    while shag < 10:
        pobeda = proverka_pobedi()
        if pobeda:
            break
        index = input("Игрок " + tekushiy_igrok + " укажите номер свободного поля: ")

        if hod_igri(int(index), tekushiy_igrok):
            print("Ход выполнен")

            if tekushiy_igrok == "X":
                tekushiy_igrok = "O"
            else:
                tekushiy_igrok = "X"

            vivod_stola()
            shag += 1
        else:
            print("Неверный индекс, введите новый")
    if pobeda:
        print("Выиграл " + pobeda)
    else:
        print("Ничья")


print("Начало игры")
nachalo_igri()
