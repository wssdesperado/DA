from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.models import CoherenceModel
from pprint import pprint
import gensim
import pandas as pd
import json
def get_stopwords():
    stop_words = []
    with open('../dataset/stops.txt','r') as f:
        for stop in f.readlines():
            stop_words.append(stop.strip('\n'))
    return stop_words
def LDA():
    #stop_words = stopwords.word('english')
    stop_words = get_stopwords()
    # manually add some words
    stop_words.extend(['data','case','covid','report','test','total','update','2021','2020','19','thi','updat','due','http'])
    tokenizer = RegexpTokenizer(r'\w+')
    p_stemmer = PorterStemmer()
    texts = []
    with open('../dataset/States_info.json','r') as f:
        data = json.load(f)
        for temp in data :
            doc = temp['notes']
            # clean and tokenize document string
            raw = doc.lower()
            tokens = tokenizer.tokenize(raw)
            # stem tokens, do the stem step first
            stemmed_tokens = [p_stemmer.stem(i) for i in tokens]
            # remove stop words from tokens
            stopped_tokens = [i for i in stemmed_tokens if not i in stop_words]
            # add tokens to list
            texts.append(stopped_tokens)
            # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(texts)
        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in texts]
        # generate LDA model
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=30)
        list = ldamodel.get_document_topics(corpus)
        print(list)
        pprint(ldamodel.print_topics(num_topics=5))
        # Compute Coherence Score
        # Score near 0 is good
        coherence_model_lda = CoherenceModel(model=ldamodel, texts=texts,
                                             dictionary=dictionary, coherence='u_mass')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)

        df_topic_sents_keywords = format_topics_sentences(ldamodel, corpus,texts)

        # Format
        df_dominant_topic = df_topic_sents_keywords.reset_index()
        df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

        # Show
        pd.set_option('display.width', None)
        print(df_dominant_topic.head(10))
        df_dominant_topic.to_csv('../dataset/LDA_results.csv')
        # Distribution
        topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()
        topic_distribution  = topic_counts.reset_index()
        topic_distribution.columns = ['Topic_No','Documents_number']
        print(topic_distribution)

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


if __name__ == '__main__':
    LDA()
