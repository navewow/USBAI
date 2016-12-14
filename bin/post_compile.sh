# bin/post_compile
#!/usr/bin/env bash

echo "-----> Running install_nltk_data"
chmod +x bin/install_nltk_data
bin/install_nltk_data


echo "-----> Post-compile done"