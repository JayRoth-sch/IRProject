
def output_refiner(file_path):
    input = []
    output = []
    count = 1
    read_file = open(file_path, 'r')
    Lines = read_file.readlines()

    for i in range(1,len(Lines),8):
        input.append(Lines[i][9:])
        if(i + 2 < len(Lines)):
            read_line = Lines[i][10:]
            processed_line = ''
            for i in range(len(read_line)):
                if(read_line[i] != '#'):
                    processed_line = processed_line + read_line[i]
            output.append(processed_line)
    
    return input, output



if __name__ == "__main__":
    input, output = output_refiner('output_election.txt')
    for i in range(len(input)):
        print("Input: " + str(input[i]))
        print("Output: " + str(output[i]))

