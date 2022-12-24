import os
import re
import ast
import graphviz as gv

path = "/home/mk/Documents/Projects/muse"

modules = []
for filename in os.listdir(path):
    module = re.findall("^(\S+).py$", filename)
    if module: modules.append(module[0])

def clean(lines):
    # omit comments and empty lines
    cleanLines = []
    for i, line in enumerate(lines):
        if "#" in line:
            commentStart = line.index("#")
            lines[i] = lines[i][:commentStart]
        if (len(lines[i]) != 0) and (len(set(lines[i].split(" "))) > 1):
            cleanLines.append(lines[i])
    return cleanLines


def funcs(lines):
    fileFuncs = []
    for i, line in enumerate(lines):
        func = re.findall("^\s*[A-Za-z ]+ def (\S+)\s*\(\s*\S+\s*(?:,\s*\S+)*\):", line)
        # params = re.findall("^\s*def \S+\s*\((\s*\S+\s*(?:,\s*\S+)*)\):", line)
        if func: fileFuncs.append(func[0])
    return fileFuncs

userFuncs = {}
for module in modules:
    with open(path+"/" + module + '.py') as f:
        moduleLines = [line.rstrip() for line in f]
    userFuncs[module] = funcs(clean(moduleLines))
print(userFuncs)

A = gv.Digraph()
nodes = set([])
for module, funcs in userFuncs.items():
    for func in funcs:
        A.node(func)
        nodes.add(func)

for module in modules:
    with open(path+"/" + module + '.py') as f:
        moduleLines = clean([line.rstrip() for line in f])

    lastFunc = None
    for i, line in enumerate(moduleLines):
        func = re.findall("^\s*[A-Za-z ]+ def (\S+)\s*\(\s*\S+\s*(?:,\s*\S+)*\):", line)
        if (func): lastFunc = func[0]
        elif (lastFunc):
            for node in nodes:
                if line.find(node) != -1: A.edge(lastFunc, node)

A.view()

