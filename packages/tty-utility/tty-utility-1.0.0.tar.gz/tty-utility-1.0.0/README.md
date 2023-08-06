# tty-utility
**Tty-utility** is an console for python programs

# Install
## Python pip
pip install tty-utility

## Python direct install
* Download archive & extract
* `python setup.py install`

# Usage
## Imports
`from ttyutility import Command`

Import an **Command** base class

`from ttyutility import Console`

Import an **Console** class

## Command class
**Command** class is an base class for new command.
It's necessary inherit of **Command**.

### configure
The **configure** method register an command in system.
But for register arguments of command, it's necessary of reimplement method.

In method, call parent method first. Used **add_argument** method for
register a new argument.

### add_argument
Add new argument of command :
* name of argument
* number of parameters (0 by default)
* type of parameter (str by default)
* help text (not help text by defaut)

**add_argument** is used in **configure** method.

### execute
**execute** method, run the treatment of command and arguments.

## Console class
**Console** class is an console manager.

For manage console: used register, for register
all of commands, and run for run console.

### register
Register a new command in console system.

* Name of command
* Instance of Command class or herited of class

## run
Run the console system.

* List or arguments (None by default)

The list of arguments (tuple), simulate a command line.

# Example
```python
from ttyutility import Command, Console


class NewCommand(Command):
    test = "ds"

    def configure(self, name: str, parser, prog: str = None, help: str = None):
        super(NewCommand, self).configure(name, parser, prog, help)

        self.add_argument('tt')

    def execute(self, args: dict):
        if args['tt']:
            print(args)


console = Console()
console.register('test', NewCommand())
console.run()
```

Declaration of new command, add argument in configure method and treatment in execute method.

Create instance of console, register new command and run console. 

# Credits
Package developed by Christophe Daloz - De Los Rios <christophedlr@gmail.com>
