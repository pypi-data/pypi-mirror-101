import os
from dataclasses import dataclass


@dataclass
class BinaryConverter:

    @staticmethod
    def convertToList(treeList):
        new_list = []

        for n in treeList:
            if n == None:
                n = ""

            if type(n) == int:
                new_list.append(n)
            else:
                for x in BinaryConverter.convertToList(n):
                    new_list.append(x)

        return new_list
