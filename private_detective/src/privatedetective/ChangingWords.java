package privatedetective;

import java.util.Set;

public class ChangingWords {
	
		
	public static void main(String[] args) {
		String inputFilePath = args[0];
		String outputFilePath = args[1];
		ChangingWordsFinder sentenceSimilarityFinder = new ChangingWordsFinder();
		
		try {
			String fileContent = FileHandler.readFile(inputFilePath);
			Set<String> foundChangingWords = sentenceSimilarityFinder.findChangingWords(fileContent);
			FileHandler.writeFile(outputFilePath, foundChangingWords);	
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		

	}

}
