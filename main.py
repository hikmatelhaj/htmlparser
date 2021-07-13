import tkinter
from tkinter import *
import doctest

"""------------------------------------------------DOCTESTS------------------------------------------------"""


def test_pretty(word):
    """
    >>> HTMLParser("hello world").prettify()
    'hello world\\n'
    >>> HTMLParser("<html>test</html>").prettify()
    '<html>test</html>\\n'
    >>> HTMLParser('<!DOCTYPE html> <html lang="en">').prettify()
    '<!DOCTYPE html> \\n<html lang="en">\\n'
    >>> HTMLParser('<html>Will words like html, body affect something?</html>').prettify()
    '<html>Will words like html, body affect something?</html>\\n'
    >>> HTMLParser("<body>test</body>").prettify()
    '<body>test</body>\\n'
    """
    return HTMLParser(word).prettify()


def test_get_text(word):
    """
    >>> HTMLParser("hello world").get_text()
    ''
    >>> HTMLParser("<h1>Hello world</h1>").get_text()
    'Hello world\\n'
    >>> HTMLParser("<h1>Hello world<<<>>>>></h1>").get_text()
    'Hello world<<<>>>>>\\n'
    >>> HTMLParser("<h2>Getting text from h2 element</h2>").get_text()
    'Getting text from h2 element\\n'
    >>> HTMLParser("<p>Getting text from p element</p>").get_text()
    'Getting text from p element\\n\\n'
    """
    return HTMLParser(word).get_text()


"""------------------------------------------------NO GUI------------------------------------------------"""

# output type is set on GUI, if you want to change it to console check out the last lines

html_raw = '''<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> </head> <body> <h1>Test Heading Level 1</h1> <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ratione similique ipsum quia doloremque tempora cum dolor ad? Sit ex facere, aspernatur, minus dolore corrupti non labore reprehenderit, dolor magni consectetur. </p> <h2>Test Heading Level 2</h2> <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aspernatur sed autem mollitia ab, recusandae commodi perspiciatis dignissimos voluptas veritatis quibusdam amet debitis ipsum rerum aliquid obcaecati distinctio nisi. Accusantium, voluptatibus.Laboriosam praesentium deserunt quo. Ratione tempore perspiciatis laboriosam quaerat officiis explicabo obcaecati nobis, amet ullam quidem animi asperiores consequatur at delectus sint veritatis omnis, vero nesciunt eos dolores sapiente quo?</p> </body> </html>'''


def no_gui():
    """
    :return: (void) printing the data 
    """
    html_pretty = HTMLParser(html_raw)
    print(html_pretty.prettify())
    print(html_pretty.get_text())


class RawText:

    """This class will contain raw text and will process it when the method prettify/get_text is called,
    but still return raw text. """
    def __init__(self, data):
        """
        :param data: compressed string splitting into an array
        :param generator: generator object with the elements of data prettified
        :param generator2: generator object
        :param htmltagspretty: array of all the elements that require a tab
        :param htmltagsclear: array of all the elements that where the program should capture data in the clear text
        :param htmltagsenter: array of all the elements that require an enter in the clear text
        """
        self.data = data.split("> ")  # assuming the user doesn't type something like >
        self.generator_pretty = None
        self.generator_clear = None
        self.htmltagspretty = ["html", "body", "head", "div", "section"]
        self.htmltagsclear = ["h1", "h2", "p", "title"]
        self.htmltagsenter = ["p", "title"]

    def init_html_tags_pretty(self):
        """
        :return: (list, list) editing the htmltagspretty tags to something like <html (first return) and </html (second return)
        """
        html_tags_start = []
        html_tags_end = []
        for el in self.htmltagspretty:
            html_tags_start.append("<" + el)
        for el in self.htmltagspretty:
            html_tags_end.append("</" + el)
        return html_tags_start, html_tags_end

    def init_html_tags_clear_and_enter(self, tags):
        """
        :return: (list) editing the htmltagspretty tags to something like <p> or <h1> depending which array
        """
        html_tags_clear = []
        for el in tags:
            html_tags_clear.append("<" + el + ">")
        return html_tags_clear

    def check_html_tags(self, html_tags_start, element):
        """
        :return: (bool) check if element has one of the array elements of html_tags_start
        """
        counter = 0
        element_array = html_tags_start[counter]
        element_found = False
        while counter < len(html_tags_start) and not element_found:  # LAATSTE ELEMENT
            element_array = html_tags_start[counter]
            if element.find(element_array) != -1:
                element_found = True
            counter += 1

        return element_found

    def get_text(self):
        """
        :return: (void) initialize generator2 only when user wants to (will be overridden
        """
        self.generator_clear = self.get_text_help()

    def prettify(self):
        """
        :return: (void) initialize generator2 only when user wants to
        """
        self.generator_pretty = self.prettify_help()

    def prettify_help(self):
        """
         :return: (generator) yielding elements of the generator, here is the actual code from the prettify
         """
        html_pretty_start, html_pretty_end = self.init_html_tags_pretty()
        tabs = ""
        for el in self.data:
            # if there is a closing tag, no need to put an extra, rfind because closing tags are at the end
            if el.rfind(">") == len(el) - 1 or el.find("<") == -1:  # if no opening, no need to close
                extra_str = False
            else:
                extra_str = True
            if self.check_html_tags(html_pretty_end, el):
                tabs = tabs.replace("\t", "", 1)  # only replace once

            if extra_str:  # adding "> " because that was gone by splitting in the constructor
                yield tabs + el + "> "
            else:
                yield tabs + el

            # tabs must be added after the tag is written, that's why this code is under the yield
            if self.check_html_tags(html_pretty_start, el):  # with these elements a tab is required
                tabs += "\t"

    def get_text_help(self):
        """
        :return: (generator) yielding elements of the generator2, here is the actual code from the get_text
        """
        html_clear_total = self.init_html_tags_clear_and_enter(self.htmltagsclear)
        html_enter_tags = self.init_html_tags_clear_and_enter(self.htmltagsenter)
        for el in self.data:
            if self.check_html_tags(html_clear_total, el):  # different types of text you want to capture (expandable)
                array_without_first = el.split(">")[1:]
                filtered = ">".join(array_without_first)
                # filtering out the first one, but the other words might not be in 1 element of the array
                # 1 string of the other words #need to join again because there may be < or > in the text itself
                second_word_joined = filtered
                array_of_words = second_word_joined.split("<")[:-1]  # deleting last element
                content = "<".join(array_of_words)  # its now turned into a string
                if self.check_html_tags(html_enter_tags, el):
                    content += "\n"  # after p tag put an enter
                yield content

    """ GET_TEXT SHOWN IN STEPS:
    1. <h1>Test Heading <Level> 1</h1>
    2. Test Heading <Level> 1</h1>
    3. Test Heading <Level> 1 
    """

    def getGenPretty(self):
        """
        :return: (generator) a simple getter
        """
        return self.generator_pretty

    def getGenClear(self):
        """
        :return: (generator) a simple getter
        """
        return self.generator_clear


