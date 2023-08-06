import math
from dataclasses import dataclass
from .BinaryConverter import BinaryConverter
from .MergeSortClass import MergeSortClass


@dataclass
class BinaryTreeSearch:
    # searchInput: int
    # searchTree: list

    def binarySearch(self, mList, search_input):
        convertedList = BinaryConverter.convertToList(mList)
        sortedList = MergeSortClass.runMergeSort(convertedList)

        if type(search_input) != int:
            return "input entered is not a number"

        if len(sortedList) > 0:
            middle = math.ceil(len(sortedList) / 2)
            leftSide = sortedList[:middle]
            rightSide = sortedList[middle:]

            if (middle - 1) == 1 and search_input not in sortedList:
                return False

            if search_input == sortedList[middle - 1]:
                return True

            if search_input > sortedList[middle - 1]:
                sortedList = rightSide
                return self.binarySearch(sortedList, search_input)
            else:
                sortedList = leftSide
                return self.binarySearch(sortedList, search_input)

            return sortedList
