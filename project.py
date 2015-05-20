import requests_oauthlib
import webbrowser
import json
import test106 as test

####twitter client key and client secret
client_key = 'zaPvoQyvecQPO7OxZ3ATfI336' 
client_secret = 'ke1tnUg9A04gR5EcDF2Q6u3QtXXtgNnssu7trc2taUOXy4DCX8'

###instance of OAuth1Session with client keys
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret)

#dictionaries of parameters for three democratic and three republican presidential candidates
clinton = {'user_id': '1339835893', 'screen_name':'HillaryClinton'}
omalley = {'user_id': '15824288', 'screen_name':'GovernorOMalley'}
warren = {'user_id': '970207298', 'screen_name':'SenWarren'}

cruz = {'user_id': '23022687', 'screen_name':'tedcruz'}
bush = {'user_id': '113047940', 'screen_name':'JebBush'}
paul = {'user_id': '216881337', 'screen_name':'RandPaul'}

####create a list of stop words that we can use multiple times 
stop = open("stopwords.txt", "r")
stop_words = stop.read().split()
stop_words += ['&amp;', 'rt'] #get rid of these two commonly used twitter phrases

###create string of democratic platform and republican platforms
def collapse_whitespace(txt): #turns newlines and tabs into spaces and collapses multiple spaces
    txt = txt.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    res = ""
    prev = ""
    for c in txt:
        if c != " " or prev != " ":
            res += c
        prev = c
    return res 
ddat = open("demplatform.txt", 'r')
dplat = collapse_whitespace(ddat.read()) #democratic platform
ddat.close
rdat = open("repplatform.txt", "r")
rplat = collapse_whitespace(rdat.read()) #republican platform
rdat.close

###accumulate top 50 words in each platform
def top_50w(string):
    wrds = {}
    for i in string.split():
        i = i.lower()
        if not i in stop_words:
            if i in wrds:
                wrds[i] += 1
            else:
                wrds[i] = 1
    top50 = sorted(wrds, key= lambda x: wrds[x], reverse = True)[:51]
    return top50
dplat_50 = top_50w(dplat) #top 50 words in 2012 democratic platform
rplat_50 = top_50w(rplat) #top 50 words in 2012 republican platform

#function that gets the most recent 500 tweets for a politician given his/her dictionary of parameters
def list_of_tweets(polit_dict):
    ids = []
    max_id = None
    polit_dict['count'] = 100
    tweets = []
    for i in range(5): #5 pages with 100 words each
        if len(ids) > 0:
            polit_dict['max_id'] = min(ids) - 1
        r = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json",
                    params = polit_dict)           
        response = r.json()
        ids = ids + [tweet['id'] for tweet in response]
        tweets += [response[a]["text"] for a in range(len(response))]
    return tweets

def remove_non_ascii(txt): #gets rid of a string's non-ascii characters
    return ''.join(i for i in txt if ord(i)<128)
test.testEqual(remove_non_ascii(u'a' + u'\xc2' + u'b'), u'ab')
test.testEqual(remove_non_ascii(u'\xc2'), '')
 
class Candidate: #each instance will be one candidate
    def __init__(self, cand, party_affil, twitter_dict):
        self.name = cand
        self.party = party_affil
        self.handle = twitter_dict["screen_name"]
        self.id = twitter_dict["user_id"]
        self.dict = twitter_dict
    def top_50(self): #top fifty words in the candidate's last 500 tweets
        all_tweets = list_of_tweets(self.dict)
        string_of_all_tweets = " ".join(all_tweets)
        return top_50w(string_of_all_tweets)
    def string_of_tweets(self): #
        all_tweets = list_of_tweets(self.dict)
        string_of_all_tweets = " ".join(all_tweets)
        string_of_all_tweets = str(remove_non_ascii(string_of_all_tweets))
        return string_of_all_tweets
test_case = Candidate(cand = 'Barack Obama', party_affil='Democrat', twitter_dict={'user_id': '813286', 'screen_name':'BarackObama'})
test.testEqual(test_case.handle, 'BarackObama')
test.testEqual(type(test_case.top_50()), type([]))

        
def overlap(cand): #how many words overlap with the party platform
    accum = 0
    if cand.party.lower() == "democrat":
        for i in cand.top_50():
            if i in dplat_50:
                accum += 1
        return accum
    elif cand.party.lower() == "republican":
        for i in cand.top_50():
            if i in rplat_50:
                accum += 1
        return accum
    else:
        return "error: incorrect party entry"
            