class HTMLParser(RawText):

    """This class will contain call the rawtext constructor and there the data will be processed with
    methods like prettify/get_text"""

    def __init__(self, data):
        """ calling constructor of RawText and process the data there"""
        RawText.__init__(self, data)

    def prettify(self):
        """
        OVERRIDE! There will be prettified text printed here
        :return: (string) appending the generator elements to a string for the GUI output
        [print(n) for n in super().getGenPretty()] for printing
        """
        super().prettify()  # initialize generator_pretty in RawText
        output = ""
        for n in super().getGenPretty():
            output += n
            output += "\n"
        return output

    def get_text(self):
        """
        OVERRIDE! There will be cleared text printed here
        :return: (string) appending the generator elements to a string for the GUI output
        [print(n) for n in super().getGenClear()] for printing
        """
        super().get_text()  # initialize generator_pretty in RawText
        output = ""
        for n in super().getGenClear():
            output += n
            output += "\n"
        return output


"""------------------------------------------------GUI START------------------------------------------------"""

window = Tk()
window.title("HTML Parser")

input_details = Text(window, height="30", width="80")
output_details = Text(window, height="30", width="80")
output_details.insert(END, "Here will be the output...")


def pretty_button_onclick():
    """
    :return: (void) when button is clicked, it should make an object of the HTMLParser and replace it on the GUI with pretty text
    """
    html_pretty = HTMLParser(input_details.get("1.0", "end-1c"))
    data = html_pretty.prettify()
    output_details.delete("1.0", "end-1c")  # clear the output before inserting new text
    output_details.insert(END, data)


def clear_button_onclick():
    """
    :return: (void) when button is clicked, it should make an object of the HTMLParser and replace it on the GUI with clear text
    """
    html_clear = HTMLParser(input_details.get("1.0", "end-1c"))
    data = html_clear.get_text()
    output_details.delete("1.0", "end-1c")  # clear the output before inserting new text
    output_details.insert(END, data)


pretty_button = Button(window, text="Make pretty", command=pretty_button_onclick)
clear_button = Button(window, text="Text form", command=clear_button_onclick)
input_title = tkinter.Label(text="Enter your details in the first textbox")
input_title2 = tkinter.Label(text="Your output will appear under this text")
input_title.grid(row=1, column=0)
input_title2.grid(row=1, column=1)
pretty_button.grid(row=8, column=0)
clear_button.grid(row=8, column=1)
input_details.grid(row=2, column=0)
output_details.grid(row=2, column=1)

""" ------------------------------------------------GUI DONE------------------------------------------------"""
if __name__ == "__main__":
    window.mainloop()  # this will activate the GUI. To use it without GUI, set this code in comment
    #no_gui()  # put this line out of comment in order to activate the console
