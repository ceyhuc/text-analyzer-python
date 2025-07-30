import locale
from sys import argv

locale.setlocale(locale.LC_ALL, "en_US")

def sentence_counter(text):
    # Count how many sentences are in the text, treating ellipses as sentence endings
    sentence_num = text.count("...")
    text = text.replace("...","")
    for i in (".", "!", "?"):
        sentence_num += text.count(i)
    return sentence_num

def text_cleaner(text):
    # Convert text to lowercase and remove specified punctuation
    text = text.lower()
    punctuations = (".", "!", "(", ")", "?", ";", "...", ",", ":","[","]","{","}","/","+","*","%","^","<",">","£")
    for punctuation in punctuations:
        text = text.replace(punctuation,"")
    text = text.replace("\n", " ")
    # Remove ending apostrophes from words
    cleaned_text = []
    for word in text.split():
        if word.endswith("'"):
            word = word[:-1]
        cleaned_text.append(word)
    cleaned_text = " ".join(cleaned_text)
    return cleaned_text

def word_counter(text):
    # Count the number of words in the cleaned text
    cleaned_text = text_cleaner(text)
    return len(cleaned_text.split())

def character_counter(text):
    # Count the number of all characters in the text, including spaces and punctuation
    return len(text)

def character_words(text):
    # Count the number of characters in the text excluding spaces and punctuation
    text = text_cleaner(text)
    text = text.replace(" ", "")
    return len(text)

def freq_aow(text):
    # Calculate the frequency of each word in the cleaned text
    words = text_cleaner(text).split()
    total_words = len(words)
    word_list = {}
    # Count occurrences of each word
    for word in words:
        if word not in word_list:
            word_list.update({word: 1})
        else:
            word_list[word] += 1
    # Calculate the frequency as a percentage of total words
    word_list = {word: count / total_words for word, count in word_list.items()}
    # Sort words by frequency (descending), then alphabetically
    word_list = dict(sorted(word_list.items(), key=lambda item: (-item[1], item[0])))
    return word_list

def longest_words_find(all_text):
    # Find the longest words in the text, sorted by length and frequency
    word_list = freq_aow(all_text)
    sorted_word_list = sorted(word_list.items(), key=lambda item: (-len(item[0]), (-item[1]), item[0]))
    max_len = len(sorted_word_list[0][0])
    longest_words = []
    # Collect words with the maximum length into a list
    for key, value in sorted_word_list:
        if len(key) == max_len:
            longest_words.append((key, value))
        else:
            break
    # Convert our list to dictionary that we need
    longest_words = dict(longest_words)
    return longest_words
# Same attitude with above function just the opposite
def shortest_words_find(all_text):
    # Find the shortest words in the text, sorted by length and frequency
    word_list = freq_aow(all_text)
    sorted_word_list = sorted(word_list.items(), key=lambda item: (len(item[0]),(-item[1]), item[0]))
    min_len = len(sorted_word_list[0][0])
    shortest_words = []
    # Collect words with the minimum length into a list
    for key, value in sorted_word_list:
        if len(key) == min_len:
            shortest_words.append((key, value))
        else:
            break
    # Convert our list to dictionary that we need
    shortest_words = dict(shortest_words)
    return shortest_words

def stat_writer(text, output_file):
    # Call functions to calculate we need statistics
    num_of_words = word_counter(text)
    num_of_sentences = sentence_counter(text)
    # Calculate the average number of words per sentence
    # Be sure number of sentences not equals zero to avoid 0/0 error
    average_word_sen = num_of_words / num_of_sentences if num_of_sentences > 0 else 0
    word_list = freq_aow(text)
    shortest_words = shortest_words_find(text)
    longest_words = longest_words_find(text)
    # Write statistics to the output file
    output_file.write(f"Statistics about {argv[1]:7}:")
    output_file.write(f"\n#Words                  : {num_of_words}")
    output_file.write(f"\n#Sentences              : {num_of_sentences}")
    output_file.write(f"\n#Words/#Sentences       : {average_word_sen:.2f}")
    output_file.write(f"\n#Characters             : {character_counter(text)}")
    output_file.write(f"\n#Characters (Just Words): {character_words(text)}")
    # Write the shortest word and its frequency
    if len(shortest_words) == 1:
        output_file.write(f"\nThe Shortest Word       : ")
        for word, freq in shortest_words.items():
            output_file.write(f"{word:24} ({freq:.4f})")
    # there are more than one shortest word, write line by line
    else:
        output_file.write(f"\nThe Shortest Words      :")
        for word, freq in shortest_words.items():
            output_file.write(f"\n{word:24} ({freq:.4f})")
    # Write the longest word and its frequency
    if len(longest_words) == 1:
        output_file.write(f"\nThe Longest Word        : ")
        for word, freq in longest_words.items():
            output_file.write(f"{word:24} ({freq:.4f})")
    # There are more than one longest word, write line by line
    else:
        output_file.write(f"\nThe Longest Words       :")
        for word, freq in longest_words.items():
            output_file.write(f"\n{word:24} ({freq:.4f})")
    # Write the frequency of all words in the text
    output_file.write("\nWords and Frequencies   :")
    word_items = list(word_list.items())
    for word, freq in word_items:
        output_file.write(f"\n{word:24}: {freq:.4f}")
    output_file.close()


# Main function to process input text and write analysis to output file
def main():
    # Open input file that contains text we be analyzed
    input_file = open(argv[1], "r")
    # Read all content of the input file into a string variable we use for our functions
    all_text = input_file.read()
    input_file.close()
    # Open output file, then write statistics to the output file with stat_writer function
    output_file = open(argv[2], "w")
    stat_writer(all_text, output_file)

if __name__ == "__main__":
    main()