#####create Shannon guesser
def guesser(prev_txt, rls): #creating the guesser
    all_guesses = ""
    for (suffix, guesses) in rls:
        try:
            if suffix == None or prev_txt[-len(suffix):] == suffix:
                all_guesses += guesses
        except:   
            pass 
    return all_guesses    
    
def next_letter_frequencies(txt): #function to get a dictionary of next letter frequencies
    r = {} 
    for i in range(len(txt)-1): 
        if txt[i] not in r:
            r[txt[i]] = {}
        next_letter_freqs = r[txt[i]]
        next_letter = txt[i+1]
        if next_letter not in next_letter_freqs: 
            next_letter_freqs[next_letter] = 1 
        else: 
            next_letter_freqs[next_letter] = next_letter_freqs[next_letter] + 1 
    return r 
test.testEqual(type(next_letter_frequencies('Hello my name is Dominic Russel')), type({}))   
    
dem_letter_counts = next_letter_frequencies(dplat)
rep_letter_counts = next_letter_frequencies(rplat)

def concat_all(L):
    res = ""
    for s in L:
        res += s
    return res 
    
def letter_rule(counts): #the letter rule we are going to use
    ltr_rls = []
    for i in counts:
        kys = counts[i].keys()       
        freqs_lst = sorted(kys, key= lambda x: counts[i][x], reverse=True)
        freqs_str = concat_all(freqs_lst)
        tup = (i, freqs_str)
        ltr_rls.append(tup)
    return ltr_rls

ltr_rls_dem = letter_rule(dem_letter_counts) #letter rule with democratic platform as training data
ltr_rls_rep = letter_rule(rep_letter_counts) #letter rule with republican platform as training data

def performance(txt, rls): 
    tot = 0
    for i in range(len(txt)-1):
        to_try = guesser(txt[:i+1], rls) 
        guess_count = to_try.index(txt[i+1])
        tot = tot + guess_count
    return float(tot)/len(txt) -1   

    
def shannon(cand):
    print "running guesser for %s" % cand.name #update to let user know what is going on with program
    string_of_all_tweets = cand.string_of_tweets()
    lets = []
    for x in string_of_all_tweets:
        if x not in lets:
            lets.append(x)
    alphabet = "".join(sorted(lets))
    default_rule = (None, alphabet)
    if cand.party.lower() == 'democrat': #if a democrat own rules are based on the democratic platform, other wise rules based on republican platform
        rules_own = ltr_rls_dem + [default_rule]
        rules_opp = ltr_rls_rep + [default_rule]
    elif cand.party.lower() == 'republican':
        rules_own = ltr_rls_rep + [default_rule]
        rules_opp = ltr_rls_dem + [default_rule]
    else:
        print 'incorrect party'
    own_perf = performance(string_of_all_tweets[:20000], rules_own) #only first 20,0000 characters or it takes too long
    opp_perf = performance(string_of_all_tweets[:20000], rules_opp) 
    print "own party guesser took %.2f guesses per character, opposite party guesser took %.2f guesses per character" % (own_perf, opp_perf)
    return [own_perf , opp_perf - own_perf]
    
Cruz = Candidate(cand = 'Ted Cruz', party_affil = 'Republican', twitter_dict = cruz)
Bush = Candidate(cand = 'Jeb Bush', party_affil = 'Republican', twitter_dict = bush)
Paul = Candidate(cand= 'Rand Paul', party_affil = 'Republican', twitter_dict = paul)

Clinton = Candidate(cand = 'Hillary Clinton', party_affil = 'Democrat', twitter_dict = clinton)
Warren = Candidate(cand = 'Elizabath Warren', party_affil = 'Democrat', twitter_dict = warren)
Omalley = Candidate(cand = "Martin O'Malley", party_affil = 'Democrat', twitter_dict = omalley)

polit = [Cruz, Bush, Paul, Clinton, Warren, Omalley] #list of all instances of the candidate class

dat = open('proj_output.csv', 'w')
dat.write("polit_name, polit_party, polity_handle, overlap_words, own_guesser_perf, guesser_diff\n")
for i in polit:
    list_of_perf = shannon(i)
    dat.write("%s, %s, %s, %d, %.2f, %.2f\n" % (i.name, i.party, i.handle, overlap(i), list_of_perf[0], list_of_perf[1]))