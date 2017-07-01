# private_detective

What can you say about the complexity of your code?
As I go over each sentence and compare all the words of the sentence to all other sentences to find the difference
then the complexity is O(n)[3]

How will your algorithm scale?If you had two weeks to do this task, what would you have done differently? 
My algorithm won't scale for a very large data set.
I could use one of the available algorithms for similarity in text 
(I will need to find an existing implementation in java and read about it a bit to find the best match):

1) Cosine similarity
2) Jaccard similarity
3) Dice's coefficient
4) Matching similarity
5) Overlap similarity

I could use indexed text to improve performance (for example: index the text using Lucene)

What would be better?
1) Find a better mechanism for the search as mentioned above
2) Add logging
3) Add tests (including performance tests)
