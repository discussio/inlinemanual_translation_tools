# convertToINM.py - converts files formatted by POEditor into
# files ready to upload into Inline Manual (.json -> .json)
# @author d3sandoval - Daniel Sandoval (daniel@discuss.io)

###
# HOW TO USE
# Download .json files for every language using the "export" button in POEditor
# Place downloaded files into a folder called "fromPOEditor", located in the same directory as this script (/bin/inlinemanual/fromPOEditor on DIO boxes)
# Run this script by entering "python convertToINM.py" in your terminal
# json files starting with "topic_" will be created in the /export folder when script is finished
#     upload these to Inline Manual (?: https://inlinemanual.zendesk.com/hc/en-us/articles/206420473)
# Note: You can also update terms to/from POEditor using a github connection
#       (?: https://poeditor.com/help/how_to_translate_a_language_file_from_a_github_project)
###

import json
import os
import copy
import codecs

# from pprint import pprint #for testing
project_name = "DIO" #name of POEditor project - appears at beginning of .json files
json_data = {}

# make output directory if not already exists
if not os.path.exists("export"):
    os.makedirs("export")

# load pre-translated topics to pair and merge
for filename in os.listdir("./toTranslate"):
    if filename.startswith("topic"):
        jsonFile = open("./toTranslate/" + filename, "r")
        data = json.load(jsonFile)
        name = filename.split("_")

        json_data[name[1]] = data

# load translated terms and match up with topics
for filename in os.listdir("./fromPOEditor"):
    if filename.startswith(project_name):

        # load POEditor .json file for processing
        with open("./fromPOEditor/" + filename) as data_file:
            data = json.load(data_file)

        # interpret and add to json data
        title = True # first entry for step is title, second is content
        for item in data:
            if (item['context']):
                context = item['context'].split()
                steps = json_data[context[0]]["steps"]
                this_step = steps[int(context[1])]
                if title:
                    this_step["title"] = item["definition"]
                    title = False
                else:
                    this_step["content"] = item["definition"]
                    title = True #reset title to true for next step
#         pprint(json_data)

        # after all topics have been translated, export as .json
        for topic in json_data.itervalues():
#             pprint(topic)
            lang_name = filename.split(".")[0]
            outfile_name = "topic_" + str(topic["topic_id"]) + "-" + lang_name.split("_")[1] + ".json"
            with codecs.open("./export/" + outfile_name, 'w', encoding='utf8') as outfile:
                json.dump(topic, outfile, indent = 2, ensure_ascii=False)
#             code for testing
#         print "json data for " + filename + " :\n"
#         pprint(json_data)
#         print "\n\n\n"
