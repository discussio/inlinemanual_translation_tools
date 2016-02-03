# convertToPOEditor.py - converts files formatted by inline manual into
# files ready to upload into POEditor (.json -> .json)
# @author d3sandoval - Daniel Sandoval (daniel@discuss.io)

###
# HOW TO USE
# Download .json files for every topic in inline manual (?: https://inlinemanual.zendesk.com/hc/en-us/articles/206420473)
# Place downloaded files into a folder called "toTranslate", located in the same directory as this script (/bin/inlinemanual/toTranslate on DIO boxes)
# Run this script by entering "python convertToPOEditor.py" in your terminal
# uploadToPOEditor.json will be created when script is finished - upload this to POEditor (?: https://poeditor.com/help/)
# !!! Careful this will overwrite any other file named POEditor.json in the directory
# Note: You can also update terms to/from POEditor using a github connection
#       (?: https://poeditor.com/help/how_to_translate_a_language_file_from_a_github_project)
###

import json
import os
import copy

from pprint import pprint #for testing

json_data = []
topic = {}
for filename in os.listdir("./toTranslate"):
    if filename.startswith("topic"):

        # load INM .json file for processing
        with open("./toTranslate/" + filename) as data_file:
            data = json.load(data_file)

        # pprint(data);
        # interpret and add to json data
        step = 0
        for item in data["steps"]:
            topic["context"] = str(data["id"]) + " " + str(step) # convert to array using .split()
            topic["defintion"] = "Topic #" + str(data["id"]) + " Step #" + str(step) # human-readable version of "context"
            topic["reference"] = item["element"] # reference element on page, for context

            # create a term for the step title
            topicTitle = copy.deepcopy(topic)
            topicTitle["term"] = item["title"]
            json_data.append(topicTitle)

            # create a term for the step content
            topic["term"] = item["content"]
            json_data.append(topic)

            step += 1
            topic = {}

            # code for testing
#             print "json data now: \n"
#             pprint(json_data)
#             print "\n\n\n"

# write jsonData to POEditor.json output file
with open('uploadToPOEditor.json', 'w') as outfile:
                json.dump(json_data, outfile, indent = 2, ensure_ascii=False)
