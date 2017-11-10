# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 14:29:23 2017

@author: oznura
"""


from __future__ import print_function
from nltk.tokenize import WordPunctTokenizer
import json

import nltk


grammar = r"""
  NP: {<PRP\$|PRP>* <RBS>* <CD>+ <CC>* <NN|NNS>* <JJ>* <NN|NNS>*} 
      {<PRP\$|PRP> <NN|NNS>+}               
"""

def extractSentences(document):
        sentences = nltk.sent_tokenize(document) 
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences] 
        return sentences

def parseGrammer(reviewText, reviewId):
    result = ""
    extractedReviewSentence = extractSentences(reviewText)
    cp = nltk.RegexpParser(grammar)
    for sent in extractedReviewSentence:
        parsed_sent = cp.parse(sent)
        for subtree in parsed_sent.subtrees():
            if subtree.label() == 'NP': 
                oneTerm = ""
                for element in subtree:
                    oneTerm += str(element) + ";"
                if(oneTerm != ""):
                    result += str(reviewId) + "@@@" + oneTerm[:-1] + "\n"
    return result


    
def readData():
    reviewfileName = 'reviews.csv'
    reviewTermFileName = 'Terms.csv'
    reviewSummaryFileName = 'Summary.csv'
    targetReview = open(reviewfileName, 'w', encoding='utf-8')
    targetTerm = open(reviewTermFileName, 'w', encoding='utf-8')
    targetSummary = open(reviewSummaryFileName, 'w', encoding='utf-8')
    
    tagList = ["CD","CC","DT","JJ","JJR","JJS","PDT","NN","PRP$","PRP","NNS", "NNP"]
    tagListNumeric = ["CD"]

    reviewID = 1
    word_punct_tokenizer = WordPunctTokenizer()
    with open('reviews_Baby.json') as f:
        for line in f:
            oneReviewData = json.loads(line)
            if 'reviewerName' in oneReviewData:
                reviewerName = oneReviewData['reviewerName'].replace("'","").replace('"',"").replace(","," ").replace("\\"," ")
            if 'reviewerID' in oneReviewData:
                reviewerID = oneReviewData['reviewerID'].replace("'","").replace('"',"").replace(","," ")
            if 'asin' in oneReviewData:
                asin = oneReviewData['asin'].replace("'","").replace('"',"").replace(","," ")
            if 'helpful' in oneReviewData:
                helpful = str(oneReviewData['helpful']).replace(","," ")
            if 'overall' in oneReviewData:
                overall = oneReviewData['overall']
            if 'summary' in oneReviewData:
                summary = oneReviewData['summary'].replace("'","").replace('"',"").replace(","," ")
            if 'reviewTime' in oneReviewData:
                reviewTime = oneReviewData['reviewTime'].replace("'","").replace('"',"").replace(","," ")
            if 'unixReviewTime' in oneReviewData:
                unixReviewTime = oneReviewData['unixReviewTime']
            
            review = reviewerID + ',' + asin + ',' + reviewerName + ',' + helpful + ',' + str(overall) + ',' + summary.replace("'","").replace('"',"") + ',' + str(reviewTime).replace(',',"") + ',' +  str(unixReviewTime) + ',' + str(reviewID)
            termText = "" 
            summaryText = ""
            
            if(oneReviewData['reviewText'] is not None and oneReviewData['reviewText'] != ''):
                reviewText = oneReviewData['reviewText'].replace("-", " ")
                termText = parseGrammer(reviewText, reviewID).strip()
            if(oneReviewData['summary'] is not None and oneReviewData['summary'] != ''):
                reviewSummary = oneReviewData['summary'].replace("-", " ")
                summaryText = parseGrammer(reviewSummary, reviewID).strip()
            if(reviewID != None and 
            ((termText != None and termText != "") or(summaryText != None and summaryText != ""))):
                targetReview.write(review + '\n')  
                targetReview.flush()
                
                if(termText != None and termText != ""):
                    targetTerm.write(termText + '\n')   
                    targetTerm.flush()           
                if(summaryText != None and summaryText != ""):
                    targetSummary.write(summaryText + '\n')   
                    targetSummary.flush() 
                #print(termText)
            print(reviewID)
            reviewID += 1
                        
    targetReview.close()
    targetTerm.close()
    targetSummary.close()



readData()

