import ast

def output_refiner(file_path):
    mean_max_one = 0
    mean_min_one = 0
    mean_actual_one = 0

    mean_max_two = 0
    mean_min_two = 0
    mean_actual_two = 0

    mean_max_difference = 0
    mean_actual_difference = 0
    mean_min_difference = 0



    count = 0
    malformed_line_count = 0
    read_file = open(file_path, 'r')
    Lines = read_file.readlines()

    for line in Lines:
        try:
            processed_tuple = ast.literal_eval(line)
            mean_max_one = mean_max_one + processed_tuple[0][0][0]
            mean_max_two = mean_max_two + processed_tuple[1][0][0]
            mean_max_difference = mean_max_difference + abs(processed_tuple[0][0][0] - processed_tuple[1][0][0])


            mean_actual_one = mean_actual_one + processed_tuple[0][0][1]
            mean_actual_two = mean_actual_two + processed_tuple[1][0][1]
            mean_actual_difference = mean_actual_difference + abs(processed_tuple[0][0][1] - processed_tuple[1][0][1])

            mean_min_one = mean_min_one + processed_tuple[0][0][2]
            mean_min_two = mean_min_two + processed_tuple[1][0][2]
            mean_min_difference = mean_min_difference + abs(processed_tuple[0][0][2] - processed_tuple[1][0][2])


            count = count + 1
        except Exception:
            malformed_line_count = malformed_line_count + 1
            pass

    
    mean_max_one = mean_max_one/count
    mean_actual_one = mean_actual_one/count
    mean_min_one = mean_min_one/count

    mean_actual_difference = mean_actual_difference/count
    mean_min_difference = mean_min_difference/count
    mean_max_difference = mean_max_difference/count

    print("Printing Report -----------------------------------------------------------------------------------------------------------")

    print("Mean max one: " + str(mean_max_one) + " Mean max two: " + str(mean_max_two) + " Mean difference: " + str(mean_max_difference))
    print("Mean actual one: " + str(mean_actual_one) + " Mean actual two: " + str(mean_actual_two) + " Mean difference: " + str(mean_actual_difference))
    print("Mean min one: " + str(mean_min_one) + " Mean min two: " + str(mean_min_two) + " Mean difference: " + str(mean_min_difference)) 
    print("Number of malformed lines..." + str(malformed_line_count))
    



if __name__ == "__main__":
    output_refiner('biases_from_txt3.txt')
    


