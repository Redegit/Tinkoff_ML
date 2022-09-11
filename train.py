import argparse
import re
from datetime import datetime
from os import listdir
from pickle import dump


def main():
    # получаем аргументы
    parser.add_argument('--input-dir', default='', type=str,
                        help='путь к директории с текстовыми файлами в формате .txt')
    parser.add_argument('--model', default=f'data/models/{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.pkl', type=str,
                        help='путь к файлу, в который сохраняется модель '
                             '(по умолчанию: data/models/dd-mm-yyyy-HH-MM-SS.pkl)')
    args = parser.parse_args()

    # проверяем путь к папке с текстами
    if not args.input_dir:
        args.input_dir = input("Введите путь к директории с файлами >> ")
    try:
        samples = list(filter(lambda elem: elem[-4:] == '.txt', listdir(args.input_dir)))
    except FileNotFoundError:
        print("Ошибка: такой директории с документами не существует")
        return

    # проверяем путь к файлу для модели, даем файлу расширение .pkl и помещаем в папку models, если не указана иная
    try:
        if not args.model[-4:] == '.pkl':
            args.model += '.pkl'
        if not any(char in ['/', '\\'] for char in args.model):
            args.model = "data/models/" + args.model
        model_file = open(file=args.model, mode='wb')
    except FileNotFoundError:
        print("Ошибка: такой директории для модели не существует")
        return

    # генератор, читающий файлы (поддерживаются кодировки cp1251 и utf-8) и возвращающий очередное слово
    def text_gen():
        for sample in samples:
            try:
                text = open(args.input_dir + '/' + sample, encoding='cp1251')
                for line in text:
                    for word in list(filter(lambda b_word: b_word not in ['\n', ''],
                                            map(lambda a_word: re.sub(r"[\W\d]", '', a_word), line.lower().split()))):
                        yield word
            except UnicodeDecodeError:
                text = open(args.input_dir + '/' + sample, encoding='utf-8')
                for line in text:
                    for word in list(filter(lambda b_word: b_word not in ['\n', ''],
                                            map(lambda a_word: re.sub(r"[\W\d]", '', a_word), line.lower().split()))):
                        yield word

    print("Читаю файлы...")
    # создаем нашу модель на основе вложенных словарей
    gen = text_gen()
    try:
        current_word = next(gen)
    except StopIteration:
        print("Файлы не содержат буквенных символов, либо не поддерживается кодировка")
        return
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

    print('Создаю модель...')
    # преобразовываем частоту появлений слов в вероятность
    for dic in model_dict.values():
        appear_frequency = sum(dic.values())
        for key, value in dic.items():
            dic[key] = value/appear_frequency

    # сохраняем модель при помощи pickle.dump()
    dump(model_dict, model_file)
    model_file.close()

    print("Программа завершена успешно\n"
          f"Модель на основе файлов из {args.input_dir} сохранена в {args.model}")


# описание при вызове train.py -h/--help
parser = argparse.ArgumentParser(
    prog='train.py',
    description='Скрипт, обучающий модель для генерации текстов произвольной длины',
    epilog='By RedRaccoon - Преснухин Дмитрий'
)

# словарь для модели
model_dict = {}

if __name__ == "__main__":
    main()
