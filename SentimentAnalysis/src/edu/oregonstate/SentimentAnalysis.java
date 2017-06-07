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

    static class Probabilities {
        double probPositive = 0;
        double probNegative = 0;
        WordProbabilities[] words;
    }

    static class WordProbabilities {
        double probExistsInPositive = 0;
        double probExistsInNegative = 0;
        double probMissingInPositive = 0;
        double probMissingInNegative = 0;
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

        Probabilities probs = calculateProbabilities(trainingMatrix, vocabulary);

        float trainingAccuracy = classify(trainingMatrix, vocabulary, probs);
        float testingAccuracy = classify(testingMatrix, vocabulary, probs);

        System.out.println("Prediction Accuracies:");
        System.out.println("\tTraining set: " + trainingAccuracy);
        System.out.println("\tTesting set: " + testingAccuracy);
    }

    static float classify(boolean[][] reviewMatrix, String[] vocabulary, Probabilities probs) {
        int correctPredictions = 0;

        for (boolean[] reviewLine : reviewMatrix) {
            double predictPositive = Math.log10(probs.probPositive);
            double predictNegative = Math.log10(probs.probNegative);
            for (int wordNum = 0; wordNum < vocabulary.length; wordNum++) {
                if (reviewLine[wordNum]) {
                    predictPositive += Math.log10(probs.words[wordNum].probExistsInPositive);
                    predictNegative += Math.log10(probs.words[wordNum].probExistsInNegative);
                } else {
                    predictPositive += Math.log10(probs.words[wordNum].probMissingInPositive);
                    predictNegative += Math.log10(probs.words[wordNum].probMissingInNegative);
                }
            }

            if (reviewLine[vocabulary.length] ^ predictPositive < predictNegative)
                correctPredictions++;
        }

        return ((float) correctPredictions) / reviewMatrix.length;
    }

    static Probabilities calculateProbabilities(boolean[][] reviewMatrix, String[] vocabulary) {
        int totalReviews = reviewMatrix.length;
        int positiveReviews = 0, negativeReviews = 0;
        for (boolean[] reviewLine : reviewMatrix) {
            if (reviewLine[vocabulary.length]) {
                positiveReviews++;
            } else {
                negativeReviews++;
            }
        }

        WordProbabilities[] wordProbs = new WordProbabilities[vocabulary.length];

        for (int wordNum = 0; wordNum < vocabulary.length; wordNum++) {
            int countExistsInPositive = 0, countExistsInNegative = 0, countMissingInPositive = 0, countMissingInNegative = 0;

            for (boolean[] reviewLine : reviewMatrix) {
                boolean wordExists = reviewLine[wordNum];
                boolean positiveReview = reviewLine[vocabulary.length];
                if (wordExists) {
                    if (positiveReview) countExistsInPositive++;
                    else countExistsInNegative++;
                } else {
                    if (positiveReview) countMissingInPositive++;
                    else countMissingInNegative++;
                }
            }
            WordProbabilities wordProb = new WordProbabilities();
            wordProb.probExistsInPositive = ((double) countExistsInPositive + 1) / (positiveReviews + 2);
            wordProb.probExistsInNegative = ((double) countExistsInNegative + 1) / (negativeReviews + 2);
            wordProb.probMissingInPositive = ((double) countMissingInPositive + 1) / (positiveReviews + 2);
            wordProb.probMissingInNegative = ((double) countMissingInNegative + 1) / (negativeReviews + 2);

            wordProbs[wordNum] = wordProb;
        }

        Probabilities probs = new Probabilities();
        probs.probPositive = ((double) positiveReviews) / totalReviews;
        probs.probNegative = 1 - probs.probPositive;
        probs.words = wordProbs;

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
