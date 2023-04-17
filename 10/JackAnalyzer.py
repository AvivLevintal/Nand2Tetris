
import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackAnalyzer:
    """
    Class for analyzing both files, and creating XML out of them.
    """
    tokenizer = None
    comp_engnie = None
    filename = None
    
    def __init__(self, filename):
        self.filename = filename
        self.tokenizer = JackTokenizer(filename)
        self.comp_engnie = CompilationEngine(filename.replace(".jack", "T.xml"))

    def start_process(self):       
        """
        Function for processing both XML files.

        @returns: None
        """
        token_list = self.tokenizer.generate_tokens()
        self.create_xml(token_list, self.filename, "token")
        post_parsing = self.comp_engnie.parse_tokens()
        self.create_xml(post_parsing, self.filename)

    def create_xml(self, final_list, filename, option = "parse"):
        """
        Function for creating XML files. Creates both tokenized, and final
        version of the XMLs

        @type final_list: list
        @param final_list: the final processed list ready to be written.

        @type filename: str
        @param filename: the filename to be written to/
        
        @type option: str
        @param option: which type of file is being parsed.

        @returns: None
        """
        if option == "token":
            output = filename.replace(".jack", "T.xml")
        else:
            output = filename.replace(".jack", ".xml")

        with open(output, mode="w") as f:
            for line in final_list:
                f.write(line + "\n")

def main():

    analyzer = None

    if os.path.isfile(sys.argv[1]):

        if sys.argv[1].endswith(".jack"):

            filename = sys.argv[1]
            analyzer = JackAnalyzer(filename)
            analyzer.start_process()
    else:

        directory = sys.argv[1]

        for filename in os.listdir(directory):
            if filename.endswith(".jack"):
                filename = (directory if directory.endswith("/") else directory + "/") + filename
                analyzer = JackAnalyzer(filename)
                analyzer.start_process()

if __name__ == "__main__":
    main()