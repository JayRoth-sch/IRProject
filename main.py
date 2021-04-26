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


def main(min_votes=25):
    url_arr = ['https://www.politico.com/news/2021/04/25/house-republicans-florida-retreat-484588',
               'https://www.nytimes.com/2021/04/25/us/Election-audit-Arizona-Republicans.html',
               'https://www.dallasnews.com/news/politics/2021/04/26/donald-trump-backs-susan-wright-for-congress/',
               'https://www.texastribune.org/2021/04/26/texas-congress-special-election-donald-trump-endorsement/',
               'https://www.cnn.com/2021/04/26/politics/doug-collins-not-running-senate-georgia-governor/index.html',
               'https://slate.com/news-and-politics/2021/04/joe-arpaio-donald-trump-pardon-history.html',
               'https://dailyprogress.com/news/local/education/pvcc-officials-hope-for-fall-semester-that-resembles'
               '-normal/article_0879bab0-a201-11eb-9307-bb03d1d2fa16.html#tracking-source=home-top-story-1',
               'https://www.nytimes.com/2021/04/26/opinion/biden-early-childhood-education.html',
               'https://www.newsweek.com/house-gop-attendance-joe-bidens-congressional-address-likely-slim-due-recess'
               '-1586541',
               'https://www.cnbc.com/2021/04/26/75-percent-of-stock-owners-wont-pay-bidens-likely-capital-gains-tax'
               '-hike.html',
               'https://abcnews.go.com/Politics/bidens-1st-100-days-promises-broken-progress/story?id=77242864',
               'https://markets.businessinsider.com/news/stocks/stock-market-performance-president-biden-100-days'
               '-best-75-years-2021-4-1030346645',
               'https://apnews.com/article/politics-immigration-health-joe-biden-election-2020'
               '-0bf5f72ba4194ba4247dcf7130af70b6',
               'https://www.washingtonpost.com/politics/2021/04/26/joe-biden-live-updates/',
               'https://nymag.com/intelligencer/2021/04/joe-biden-first-100-days.html']
    dset_path = 'allsides.csv'
    dset_dict = dict_from_csv(dset_path, min_votes)
    print(NaN_count)  # number of sources for which the bias is not determined
    print(line_len_mismatch_count)  # number of lines in the dataset that were processed incorrectly
    for url in url_arr:
        print(match_url(url, dset_dict))


main()
