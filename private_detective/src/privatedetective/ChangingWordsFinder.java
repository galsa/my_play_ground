package privatedetective;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class ChangingWordsFinder {

	public Set<String> findChangingWords(String content) {
		Set<String> allChangingWords = new HashSet<String>();
		
		String[] sentences = content.split("\n");
		for (String sentence : sentences) {
			allChangingWords.add(findChangingWord(sentence, sentences));
		}

		return allChangingWords;
	}

	private String findChangingWord(String sentenceToFind, String[] sentences) {
		// sample input: 
		//01-01-2012 19:45:00 Naomi is getting into the car
		//02-01-2012 09:13:15 George is getting into the car
		String strippedSentenceToFind = stripDateTimeFromSentence(sentenceToFind);
		StringBuilder changingWords = new StringBuilder();
		for (String currentSentence : sentences) {
			String StrippedCurrentSentence = stripDateTimeFromSentence(currentSentence);	
			//ignore similar sentences
			if(!strippedSentenceToFind.equals(StrippedCurrentSentence)) {
				//compare all words in the two sentences and see if they match 
				//if not put the word that does not match into a list 
				//if list contains one word then we found a changing word 
				// add changing word to outer list
				String[] sentenceContent = strippedSentenceToFind.split(" ");
				ArrayList<String> currentChangingWords = new ArrayList<>();
				for (String word : sentenceContent) {
					if(!currentSentence.contains(word)){
						currentChangingWords.add(word);
					}
				}
				if(currentChangingWords.size() == 1) {
					changingWords.append(currentChangingWords.get(0));
					changingWords.append("\n");
				}
			}
		}
		
		return changingWords.toString();
	}
	
	
	private String stripDateTimeFromSentence(String inputString) {
		//could use regular expression to do all in one (was too lazy)
		String removeDash = inputString.replaceAll("-", "");
		String removeTwoDots = removeDash.replaceAll(":", "");
		String removeNumbers = removeTwoDots.replaceAll("[0-9]","");
		return removeNumbers.trim().toLowerCase();
	}
	
	

}
