from googlesearch import search

query = "Is Obama a good president?"

for j in search(query, tpe="nws", num=10, stop=10, pause=2):
    print(j)

# Also can use "Google API Client" which is more robust 