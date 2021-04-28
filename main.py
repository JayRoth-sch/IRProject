from googlesearch import search

NaN_count = 0
line_len_mismatch_count = 0


# maps bias string descriptors to integer biases


def bias_map(bias):
    global NaN_count
    bias = str(bias)
    if bias == "left":
        return -2
    elif bias == "left-center":
        return -1
    elif bias == "right-center":
        return 1
    elif bias == "right":
        return 2
    elif bias == "center":
        return 0
    else:
        NaN_count += 1
        return "NaN"


# creates a "<org_name>":{"bias_val": int, "agree_ratio": float, "total_votes": int} dict from the csv at path


def dict_from_csv(path, min_votes=25):
    global line_len_mismatch_count
    d = dict()
    f = open(path, 'r')
    next(f)  # skip the first line
    for line in f:  # add the entries to the dict
        line = line.split(',')
        if len(line) != 8:
            line_len_mismatch_count += 1
        for i in range(len(line)):
            line[i] = str(line[i]).strip().lower()
        if int(line[7]) > min_votes:
            d[line[6]] = {"bias_val": bias_map(line[4]), "agree_ratio": float(line[1]), "total_votes": int(line[7])}

    f.close()
    return d


def match_url(url, dset_dict):  # tries to find keys in the dict that match the url
    possible_orgs = []
    url = str(url).split("/")[2].replace('www.', '').split('.')[0]
    print(url)
    for key in dset_dict.keys():
        if key.replace(' ', '').find(url) >= 0:
            possible_orgs.append(key)

    return possible_orgs


def query_bias(query, dset_dict, discount=False):
    rank = 1
    results_bias = 0
    for result in search(query, tpe="nws", num=10, stop=10, pause=2):
        if discount:
            if len(match_url(result, dset_dict)) > 0:
                results_bias += float(dset_dict[match_url(result, dset_dict)[0]]['bias_val']) / rank
            else:
                print("no bias for:", result)
        else:
            if len(match_url(result, dset_dict)) > 0:
                results_bias += float(dset_dict[match_url(result, dset_dict)[0]]['bias_val'])
            else:
                print("no bias for:", result)
        rank += 1
    return results_bias


def main(q_arr, min_votes=25):
    queries_bias = []
    dset_path = 'allsides.csv'
    dset_dict = dict_from_csv(dset_path, min_votes)
    print(NaN_count)  # number of sources for which the bias is not determined
    print(line_len_mismatch_count)  # number of lines in the dataset that were processed incorrectly
    for query in q_arr:
        queries_bias.append(query_bias(query, dset_dict, discount=True))
    print(queries_bias)


queries = ["Is Obama a good president?", "Is Obama a bad president?"]

main(queries)
