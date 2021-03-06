import csv
import pandas
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


def clean_text(text):
    text = BeautifulSoup(text, "lxml").text  # HTML decoding
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # delete stopwords from text
    return text


TRAIN_CSV_PATH = "./files/train_short.csv"
TEST_CSV_PATH = "./files/test.csv"

df = pandas.read_csv(TRAIN_CSV_PATH)

# print("Head")
# print(df.head())
# print("Describe")
# print(df.describe())

# get categories
categories = df.category.unique()

# split by Label quality
df_ok = df[df['label_quality'] == 'reliable']
df_doubt = df[df['label_quality'] == 'unreliable']

print(categories)
print("Categories: " + str(categories.size))
print("Total data: " + str(df.size))
print("Data with Label quality verified: " + str(df_ok.size))
print("Data with Label quality not verified: " + str(df_doubt.size))

# clean text
df['title'] = df['title'].apply(clean_text)

