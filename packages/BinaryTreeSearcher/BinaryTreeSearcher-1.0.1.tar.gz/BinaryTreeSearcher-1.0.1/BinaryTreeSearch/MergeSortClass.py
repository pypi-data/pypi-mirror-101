import os
import math
from dataclasses import dataclass


@dataclass
class MergeSortClass:

    @staticmethod
    def runMergeSort(arr):
        i = 0
        j = 0
        temp = 0
        if len(arr) > 1:
            middle = math.ceil(len(arr) / 2)

            # splice the list to left and right
            leftSide = arr[:middle]
            rightSide = arr[middle:]

            MergeSortClass.runMergeSort(leftSide)
            MergeSortClass.runMergeSort(rightSide)

            while i < len(leftSide) and j < len(rightSide):
                if leftSide[i] < rightSide[j]:
                    arr[temp] = leftSide[i]
                    i += 1
                else:
                    arr[temp] = rightSide[j]
                    j += 1

                temp += 1

            while i < len(leftSide):
                arr[temp] = leftSide[i]
                i += 1
                temp += 1

            while j < len(rightSide):
                arr[temp] = rightSide[j]
                j += 1
                temp += 1

            return arr
