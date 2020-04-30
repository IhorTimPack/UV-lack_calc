from xml.etree import ElementTree

# <cube color="blue"><cube color="red"><cube color="green"></cube></cube><cube color="red"></cube></cube>
root = ElementTree.fromstring(input())
all_colors = {"red": 0, "green": 0, "blue": 0}


def func(root_in, level):
    all_colors[root_in.attrib["color"]] += level
    for i in root_in:
        func(i, level + 1)


func(root, 1)
print(all_colors)