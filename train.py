import argparse
from datetime import datetime
import os
import re
import time


def main():
    # получаем аргументы
    parser.add_argument('--input-dir', default='text_samples', type=str,
                        help='путь к директории с текстовыми файлами в формате .txt')
    parser.add_argument('--model', default=f'models/{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.model', type=str,
                        help='путь к файлу, в который сохраняется модель '
                             '(по умолчанию: Tinkoff_ML/models/dd-mm-yyyy-HH-MM-SS.model)')
    args = parser.parse_args()

    # проверяем путь к папке с текстами
    try:
        samples = list(filter(lambda elem: elem[-4:] == '.txt', os.listdir(args.input_dir)))
    except FileNotFoundError:
        print("Ошибка: такой директории с документами не существует")
        return

    # проверяем путь к файлу для модели, даем файлу расширение .model и помещаем в папку models, если не указана иная
    try:
        if not args.model[-6:] == '.model':
            args.model += '.model'
        if not any(char in ['/', '\\'] for char in args.model):
            args.model = "models/" + args.model
        model_file = open(file=args.model, mode='w')
    except FileNotFoundError:
        print("Ошибка: такой директории для модели не существует")
        return

    # генератор, возвращающий очередное слово
    def text_gen():
        for sample in samples:
            with open(args.input_dir + '/' + sample, encoding='ANSI') as text:
                for line in text:
                    for word in list(filter(lambda b_word: b_word not in ['\n', ''],
                                            map(lambda a_word: re.sub(r"[\W\d]", '', a_word), line.lower().split()))):
                        yield word

    # создаем наше модель на основе двух вложенных словарей
    # вероятностью появления очередного слова будет служить число его появлений в тексте
    gen = text_gen()
    current_word = next(gen)
    while True:
        if current_word not in model_dict.keys():
            model_dict[current_word] = {}
        try:
            next_word = next(gen)
        except StopIteration:
            break
        if next_word in model_dict[current_word].keys():
            model_dict[current_word][next_word] += 1
        else:
            model_dict[current_word][next_word] = 1
        current_word = next_word

    # print(model_dict)
    model_file.write(f'{model_dict}')
    model_file.close()
    # print(samples)
    # print(f"{args.input_dir}")
    # print(f"{args.model}")
    print("Программа завершена успешно\n"
          f"Модель на основе файлов из {args.input_dir} сохранена в {args.model}")


parser = argparse.ArgumentParser(
    prog='train.py',
    description='Скрипт, обучающий модель для генерации текстов произвольной длины',
    epilog='By RedRaccoon - Преснухин Дмитрий'
)

model_dict = {}


if __name__ == "__main__":
    start = time.monotonic()  # не забыть убрать
    main()
    print(time.monotonic()-start)
