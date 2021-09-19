import pandas as pd
from wordcloud import WordCloud ,STOPWORDS

#Reading the .csv files
df = pd.read_csv('Final_Etsy_Screapped_Reviews.csv')

#Starting of the wordcloud
str1 = ''
#Iteration through the .csv file
for i in df.reviews[:1000]:
    str1 = str1+i
    str1 = str1.lower()
    stopwords = set(STOPWORDS)
    cloud = WordCloud(width = 800, height = 400,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(str1)
    cloud.to_file("wordCloud.png")
