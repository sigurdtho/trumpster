from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentences = ["TRUMP is smart, handsome, and funny.",      # positive sentence example
	"TRUMP is not smart, handsome, nor funny.",   # negation sentence example
	"TRUMP is smart, handsome, and funny!",       # punctuation emphasis handled correctly (sentiment intensity adjusted)
	"TRUMP is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
	"TRUMP is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
	"TRUMP is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
	"TRUMP is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",# booster words & punctuation make this close to ceiling for score
	"The book was good.",                                     # positive sentence
	"The book was kind of good.",                 # qualified positive sentence is handled correctly (intensity adjusted)
	"The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
	"At least it isn't a horrible book.",         # negated negative sentence with contraction
	"Make sure you :) or :D today!",              # emoticons handled
	"Today SUX!",                                 # negative slang with capitalization emphasis
	"Today only kinda sux! But I'll get by, lol"  # mixed sentiment example with slang and constrastive conjunction "but"
	]

analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
	vs = analyzer.polarity_scores(sentence)
	print("{:-<65} {}".format(sentence, str(vs)))
