# bin/post_compile
#!/usr/bin/env bash

python -m nltk.downloader averaged_perceptron_tagger
python -m nltk.downloader maxent_ne_chunker
python -m nltk.downloader maxent_treebank_pos_tagger
python -m nltk.downloader punkt
python -m nltk.downloader words

echo "-----> Running install_nltk_data"
chmod +x bin/install_nltk_data
bin/install_nltk_data


echo "-----> Post-compile done"