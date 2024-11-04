AI code completion

This repo is dedicated to small research in AI code completion <br>
*rotating.py* and *settle_debts* are two files from my projects

First one is geometry problem, implementation of 3d polyhedrons rotation, while second is some backend code.

First thing I did, was splitting code into meaningful parts - I wrote a script for that (*dataset_creation.py*), which is splitting code into data samples by
empty string delimeter. I checked prior to that that in two code files being studied, empty lines split meaningful pieces of code (for example to avoid variable being initiated at first chunk and used in second)

Then I wrote code-in-the middle generator *code_completer.py*, which was completing middle part of the code, which was initially taken out. I tried to take out approximately central third of each of the sample chunks of code.
The result of generation, as well as expected results, I put in CSV files - *results.csv* for geometry code completion and *results01.csv* for backend code completion

And of course the most interesting part is analysis of what was generated. First thing I noticed was the intersting behaviour of generated code, depending on number of tokens given for the code completion
It is quiet hard to fing right number, because when code is not 2 + 2 = 4, there is a variety of possible completions. For example given class initialization and end of some class function, depending on the number of tokens,
model would generate 1 or 10 different class functions (in geometry problem especially).

So, I decided to make number of tokens depending on the length of the initial data sample, however no one knows the exact formula for this number, so I used some heuristic formula.

Next step was to manually review and compare completed code with actual one. Prior to review I expected to see the following: 
1. The Geometry code should be completed perfectly or at least near to perfect, since it is very structurized and formulas are really basic
2. The backend code is not going to be completed very well, since there is a variety of possible completions, and different parts of code are depending on different parts of code, not only themselves

After manually analizing the code, I realized that 2 prediction was right and 1 was wrong. I even didn't fing any sense in putting labels on each sample, after viewing each example it was pretty clear, that code was absolutly as not expected

However, the geometry part was still better. I found 1 full match and around 10 out of nearly 30 examples, where main idea of the middle part of the code chunk was implemented quite the same as in original, but with tiny mistakes, mistypes OR (which was the case quite often)
with extra not-needed code. Samples from *settle_debts.py* were absolutly disappointing, I didn't find almost any correlation. So, relation between these two files code completion was as I initially expected, but the actual code completion was awful

Then I computed some metrics with *metrics.computation.py*. I chose exact match, chrf, bleu and rouge_l. I got the following results:
```
[em = 6.451612903225806, chrf = 32.76398059704879, bleu = 14.694877275265153, rouge_L = 0.3238015509319212]
``` 
geometry code
```
[em = 7.6923076923076925,chrf = 36.61228935092885,bleu = 12.136081968730364, rouge_L = 0.3421459745927831]
```
backend code
(honestly, exact match is not exactly exact :). Number of spaces was failing the only candidate for the whole match, so I reduced the requirements for the match, ignoring the spaces)

Actually, the results in general correlates pretty much with my impression of the completed pieces of code. The exact match is low, as expected (probably only 1 or 2 completions match fully from each of the code files chunks)
Chrf - which shows how good n-grams of characters matches show relatively high percentage, around 35 per cent. It is quite expectable, as character n-grams match correlates really week with real code correlation
Bleu - which is the same n-grams metric, but of words, expectedly, is showing much lower percentages - around 13 per cent. Of course, I would expect such numbers, since completion is realy bad
The last metric, showing the relation of LCS of generated and expected code is not very low. I think it could be because code structure is somewhere conserved, while useless pieces of code are inserted enough to break it's logic but not to resuce the length of LCS to 0

The only thing I didn't expected is that backend code metrics are quite the same as ones for the geometry code


