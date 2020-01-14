#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 00:11:32 2019

@author: imox
"""
import re

aHrefLink = '''<a href="{link}" target="_blank">{link-text}</a>'''
markDownLink  = '''[{link-text}]({link}" target="_blank)'''
boldLinks = list()
text = ''''''
    
def isLinkTextBold(text):
    if text.find('**') != -1:
        return 1
    else:
        return 0

def findLinkAndTextFromMarkup(text):
    name_regex = "[^]]+"
    url_regex = "http[s]?://[^)]+"
    markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)
    match = re.findall(markup_regex, text)
    return match

def replaceMarkDownUrlWithATag(markdownUrl,aTag,text):
    # only if _blank is there as ![]() are fine
    if markdownUrl.find('_blank') != -1:
        text =  text.replace(markdownUrl,aTag)
    else:
        print("markdownUrl:"+markdownUrl)
    
    return text

    
def removeTagFromHashLine(text):
    # '###<' doesnt work '###\n<' works
    text=text.replace('###<','###\n<')
    return text

def changeMarkdownToHeader(text):
    h3regex = re.compile(".*?\###(.*?)\\n")
    h3result = re.findall(h3regex, text)
    
    for result in h3result:
        tempMarkDown = '###'+result+'\n'
        newHeader =  '<h3>'+result+'</h3>\n\n'
        text = text.replace(tempMarkDown,newHeader)
        
    h2regex = re.compile(".*?\##(.*?)\\n")
    h2result = re.findall(h2regex, text)
    
    for result in h2result:
        tempMarkDown = '##'+result+'\n'
        newHeader =  '<h2>'+result+'</h2>\n\n'
        text = text.replace(tempMarkDown,newHeader)
                          
        
    return text
        
def BoldMarkdownAfterBreak(text):
    #<br>\n**Bold Text** doesn't work, correct it
    text=text.replace('<br>\n**','<br>\n\n**')
    text=text.replace('</br>\n#','</br>\n\n#')
    text=text.replace('<hr>\n*','<hr>\n\n*')
     
    return text

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def changeRealtiveImageUrlToAbsolute(link):
    if link.find('techpacker.com') == -1:
        pass
    
def boldMarkDownToHTML(text):
    text = text.replace('**',"<b>")
    text = rreplace(text, '<b>', '</b> ', 1)
    return text
    

with open('data.md', 'r+') as file:
    # file name data.md is pre-assumed to exist in same directory as this file
    # data.md is used as input caret and output caret
    
    # read file as string
    markdown = file.read()
    markdownCopy = markdown
    
    #list of links , is a list [] of tuples () , so [(linkTest,linkUrl)(linkTest,linkUrl),...]
    listOfLinks = findLinkAndTextFromMarkup(markdown)
    
    for link in listOfLinks:
        #we will make href link <a></a> and replace markdown links with them []()
        newHref = ''
        markDownUrl = ''
        
        #clean url link by removing target blank
        linkUrl = link[1].replace('''" target="_blank''','')
        linkText = link[0]
        
        markDownUrl = markDownLink.replace('{link}',linkUrl)
        markDownUrl = markDownUrl.replace('{link-text}',linkText)

        #replace bold url text **text** to <b>text<b>
        if isLinkTextBold(linkText):
            boldLinks.append(linkUrl)
            linkText = boldMarkDownToHTML(linkText)
               
        newHref = aHrefLink.replace('{link}',linkUrl)
        newHref = newHref.replace('{link-text}',linkText)
        
        markdownCopy = replaceMarkDownUrlWithATag(markDownUrl,newHref,markdownCopy)
        
    #remove all wrong image references to /blot/blog => /blog
    markdownCopy = markdownCopy.replace('/blot/','/')
    
    markdownCopy = BoldMarkdownAfterBreak(markdownCopy) 
    markdownCopy = removeTagFromHashLine(markdownCopy)
    markdownCopy = changeMarkdownToHeader(markdownCopy)
    
    #seek back to start, so as to overwrite and not append
    file.seek(0)
    file.write(markdownCopy)
    
    #to know which link had **text**, so we need to add <b></b> tag
    print(boldLinks)
