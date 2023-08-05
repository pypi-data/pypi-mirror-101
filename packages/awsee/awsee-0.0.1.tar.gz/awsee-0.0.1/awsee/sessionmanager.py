import os
import logging
import sys
import re, uuid
import atexit 
from os.path import expanduser
import signal, subprocess

from awsee.logmanager import LogManager
from awsee.preferences import Preferences
from awsee.functions import Functions
from arnparse import arnparse
from awsee.awsservices import AwsServices
from awsee.messages import Messages
from awsee.style import Style
from awsee.emoticons import Emoticons
from awsee.utils import Utils
from tinydb import Query, where
from shutil import which
from awsee.repository import Repository, CredentialsRepository, ConfigRepository, RoleRepository, MfaRepository

class SessionManager:

    SCRIPTS_PREFIX_NAME_FILE = "set-awssession-"

    def __init__(self):
        self.credentialsRepository = CredentialsRepository()
        self.roleRepository        = RoleRepository()
        self.mfaRepository         = MfaRepository()
        self.preferences           = Preferences()

    # Start a Session and immediatly Assume a Role 
    def startCredentialsOwnerSessionWithMFA(self, mfaToken, profile, mfa):
        # TODO:
        pass 

    # Assume a Role
    def assumeRole(self, role, profile=None, mfaToken=None):
        aws = AwsServices()

        stsToken = aws.assumeRole(role['role-arn'], profile, mfaToken)
        if not stsToken:
            return None, None, None
        
        return self.createAWSSessionOnTerminalUser(stsToken["Credentials"], role['profile'], role['role-name'])
    
    # Using Credentials Owner with MFA
    def startAWSSessionWithMFA(self, profile, mfa, mfaToken):
        aws = AwsServices()

        stsToken = aws.getSessionToken(mfaSerial=mfa['mfa-device'],mfaToken=mfaToken, profile=profile['profile'])
        if not stsToken:
            return None, None, None

        return self.createAWSSessionOnTerminalUser(stsToken["Credentials"], profile['profile'], None)

    def createAWSSessionOnTerminalUser(self, stsToken, profile, role):
        accessKey      = stsToken["AccessKeyId"]
        secretKey      = stsToken["SecretAccessKey"]
        sessionToken   = stsToken["SessionToken"]
        expiration     = stsToken["Expiration"]
        output         = None
        scriptFileWin  = None
        scriptFileBash = None

        if not role:
           role = ""
        else:
           role = "_" + role.replace(" ","_").lower()

        if Utils.isWindows():
            nameProfile     = profile.replace(" ","_")
            scriptFileWin   = f"{self.SCRIPTS_PREFIX_NAME_FILE}{nameProfile}{role}.bat"
            scriptFileBash  = f"{self.SCRIPTS_PREFIX_NAME_FILE}{nameProfile}{role}.sh"

            terminalCommand = self.preferences.windows.terminalCommand
            # Check if there's a Terminal Commmand Set
            if not terminalCommand or terminalCommand.lstrip().rstrip() == "":
                # Check CMDER is installed (then use it)
                if which("cmder") and os.environ['CMDER_ROOT'] != "":
                    outputWin, environmentsWin = self.createEnvironment(False, scriptFileWin, accessKey, secretKey, sessionToken, expiration)
                    output = outputWin
                    os.system("start %CMDER_ROOT%\\vendor\\conemu-maximus5\\ConEmu.exe /icon \"%CMDER_ROOT%\\cmder.exe\" /title AWSEE /loadcfgfile \"%CMDER_ROOT%\\config\\ConEmu.xml\" /cmd cmd /k " + environmentsWin)
                    #os.system("start %CMDER_ROOT%\\vendor\\conemu-maximus5\\ConEmu.exe /icon \"%CMDER_ROOT%\\cmder.exe\" /title AWSEE /cmd cmd /k " + environmentsWin)
                else:
                    # Last option (windows default cmd)
                    if which("cmd"):
                        outputWin, environmentsWin = self.createEnvironment(False, scriptFileWin, accessKey, secretKey, sessionToken, expiration)
                        output = outputWin
                        os.system("start cmd.exe /c cmd /k" + environmentsWin)
                    else:
                        msg = f"""\n{Style.GREEN}    Please set a {Style.IBLUE}terminal-command{Style.GREEN} at your {Style.IBLUE}~/.awsee/awsee.ini{Style.GREEN}, WINDOWS section in order \n    to open a Terminal ready to use with your AWS Session Token configured.
                        \n    Example: \n    {Style.IBLUE}[WINDOWS]\n    terminal-command = {Style.IGREEN}d:\Program Files\Git\git-bash.exe{Style.RESET}
                        """
                        Messages.showError("No Terminal Found (CMDER or CMD)",msg)
                        return None, None
            else:
                if "git-bash.exe" in terminalCommand or "sh.exe" in terminalCommand:
                    outputBash, environmentsBash = self.createEnvironment(True, scriptFileBash, accessKey, secretKey, sessionToken, expiration)
                    output = outputBash

                    # Regarding the place where Python is running (not the Target Console to Open, configured at awsee.ini)...  
                    # Check if the Call to open a Shell Script Terminal were made inside a GitBash, if not... change to Windows Style (the Output Python window)
                    if not Utils.isRunningOnGitBash():
                        outputWin, _ = self.createEnvironment(False, scriptFileWin, accessKey, secretKey, sessionToken, expiration)
                        output = outputWin

                if "git-bash.exe" in terminalCommand:
                    os.system(f"start {terminalCommand} --needs-console --no-hide --command=usr\\bin\\bash.exe --login -i -c \"sh -c 'source ./{environmentsBash}; exec sh'\"")
                elif "sh.exe" in terminalCommand:
                    os.system(f"start {terminalCommand} --login -i -l -c \"sh -c 'source ./{environmentsBash}; exec sh'\"")
                else:
                    msg = f"""\n{Style.GREEN}    Please check the {Style.IBLUE}terminal-command{Style.GREEN} set at your {Style.IBLUE}~/.awsee/awsee.ini{Style.GREEN}, WINDOWS section in order \n    to open a Terminal ready to use with your AWS Session Token configured.
                    \n    Example: \n    {Style.IBLUE}[WINDOWS]\n    terminal-command = {Style.IGREEN}d:\Program Files\Git\sh.exe{Style.RESET}
                    """
                    Messages.showError(f"Terminal Command set \"{terminalCommand}\" not supported (Use git-bash.exe, sh.exe or let it blank, for system default",msg)
                    return None, None
        else:
            # LINUX
            # TODO:
              print("export AWS_ACCESS_KEY")
        
        

        return output, scriptFileWin, scriptFileBash

    # Script to Help clean environment variables, etc. 
    def createCleanEnvironmentScript(self, scriptFile):
        print()
        if ".bat" in scriptFile:
            cleanFileName = "clean.bat"
            content = f"""@ECHO OFF
set AWS_ACCESS_KEY_ID=
set AWS_SECRET_ACCESS_KEY=
set AWS_SESSION_TOKEN=
set AWS_EXPIRATION=
DEL {scriptFile}
            """
        else:
            cleanFileName = "clean.sh"
            content = f"""unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
unset AWS_EXPIRATION
rm {scriptFile}
            """
        with open(f"{cleanFileName}",'w') as fout:
            fout.write(content)

    # Create Contents, Script File for Environments Variables and Clipboard (Win and Bash)
    def createEnvironment(self, isBashEnv, scriptFile, accessKey, secretKey, sessionToken, expiration):
        output           = self.createOutputStartSession(isBashEnv, scriptFile, accessKey, secretKey, sessionToken, expiration)
        initFileContent  = self.createContentScriptFileStartSession(isBashEnv, accessKey, secretKey, sessionToken, expiration)
        with open(f"{scriptFile}",'w') as fout:
            fout.write(initFileContent)
        environments = f"\"{scriptFile}\""
        self.addEnvironmentVariablesConfigurationToClipboard(isBashEnv,accessKey, secretKey, sessionToken, expiration)

        self.createCleanEnvironmentScript(scriptFile)

        return output, environments

    def createOutputStartSession(self, forBash, scriptFile, accessKey, secretKey, sessionToken, expiration):
        commandEnvSet = "set"
        executeScript = f"{scriptFile}"
        if forBash:
            commandEnvSet = "export"
            executeScript = f"source ./{scriptFile}"

        output  = "\n"
        output += f" {Style.GREEN}======================="
        output += f"\n {Style.IMAGENTA}  >>> AWS SESSION <<<\n"
        output += f" {Style.GREEN}======================="
        output += f"""\n {Style.GREEN}set AWS_ACCESS_KEY_ID{Style.WHITE}={Style.IBLUE}{accessKey}\r
 {Style.GREEN}{commandEnvSet} AWS_SECRET_ACCESS_KEY{Style.WHITE}={Style.IBLUE}{secretKey}\r
 {Style.GREEN}{commandEnvSet} AWS_SESSION_TOKEN{Style.WHITE}={Style.IBLUE}{sessionToken}\r
 {Style.GREEN}{commandEnvSet} AWS_EXPIRATION{Style.WHITE}={Style.IBLUE}{expiration}\r

 {Style.IMAGENTA}  >>> Opening in another window...

 {Style.GREEN}or...
 {Style.GREEN}To setup this AWS Session at this same Window
 Hit [Shift + Insert] or execute the script:

 {Style.IBLUE}  >>> {executeScript}{Style.RESET}
        """
        return output

    def addEnvironmentVariablesConfigurationToClipboard(self, forBash, accessKey, secretKey, sessionToken, expiration):
        command = "set" if not forBash else "export"
        # Add to Clipboard (SETs environmentsWin)
        forClipboard  = f"{command} AWS_ACCESS_KEY_ID={accessKey}\r\n"
        forClipboard += f"{command} AWS_SECRET_ACCESS_KEY={secretKey}\r\n"
        forClipboard += f"{command} AWS_SESSION_TOKEN={sessionToken}\r\n"
        if forBash:
           forClipboard += f"{command} AWS_EXPIRATION=\"{expiration}\"\r\n"
        else:
           forClipboard += f"{command} AWS_EXPIRATION={expiration}\r\n" 
        Utils.addToClipboard(forClipboard)

    def createContentScriptFileStartSession(self, forBash, accessKey, secretKey, sessionToken, expiration):
        initFileContent = self.createBashScriptFile(accessKey, secretKey, sessionToken, expiration) if forBash else \
                          self.createCMDscriptFile(accessKey, secretKey, sessionToken, expiration)
        return initFileContent

    def createCMDscriptFile(self, accessKey, secretKey, sessionToken, expiration):
        return f"""
        @ECHO OFF
        ECHO.
        ECHO.=============================
        ECHO.  AWSCLI Session Configured
        ECHO.=============================
        set AWS_ACCESS_KEY_ID={accessKey}
        set AWS_SECRET_ACCESS_KEY={secretKey}
        set AWS_SESSION_TOKEN={sessionToken}
        set AWS_EXPIRATION={expiration}

        for /F "delims=" %%i in ('aws sts get-caller-identity') do (
            SET "string=%%i"
            echo %%i | findstr /C:"Account">nul && (
                SET ACCOUNT=%%i
            )
            echo %%i | findstr /C:"Arn">nul && (
                SET USERARN=%%i
            )
        )
        set ACCOUNT=%ACCOUNT:Account:=%
        set ACCOUNT=%ACCOUNT:"=%
        set ACCOUNT=%ACCOUNT:,=%
        set ACCOUNT=%ACCOUNT: =%

        set USERARN=%USERARN:Arn:=%
        set USERARN=%USERARN:"=%
        set USERARN=%USERARN:,=%
        set USERARN=%USERARN: =%

        set AWS_ACCOUNT=%ACCOUNT%
        set AWS_USER=%USERARN%

        ECHO.Expires at...: {expiration:%Y-%m-%d %H:%M}
        ECHO.Account......: %ACCOUNT%
        ECHO.User.........: %USERARN%
        ECHO.
        """

    def createBashScriptFile(self, accessKey, secretKey, sessionToken, expiration):
        return f"""
        #!/bin/sh
        echo 
        echo =============================
        echo   AWSCLI Session Configured
        echo =============================
        export AWS_ACCESS_KEY_ID={accessKey}
        export AWS_SECRET_ACCESS_KEY={secretKey}
        export AWS_SESSION_TOKEN={sessionToken}
        export AWS_EXPIRATION="{expiration}"

        vlr="$(aws sts get-caller-identity)"
        account=$(echo "$vlr" | grep '"Account"' | sed s/\\"//g | sed s/,//g | sed s/"Account:"//g)
        arn=$(echo "$vlr" | grep '"Arn"' | sed s/\\"//g | sed s/,//g | sed s/"Arn:"//g )

        export AWS_ACCOUNT=$account
        export AWS_USER=$arn

        echo Expires at...: "{expiration}"
        echo Account......: $account
        echo User.........: $arn
        echo
        """
        