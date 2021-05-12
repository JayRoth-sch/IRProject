f = open('output_election.txt', 'r')
d = open('parsed_out3.txt', 'w')
in_line = None
prediction = None
for line in f:

    if line.find("PRED SEQ") > -1:
        prediction = line[max(line.find("b'"), line.find('b"'))+2:max(line.rfind("'"), line.rfind('"'))].replace(" ##", '')
    if line.find("IN SEQ") > -1:
        in_line = line[max(line.find("b'"), line.find('b"'))+2:max(line.rfind("'"), line.rfind('"'))].replace(" ##", '')
    if prediction is not None:
        if line.find("#####") > -1:
            d.write(str(prediction + ", " + in_line + "\n"))

f.close()
d.close()

d = open('parsed_out3.txt', 'r')
for line in d:
    print(line)

d.close()
