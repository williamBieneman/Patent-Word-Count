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
        self.phrase_counts = self.count_phrases()

    def __repr__(self):
        return "WordCount Object"

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
        sorted_word_counts = {x:y for x, y in sorted(self.word_counts.items(),\
                                reverse = True, key = lambda item: item[1])}
        self.word_counts = sorted_word_counts
        # This line made more sense when self.word_counts was a list of tuples,
        # but now it is just finding the first key of self.word_counts
        # (skipping the total), and finding the value associated with it.
        self.most_counted_word = self.word_counts[
                                            list(self.word_counts.keys())[1]
                                            ]
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
            counts = self.word_counts
        max_length = len(max(counts, key = lambda word: len(word)))
        # When I had this in the f-string below, as {'"' + word + '"'}..., it
        # didn't parse correctly so I changed it to use a variable
        quotation_mark = "\""
        for word in counts:
            if word == "Total words":
                print(f"{word:{max_length}}: {counts[word]:<6,}")
                continue
            if counts[word] > int(self.min_return):
                print(f"{quotation_mark + word + quotation_mark:{max_length}}",
                      f"appears {counts[word]:^6,} times.")

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
                # Sometimes, a phrase of just " " passes through, so let's skip
                # that
                if phrase_string.isspace():
                    pass
                else:
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

class WordContext():
    def __init__(self, term, WordCountObj, return_num=10):
        """Finds the context of the given term in the text from the
        WordCount object provided.
        return_num defines the default number of instances to be returned."""
        # Checks if WordCountObj is a WordCount Object.
        if repr(WordCountObj) != "WordCount Object":
            raise TypeError("WordCountObj must be a WordCount object.")
        self.punctuation = ["!", ".", "?"]
        self.numerals = ['0','1','2','3','4','5','6','7','8','9']
        self.raw_text = WordCountObj.raw_text
        self.fixed_text = WordCountObj.raw_text
        self.term = term
        self.return_num = return_num
        self.context = self.get_context(term = self.term,
                                        text = self.raw_text,
                                        return_num = return_num)
        self.lines_with = self.get_lines_with(term = self.term,
                                              text = self.raw_text,
                                              return_num = return_num)
        self.sentences = self.get_sentences(term = self.term,
                                            text = self.raw_text,
                                            return_num = return_num)

    def __repr__(self):
        return "WordContext Object"

    def get_lines_with(self, term=None, text=None, return_num=10):
        """Gets the lines containing passed term in the text, returning the
        first ones up to return.
        If None is passed for term or text, it wil be replaced by self.term or
        self.raw_text respectively."""
        if term == None:
            term = self.term
        if text == None:
            text = self.raw_text
        # Splits text into lines, and then choses the first return_num with
        # the term in them.
        split_text = text.split('\n')
        lines_with_term = []
        n = 0
        for line in split_text:
            if n >= return_num:
                break
            elif term in line:
                lines_with_term.append(line)
                n += 1
            else:
                continue
        return lines_with_term

    def get_context(self, term=None, text=None, leading=10,
                    following=25, return_num=10):
        """Gets the context of the term in the text, meaning the {leading}
        words before it and the {following} words after, returning the first
        instances up to {return}
        If term or text is entered as None, it will be replaced by self.term
        or self.raw_text respectively."""
        if term == None:
            term = self.term
        if text == None:
            text = self.raw_text
        split_text = text.split(term)
        contexts_of_term = []
        n = 0
        # This loop takes the items in the text, and then for the first
        # return_num adds them to contexts_of_term with the term added as well
        # as the following item.
        # Adding the term is nessecary, as .spit(term) removes the term.
        for item in split_text:
            if n >= return_num:
                break
            else:
                context = ""
                split_text[0] = split_text[0].split(" ")
                split_text[1] = split_text[1].split(" ")
                # Adds the last {leading} words of the first item,
                for word in split_text[0][-leading:]:
                    context += word + " "
                # the term,
                context += term
                # and the first {following} words of the next item.
                for word in split_text[1][:following]:
                    context += word + " "
                # Then, removes the first two items of split_text, to avoid
                # repeating the same ones.
                del split_text[0:2]
                contexts_of_term.append(context)
                n += 1
                # Removes the following whitespace added when adding the
                # words following the term.
                context = context[:-1]
        return contexts_of_term

    def get_sentences(self, term=None, text=None,
                      leading=1, following=2, return_num=10):
        """Gets the first {return_num} sentences with the term in them.
        If term or text is entered as None, it will be replaced by self.term
        or self.raw_text respectively."""
        if term == None:
            term = self.term
        if text == None:
            text = self.raw_text
        sentences = []
        # Decides where each sentence starts, and where each sentence ends,
        # using the punctuation: "!", ".", "?" as terminating punctuation.
        for char in text:
            if char in self.punctuation:
                sentence = text[:text.index(char)+1]
                sentences.append(sentence)
                text = text[text.index(char)+1:]
        sentences_with_term = []
        n = 0
        # Finds every sentence with the term.
        for sentence in sentences:
            if n >= return_num:
                break
            else:
                if term in sentence:
                    sentences_with_term.append(sentence)
                    n += 1
        # If requested to find sentences following or leading to the sentence
        # with the term:
        if (leading != 0) or (following != 0):
            # Creates sentences_surrounding_term, so that sentences_with_term
            # doesn't get modified while recording changes.
            sentences_surrounding_term = []
            # Takes each sentence with the term in it...
            for sentence in sentences_with_term:
                # Finds its index in sentences, and then adjusts it to have
                # both the leading...
                leading_index = sentences.index(sentence) - leading
                if leading_index < 0:
                    leading_index = 0
                # and the following.
                following_index = sentences.index(sentence) + following + 1
                # Then gets those sentences.
                surrounding = sentences[leading_index:following_index]
                context = ""
                # And adds them to "context"
                for item in surrounding:
                    context += item
                # Then it appends this to sentences_surrounding_term.
                sentences_surrounding_term.append(context)
            # Finally, re-copies sentences_surrounding_term to
            # sentences_with_term
            sentences_with_term = sentences_surrounding_term
        return sentences_with_term

    def pretty_print(self, list_of_contexts):
        """Pretty prints any list of contexts, ie lines with term, contexts,
        or sentences with term."""
        n = 0
        for context in list_of_contexts:
            n += 1
            print(f"{n:>3}. {context}\n")
