#fachreyzaputra@gmail.com

import pandas as pd, numpy as np, tweepy, re, string, csv, sqlite3, datetime as dt
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

token_data = open (r'twitter-token.csv')
tokens = csv.reader(token_data, delimiter=',')

data_token = []
for row in tokens:
    data_token.append(row[1])

consumer_key = data_token[0]
consumer_secret = data_token[1]
access_token = data_token[2]
access_token_secret = data_token[3]

def twitter_setup():
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Return API with authentication:
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api 
extractor = twitter_setup()

def update_data():
    tweets = []
    count = 1

    search_words = "vaksin covid"
    new_search = search_words + " -filter:retweets"

    for tweet in tweepy.Cursor(extractor.search, q=new_search, count=500).items(50000):
        #print(count)
        count += 1
        try: 
            data = [tweet.id, tweet.created_at, tweet.text, tweet.user._json['screen_name']]
            data = tuple(data)
            tweets.append(data)

        except tweepy.TweepError as e:
            print(e.reason)
            continue

        except StopIteration:
            break

    df = pd.DataFrame(tweets, columns = ['ID', 'Created_at', 'Tweets', 'Username'])
    df['Created_at'] = df['Created_at'].dt.normalize()
    print("\nJumlah Tweets yang di ekstrak : {}.\n".format(len(tweets)))

    #punc
    def remove_punct(text):
        text = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', text) # Menghapus @mentions
        text = re.sub(r'#', ' ', text) # Menghapus '#' hash tag
        text = re.sub(r'RT[\s]+', ' ', text) # Menghapus RT
        text = re.sub(r'[0-9]+', ' ', text) #Menghapus angka
        text = text.lower()
        return text
    df['Tweets_punct'] = df['Tweets'].apply(remove_punct)

    #token and lower
    def tokenization(text):
        text = re.split(r'\W+', text)
        return text
    df['Tweet_tokenized'] = df['Tweets_punct'].apply(tokenization)

    #stopword
    factory = StopWordRemoverFactory()
    stopword = factory.get_stop_words()
    def remove_stopwords(text):
        text = [word for word in text if word not in stopword]
        return text
    df['Tweet_nonstop'] = df['Tweet_tokenized'].apply(remove_stopwords)

    #stem
    factory_stem = StemmerFactory()
    stemmer = factory_stem.create_stemmer()
    def stemming(text):
        text = [stemmer.stem(word) for word in text]
        return text
    df['Tweet_stemmed'] = df['Tweet_nonstop'].apply(stemming)

    df.to_csv(r"tweet-vaksin-covid.csv", index=False)

    def updateSqliteTable():
        try:
            sqliteConnection = sqlite3.connect(r'tweet-vaksin-covid.db')
            cursor = sqliteConnection.cursor()
            #print("Connected to SQLite")

            read_data = pd.read_csv (r"tweet-vaksin-covid.csv")
            
            sql_drop_query = """DROP TABLE IF EXISTS Tweets_VaksinCovid"""
            cursor.execute(sql_drop_query)
            sqliteConnection.commit()
            
            sql_create_table_query = '''CREATE TABLE IF NOT EXISTS Tweets_VaksinCovid (
                ID INT PRIMARY KEY,
                Created_at DATE,
                Tweets TEXT,
                Username TEXT,
                Tweets_punct TEXT,
                Tweet_tokenized TEXT,
                Tweet_nonstop TEXT,
                Tweet_stemmed TEXT);'''
            cursor.execute(sql_create_table_query)
            sqliteConnection.commit()

            read_data.to_sql('Tweets_VaksinCovid', sqliteConnection, if_exists='append', index = False) 

            sql_select = '''SELECT * FROM Tweets_VaksinCovid'''  
            cursor.execute(sql_select)
            sqliteConnection.commit()

            print("\nRecord Updated successfully\n")
            cursor.close()
        except sqlite3.Error as error:
            print("\nFailed to update sqlite table\n", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                #print("The SQLite connection is closed")
    updateSqliteTable()

def sentiment_analysis():
    pos_list= open(r"kata_positif.txt")
    pos_kata = pos_list.readlines()
    neg_list= open(r"kata_negatif.txt")
    neg_kata = neg_list.readlines()
    
    sentiment_data = pd.read_csv (r"tweet-vaksin-covid.csv")
    a = []
    items = sentiment_data['Tweet_stemmed']
    for kata in items:
        count_p = 0
        count_n = 0
        for kata_pos in pos_kata:
            if kata_pos.strip() in kata:
                count_p +=1
        for kata_neg in neg_kata:
            if kata_neg.strip() in kata:
                count_n +=1
        a.append(count_p - count_n)

    sentiment_data["value"] = a
    sentiment_data.to_csv(r"tweet-vaksin-covid-sentiment.csv", index=False)

    def updateSqliteTable():
        try:
            sqliteConnection = sqlite3.connect(r'tweet-vaksin-covid.db')
            cursor = sqliteConnection.cursor()

            read_data = pd.read_csv (r"tweet-vaksin-covid-sentiment.csv")
            read_data.drop(columns=['Tweets_punct', 'Tweet_tokenized', 'Tweet_nonstop'])
            read_data['sentiment_id'] = read_data.index + 1
            read_data = read_data[['sentiment_id', 'Tweets', 'ID', 'Username', 'Created_at', 'Tweet_stemmed', 'value']]
            
            sql_drop_query = """DROP TABLE IF EXISTS Sentiment_Tweets_VaksinCovid"""
            cursor.execute(sql_drop_query)
            sqliteConnection.commit()
            
            sql_create_table_query = '''CREATE TABLE IF NOT EXISTS Sentiment_Tweets_VaksinCovid (
                sentiment_id INT PRIMARY KEY,
                Tweets TEXT,
                ID INT,
                Username TEXT,
                Created_at DATE,
                Tweet_stemmed TEXT,
                value INT);'''
            cursor.execute(sql_create_table_query)
            sqliteConnection.commit()

            read_data.to_sql('Sentiment_Tweets_VaksinCovid', sqliteConnection, if_exists='append', index = False) 

            sql_select = '''SELECT * FROM Sentiment_Tweets_VaksinCovid'''  
            cursor.execute(sql_select)
            sqliteConnection.commit()
            print("\nRecord Updated successfully\n")
            cursor.close()
        except sqlite3.Error as error:
            print("\nFailed to update sqlite table\n", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
    updateSqliteTable()

def lihat_data():
    try:
        sqliteConnection = sqlite3.connect(r'tweet-vaksin-covid.db')
        df_sql = pd.read_sql_query("SELECT ID, Created_at, Tweets, Username FROM Tweets_VaksinCovid;", sqliteConnection)
        cursor = sqliteConnection.cursor()

        input_from_date = input("Tanggal awal (format : 2020-09-09) : ")
        input_to_date = input("Tanggal akhir (format : 2020-09-09) : ")
        df_sql_filter = df_sql[(df_sql['Created_at'] >= input_from_date) & (df_sql['Created_at'] <= input_to_date)]
        print(df_sql_filter)

        cursor.close()
    except sqlite3.Error as error:
        print("\nFailed to update sqlite table\n", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def visualisasi():
    try:
        sqliteConnection = sqlite3.connect(r'tweet-vaksin-covid.db')
        df_sql = pd.read_sql_query("SELECT * FROM Sentiment_Tweets_VaksinCovid;", sqliteConnection)
        cursor = sqliteConnection.cursor()

        input_from_date = input("Tanggal awal (format : 2020-09-09) : ")
        input_to_date = input("Tanggal akhir (format : 2020-09-09) : ")
        df_sql_filter = df_sql[(df_sql['Created_at'] >= input_from_date) & (df_sql['Created_at'] <= input_to_date)]
        
        print ("Mean Kata Positif - Negatif: "+str(np.mean(df_sql_filter["value"])))
        print ("Standar deviasi Kata Positif - Negatif: "+str(np.std(df_sql_filter["value"])))
        print ("Median Kata Positif - Negatif: "+str(np.median(df_sql_filter["value"])))

        labels, counts = np.unique(df_sql_filter["value"], return_counts=True)
        plt.bar(labels, counts, align='center')
        plt.gca().set_xticks(labels)
        plt.xlabel("Banyaknya Kata P-N")
        plt.ylabel("Jumlah")
        plt.title("Grafik Kata P-N pada Tweet Tentang Vaksin COVID")

        plt.show()

        plt.show()
        cursor.close()
    except sqlite3.Error as error:
        print("\nFailed to update sqlite table\n", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

while True:
    print("\nApa yang ingin ada lakukan?\n   1. Update Data\n   2. Update Nilai Sentiment\n   3. Lihat Data\n   4. Visualisasi\n   5. Keluar")
    try:
        g = input("Input anda :\n")
        g = int(g)
        if not 6 > g > 0:
            print('Nilai yang dimasukkan antara 1 sampai 5!')
            continue
    except ValueError:
        print('Masukkan Integer')
        continue
    if g == 1:
        update_data()
        continue
    if g == 2:
        sentiment_analysis()
        continue
    if g == 3:
        lihat_data()
        continue
    if g == 4:
        visualisasi()
        continue
    if g == 5:
        print("\nSelamat anda berhasil keluar\n")
        break