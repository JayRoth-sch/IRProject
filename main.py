from googlesearch import search
from itertools import combinations

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
    for key in dset_dict.keys():
        if key.replace(' ', '').find(url) >= 0:
            possible_orgs.append(key)

    return possible_orgs


def mutate_query(query):
    suggestions = []
    instead_say = {"government": ["Washington"], "inheritance": ["the death tax"], "estate tax": ["the death tax"],
                   "global economy": ["free market economy"], "globalization": ["free market economy"],
                   "capitalism": ["free market economy"],
                   "outsourcing": ["taxation", "regulation", "litigation", "innovation", "education"],
                   "undocumented worker": ["illegal alien"], "foreign": ["international"],
                   "tort reform": ["lawsuit abuse"],
                   "trial lawyer": ["personal injury lawyer"], "corporate transparency": ["corporate accountability"],
                   "school choice": ["parental choice", "equal opportunity education"]}

    swap_left = []
    swap_right = []

    swap_combinations = set()

    for key in instead_say.keys():
        if query.find(key) > -1:
            swap_right.append(key)

    for val in instead_say.values():
        for i in val:
            if query.find(i) > -1:
                swap_left.append(i)

    for i in range(1, len(swap_right+swap_left) + 1):
        if len(swap_combinations) > 10:
            break
        for j in combinations(swap_left+swap_right, i):
            swap_combinations.add(tuple(j))

    for i in swap_combinations:
        q = query
        for j in i:
            if j in instead_say.keys():
                q = q.replace(j, instead_say[j][0])
            else:
                for k in instead_say.keys():
                    if j in instead_say[k]:
                        q = q.replace(j, k)
        suggestions.append(q)

    return suggestions


def query_bias(query, dset_dict, discount=False, stop_after=10):
    rank = 1
    results_bias = 0
    iterations = 100
    plus = 0
    minus = 0
    for result in search(query, tpe="nws", num=10, stop=10, pause=2):
        iterations -= 1
        if stop_after <= 0 or iterations <= 0:
            break
        if discount:
            if len(match_url(result, dset_dict)) > 0:
                stop_after -= 1
                results_bias += float(dset_dict[match_url(result, dset_dict)[0]]['bias_val']) / rank
            else:
                minus += -2 / rank
                plus += 2 / rank
                print("no bias for:", result)
        else:
            if len(match_url(result, dset_dict)) > 0:
                stop_after -= 1
                results_bias += float(dset_dict[match_url(result, dset_dict)[0]]['bias_val'])
            else:
                minus += -2
                plus += 2
                print("no bias for:", result)
        rank += 1
    return plus + results_bias, results_bias, minus + results_bias


def main(q_arr, min_votes=25):
    queries_bias = []
    dset_path = 'allsides.csv'
    dset_dict = dict_from_csv(dset_path, min_votes)
    print(NaN_count)  # number of sources for which the bias is not determined
    print(line_len_mismatch_count)  # number of lines in the dataset that were processed incorrectly
    for query in q_arr:
        queries_bias.append([query_bias(query, dset_dict, discount=True), query])
    for x, y in queries_bias:
        if max(x) < 0:
            print("results for", y, "seem to be left-leaning.  Consider reformulating your query.", x)
            if mutate_query(y):
                print("you could try:", mutate_query(y))
        if min(x) > 0:
            print("results for", y, "seem to be right-leaning.  Consider reformulating your query.", x)
            if mutate_query(y):
                print("you could try:", mutate_query(y))


queries = ["Is Obama a good president?", "Is Obama a bad president?", "Is Joe Biden a good president?",
           "Is Joe Biden a bad president?", "Climate Change"]

queries2 = ["WAP", "Transgender", "Second Amendment", "Freedom of Speech"]

queries3 = ["government", "washington", "inheritance", "the death tax"]

"""
query = ""
while query != "#":
    query = input("query: ")
    main([query])
"""
main(["illegal alien"])
