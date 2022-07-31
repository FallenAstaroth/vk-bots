from sys import stdout
from os import system, remove


class Logger:

    def __init__(self):

        system("")

        self.answers = 0
        self.errors = 0

    def update_logs(self, text: str):

        stdout.write(f'\r{text}')
        stdout.flush()

    def logging(self, answer):

        if answer is not None:

            self.answers += 1

        else:

            self.errors += 1

        self.update_logs(f"Ответов: \033[32m{self.answers}\033[0m | Ошибок: \033[31m{self.errors}\033[0m")

    def write_error(self, page: str, answer: str, error: str):

        remove(f'errors.txt')

        with open(f'errors.txt', 'a', encoding='utf-8') as logger:
            logger.write("-" * 50 + f"\n{page}\n{answer}\n\n{error}\n" + "-" * 50)