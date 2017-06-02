package edu.oregonstate;

import java.io.*;
import java.util.*;

public class SentimentAnalysis {

    static class Review {
        List<String> words;
        boolean rating;
        Review(List<String> words, boolean rating) {
            this.words = words;
            this.rating = rating;
        }
    }

    static class WordProbabilities {
        int positiveCount = 0;
        int negativeCount = 0;
        float probExistsInPositive = 0;
        float probExistsInNegative = 0;
        float probMissingInPositive = 0;
        float probMissingInNegative = 0;
        int totalCount() {
            return positiveCount + negativeCount;
        }
    }

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Incorrect number of arguments");
            return;
        }

        Review[] trainingReviews = null, testingReviews = null;
        try {
            trainingReviews = readReviews(args[0]);
            testingReviews = readReviews(args[1]);
        } catch (IOException e) {
            e.printStackTrace();
        }

        String[] vocabulary = getWordsInReviews(trainingReviews);

        boolean[][] trainingMatrix = featurizeReviewSet(trainingReviews, vocabulary);
        boolean[][] testingMatrix = featurizeReviewSet(testingReviews, vocabulary);

        writeReviewMatrixToFile(trainingMatrix, vocabulary, "preprocessed_train.txt");
        writeReviewMatrixToFile(testingMatrix, vocabulary, "preprocessed_test.txt");

        WordProbabilities[] probs = calculateProbabilities(trainingMatrix, vocabulary);

        classify(testingMatrix, vocabulary, probs);
    }

    static void classify(boolean[][] reviewMatrix, String[] vocabulary, WordProbabilities[] probs) {
        int totalReviews = reviewMatrix.length;
        int positiveReviews = 0, negativeReviews = 0;
        for (boolean[] reviewLine : reviewMatrix) {
            if (reviewLine[vocabulary.length]) {
                positiveReviews++;
            } else {
                negativeReviews++;
            }
        }
        double probPositive = (double)positiveReviews / totalReviews;
        double probNegative = (double)negativeReviews / totalReviews;

        int correctPrecitions = 0, wrongPredictions = 0;

        for (boolean[] reviewLine : reviewMatrix) {
            double predictPositive = Math.log10(probPositive);
            double predictNegative = Math.log10(probNegative);
            for (int wordNum = 0; wordNum < vocabulary.length; wordNum++) {
                if (reviewLine[wordNum]) {
                    predictPositive += Math.log10(probs[wordNum].probExistsInPositive);
                    predictNegative += Math.log10(probs[wordNum].probExistsInNegative);
                } else {
                    predictPositive += Math.log10(probs[wordNum].probMissingInPositive);
                    predictNegative += Math.log10(probs[wordNum].probMissingInNegative);
                }
            }

            if (reviewLine[vocabulary.length] && predictPositive > predictNegative)
                correctPrecitions++;
            else wrongPredictions++;
        }
        System.out.println("Prediction accuracy: " + (float)correctPrecitions / reviewMatrix.length);
    }

    static WordProbabilities[] calculateProbabilities(boolean[][] reviewMatrix, String[] vocabulary) {
        int totalReviews = reviewMatrix.length;
        int positiveReviews = 0, negativeReviews = 0;
        for (boolean[] reviewLine : reviewMatrix) {
            if (reviewLine[vocabulary.length]) {
                positiveReviews++;
            } else {
                negativeReviews++;
            }
        }
        double probPositive = (double)positiveReviews / totalReviews;
        double probNegative = (double)negativeReviews / totalReviews;

        WordProbabilities[] probs = new WordProbabilities[vocabulary.length];

        for (int wordNum = 0; wordNum < vocabulary.length; wordNum++) {
            WordProbabilities wordProbabilities = new WordProbabilities();
            for (int reviewNum = 0; reviewNum < reviewMatrix.length; reviewNum++) {
                if (reviewMatrix[reviewNum][wordNum]) {
                    if (reviewMatrix[reviewNum][vocabulary.length])
                        wordProbabilities.positiveCount++;
                    else
                        wordProbabilities.negativeCount++;
                }
            }
            wordProbabilities.probExistsInPositive = (float)wordProbabilities.positiveCount / positiveReviews;
            wordProbabilities.probExistsInPositive = (float)wordProbabilities.negativeCount / negativeReviews;
            wordProbabilities.probMissingInPositive = 1 - wordProbabilities.probExistsInPositive;
            wordProbabilities.probMissingInNegative = 1 - wordProbabilities.probExistsInNegative;

            probs[wordNum] = wordProbabilities;
        }

        return probs;
    }

    static void writeReviewMatrixToFile(boolean[][] reviewMatrix, String[] vocabulary, String filename) {
        try (FileWriter fileWriter = new FileWriter(filename)) {
            for (String word : vocabulary) {
                fileWriter.write(word + ",");
            }
            fileWriter.write("classlabel\n");
            for (boolean[] reviewLine : reviewMatrix) {
                for (int wordNum = 0; wordNum < vocabulary.length; wordNum++) {
                    fileWriter.write((reviewLine[wordNum] ? 1 : 0) + ",");
                }
                fileWriter.write((reviewLine[vocabulary.length] ? 1 : 0) + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static boolean[][] featurizeReviewSet(Review[] reviews, String[] vocabulary) {
        boolean[][] reviewMatrix = new boolean[reviews.length][vocabulary.length + 1];
        for (int reviewNum = 0; reviewNum < reviews.length; reviewNum++) {
            Review review = reviews[reviewNum];
            for (int wordNum = 0; wordNum < vocabulary.length; wordNum++) {
                reviewMatrix[reviewNum][wordNum] = review.words.contains(vocabulary[wordNum]);
            }
            reviewMatrix[reviewNum][vocabulary.length] = review.rating;
        }
        return reviewMatrix;
    }

    static String[] getWordsInReviews(Review[] reviews) {
        Set<String> words = new HashSet<>();
        for (Review review : reviews) {
            words.addAll(review.words);
        }
        List<String> sortedWords = new ArrayList<>(words);
        Collections.sort(sortedWords);
        return sortedWords.toArray(new String[words.size()]);
    }

    static Review[] readReviews(String filename) throws IOException {
//        String cwd = Paths.get(".").toAbsolutePath().normalize().toString();
        FileReader fileReader = new FileReader(filename);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        List<Review> reviews = new ArrayList<>();
        String line;
        while ((line = bufferedReader.readLine()) != null) {
            String[] wordsAndRating = line.split("\t");
            String[] words = wordsAndRating[0].toLowerCase().replaceAll("\\W", " ").trim().split(" +");
            boolean rating = !"0".equals(wordsAndRating[1].trim());
            reviews.add(new Review(Arrays.asList(words), rating));
        }
        bufferedReader.close();
        return reviews.toArray(new Review[reviews.size()]);
    }
}
