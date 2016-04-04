import os
from espeak import espeak
from tkinter import *
from bs4 import BeautifulSoup
import tkinter as tk
import urllib
import re
import pickle


lis=map(chr,range(97,123))
lis=list(lis)
lis.append("'")

class TrieNode:
    # Initialize your data structure here.
    def __init__(self):
        self.val = None
        self.pointers={}
        self.end=0


class Trie:

    def __init__(self):
        self.root = TrieNode()

    # @param {string} word
    # @return {void}
    # Inserts a word into the trie.
    def insert(self, word):
        self.rec_insert(word, self.root)
        return

    def rec_insert(self, word, node):
        if word[:1] not in node.pointers:
            newNode=TrieNode()
            newNode.val=word[:1]
            node.pointers[word[:1]]=newNode
            self.rec_insert(word, node)
        else:
            nextNode = node.pointers[word[:1]]
            if len(word[1:])==0:
                node.end=1
                return
            return self.rec_insert(word[1:], nextNode)


    # @param {string} word
    # @return {boolean}
    # Returns if the word is in the trie.
    def search(self, word):
        if len(word)==0:
            return False
        return self.rec_search(word,self.root)

    def rec_search(self, word, node):
        if word[:1] not in node.pointers:
            return False
        else:
            nextNode = node.pointers[word[:1]]
            if len(word[1:])==0:
                if nextNode.end == 1:
                    return True
                else:
                    return False
            return self.rec_search(word[1:],nextNode)


    # @param {string} prefix
    # @return {boolean}
    # Returns if there is any word in the trie that starts with the given prefix.
    def startsWith(self, prefix):
        if len(prefix)==0:
            return True
        return self.rec_search_prefix(prefix,self.root)

    def rec_search_prefix(self, word, node):
        if word[:1] not in node.pointers:
            return False
        else:
            if len(word[1:])==0:#still have remaining in the prefix
                return True
            nextNode = node.pointers[word[:1]]
            return self.rec_search_prefix(word[1:],nextNode)
            
    
    def findAll(self,node,word,sugg):
    	for c in lis:
    		if c in node.pointers:
    			if node.pointers[c].end==1:
    				sugg.append(word+str(c))
    			self.findAll(node.pointers[c],word+str(c),sugg)
    	return
    	        

    def didUMean(self,word,sugg):
    	if self.startsWith(word):
    		top=self.root
    		for c in word:
    			top=top.pointers[c]
    		self.findAll(top,word,sugg)
    	else:
    		return
    	         

'''
trie=Trie()

file = open('words.txt','r')
dict=file.readlines()
for words in dict:
	trie.insert(words.lower())
file.close()

pickle.dump(trie,open("save.p", "wb"))
'''

trie = pickle.load(open( "save.p", "rb"))

class EditDist:
	def __init__(self):
		pass
	

while True:

	word= input("Enter the word:")
	word=word.lower()
	espeak.synth(word)
	if word=='exit':
		break

	if trie.search(word):
		print("Found")
		urlStr='http://www.dictionary.com/browse/'+word+'?s=t'
		url=urllib.request.urlopen(urlStr)
		content = url.read()
		soup = BeautifulSoup(content)
		# kill all script and style elements
		for script in soup(["script", "style"]):
		    script.extract()    # rip it out
		# get text
		text = soup.get_text()
		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		res=[chunk for chunk in chunks if chunk]
		res=res[:res.index('About')]
		
		nearbyInd=res.index('Nearby words for '+word)
		nearbyWords=res[nearbyInd:]
		res=res[:nearbyInd]
		
		for i in range(len(res)):
			print(i,res[i])
		text = '\n'.join(chunk for chunk in chunks if chunk)

		#print(text)
		
	else:
		print("Not Found\nDid You Mean:")
		sugg=[]
		trie.didUMean(word.lower(),sugg)
		sugg.sort(key = lambda s: len(s))
		for words in sugg[:min(len(sugg),10)]:
			print(words)

root = Tk()
entry = Entry(root, width=10)
entry.pack()
soundIcon = PhotoImage(file='soundIcon.png')
root.mainloop()
      
