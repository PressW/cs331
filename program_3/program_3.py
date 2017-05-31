import nltk, random
import numpy as np
from nltk.tokenize import word_tokenize, RegexpTokenizer




# Read in files to a data structure
def read_reviews():
    raw_training = []
    raw_testing = []
    raw_all = []
    tokenizer = RegexpTokenizer(r'\w+')

    with open("trainingSet.txt", 'r') as training_file:
        lines = training_file.read().lower().splitlines()
        for line in lines:
            line = tokenizer.tokenize(line)
            raw_training.append(line)
            raw_all.append(line[:-1])

    with open("testSet.txt", 'r') as testing_file:
        lines = testing_file.read().lower().splitlines()
        for line in lines:
            line = tokenizer.tokenize(line)
            raw_testing.append(line)
            #raw_all.append(line[:-1])

    return raw_training, raw_testing, raw_all



# Gets frequency distribution for most / least common words
def freq_dist(tokens, word_dist=None):
    # iterate through each word in each review and create frequency distrubution
    all_words = [w for i in range(0, len(tokens)) for w in tokens[i]]
    all_words = nltk.FreqDist(all_words)

    # print(all_words.most_common(25))
    if word_dist is not None:
        print(word_dist, ":", all_words[word_dist])

    return all_words



# Creates a feature dictionary of reviews with True/False values for each word in the lexicon
def get_features(review, word_features):
    review_words = set(review)
    features = {}
    for word in word_features:
        features[word] = (word in review_words)
    return features



# Takes the raw initial data and produces the lexicon, training set, and testing set
def create_featureset(tokenized_reviews, train, test):
    random.shuffle(tokenized_reviews)
    all_words = freq_dist(tokenized_reviews)
    features = list(all_words.keys())
    train_feat = [(get_features(review, features), int(review[-1])) for review in train]
    test_feat = [(get_features(review, features), int(review[-1])) for review in test]

    return features, train_feat, test_feat



def classifier(features, dataset):
    total_reviews = len(dataset)
    positive_reviews = sum([review_tuple[1] for review_tuple in dataset])
    negative_reviews = total_reviews - positive_reviews

    global prob_positive
    global prob_negative
    prob_positive = float(positive_reviews) / total_reviews
    prob_negative = float(negative_reviews) / total_reviews

    probabilities = {}
    for word in features:
        total_wc = 0
        positive_wc = 0
        negative_wc = 0

        for review_tuple in dataset:
            if review_tuple[0][word]:
                total_wc += 1
                if review_tuple[1]:
                    positive_wc += 1
                else:
                    negative_wc += 1

        prob_exists_positive = float(positive_wc) / positive_reviews
        prob_exists_negative = float(negative_wc) / negative_reviews
        prob_missing_positive = 1 - prob_exists_positive
        prob_missing_negative = 1 - prob_exists_negative
        probabilities[word] = (prob_exists_positive, prob_exists_negative, prob_missing_positive, prob_missing_negative)

    return probabilities

def applyClassifier(dataset, probs):
    results = []
    predict_count = 0
    predict_correct = 0
    for review_tuple in dataset:
        prob_positive_review = np.log(prob_positive)
        prob_negative_review = np.log(prob_negative)

        for word in review_tuple[0]:
            if review_tuple[0][word]:
                prob_positive_review *= np.log(probs[word][0])
                prob_negative_review *= np.log(probs[word][1])
            else:
                prob_positive_review *= np.log(probs[word][2])
                prob_negative_review *= np.log(probs[word][3])

        prediction = prob_positive_review > prob_negative_review
        predict_count += 1
        if prediction and (review_tuple[1] == 1):
            predict_correct += 1
        if (not prediction) and (review_tuple[1] == 0):
            predict_correct += 1
        results.append(prediction)
        print(prediction)
    print("Accuracy: ", (float(predict_correct)/predict_count))






if __name__ == "__main__":

    # Baseline dataset for trainig the classifier
    training_set, testing_set, raw_all = read_reviews()


    # Generate feature_dict, training_set, and testing_set
    features, training, testing = create_featureset(raw_all, training_set, testing_set)
    #print(testing[0:1])


    # Train the classifier
    probs = classifier(features, training)
    # for word in probs:
    #     print(probs[word])


    # Apply classifier to testing set
    applyClassifier(training, probs)
