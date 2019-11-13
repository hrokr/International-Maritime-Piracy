
class Stopword_processor():
    """
    Reads in the downloaded .txt stopwords
    """

    def __init__(self, name):
        self.name = name

    def getData(self, path):
        df = pd.read_csv('../data/additional_stopwords.csv')

    def in_and_out(self, quotes, wo_quotes):
        with open(quotes, 'r') as f, open(wo_quotes, 'w') as fo:
            for line in f:
                fo.write(line.replace('"', '').replace("'", ""))

    def add_numbers_to_stops(self, wo_quotes):
        with open(wo_quotes, 'r') as f:
            s = [i for i in f]
            nums = set(s)
            return nums



if __name__ == "__main__":
    quotes = '../data/additional_stopwords.csv'
    wo_quotes = '../data/add_num_stops.txt'
    
    in_and_out(quotes, wo_quotes)
    add_numbers_to_stops(wo_quotes)