# Insertion sort ==========================================================================================================
def insertion_sort(arr):
    ''' Function to sort an array using insertion sort '''
    
    # loop to iterate over all the values in array starting from 1
    for i in range(1, len(arr)):
        
        j = i-1 # Setting j as previous value of i
        key = i # Setting key as i
        
        # Loop to check whether key value is less than j previous value
        while (arr[key] < arr[j]) and (j >= 0):

            # Swapping values if previous value is indeed greater than key value
            temp = arr[key]
            arr[key] = arr[j]
            arr[j] = temp

            # decreasing value of key and previous value if values are swapped
            key -=1
            j -=1      
            
        # In case value of key is greater than previous value we need to break out of loop
        # As our assumption is all the previous values are sorted
    return arr 


# Bubble Sort =============================================================================================================
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i] < arr[j]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
    return arr


# Merge sort ==============================================================================================================
def mergeSort(arr):
    '''Function to sort an array using merge sort'''
    if len(arr) == 1:
        return arr
    else:
    
        mid = len(arr) // 2

        l_arr = mergeSort(arr[0 : mid])
        r_arr = mergeSort(arr[mid : len(arr)])

    return merge(l_arr, r_arr)


def merge(l_arr, r_arr):
    '''Function to merge to array according to values in ascending order'''
    merged_list = []

    i, j = 0, 0

    while (i < len(l_arr)) and (j <  len(r_arr)):
        
        if l_arr[i] <= r_arr[j]:
            merged_list.append(l_arr[i])
            i+=1
        else:
            merged_list.append(r_arr[j])
            j +=1
        
        if j == len(r_arr):
            for k in l_arr[i:]:
                merged_list.append(k)
        
        if i == len(l_arr):
            for k in r_arr[j:]:
                merged_list.append(k)

    return merged_list

# Heap sort ===============================================================================================================
def Max_Heapify(arr, node):
    ''' Function for rep invariant of a max heap'''
    arr_size = len(arr)
    if node == 0:
        left_child = 1
        right_child = 2
    else:
        left_child = 2 * node
        right_child = left_child + 1

    if arr_size == 2:
        if arr[0] < arr[1]:
            temp = arr[0]
            arr[0] = arr[1]
            arr[1] = temp
            return arr

    if ((arr_size > left_child) and (arr_size > right_child)) and ((arr[node] < arr[left_child]) or (arr[node] < arr[right_child])):
       
        if arr[left_child] > arr[right_child]:
            temp = arr[left_child]
            arr[left_child] = arr[node]
            arr[node] = temp
            if arr_size >= left_child:
                Max_Heapify(arr, left_child)

        else:
            temp = arr[right_child]
            arr[right_child] = arr[node]
            arr[node] = temp
            if arr_size >= right_child:
                Max_Heapify(arr, right_child)

    return arr


def Build_Max_heap(arr):
    ''' Function to Build max heaps '''
    i = (len(arr) // 2) - 1
    while i >= 0:
        arr = Max_Heapify(arr, i)
        i -= 1

    return arr


def heap_sort(arr):
    '''Function to return sorted array'''
    n = len(arr) - 1 # Length of array
    arr_sorted = [0] * len(arr) # Initializing an array with same size as given array

    while n > -1:

        arr_sorted[n] = arr[0]
        arr[0] = arr[n]
        arr = Build_Max_heap(arr[:n])
        n -= 1
    
    return arr_sorted