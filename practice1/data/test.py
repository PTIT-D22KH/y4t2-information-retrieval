from warnings import filterwarnings
from pyvi import ViTokenizer
# import spacy
# from spacy.lang.vi import Vietnamese
filterwarnings("ignore", category=Warning, message=".*dtype\\(\\): align should be passed.*")

def main():
    text = "Hà Nội là thủ đô của Việt Nam"
    result = ViTokenizer.tokenize(text)
    result = result.split(" ")
    print(result)

if __name__ == "__main__":
    main()