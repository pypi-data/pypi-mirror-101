this is a trial library for python

**\*\*** HOW TO USE **\*\***

install the package by running
pip install BinaryTreeSearch

then import the package as
from BinaryTreeSearch.BinaryTreeClass import BinaryTreeSearch

create an instance of the class as
tree = BinaryTreeSearch();

then call the binarySearch method on the instance

the method takes in two arguement
-->> the tree you want to search through
-->> the item or number you are searching for

example
from BinaryTreeSearch.BinaryTreeClass import BinaryTreeSearch

tree = BinaryTreeSearch();

tree_list = [3, [8, [5, None, 11], 94], [7, 15, 29]]
isNumber = tree.binarySearch(tree_list, 11)

print(isNumber)
