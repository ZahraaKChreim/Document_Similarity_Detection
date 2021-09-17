# Document_Similarity_Detection

## Project Description
Document_Similarity_Detection is a project that mainly aims to reduce the number of web pages returned after a user search query, by detecting the redundant documents and the
duplications. To do that, we build an appropriate new model of document representation and similarity detection, which takes into account the different content types of the web 
document, such as titles, subtitles, links, texts, etc. The mechanism is based on multiple representations of texts, especially the graphical representation.

The model is called **REDUCE++**: **RE**sult **DU**plication detection in ****}earch **E**ngines. It includes content-type-based similarity computation measures, in addition to a 
new graph-based clustering algorithm. First, it divides the web page into different types of content. Then, it finds for each type a suitable similarity measure. Next, it adds the 
different calculated similarity scores to get the final similarity score between the two documents, using a weighted formula. Finally, we suggest a new graph-based algorithm to 
cluster search results according to their similarity.

REDUCE++ is a validated system, able to correctly detect the similarity between two web pages, as well as to reduce the number of web pages returned after a user search query.
This way, we improved the search performance, especially by reducing the problem of duplication.

## Installation
1. Clone the repo
git clone https://github.com/ZahraaKChreim/Document_Similarity_Detection
2. Create a new python environement
3. Install required libraries
pip install -r requirements.txt
4. Install additional requirements
- conda install -c conda-forge selenium
- python -m spacy download en
- python -m spacy download fr_core_news_md
5. Install nltk requirements
- import nltk
- nltk.download('punkt')
- nltk.download('stopwords')
- nltk.download('averaged_perceptron_tagger')
- nltk.download('wordnet')
