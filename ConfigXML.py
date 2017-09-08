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
    ignoreCount = 0
    
    for entry in self.configFile.fetchText():
      if first:
        first = False
        continue
      
      if ignoreCount > 0:
        ignoreCount -= 1
        continue
      if len(entry.contents) > 0:
        currentValue = entry.contents[0]
      else:
        currentValue = ""
        
      entriesDict = {}
      if len(entry.contents) > 1:        
        # Process as a separate dictionary
        for singleEntry in entry.contents:
          if singleEntry == '\n':
            continue
          ignoreCount += 1
          entriesDict[singleEntry.name] = singleEntry.contents[0]
        currentValue = entriesDict
          
      if entry.name in self.configDict:
        existingEntry = self.configDict[entry.name]
        if isinstance(existingEntry, list):
          list(existingEntry).append(currentValue)
        else:
          newlist = []
          newlist.append(existingEntry)
          newlist.append(currentValue)
          self.configDict[entry.name] = newlist
      else:
        self.configDict[entry.name] = currentValue
  def getConfigValueRecurse(self, configDictionary, query):
    # For multiple layers of XML
    querylist = query.split(".")
    if len(querylist) == 1:
      return configDictionary[querylist[0]]
    
    self.getConfigValueRecurse(configDictionary[querylist[0]], ".".join(querylist[1:]))
    
  def getConfigValue(self, query):
    return self.getConfigValueRecurse(self.configDict, query)

  def getValue(self, key):
    try:
      returnVal = self.configDict[key]
    except:
      returnVal = None
      
    if returnVal is None:
      try:
        returnVal = self.defaultDict[key]
      except:
        returnVal = None
        
    return returnVal
