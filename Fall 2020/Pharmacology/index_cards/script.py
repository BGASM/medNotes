from pymongo import MongoClient as MC

def make_set(sett, param):
    temp_set = []
    for i in sett:
        if param.lower() in i.lower():
            temp_set.append(i)
    return temp_set

def group():
    suffix = ['olol', 'ilol', 'amine','imine','rine','dine','terol','enol','line','osin']
    actions = [
        'Alpha 2 Agonist',
        'Alpha 1 Agonist',
        'Beta 1 Agonist',
        'Beta 2 Agonist',
        'Alpha 2 Antagonist',
        'Alpha 1 Antagonist',
        'Beta 1 Antagonist',
        'Beta 2 Antagonist',
        'Alpha Agonist',
        'Beta Agonist',
        'Alpha Antagonist',
        'Beta Antagonist'    
    ]

    output = {}
    for i in suffix:
        targ = make_set(terms, i)
        output[i] = targ
    for i in actions:
        targ = make_set(terms, i)
        output[i] = targ
        
    for key in output:
        for n in output[key]:
            if ';' in n:
                n = n.rpartition(';')[0]
            else:
                output[key].pop(n)           

    for key in output:
        print(f'\n-{key}\n{"".join(output[key])}\n')

def read_cards():
    with open('Pharmacology\index_cards\index.txt', 'r') as filein:
        bigstring = filein.read()
    return bigstring

def get_db(terms):
    cli = MC()
    db = cli['test']
    study = db['study']
    add_many(study, terms)
    

def add_many(coll, articles):
    result = []
    for paper in articles:
        Term = paper['Term']
        tmp = coll.replace_one(
            {"Term": Term},
            paper,
            upsert=True,
        )
        result.append(tmp.upserted_id)
    print(result)
    
        
def parse_cards():
    bigstring = read_cards()
    term_dict = []
    terms = bigstring.replace('\n',' ').split('$')
    for term in terms:
        spliced_term = term.partition(';')
        term_dict.append({'Term':spliced_term[0], 'Definition':spliced_term[2]})
    get_db(term_dict)
    

parse_cards()