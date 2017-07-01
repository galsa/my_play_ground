package privatedetective;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;

public class FileHandler {

	public static String readFile(String file) throws Exception {
		FileReader fileReader = new FileReader(new File(file));
		try {
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			StringBuffer fileContent = new StringBuffer();
			String line;
			System.out.println("start readingLines:");
			while ((line = bufferedReader.readLine()) != null) {
				System.out.println(line);
				fileContent.append(line);
				fileContent.append("\n");
			}
			System.out.println("Done reading file");

			return fileContent.toString();
		} finally {
			fileReader.close();
		}
	}

	public static void writeFile(String outputFilePath, Set<String> contentToWrite) {
		BufferedWriter bw = null;
		FileWriter fw = null;
		try {
			fw = new FileWriter(outputFilePath);
			bw = new BufferedWriter(fw);
			System.out.println("start writing lines:");
			bw.write("The changing word was:");
			bw.write("\n");
			for (String currentContent : contentToWrite) {
				System.out.println(currentContent);
				bw.write(currentContent);
			}
			System.out.println("Done writing file");
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (bw != null)
					bw.close();

				if (fw != null)
					fw.close();

			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}

	}

}
