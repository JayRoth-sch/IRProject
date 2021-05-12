"""
used to make lists of queries with "left/right leaning" terms
"""

left_queries = []
right_queries = []

with open("handpicked_queries.csv") as f:
	f.readline() # skip header
	for line in f:
		base_terms, query = line.strip().split(",")
		left_terms, right_terms = base_terms.split("|")
		for term in left_terms.split("/"):
			left_queries.append(query.replace("X", term).replace("\"", "").replace("[", "").replace("]", ""))
		for term in right_terms.split("/"):
			right_queries.append(query.replace("X", term).replace("\"", "").replace("[", "").replace("]", ""))

with open("left_queries.csv", "w") as f:
	for lq in left_queries:
		f.write(lq+"\n")

with open("right_queries.csv", "w") as f:
	for rq in right_queries:
		f.write(rq+"\n")