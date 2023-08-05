# Copyright (c) 2020 邢子文(XING-ZIWEN) <Rick.Xing@Nachmath.com>
# STAMP|44301


# pip install psutil

import psutil


def get_cpu_percent():
    return psutil.cpu_percent(interval=1)


if __name__ == '__main__':
    print(get_cpu_percent())
