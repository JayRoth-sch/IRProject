import ast

i = [[(-0.050160782769962664, -0.33076886270830935, -0.6113769426466561), 'government'], [(0.5621637005755706, -0.1006457090847222, -0.7634551187450151), 'inheritance'], [(0.07695250081724773, -0.07599088773175333, -0.2289342762807544), 'estate tax'], [(0.5445945652105602, -0.1244113853567481, -0.7934173359240563), 'global economy'], [(0.93464053249257, 0.0, -0.9346405324925701), 'globalization'], [(0.9092875005831997, -0.010952768257255262, -0.9311930370977102), 'capitalism'], [(0.8189190851981172, -0.03377372788077926, -0.8864665409596756), 'outsourcing'], [(0.9308878960613723, -0.0037526364311976953, -0.9383931689237678), 'undocumented worker'], [(-0.2203154181304532, -0.23272209367849458, -0.24512876922653595), 'foreign'], [(0.9421458053549655, 0.0, -0.9421458053549654), 'tort reform'], [(0.8234874414004942, -0.03752636431197695, -0.8985401700244482), 'trial lawyer'], [(0.9421458053549655, 0.0, -0.9421458053549654), 'corporate transparency'], [(0.8851526395561504, -0.018997721932938333, -0.9231480834220271), 'school choice']]
j = [[(-0.20112302818264652, -0.381089611179204, -0.5610561941757615), 'Washington'], [(0.6700984272752886, -0.07599088773175333, -0.8220802027387951), 'the death tax'], [(0.6700984272752886, -0.07599088773175333, -0.8220802027387951), 'the death tax'], [(0.5597568438114592, -0.1017808816051595, -0.7633186070217781), 'free market economy'], [(0.5597568438114592, -0.1017808816051595, -0.7633186070217781), 'free market economy'], [(0.5597568438114592, -0.1017808816051595, -0.7633186070217781), 'free market economy'], [(-0.10515566966916494, -0.31391952513223176, -0.5226833805952986), 'taxation'], [(0.9004455903184931, -0.01240667554804136, -0.9252589414145759), 'regulation'], [(0.9337023733847707, 0.032760516044355883, -0.868181341296059), 'litigation'], [(0.004748951830628557, -0.3124656178414456, -0.6296801875135198), 'innovation'], [(0.8924984253702201, -0.008443431970194815, -0.9093852893106097), 'education'], [(0.266209443705092, 0.20524786488028543, 0.14428628605547886), 'illegal alien'], [(0.8745983495934069, 0.0, -0.874598349593407), 'international'], [(0.7910435540550207, -0.06655066170952163, -0.924144877474064), 'lawsuit abuse'], [(0.9235357920329034, -0.00620333777402068, -0.9359424675809447), 'personal injury lawyer'], [(0.9421458053549655, 0.0, -0.9421458053549654), 'corporate accountability'], [(0.9236598587883839, 0.0, -0.9236598587883837), 'parental choice'], [(0.08586922448427525, -0.08278315967222116, -0.2514355438287176), 'equal opportunity education']]


def avg_bias(arr):
    avg = [0, 0, 0]
    for res in arr:
        res = res[0]
        for n in range(len(avg)):
            avg[n] += res[n]

    for n in range(len(avg)):
        avg[n] /= len(arr)

    return avg


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
    mean_count = 0
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


            count += 1
            if abs(mean_min_difference) or abs(mean_max_difference) or abs(mean_actual_difference):
                mean_count += 1
        except Exception:
            malformed_line_count = malformed_line_count + 1
            pass

    mean_max_one = mean_max_one / count
    mean_actual_one = mean_actual_one / count
    mean_min_one = mean_min_one / count

    mean_max_two = mean_max_two / count
    mean_actual_two = mean_actual_two / count
    mean_min_two = mean_min_two / count

    mean_actual_difference = mean_actual_difference / mean_count
    mean_min_difference = mean_min_difference / mean_count
    mean_max_difference = mean_max_difference / mean_count

    print("Printing Report -----------------------------------------------------------------------------------------------------------")

    print("Mean max one: " + str(mean_max_one) + " Mean max two: " + str(mean_max_two) + " Mean difference: " + str(mean_max_difference))
    print("Mean actual one: " + str(mean_actual_one) + " Mean actual two: " + str(mean_actual_two) + " Mean difference: " + str(mean_actual_difference))
    print("Mean min one: " + str(mean_min_one) + " Mean min two: " + str(mean_min_two) + " Mean difference: " + str(mean_min_difference)) 
    print("Number of malformed lines..." + str(malformed_line_count))
    print("Number of lines", count)
    

print(avg_bias(i))
print(avg_bias(j))

