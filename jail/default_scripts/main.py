import measure

def count_numbers():
    input_string = input()
    numbers = input_string.split()
    return len(numbers)

if __name__ == '__main__':
    measure.start_measurement()
    result = count_numbers()
    measure.end_measurement()
    print("DEBUG: Ending measurement")
    print(result)
