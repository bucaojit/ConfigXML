from ConfigXML import xmlparser

conf = xmlparser("schedule.xml", "DefaultOptions.xml")
value=conf.getValue("port")
print value