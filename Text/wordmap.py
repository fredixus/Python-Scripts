import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def displayWordMap(dataToDisplay) -> None:
    """
    Gets the list of strings.
    :param dataToDisplay: {list(str), pd.Series(object)} :: Server name with SQL:

    :return:
        None: Display graph.
    """

    # Join tekxtto one string:
    text = " ".join(str(row) for row in dataToDisplay)

    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_font_size=100, background_color="white", stopwords = STOPWORDS).generate(text)

    # Display the generated image:
    plt.figure(figsize=[12,8])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

