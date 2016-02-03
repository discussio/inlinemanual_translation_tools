#What is it good for?
These two scripts allow you to convert single-language inline manual topics into muliple topics for each language your application supports:

1.  convertToPOEditor.py - converts files formatted by inline manual into files ready to upload into POEditor (.json -> .json)
2.  convertToINM.py -  converts files formatted by POEditor into files ready to upload into Inline Manual (.json -> .json)

#How do I use it?
Watch this video for an overview of the entire process:

Here are the steps (most taken from: https://inlinemanual.zendesk.com/hc/en-us/articles/206420473-Translation-workflow):

1.  Download the latest revision of each topic you'd like to translate
2.  Copy all the downloaded topics into the toTranslate folder in wherever you clone this repository
3.  Run convertToPOEditor.py (`python convertToPOEditor.py`) from the root directory
4.  Open your POEditor project and upload the file, uploadToPOEditor.json that was generated upon completion of step 3
5.  Verify that terms uploaded correctly and hire translators for each language
6.  When translation is complete, export each language's terms in .json format
7.  Place these files (named "<Project\_Name>\_<Language>") in the fromPOEditor folder
8.  Run convertToINM.py (`python convertToINM.py`), translated topics will appear in /export folder (generated by script)
9.  Clone each topic as many times as there are languages - set each new topic to its destination language
10. Upload the translated topics (named "topic\_<id>\_<Language>") into their language-specific topic
11. Add the new topics to your site on INM, don't forget to localize the player interface

**Note:** Every new topic will have a new id but will still reference its parent within its internal .json. You can take advantage of this to easily call translated topics using the parent topic id (see "Why aren't my translated topics playing?" below).

#Why aren't my translated topics playing?
First, familiarize yourself with how InlineManual handles multiple-language tutorials: [https://inlinemanual.com/blog/language-handling-tutorials](https://inlinemanual.com/blog/language-handling-tutorials). As mentioned in that blog post and the video above, you'll need to set the language (right above your player's embed code) to load the correct topic for your users:
`window.inlineManualOptions = { language: 'de'};`

After that, you'll have to call your translated topic from the javascript or url-based API. At Discuss.io, we wrote a method to make calling the translated topic as easy as calling the original language one (i18n\_topic is called from an onclick event):


    function i18n_topic(topic_id) {
        var topics = inline_manual_player.getValidTopics();
        if (topic_id in topics) {
        	inline_manual_player.activateTopic(topic_id); // meeting room tour
        	return topic_id;
        } else {
        	for (var topic in topics) {
        		if (topics[topic]["parent_id"] == topic_id) {
        			inline_manual_player.activateTopic(topics[topic]["id"]);
        			return topics[topic]["id"];
        		}
        	}
        }
    
        // in case there is no translated version of topic
        var origLang = <?php echo '"' . I18N::getLanguageISO2() . '"' ?>;
        inline_manual_player.setLanguage("en");
        inline_manual_player.activateTopic(topic_id);
        inline_manual_player.setLanguage(origLang);
        return topic_id;
    
    }


#What's next?
Discuss.io (the writers of these scripts) no longer uses POEditor for translation so this repository will not be updated by us if either tool changes its input/output syntax for its .json formats. We have requested that InlineManual make it easier to upload topics and set their language in batch rather than having to clone them all individually and use the web GUI to upload new strings. Once this is possible, the last step of this process (uploading translated topics into INM) will change and the code could be rewritten around the new uploading possibilities.
