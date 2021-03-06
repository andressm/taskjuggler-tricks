# README

This are some files which I use to speed up my work with the [Taskjuggler](https://github.com/taskjuggler/TaskJuggler), which
is a excellent project management software.

## add-to-vimrc
This is an extract of my .vimrc file. This file have some shortcuts and my
preferences to work with
[Taskjuggler](https://github.com/taskjuggler/TaskJuggler). For example this is a
shortcut to use F5 to compile a tjp project in vim:

    autocmd BufNewFile,BufRead *.tjp map <F5> <Esc>:w<CR>:make %<CR>

## update-costs 
In my projects I need to calculate several types of
administratives costs based in the executing project cost. Taskjuggler can give
me a very good approximation of the executing project cost, but then I need to
calculate manually the administratives costs and finally I must write each
administrative costs in the project in order to get a fully account report.

So here is my semi-automatic solution: We need to define a macro which value
will be variable. This value will correspond to adminsitrative cost. The name
of the macro could have any letter, but the finals characters must be a number.
This number is the percent of the administrative cost based in the total
project cost, and must be in the range 1-100. For now only integer values are
allowed. Here are an example:

    # Project cost: 00
    macro overhead20 [00]

This mean that administrative cost are 20% of the project cost. It's important
that the first time you set the macro fill the brackets [] with any number. The
first line will be also updated but with the project cost. Now, we need to
define an account to credit this macro:

    account overhead 'Overhead (20%)'{ 
        credit ${projectstart} 'Overhead charge' ${overhead20}
    }

So, we need to update de value of the macro based in the project cost which we
enter. In order to do this I wrote this python script which will ask the
project file and the project cost and will update all administrative costs and
compile with `tj3` to get the updated reports. Here is an example:

    Processing file: test.tjp
    Enter the project cost (only integer values!): 2175
    Project cost: 2175
    Changing: macro overhead20 [400]  -->  macro overhead20 [435]
    TaskJuggler v3.1.0 - A Project Management Software

    Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011, 2012
                  by Chris Schlaeger <chris@linux.com>

    This program is free software; you can redistribute it and/or modify it under
    the terms of version 2 of the GNU General Public License as published by the
    Free Software Foundation.

    Reading file test.tjp                                        [      Done      ]
    Preparing scenario Plan Scenario                             [      Done      ]
    Scheduling scenario Plan Scenario                            [      Done      ]
    Checking scenario Plan Scenario                              [      Done      ]
    Report Budget                                                [      Done      ]

### Installation
Is quite easy: 

    mkdir -p ~/.vim/bundle
    cd ~/.vim/bundle/
    git clone https://andressm@github.com/andressm/taskjuggler-tricks.git

Finally add to your `~/.vimrc` file the following lines in order to update
administrative costs with the F6 key.

    autocmd BufNewFile,BufRead *.tjp map <F6> <Esc>:w<CR>:!python ~/.vim/bundle/taskjuggler-tricks/update-costs.py %<CR>
