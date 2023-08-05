import subprocess
from functools import wraps


class RunPytestTests:

    def __init__(self, mode='short', failfast=True, passrate=1, limit=0):
        self.failfast = failfast
        self.mode = mode
        self.passrate = passrate
        self.limit = limit

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            args = [
                f'pytest',
                f'--grader-mode={self.mode}',
                f'--taskname="{grader.taskName}"',
                f'--passrate={self.passrate}',
                f'--limit={self.limit}',

            ]

            if self.failfast:
                args.append('-x')

            args.append(f'{grader.testsDir}')

            subprocess.run(
                args,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                cwd=grader.cwd
            )
            return func(grader)

        return wrapper
