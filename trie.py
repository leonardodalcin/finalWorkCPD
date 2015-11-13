### *********************************************************
### Module: trie.py
### Description: A list and tuple based Python implementation
### of the Trie data structure that supports the following
### methods:
### 1. insert_key(k, v, trie) - insert a non-empty string key k
###    into trie and associate k with value v
### 2. has_key(k, trie) - True if trie has key k
### 3. retrieve_val(k, trie) - retrieve value indexed under key
###    k in trie
### 4. start_with_prefix(prefix, trie) - return the list of
###    all keys in trie that start with prefix.
###
### Bugs, comments to vladimir dot kulyukin at gmail dot com
### *********************************************************

### ***************** HELPER FUNCTIONS **********************

def is_trie_bucket(x):
    return isinstance(x, tuple) and \
           len(x) == 2 and \
           isinstance(x[0], str) and \
           isinstance(x[1], list) and \
           len(x[1]) == 1

def is_trie_branch(x):
    return isinstance(x, list)

def get_bucket_key(b):
    return b[0]

def get_bucket_val(b):
    return b[1][0]

### ******************** INSERT_KEY ************************

def insert_key(key, v, trie):
#nao insere nomes vazios
    if key == '':
        return None
#nao insere se o nome ja esta na arvore
    elif has_key(key, trie) and retrieve_val(key, trie) == v:
        return None
    else:
        tr = trie
#se nao, percorre a arvore para cada letra c do nome
        for c in key:
            branch = find_child_branch(tr, c)
            if branch == None: #se nao tem nenhum caminho para a letra c, cria um novo
                new_branch = [c]
                tr.append(new_branch)
                tr = new_branch
            else:
                tr = branch #se achou, repete o processo no proximo nodo
        ## tr is now bound to the branch, so insert
        ## a new bucket.
        tr.append((key,[v]))
        return None

## a branch is either empty or it is a list whose first
## element is a character and the rest are buckets or
## sub-branches.
def get_child_branches(trie):
    if trie == []:
        return []
    else:
        return trie[1:]

def find_child_branch(trie, c):
    for branch in get_child_branches(trie):
       if branch[0] == c:
           return branch
    return None

### ************************ HAS_KEY *************************
       
def has_key(key, trie):
    br = retrieve_branch(k, trie)
    if br == None:
        return False
    else:
        return is_trie_bucket(get_child_branches(br)[0])

### ******************** RETRIEVE_VAL ************************

## find a branch in trie that is indexed under k.
def retrieve_branch(key, trie):
    if key == '':
        return None
    else:
        tr = trie
        for c in key:
            br = find_child_branch(tr, c)
            if br == None:
                return None
            else:
                tr = br
        return tr

## find a branch and retrieve its bucket, second element.
def retrieve_val(key, trie):
    if not has_key(key, trie): return None
    br = retrieve_branch(key, trie)
    return get_bucket_val(br[1])

### *************** START_WITH_PREFIX ************************

def start_with_prefix(prefix, trie):
    ## 1. find the branch indexed by prefix
    br = retrieve_branch(prefix, trie)
    if br == None: return []

    key_list = []
    q = get_child_branches(br)
    ## 2. go through the sub-branches of the
    ## branch indexed by the prefix and
    ## collect the bucket strings into key_list
    while not q == []:
        curr_br = q.pop(0)
        if is_trie_bucket(curr_br):
            key_list.append(get_bucket_key(curr_br))
        elif is_trie_branch(curr_br):
            q.extend(get_child_branches(curr_br))
        else:
            return 'ERROR: bad branch'
    return key_list
