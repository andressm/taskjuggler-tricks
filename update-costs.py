#!/usr/bin/env python
#-*- coding:utf-8 -*-

# TODO add support for float percent definition
# TODO add custom float numbers for project cost input

import re
import shutil
import sys
import os

# open file
try:
    # getting names
    file_in_name = sys.argv[1]
    file_out_name = "%s_tmp" % file_in_name
    # open files
    file_in = open(file_in_name)
    file_out = open(file_out_name, 'w')
    # print if all if ok
    print "Processing file: %s" % file_in_name
except(RuntimeError, TypeError, NameError, IOError, IndexError):
    print "You must give the project file to process"
    exit()

# getting the project cost
try:
    project_cost = raw_input('Enter the project cost: ')
    total_tmp = re.sub('\.', '', project_cost)
    total = float(total_tmp)
    print "Project cost: %s" % project_cost
except:
    print "You must enter a valid project cost"
    exit()

def replace_costs(file_in, total):
    for line in file_in:
        # search for macro costs
        macros = re.compile('^macro ([a-zA-Z]+)(\d+).+\[(\d+)\]')
        macros_var = macros.search(line)
        if macros_var:
            percent = float(macros_var.group(2)) / 100
            cost_tmp = float(total) * percent
            cost = round(cost_tmp)
            line_new = re.sub('\[\d+\]', '[%d]', line) % cost
            print "Changing: %s  -->  %s" %(line.strip(), line_new.strip())
            line = line_new

        # re.sub for the project cost line
        pcostpatt = re.compile('.+Project cost: (\d+)')
        pcost = re.match(pcostpatt, line)
        if pcost:
            line = re.sub('(\d+)', '%d', line) % total

        # writing results
        file_out.write(line)

    # closing files
    file_in.close()
    file_out.close()

    # remove tmp file and rewrite file_in
    shutil.move(file_out_name, file_in_name)

try:
    # replacing costs
    replace_costs(file_in, total)
    # gettin reports
    tj = 'tj3 %s' % file_in_name
    os.system(tj)
except:
    print 'There is an error'
    exit()
