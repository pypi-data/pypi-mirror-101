from awsee.style import Style
from awsee.emoticons import Emoticons


class Messages:

    def __init__(self):
        pass

    @staticmethod
    def formatMessage(title,msg=None):
        emoticon = Emoticons.pointRight()
        output = ""
        #output  = Style.ICYAN + "=".ljust(len(title)+5,"=")
        output += f"\n{Style.IBLUE} {emoticon} {Style.IGREEN}{title}{Style.RESET}\n"
        #output += Style.ICYAN + "=".ljust(len(title)+5,"=")
        if msg:
           output += f"{Style.GREEN}{msg}"
        return output
    def showMessage(title,msg=None):
        print(Messages.formatMessage(title,msg))
    
    @staticmethod
    def formatWarning(title,msg=None):
        emoticon = Emoticons.ops()
        output = ""
        #output  = Style.ICYAN + "=".ljust(len(title)+5,"=")
        output = f"\n{Style.IBLUE} {emoticon} {Style.IGREEN}{title}{Style.RESET}\n"
        #output += Style.ICYAN + "=".ljust(len(title)+5,"=")
        if msg:
           output += f"{Style.GREEN}{msg}"
        return output
    def showWarning(title,msg=None):
        print(Messages.formatWarning(title,msg))

    def formatStartExecution(title,msg=None):
        emoticon = Emoticons.pointRight()
        output = ""
        output += f"{Style.IBLUE} {emoticon} {Style.IGREEN}{title}{Style.RESET}"
        if msg:
           output += f"{Style.GREEN}{msg}"
        return output
    def showStartExecution(title,msg=None):
        print(Messages.formatStartExecution(title,msg), end='\r')
    
    @staticmethod
    def formatError(title,msg=None):
        emoticon = Emoticons.ops()
        output = ""
        output = f"\n{Style.IRED} {emoticon} {Style.IMAGENTA}{title}{Style.RESET}\n"
        if msg:
           output += f"    {Style.GREEN}{msg}"
        return output
    def showError(title,msg=None):
        print(Messages.formatError(title,msg))

