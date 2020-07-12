"""Module to count words and phrases, hopefully."""

class WordCount():
    def __init__(self, text, min_return = 10):
        """Use this class to find word and phrase counts for your text.
        min_return sets the minimum number of occurences to be returned."""
        self.raw_text = text
        if min_return < 0:
            raise ValueError("min_return must be greater than or equal to 0.")
        self.min_return = min_return
        self.punctuation = [
                            "~", "!", "@", "#", "$", "%", "^", "&", "*", "(",\
                            ")", "_", "+", "`", "-", "=", "{", "}", "|", "[",\
                            "]", "\\", "'", ",", ".", "/", ":", "\"", "<",\
                            ">", "?", "`", "¡", "™", "£", "¢", "∞", "§", "¶",\
                            "•", "ª", "º", "–", "≠", "`", "⁄", "€", "‹", "›",\
                            "‡", "°", "·", "‚", "—", "±", "”", "’", "»", "“",\
                            "‘", "«", "…", "≤", "≥", "÷", "¯", "˘", "¿", "\n",\
                            ]
        self.numerals = ['0','1','2','3','4','5','6','7','8','9']
        self.fixed_text = text
        for char in self.punctuation + self.numerals:
            self.fixed_text = self.fixed_text.replace(char, ' ')
        self.fixed_text = self.fixed_text.replace('  ',' ')
        self.fixed_text = self.fixed_text.lower()
        self.word_counts = self.count_words()

    def count_words(self):
        """Counts the number of words in the text, and counts the number of
        instances of each word."""
        # Makes a list of every word.
        self.word_list = self.fixed_text.split(' ')
        for word in self.word_list:
            if word == '':
                self.word_list.remove(word)
        self.length = len(self.word_list)
        n = 0
        self.word_counts = {}
        # Counts each word in the list
        counted_words = []
        for n in range(0,self.length):
            word = self.word_list[n]
            if word not in counted_words:
                count = self.word_list.count(word)
                self.word_counts.update({word : count})
                counted_words.append(word)
        self.word_counts.update({'Total words':n})
        # This sorting was cleaner when self.word_counts was a list of tuples,
        # but I think having it be a dictionary is worth the complications.
        sorted_word_counts = {}
        sorted_word_counts = {x:y for x, y  in sorted(self.word_counts.items(),\
                                reverse = True, key = lambda item: item[1])}
        self.word_counts = sorted_word_counts
        # This line made more sense when self.word_counts was a list of tuples,
        # but now it is just finding the first key of self.word_counts (skipping the
        # total), and finding the value associated with it.
        self.most_counted_word = self.word_counts[list(self.word_counts.keys())[1]]
        # Similarly, this just finds the highest number
        self.most_counted_number = list(self.word_counts.keys())[1]
        uncounted = []
        if self.min_return == 0:
            return self.word_counts
        elif self.min_return > 0:
            for word in self.word_counts:
                if self.word_counts[word] >= self.min_return:
                    pass
                elif self.word_counts[word] < self.min_return:
                    uncounted.append(word)
        for word in uncounted:
            self.word_counts.pop(word)
        return self.word_counts

    def pretty_print(self, counts=None):
        """Pretty prints the word counts. (Default counts is self.counts.)"""
        if counts == None:
            counts = self.counts
        max_length = len(max(counts, key = lambda word: len(word)))
        for word in counts:
            if word == "Total words":
                print(f"{word:{max_length}}: {counts[word]:<6,}")
                continue
            if counts[word] > int(self.min_return):
                print(f"{'"' + word + '"':{max_length}} appears",\
                      f"{counts[word]:^6,} times.")

    def count_phrases(self, phrase_length=2):
        # Creates a list of phrases phrase_lenth words long.
        self.phrase_list = []
        for word in range(self.length):
            if word + phrase_length > self.length:
                continue
            else:
                phrase = self.word_list[word:(word + phrase_length)]
                self.phrase_list.append(phrase)
            if word - phrase_length < self.length:
                continue
            else:
                phrase = self.word_list[(word - phrase_length):word]
                self.phrase_list.append(phrase)
        # Counts each phrase in the list
        counted_phrases = []
        self.phrase_counts = dict()
        string_list_punctuation = ['[',']',"'",', '] # This list is of the
            # punctuation that is added when you make a list into a string.
        for n in range(0,len(self.phrase_list)):
            phrase = self.phrase_list[n]
            if phrase not in counted_phrases:
                count = self.phrase_list.count(phrase)
                phrase_string = str(phrase)
                for char in string_list_punctuation:
                    if char == ", ":
                        phrase_string = phrase_string.replace(char, ' ')
                    else:
                        phrase_string = phrase_string.replace(char, '')
                self.phrase_counts.update({phrase_string : count})
                counted_phrases.append(phrase)
        # This sorting was cleaner when self.phrase_counts was a list of
        # tuples, but I think having it be a dictionary is worth the
        # complications.
        sorted_phrase_counts = {x:y for x, y in\
                                sorted(self.phrase_counts.items(),\
                                reverse = True, key = lambda item: item[1])}
        self.phrase_counts = sorted_phrase_counts
        uncounted = []
        if self.min_return == 0:
            return self.phrase_counts
        elif self.min_return > 0:
            for phrase in self.phrase_counts:
                if self.phrase_counts[phrase] >= self.min_return:
                    pass
                elif self.phrase_counts[phrase] < self.min_return:
                    uncounted.append(phrase)
        for phrase in uncounted:
            self.phrase_counts.pop(phrase)
        return self.phrase_counts
