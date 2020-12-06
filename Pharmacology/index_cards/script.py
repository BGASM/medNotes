def make_set(sett, param):
    temp_set = []
    for i in sett:
        if param.lower() in i.lower():
            temp_set.append(i)
    return temp_set


with open('Pharmacology\index_cards\Index_cards.txt', 'r') as filein:
    bigstring = filein.read()


terms = bigstring.split('$')
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