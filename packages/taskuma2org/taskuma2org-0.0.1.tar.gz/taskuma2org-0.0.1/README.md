
# Table of Contents

1.  [taskuma2org](#org03c37ce)
    1.  [Install](#org74bb36b)
    2.  [Example](#org89c27bf)
        1.  [How to get log file from Taskuma](#org35659f5)
    3.  [License](#orga4bf722)


<a id="org03c37ce"></a>

# taskuma2org

taskuma2org is a Python package for parsing Taskuma log into org-mode format.
It utilizes [memacs](https://pypi.org/project/memacs/) package.

Taskuma is an iPhone App for task management and lifelogging. See AppStore.


<a id="org74bb36b"></a>

## Install

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/).

    $ pip install taskuma2org


<a id="org89c27bf"></a>

## Example

    $ taskuma2org example.csv


<a id="org35659f5"></a>

### How to get log file from Taskuma

1.  Go to "Log" tab
2.  Choose the time period by tapping the clendar button and View button
3.  Tap share button and choose "Send Report"
4.  On the screen showing map, tap email button
5.  Send mail to yourself
6.  Retrieve csv file attached the aforementioned mail.


<a id="orga4bf722"></a>

## License

GPLv3

