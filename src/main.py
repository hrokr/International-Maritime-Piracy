

if __name__ == "__main__":
    
    process_csv = Processor()

    mod_stopwords = Stopword_processor()

    quotes = '../data/additional_stopwords.csv'
    wo_quotes = '../data/add_num_stops.txt'
    
    in_and_out(quotes, wo_quotes)
    add_numbers_to_stops(wo_quotes)