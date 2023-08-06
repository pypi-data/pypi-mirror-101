
# Table of Contents

1.  [taskuma2org](#orgec06607)
    1.  [Install](#org4570ff3)
    2.  [Example](#orge76bea9)
        1.  [Help](#org267f095)
        2.  [A simple case](#org35bb189)
        3.  [If you edit `taskuma.csv` to remove first two lines](#org2c31094)
        4.  [Stdin is allowed](#orgc482cac)
    3.  [How to get log file from Taskuma](#orgd11de42)
    4.  [License](#org7348543)


<a id="orgec06607"></a>

# taskuma2org

taskuma2org is a Python package for parsing Taskuma log into org-mode format.
It utilizes [memacs](https://pypi.org/project/memacs/) package.

Taskuma is an iPhone App for task management and lifelogging. See AppStore.


<a id="org4570ff3"></a>

## Install

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/).

    $ pip install taskuma2org


<a id="orge76bea9"></a>

## Example


<a id="org267f095"></a>

### Help

    $ taskuma2org --help


<a id="org35bb189"></a>

### A simple case

    $ taskuma2org taskuma.csv


<a id="org2c31094"></a>

### If you edit `taskuma.csv` to remove first two lines

    $ taskuma2org --no-skip taskuma.csv


<a id="orgc482cac"></a>

### Stdin is allowed

    $ cat taskuma.csv | taskuma2org -


<a id="orgd11de42"></a>

## How to get log file from Taskuma

1.  Go to "Log" tab
2.  Choose the time period by tapping the clendar button and View button
3.  Tap share button and choose "Send Report"
4.  On the screen showing map, tap email button
5.  Send mail to yourself
6.  Retrieve csv file attached the aforementioned mail.


<a id="org7348543"></a>

## License

GPLv3

