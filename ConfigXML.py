from BeautifulSoup import BeautifulSoup, Comment

class xmlparser(object):

  def __init__(self, configFile, defaultConfig):
    self.defaultDict={}
    self.configDict ={}
    with open(configFile) as f:
      content  = f.read()
      self.configFile = BeautifulSoup(content)
      comments = self.configFile.findAll(text=lambda text:isinstance(text, Comment))
      [comment.extract() for comment in comments]
    with open(defaultConfig) as f:
      content = f.read()
      self.defaultConfig = BeautifulSoup(content)
      comments = self.defaultConfig.findAll(text=lambda text:isinstance(text, Comment))
      [comment.extract() for comment in comments]
    self.allOptions = self.getAllOptions()

  def getAllOptions(self):
    for option in self.defaultConfig.options:
      label=option.find('label')
      default=option.find('default')
      if label != -1 and default != -1:
        self.defaultDict[label.string]=default.string
    first = True
    
    for entry in self.defaultConfig.fetchText():
      if first:
        first = False
        continue
      
      currentValue = entry.contents
      entriesDict = {}
      # Check if key exists in the dictionary
      if len(entry.contents) > 1:
        # Process as a separate dictionary
        for singleEntry in entry.contents:
          if singleEntry == '\n':
            continue
          entriesDict[singleEntry.name] = singleEntry.contents
        currentValue = entriesDict
          
      if entry.name in self.configDict:
        existingEntry = self.configDict[entry.name]
        if not isinstance(existingEntry, list):
          list(existingEntry).append(currentValue)
        else:
          newlist = []
          newlist.append(existingEntry)
          newlist.append(currentValue)
          self.configDict[entry.name] = newlist
      else:
        self.configDict[entry.name] = currentValue
  def getConfigValue(self, configDictionary, query):
    querylist = query.split(".")
    if len(querylist) == 1:
      return configDictionary[querylist]
    
    getConfigValue(configDictionary[querylist[0]], ".".join(querylist[1:]))
    
  def getConfigValue(self, query):
    return self.getConfigValue(self.configDict, query)
    #  value.fetchText()
    #  Ignore the first, process the rest
    #  First one seems to be the outer tag
    #  If there is still one level down then dictionary
    #  If more exists then create a list
    #  Leave up to user to know if something is a list
    #    Have them iterate more

  def getValue(self, key):
    """
     algorithm:
     - Check if key exists ie schedule.database
     - What to do if list vs singleton?
     - If not in config, check for default
     - If does not exist then throw error or return null
    """
    return "Single Value"
    

  def getList(self, key):
    # This is used for list of options in the XML
    # - Return an array of the 'option' this would need to be iterated
    # - OR return an array of dictionaries, iterate through the array
    # - User will always need to know the structure of their config file
    return "Array of dictionary entries"
  

# Notes:
# Use - 
# func: find, findAll, fetchText, firstText, getString, getText, 
# tag:  contents, name
