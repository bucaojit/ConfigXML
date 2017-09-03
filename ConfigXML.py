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
    # for entry in self.configFile.configuration:
      

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
    


		
