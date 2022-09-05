import argparse
import os
import re
import time


def main():
    # получаем аргументы
    parser.add_argument('--model', required=True, type=str,
                        help='путь к файлу, из которого загружается модель ')
    parser.add_argument('--prefix', default='', type=str,
                        help='начало предложения - одно или несколько слов '
                             '(по умолчанию выбирается случайно)')
    parser.add_argument('--length', required=True, type=int,
                        help='длина генерируемой последовательности')
    args = parser.parse_args()

    with open(args.model) as mod:
        print(type(eval(mod.readline())))
    print(args)
    # print("Программа завершена успешно\n"
    #       f"Модель на основе файлов из {} сохранена в {}")


parser = argparse.ArgumentParser(
    prog='generate.py',
    description='Скрипт, генерирующий текст произвольной длины на основе созданной train.py модели',
    epilog='By RedRaccoon - Преснухин Дмитрий'
)

if __name__ == "__main__":
    start = time.monotonic()  # не забыть убрать
    main()
    print(time.monotonic()-start)
