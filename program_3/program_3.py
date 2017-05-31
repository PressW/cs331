import nltk, random
from nltk.tokenize import word_tokenize, RegexpTokenizer




# Read in files to a data structure
def read_reviews():
    raw_train = []
    raw_test = []
    raw_total = []
    tokenizer = RegexpTokenizer(r'\w+')
    
    with open("trainingSet.txt", 'r') as train_file:
        lines = train_file.read().splitlines()
        for line in lines:
            line = tokenizer.tokenize(line)
            raw_train.append(line)
            del line[-1]
            raw_total.append(line)

    with open("testSet.txt", 'r') as test_file:
        lines = test_file.read().splitlines()
        for line in lines:
            line = tokenizer.tokenize(line)
            raw_test.append(line)
            del line[-1]
            raw_total.append(line)

    return raw_train, raw_test, raw_total



# Gets frequency distribution for most / least common words
def freq_dist(tokens, word_dist=None):
    # iterate through each word in each tweet and create frequency distrubution
    all_words = [w for i in range(0, len(tokens)) for w in tokens[i]]
    all_words = nltk.FreqDist(all_words)
    
    # print(all_words.most_common(25))
    if word_dist is not None:
        print(word_dist, ":", all_words[word_dist])
    
    return all_words



# Creates a feature dictionary of tweet with True/False values for each word in the lexicon
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
    word_features = list(all_words.keys())
    train_feat = [(get_features(review, word_features), review[-1]) for review in train]
    test_feat = [(get_features(review, word_features), review[-1]) for review in test]
    
    return word_features, train_feat, test_feat





if __name__ == "__main__":
    
    # Baseline dataset for trainig the classifier
    train_set, test_set, raw_total = read_reviews()
    
                        
    # Generate feature_dict, training_set, and testing_set
    feature_dict, train_feat, test_feat = create_featureset(raw_total, train_set, test_set)
    print(test_feat)


    # Train the classifier
    
    
    # Apply classifier to testing stet
