from __future__ import print_function

import os.path
import copy

from xpinyin import Pinyin
import json
import plistlib
import hashlib
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = ''
RANGE_NAMES = {}
ITERM_PROFILE_JSON_PATH = "/Users/marskey/work/pythonTool/Default.json"
SSH_BASH_FILE_PATH = "/Users/marskey/work/xtermProfile/internelSshBash"

class SheetData:
    sheetName = ''
    __data = None
    __header = None

    def __init__(self, sheetName) -> None:
        self.sheetName = sheetName
        self.__header = None
        self.__data = None

    def openSheet(self, service, spreadsheetId, range_name):
        try:
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheetId,
                                        range=range_name).execute()

            self.__data = result.get('values', [])

            if not self.__data:
                print('No data found.')
                return False

            self.__header = self.__data[0]

        except HttpError as err:
            print(err)
            return False

        return True
                    
    def getIdxByHeaderName(self, name):
        if not self.__header:
            return -1

        for idx in range(1, len(self.__header)):
            if name == self.__header[idx]:
                return idx
        return -1

    def getValueByName(self, row, name):
        idx = self.getIdxByHeaderName(name)
        if idx >= 0 and idx < len(row):
            return row[idx]
        return ""

    def getValueByIdx(self, row, idx):
        if idx >= 0 and idx < len(row):
            return row[idx]
        return ""

    def genItermProfiles(self, templatePath, sshBashPath):
        if not os.path.exists(templatePath):
            return[]

        jsonData = {}
        with open(templatePath, 'r') as tp:
            jsonData = json.load(tp)

        profilesJsonData = [] 
        # profilesJsonData["Profiles"] = [] 

        if not self.__data or not self.__header:
            return[]

        remoteIp = self.getValueByIdx(self.__header, len(self.__header) - 1)
        if not remoteIp:
            return[]

        p = Pinyin()
        for row in range(1, len(self.__data)):
            rowData = self.__data[row]
            name = self.getValueByName(rowData, "备注")
            if not name:
                continue

            if name.find(self.sheetName) == -1:
                name = self.sheetName + "_" + name

            pinyin = p.get_pinyin(name)
            if pinyin:
                pinyin = "".join(pinyin.split('-'))

            sshPort = self.getValueByName(rowData, "ssh_22")
            if not sshPort:
                continue

            hostName = self.getValueByIdx(rowData, 0)

            profileJson = copy.deepcopy(jsonData)
            profileJson["Badge Text"] = name
            profileJson["Name"] = name + " " + pinyin
            profileJson["Tags"].append(hostName)

            commandText = f'{sshBashPath} {remoteIp} {sshPort}'
            profileJson["Initial Text"] = commandText
            profileJson["Guid"] = hostName
            profilesJsonData.append(profileJson)

        return profilesJsonData
        # jsonFileName = f"internelServers{self.sheetName}.json"
        # with open(jsonFileName, 'w') as jsonFile:
        #     jsonFile.write(json.dumps(profilesJsonData))

    def genSequelProFavorites(self):
        if not self.__data or not self.__header:
            return{}

        remoteIp = self.getValueByIdx(self.__header, len(self.__header) - 1)
        if not remoteIp:
            return{}

        # plistFile = {}
        # plistFile["SPConnectionFavorites"] = []

        directory = {}
        directory["Name"] = self.sheetName
        directory["IsExpanded"] = False
        directory["Children"] = []

        for row in range(1, len(self.__data)):
            rowData = self.__data[row]

            name = self.getValueByName(rowData, "备注")
            if not name:
                continue

            if name.find(self.sheetName) == -1:
                name = self.sheetName + "_" + name

            port = self.getValueByName(rowData, "mysql_3306")
            if not port:
                continue

            connection = {}
            connection["colorIndex"] = -1
            connection["host"] = remoteIp
            connection["name"] = name

            id = int(hashlib.md5(self.sheetName.encode("utf-8")).hexdigest(), 16) % (10 ** 19)
            connection["id"] = id

            connection["port"] = port
            connection["user"] = "root"
            directory["Children"].append(connection)

        return directory
        # plistFile["SPConnectionFavorites"].append(directory)
        # plistFileName = f"sequelPro{self.sheetName}.plist"
        # with open(plistFileName, 'wb') as fp:
        #     plistlib.dump(plistFile, fp)

    def genARDMConnections(self):
        if not self.__data or not self.__header:
            return[]

        remoteIp = self.getValueByIdx(self.__header, len(self.__header) - 1)
        if not remoteIp:
            return[]

        connections = []
        for row in range(1, len(self.__data)):
            rowData = self.__data[row]

            name = self.getValueByName(rowData, "备注")
            if not name:
                continue

            if name.find(self.sheetName) == -1:
                name = self.sheetName + "_" + name

            port = self.getValueByName(rowData, "redis_6379")
            if not port:
                continue

            connection = {}
            connection["host"] = remoteIp
            connection["port"] = port
            connection["auth"] = ""
            connection["username"] = ""
            connection["name"] = name
            connection["cluster"] = False
            connection["connectionReadOnly"] = False
            # connection["key"] = hashlib.md5(self.sheetName.encode("utf-8")).hexdigest()
            connection["order"] = row
            connections.append(connection)

        return connections
        # result = json.dumps(connections)
        # fileName = f"ARDM_{self.sheetName}.ano"
        # with open(fileName, 'wb') as file:
        #     file.write(base64.b64encode(bytes(result, 'utf-8')))

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)

    iterm2Profiles = dict(Profiles = [])
    sequelProPlist = dict(SPConnectionFavorites = [])
    ano = []

    for projectName in RANGE_NAMES:
        # sd = SheetData("BOE")
        sd = SheetData(projectName)
        sd.openSheet(service, SPREADSHEET_ID, RANGE_NAMES[sd.sheetName])
        iterm2Profiles["Profiles"].extend(sd.genItermProfiles(ITERM_PROFILE_JSON_PATH, SSH_BASH_FILE_PATH))
        sequelProPlist["SPConnectionFavorites"].append(sd.genSequelProFavorites())
        ano.extend(sd.genARDMConnections())

    #gen Item2
    with open("iterm2InternalDynamic.json", 'w') as jsonFile:
        jsonFile.write(json.dumps(iterm2Profiles))
    #gen Sequel Pro
    with open("sequelProPlist.plist", 'wb') as plistFile:
        plistlib.dump(sequelProPlist, plistFile)
    #gen Another Redis Desktop Manager
    for idx in range(len(ano)):
        ano[idx]["order"] = idx
    with open("ARDM.ano", 'wb') as file:
        file.write(base64.b64encode(bytes(json.dumps(ano), 'utf-8')))

if __name__ == '__main__':
    main()
