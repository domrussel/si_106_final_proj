READ ME - Dominic Russel final project
Using a Shannon Guesser and 2012 Party Platforms to Analyze Possible 2016 Presidential Candidates' Twitter Feeds 

The modules required for this program are: requests_oauthlib, webbrowser, json, and test106

My program uses the twitter API to get the last 500 tweets of six different confirmed or possible 2016 presidential candidates, including:
Republicans: Ted Cruz, Rand Paul, and Jeb Bush
Democrats: Hillary Clinton, Martin O'Malley, and Elizabeth Warren

For each of these candidates I created one instance of the class Candidate which takes as inputs the candidate's name, their party affiliation, and a dictionary of parameters that can be passed to a twitter oauth get call
Each instance of stores the candidate name, party, handle, id, and parameters dictionary and has two methods: one which finds the top 50 words in the feed, and another that creates a string of all the tweets combined
I used the 2012 republican and democratic party platforms to compare the most commonly used words in each party platform in that year to the most commonly used words in the candidate's current feed
I removed stop words such as "the", "that", and "and" by using the list of stop words stored in the text file stop_words.txt
My first output is the number of top 50 words that overlap between the candidate's twitter feed and the party platform.

In addition to the most common words, I also created a Shannon guesser that guesses the next letters of a string of all the twitter user's tweets using the party platform as training data.
My goal with the Shannon guesser is not to be as accurate as possible, but to investigate how similar the tweets are to the party platform. I found that the best way to do this is by using only two rules:
One that guesses the next character based on next character frequencies for all characters in the training data, and a second default "backstop" rule that will guess every character in the twitter feed
I did not include non-ascii characters in my analysis, and used a function to remove them

I ran the Shannon guesser performance function on the first 20000 characters in each candidate's twitter feed (for efficiency purposes), with both the candidate's own party platform as training data and the opposing party platform as training data
Interestingly, with only the simple rules I used, the own party platform was a more efficient guesser than the opposing party platform for every single candidate in my study.
My two outputs were the average number of Shannon guesses per word using the own party platform as training data and the difference between the two party platforms guess per word (opposing minus own).
This last statistic may tell us something about how polarized a candidate's twitter feed is, with a high difference indicates a very polarized twitter feed

I have test cases that ensure the functions remove_non_ascii (which removes non ascii characters from a string) and next_letter_frequencies (which creates a dictionary of next letter frequencies for each letter given a string) are working properly. I also used a test to test the init method in the candidate class. 
My outputs are written to the csv proj_output.csv

Submitted along with my project code in the file project.py are the files demplatform.txt, repplatform.txt, and stop_words.txt which are necessary to run the program.



