import json
from pathlib import Path
from typing import Union

import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.Data import DATA_DIR
from wordcloud import WordCloud


class chatstatistics:
    """
    Generates chat statistics from a Telegram chat json file!
    """

    def __init__(self, chat_json: Union[str, Path]):
        """
        :Param chat_json: path to Telegram export json file
        """
        
        # load chat data
        logger.info(f"loading chat data from {chat_json}")
        with open(chat_json) as f:
            self.chat_data = json.load(f)

        self.normalizer = Normalizer()
        
        # load stopwords
        logger.info(f"loading stopwords from {DATA_DIR / 'stopwords.txt'}")
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words)) 
        self.stop_words = list(map(self.normalizer.normalize, stop_words))

    def generate_word_cloud(self, output_dir: Union[str, Path]):
        """
        Generate a wordcloud from the chat data

        :Param output_dir: Path to output directory fro word cloud image!
        """
        logger.info("Loading text content...")

        text_content = ''
        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                text_content += f" {' '.join(tokens)}"

        # normalize, reshape for final word cloud
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)

        # Generate wordcloud
        logger.info("Generating word cloud...")
        wordcloud = WordCloud(font_path=str(DATA_DIR / 'BHoma.ttf'),
                    width=1200, height=1200,
                    background_color='white',
                    max_font_size=250
                    ).generate(text_content)

        logger.info(f"Saving word cloud to {output_dir}")
        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))

if __name__ == "__main__":
    chat_stats = chatstatistics(chat_json=DATA_DIR / 'result.json')
    chat_stats.generate_word_cloud(output_dir=str(DATA_DIR))
    print('you did it!')
