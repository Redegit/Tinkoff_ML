from argparse import ArgumentParser
from pickle import load
import numpy as np


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

    # загружаем полученную модель
    with open(args.model, 'rb') as f:
        model = load(f)
        args.prefix = args.prefix.lower()
        # выбираем случайный префикс, если он не задан или не существует
        if args.prefix not in model.keys():
            if not args.prefix:
                args.prefix = np.random.choice(list(model))
            else:
                choice = input("Такого слова нет в модели\nВыбрать случайно? (д/н) >> ")
                if choice.lower() not in ['y', 'yes', "да", "д"]:
                    print("Программа завершена досрочно")
                    return
                args.prefix = np.random.choice(list(model))

        out_text = [args.prefix]
        while len(out_text) < args.length:
            next_word = np.random.choice(list(model[out_text[-1]].keys()), p=list(model[out_text[-1]].values()))
            out_text.append(next_word)

    print(' '.join(out_text).capitalize() + '.')


# описание при вызове generate.py -h/--help
parser = ArgumentParser(
    prog='generate.py',
    description='Скрипт, генерирующий текст произвольной длины на основе созданной train.py модели',
    epilog='By RedRaccoon - Преснухин Дмитрий'
)

if __name__ == "__main__":
    main()
