__author__ = 'Chandra & Rashmi'
import xml.dom.minidom
from collections import defaultdict
import urllib2
import json
import re
import time
import urllib2
from lxml import html
from collections import defaultdict
import collections
import random
from prettytable import PrettyTable
import string
from bs4 import BeautifulSoup
import sys
import math
import random
# Below dictionary is useful for aggregating jobs state code wise
USA = {'WA': 'Washington ', 'DE': 'Delaware ', 'DC': 'District of Columbia ', 'WI': 'Wisconsin ', 'WV': 'West Virginia ', 'HI': 'Hawaii ', 'FL': 'Florida ', 'WY': 'Wyoming ', 'NH': 'New Hampshire ', 'NJ': 'New Jersey ', 'NM': 'New Mexico ', 'TX': 'Texas ', 'LA': 'Louisiana ', 'NC': 'North Carolina ', 'ND': 'North Dakota ', 'NE': 'Nebraska ', 'TN': 'Tennessee ', 'NY': 'New York ', 'PA': 'Pennsylvania ', 'CA': 'California ', 'NV': 'Nevada ', 'VA': 'Virginia ', 'CO': 'Colorado ', 'AK': 'Alaska ', 'AL': 'Alabama ', 'AR': 'Arkansas ', 'VT': 'Vermont ', 'IL': 'Illinois ', 'GA': 'Georgia ', 'IN': 'Indiana ', 'IA': 'Iowa ', 'OK': 'Oklahoma ', 'AZ': 'Arizona ', 'ID': 'Idaho ', 'CT': 'Connecticut ', 'ME': 'Maine ', 'MD': 'Maryland ', 'MA': 'Massachusetts ', 'OH': 'Ohio ', 'UT': 'Utah ', 'MO': 'Missouri ', 'MN': 'Minnesota ', 'MI': 'Michigan ', 'RI': 'Rhode Island ', 'KS': 'Kansas ', 'MT': 'Montana ', 'MS': 'Mississippi ', 'SC': 'South Carolina ', 'KY': 'Kentucky ', 'OR': 'Oregon ', 'SD': 'South Dakota '}


def addword(bigdict, key, olddict):
    if key in bigdict:
        bigdict[key].append(olddict)

    else:
          bigdict[key] = [olddict]



def cb():
    stateDict = defaultdict(dict)
    companyDict = {}
    problemDict = {}
    cbDict = {}
    duplicateCb = {}
    problemCount = 0
    duplicateCount = 0
    jobCount = 0

    count = 0
    url = "http://api.careerbuilder.com/v1/jobsearch?developerKey=WDHS2CM6G1X9T4LPZ4PH&JobTitle=Data+Scientist&PerPage=30&PageNumber=1"
    doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
    t1 = doc.getElementsByTagName("TotalPages")[0].firstChild.data
    totalPages = int(t1)
    totalCount = doc.getElementsByTagName("TotalCount")[0].firstChild.data

    for i in range(1, totalPages):
        url = "http://api.careerbuilder.com/v1/jobsearch?developerKey=WDHS2CM6G1X9T4LPZ4PH&JobTitle=Data+Scientist&PostedWithin=30&PageNumber="+str(i)
        doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())

        for pageEntry in range(0, 25):
            try:
                if (doc.getElementsByTagName("Company")[pageEntry].firstChild.data!= None and doc.getElementsByTagName("State")[pageEntry].firstChild.data!= None):
                    Job_title = doc.getElementsByTagName("JobTitle")[pageEntry].firstChild.data
                    city = doc.getElementsByTagName("City")[pageEntry].firstChild.data
                    company_name = doc.getElementsByTagName("Company")[pageEntry].firstChild.data
                    state = doc.getElementsByTagName("State")[pageEntry].firstChild.data
                    link_ = doc.getElementsByTagName("JobDetailsURL")[pageEntry].firstChild.data
                    Job_title = Job_title.encode('utf-8').strip()
                    Job_title = Job_title.lower()

                    company_name = company_name.encode('utf-8').strip()
                    company_name = company_name.lower()

                    state = state.encode('utf-8').strip()
                    state = state.upper()

                    city = city.encode('utf-8').strip()
                    city = city.lower()


                    list_ = [Job_title,city,link_]
                    addword(companyDict,company_name,list_)
                    temp_dict = {company_name:list_}
                    addword(stateDict,state,temp_dict)
                    keyDetails = state+company_name+Job_title+city
                    keyDetails = keyDetails.replace(" ","")
                    keyDetails = keyDetails.replace(" ","")
                    keyDetails = keyDetails.lower()
                    keyDetails = re.sub(r'[^\w\s]','',keyDetails)
                    emptyDetails=[]
                    emptyDetails.append(link_)
                    emptyDetails.append(list_)

                    if keyDetails in cbDict:
                        if (cbDict[keyDetails][0][0]==link_):
                            duplicateCount +=1
                            addword(duplicateCb,keyDetails,emptyDetails)
                            problemCount +=1
                            continue
                        else:
                            addword(cbDict,keyDetails,emptyDetails)
                            jobCount +=1
                    else:
                        addword(cbDict,keyDetails,emptyDetails)
                        jobCount +=1
                else:
                    continue
            except Exception,e:
                continue
        wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
        time.sleep(wait_time)

    with open("cb-state.txt", "w") as outfile:
        json.dump(stateDict, outfile,ensure_ascii=False,indent =4)

    with open("cb-company.txt", "w") as outfile:
        json.dump(companyDict, outfile,ensure_ascii=False,indent =4)

    with open("cb-complete-new.txt", "w") as outfile:
        json.dump(cbDict, outfile,ensure_ascii=False,indent =4)

    with open("cb-duplicates.txt", "w") as outfile:
        json.dump(duplicateCb, outfile,ensure_ascii=False,indent =4)

    with open("cb-problems.txt", "w") as outfile:
        json.dump(problemDict, outfile,ensure_ascii=False,indent =4)

    print "Number of states ",len(stateDict)," - Number of companies - ",len(companyDict)," - Number of jobs ",len(cbDict)," Number of problem jobs",len(problemDict)," Number of Duplicate jobs", len(duplicateCb)



def monster():
    printableList = []
    stateDict = defaultdict(dict)
    companyDict = {}
    problemDict={}
    mosnterDict={}
    duplicateMonster = {}
    count = 0
    problemCount = 0
    duplicateCount = 0
    jobCount = 0
    prettylist = PrettyTable(["Company", "Job Title", "City", "Link"])
    more = True
    review_url = "http://jobsearch.monster.com/search/Data-Scientist_5"
    while(more):

        count += 1
        page = html.fromstring(urllib2.urlopen(review_url).read())
        for link in page.xpath("//div[contains(@class,'jobTitleContainer')]"):
            x = link.getchildren()
            mydict_ = collections.defaultdict(list)

            for x1 in x:
                Job_title = x1.text
                link_ = x1.get("href")
                parent = x1.getparent()
                grandpar = parent.getparent()
                greatgrandpar = grandpar.getparent()
                greatGreatGrandparent = greatgrandpar.getparent()
                y_grandParentChildren = grandpar.getchildren()
                for y1 in y_grandParentChildren:
                    if y1.get("class") == "companyContainer":
                        eachChild_grandParentChildren = y1.getchildren()
                        for y3 in eachChild_grandParentChildren:
                            if y3.get("style") == "float:left":
                                y4 = y3.getchildren()
                                for y5 in y4:
                                    if y5.tag == "a":
                                        company_name = y5.get("title")
                                        break


                c = greatGreatGrandparent.getchildren()
                for child in c:
                    for cc in child:

                        if cc.get("class") == "companyCol fnt20 locationInfo":
                            c4 = cc.getchildren()
                            for c5 in c4:
                                if c5.tag == "div":
                                    for c6 in c5.getchildren():
                                        if c6.tag == "a":
                                            loc = c6.get("title")
                                            loc_ = loc.split()
                                            if len(loc_) == 2:
                                                city = str(loc_[0])
                                                city = city.replace(",","")

                                            else:
                                                city = loc_[0] + " "+loc_[1]
                                                city = str(city)
                                                city = city.replace(",","")
                                            state = loc_[-1]

                Job_title = Job_title.encode('utf-8').strip()
                Job_title = Job_title.lower()
                company_name = company_name.encode('utf-8').strip()
                company_name = company_name.lower()
                state = state.encode('utf-8').strip()
                state = state.upper()
                city = city.encode('utf-8').strip()
                city = city.lower()
                list_ = [Job_title,city,link_]
                addword(companyDict,company_name,list_)
                temp_dict = {company_name:list_}
                addword(stateDict,state,temp_dict)
                keyDetails = state+company_name+Job_title+city
                keyDetails = keyDetails.replace(" ","")
                keyDetails = keyDetails.replace(" ","")
                keyDetails = keyDetails.lower()
                keyDetails = re.sub(r'[^\w\s]','',keyDetails)
                emptyDetails=[]
                emptyDetails.append(link_)
                emptyDetails.append(list_)

                if keyDetails in mosnterDict:
                    if (mosnterDict[keyDetails][0][0]==link):
                        duplicateCount +=1
                        addword(duplicateMonster,keyDetails,emptyDetails)
                        problemCount +=1
                        continue
                    else:
                        addword(mosnterDict,keyDetails,emptyDetails)
                        jobCount +=1
                else:
                    addword(mosnterDict,keyDetails,emptyDetails)
                    jobCount +=1

        wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
        time.sleep(wait_time)

        more = False
        for link in page.xpath("//a[contains(@class,'box nextLink fnt5')]"):

            if link.get("href") != None:
                review_url = link.get("href")
                more = True



    with open("monster-state.txt", "w") as outfile:
        json.dump(stateDict, outfile,ensure_ascii=False,indent =4)

    with open("monster-company.txt", "w") as outfile:
        json.dump(companyDict, outfile,ensure_ascii=False,indent =4)

    with open("monster-complete-new.txt", "w") as outfile:
        json.dump(mosnterDict, outfile,ensure_ascii=False,indent =4)

    with open("monster-duplicates.txt", "w") as outfile:
        json.dump(duplicateMonster, outfile,ensure_ascii=False,indent =4)

    with open("monster-problems.txt", "w") as outfile:
        json.dump(problemDict, outfile,ensure_ascii=False,indent =4)

    print "Number of states ",len(stateDict)," - Number of companies - ",len(companyDict)," - Number of jobs ",len(mosnterDict)," Number of problem jobs",len(problemDict)," Number of Duplicate jobs", len(duplicateMonster)


def simplyhired():
    stateDict={}
    companyDict= {}
    simplyhiredDict={}
    problemSimplyhired={}
    duplicateSimplyhired={}
    linkcount =0
    jobcount = 0
    dictCount = 0
    problemCount = 0
    pattern = re.compile(r'\s+')
    pos = "data scientist"
    pos = re.sub(" ","+",pos)
    duplicateCount = 0
    pageNumber = 1
    bool2 = True


    while(bool2):
        url = "http://www.simplyhired.com/search?q="+pos+"&pn="+str(pageNumber)
        page = html.fromstring(urllib2.urlopen(url).read())
        pageNumber +=1
        # Below code will check for last page on simplyhired
        link3 = page.xpath("//div[contains(@class,'pages')]/span[contains(@class,'next unclickable')]")
        if (len(link3)>0):
            bool2 = False

        page = html.fromstring(urllib2.urlopen(url).read())
        link2 = page.xpath("//li/div[contains(@class,'job')]/h2/a")
        jobLink="http://www.simplyhired.com"
        jobLocation=""
        jobLinkSH=""
        jobCompany=""
        jobState=""
        details =[]
        l = link2
        for l in link2:
            linkcount+=1
            w = l.getchildren()
            jobTitle=""
            for q in w:
                jobTitle= jobTitle+q.text
            jobTitle = jobTitle.encode('ascii','ignore').decode('ascii')
            jobTitle = jobTitle.lower()
            m = l.getparent().getparent()
            n = m.getchildren()
            boo1 = True
            for o in n:
                if(o.get("class")=="company_location"):
                    a = o.getchildren()
                    if(len(a)==3):
                        compa = a[0].text
                        locat = a[2].text
                        if(compa!=None):
                            compa= compa.encode('ascii','ignore').decode('ascii')
                            jobCompany = compa.lower()
                        else:
                            jobCompany = "NA"
                        if(locat!=None):
                            jobLocation = locat.lower()
                        loc= jobLocation.split(",")
                        if(len(loc)==2):
                            jobLocation = loc[0].encode('ascii','ignore').decode('ascii')
                            jobState = loc[1].encode('ascii','ignore').decode('ascii')
                            jobLocation = jobLocation.lower()
                            jobState = re.sub(pattern, '', jobState)
                            jobState = jobState.upper()
                        else:
                            jobLocation = loc[0].encode('ascii','ignore').decode('ascii')
                            jobState = loc[0].encode('ascii','ignore').decode('ascii')
                            jobLocation = jobLocation.lower()
                            jobState = jobState.upper()

                        details = [jobTitle,jobLocation,jobState]#,jobLinkSH]
                        keyDetails = jobState+jobCompany+jobTitle+jobLocation
                        keyDetails = re.sub(pattern, '', keyDetails)
                        keyDetails = keyDetails.replace(" ","")
                        keyDetails = keyDetails.lower()

                    else:
                        jobDetails = a[0].text.lower()
                        jobDetails= jobDetails.encode('ascii','ignore').decode('ascii')
                        boo1 = False
                        details = [jobDetails]#,jobLinkSH]

                if(o.get("class")=="tools_container"):
                    temp1 = o.getchildren()
                    for t in temp1:
                        t3   = t.getchildren()
                        for t2 in t3:
                            if(t2.text=="Description"):
                                jobLinkSH = t2.get("href").encode('ascii','ignore').decode('ascii')

                    if(details!=None):
                        c = details.append(jobLinkSH)
                    else:
                        continue
            if(boo1):
                addword(companyDict,jobCompany,details)
                emptyDetails=[]
                emptyDetails.append(jobLinkSH)
                emptyDetails.append(details)
                dicto = {jobCompany:details}
                addword(stateDict,jobState,dicto)
                dictState = {jobState:dicto}
                if keyDetails in simplyhiredDict:
                    if (simplyhiredDict[keyDetails][0]==jobLinkSH):
                        duplicateCount +=1
                        addword(duplicateSimplyhired,keyDetails,emptyDetails)
                        continue
                else:
                    addword(simplyhiredDict,keyDetails,emptyDetails)
                dictCount+=1

            else:
                addword(problemSimplyhired,jobDetails,details)
                boo1 = True
                problemCount +=1

            jobcount +=1
        wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
        time.sleep(wait_time)

    with open("SimplyHired-company-temp.txt", "w") as outfile:
        json.dump(companyDict, outfile,ensure_ascii=False,indent =4)
    with open("SimplyHired_Problem-temp.txt", "w") as outfile:
        json.dump(problemSimplyhired, outfile,ensure_ascii=False,indent =4)
    with open("SimplyHired-state-temp.txt", "w") as outfile:
        json.dump(stateDict, outfile,ensure_ascii=False,indent =4)
    with open("SimplyHired-Complete-new.txt", "w") as outfile:
        json.dump(simplyhiredDict, outfile,ensure_ascii=False,indent =4)
    with open("SimplyHired-Duplicates.txt", "w") as outfile:
        json.dump(duplicateSimplyhired, outfile,ensure_ascii=False,indent =4)

    print "Number of states ",len(stateDict)," - Number of companies - ",len(companyDict)," - Number of jobs ",len(simplyhiredDict)," Number of problem jobs",len(problemSimplyhired)," Number of Duplicate jobs", len(duplicateSimplyhired)



def indeed():
    pos = "data scientist"
    stateDict={}
    companyDict= {}
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    stateDict = defaultdict(dict)
    companyDict= {}
    problemDict={}
    indeedDict={}
    duplicateIndeed={}
    problemCount = 0
    duplicateCount =0
    jobsCount = 1000
    pageNumber = 0
    last_page = 0
    pos = re.sub(" ","+",pos)

    #Setting boolean value to True. This will be used for identifying a posting with details missing
    boo1= True
    bool = True

    while(bool):
        url = "http://www.indeed.com/jobs?q="+pos+"&start="+str(pageNumber)
        page = html.fromstring(urllib2.urlopen(url).read())
        link3 = page.xpath("//div[contains(@class,'pagination')]/a[contains(@rel,'nofollow')]/span[contains(@class,'pn')]")
        if( last_page == link3[4].text):
            bool = False

        last_page = link3[4].text
        # for l in link3:
        #     print l.text
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)

        if (len(link3)>0):
            bool2 = False
        results = soup.find_all(text=re.compile('jobmap\[\d\]'))
        pattern = r'jobmap\[\d\](.*?);'
        m= re.findall(pattern,results[0])
        pat2 = r':(.)'''


        for i in range(len(m)):
            tem = re.sub(r'\'','',m[i])
            pat2 = r'jk:(.*?),efccid'
            link = re.findall(pat2,tem)
            pat2 = r'srcname:(.*?),cmp'
            company = re.findall(pat2,tem)
            pat2 = r'loc:(.*?),country'
            location = re.findall(pat2,tem)
            pat2 = r'title:(.*?),locid'
            title = re.findall(pat2,tem)

            if(len(location)!=1 or len(title) !=1 or len(link)!=1 or len(company)!=1):
                Jblink = "www.indeed.com/rc/clk?jk="+link[0].encode('utf-8')
                details=[location,title,Jblink,company]
                addword(problemDict,problemCount,details)
                continue
                problemCount +=1

            else:
                sta = re.split(r'[,]',location[0])

                if(len(sta)!=2):
                    continue

                else:
                    sta = re.split(r'[,]',location[0])
                    jobTitle= title[0].encode('utf-8')
                    link = link[0].encode('utf-8')
                    jobCompany = company[0].encode('utf-8')
                    jobLocation = sta[0].encode('utf-8')
                    jobLocation = jobLocation.strip()
                    jobLocation=jobLocation.lower()
                    jobState=sta[1].encode('utf-8')
                    jobState = re.sub(r'\d','',jobState)
                    jobState = jobState.strip()
                    jobState= jobState.upper()
                    jobTitle = jobTitle.strip()
                    jobTitle=jobTitle.lower()
                    jobLink = "www.indeed.com/rc/clk?jk="+link
                    jobCompany = jobCompany.strip()
                    jobCompany=jobCompany.lower()
                    details = [jobTitle,jobLocation,jobState,jobLink]
                    keyDetails = jobState+jobCompany+jobTitle+jobLocation
                    keyDetails = re.sub(pattern, '', keyDetails)
                    keyDetails = keyDetails.replace(" ","")
                    keyDetails = keyDetails.lower()
                    keyDetails = re.sub(r'[^\w\s]','',keyDetails)
                    addword(companyDict,jobCompany,details)
                    dicto = {jobCompany:details}
                    addword(stateDict,jobState,dicto)
                    dictState = {jobState:dicto}
                    emptyDetails=[]
                    emptyDetails.append(jobLink)
                    emptyDetails.append(details)
                    if keyDetails in indeedDict:
                        if (indeedDict[keyDetails][0]==jobLink):
                            duplicateCount +=1
                            addword(duplicateIndeed,keyDetails,emptyDetails)
                        continue
                    else:
                        addword(indeedDict,keyDetails,emptyDetails)
                        jobsCount+=1

        wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
        time.sleep(wait_time)
        pageNumber+=10

    with open("Indeed-temp.txt", "w") as outfile:
        json.dump(stateDict, outfile,ensure_ascii=False,indent =4)

    with open("Indeed-problem-temp.txt", "w") as outfile:
        json.dump(problemDict, outfile,ensure_ascii=False,indent =4)

    with open("Indeed-complete-temp.txt", "w") as outfile:
        json.dump(indeedDict, outfile,ensure_ascii=False,indent =4)

    with open("Indeed-duplicate-temp.txt", "w") as outfile:
        json.dump(duplicateIndeed, outfile,ensure_ascii=False,indent =4)

    print "Number of states ", len(stateDict), " - Number of companies - ", len(companyDict), " - Number of jobs ",len(indeedDict)," Number of problem jobs",len(problemDict)," Number of Duplicate jobs", len(duplicateIndeed)




def glassdoor():
    stateDict={}
    companyDict= {}
    problemDict={}
    glassdoorDict={}
    duplicateGlassdoor={}
    duplicateCount =0
    jobCount=0
    problemCount = 0
    page_no =1

    review_url="http://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14_IP1.htm"
    more = True
    boo1 = True
    while(more):
        request = urllib2.Request(review_url, headers={'User-Agent' : "Magic Browser"})

        try:
            page = urllib2.urlopen(request)

        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'Failed to reach url'
                print 'Reason: ', e.reason
                sys.exit()
            elif hasattr(e, 'code'):
                if e.code == 404:
                    print 'Error: ', e.code
                    sys.exit()

        content = page.read()
        soup = BeautifulSoup(content,"html5lib")
        link = soup.find('li',{'class':'next'}).findChildren()
        t = re.sub("\<|\>|\"","",str(link[0]))
        pattern = r'a href=(.*?)htm'
        m = re.findall(pattern, t)
        if(len(m)>0):
            link = m[0]
            review_url = "http://www.glassdoor.com/Job/" + str(link)+".htm"

        else:
            more= False
        job = soup.find_all('div', {'class' : 'cf jobScopePanel '})

        for tag in job:
            boo1 = True
            details =tag.findNext('div', {'class' : 'panelHeader'}).findNext('div', {'class' : 'shareJobLink '})
            jobTitle = details.get("data-jobtitle")
            jobid = details.get("data-jobid")
            jobCompany =  tag.get('employername')
            Location =tag.get('location')
            jobLink = "http://www.glassdoor.com/partner/jobListing.htm?jobListingId="+str(jobid)
            jobTitle = jobTitle.encode('utf-8').strip()
            jobCompany = jobCompany.encode('utf-8').strip()
            jobTitle = jobTitle.lower()
            jobCompany = jobCompany.lower()
            Loc2 = Location.split(",")
            if(len(Loc2)==2):
                jobLocation = Loc2[0].encode('utf-8').strip()
                jobState = Loc2[1].encode('utf-8').strip()
                jobLocation = jobLocation.lower()
                jobState = jobState.upper()
            else:
                jobLocation = Loc2[0].encode('utf-8').strip()
                jobState = Loc2[0].encode('utf-8').strip()
                jobLocation = jobLocation.lower()
                jobState = jobState.upper()
                boo1 = False

            details = [jobTitle, jobLocation, jobLink]
            if(boo1):
                addword(companyDict, jobCompany, details)
                dicto = {jobCompany:details}
                addword(stateDict, jobState, dicto)
                keyDetails = jobState + jobCompany + jobTitle + jobLocation
                keyDetails = re.sub(pattern, '', keyDetails)
                keyDetails = keyDetails.replace(" ", "")
                keyDetails = keyDetails.lower()
                keyDetails = re.sub(r'[^\w\s]', '', keyDetails)
                emptyDetails = []
                emptyDetails.append(jobLink)
                emptyDetails.append(details)
                if keyDetails in glassdoorDict:
                    if glassdoorDict[keyDetails][0][0] == jobLink:
                        duplicateCount += 1
                        addword(duplicateGlassdoor, keyDetails, emptyDetails)
                        problemCount += 1
                        continue
                    else:
                        addword(glassdoorDict, keyDetails, emptyDetails)
                        jobCount += 1
                else:
                    addword(glassdoorDict, keyDetails, emptyDetails)
                    jobCount += 1
            else:
                addword(problemDict, jobState, details)
                problemCount += 1

        wait_time = round(max(0, 1 + random.gauss(0, 0.5)), 2)
        time.sleep(wait_time)

        page_no += 1

    with open("glassdoor-state.txt", "w") as outfile:
        json.dump(stateDict, outfile, ensure_ascii=False,indent=4)

    with open("glassdoor-company.txt", "w") as outfile:
        json.dump(companyDict, outfile, ensure_ascii=False,indent=4)

    with open("glassdoor-complete-new.txt", "w") as outfile:
        json.dump(glassdoorDict, outfile, ensure_ascii=False,indent=4)

    with open("glassdoor-duplicates.txt", "w") as outfile:
        json.dump(duplicateGlassdoor, outfile, ensure_ascii=False,indent=4)

    with open("glassdoor-problems.txt", "w") as outfile:
        json.dump(problemDict, outfile, ensure_ascii=False, indent=4)

    print "Number of states ", len(stateDict), " - Number of companies - ", len(companyDict), " - Number of jobs-", len(glassdoorDict), " Number of problem jobs", len(problemDict), " Number of Duplicate jobs", len(duplicateGlassdoor)



def aggregate():

    pattern = re.compile(r'\s+')

    file1 = "SimplyHired-Complete-new.txt"
    file2 = "glassdoor-complete-new.txt"
    file3 = "indeed-complete-temp.txt"
    file4 = "monster-complete-new.txt"
    file5 = "cb-complete-new.txt"

    with open(file1) as json_data:
        simplyH = json.load(json_data)
        json_data.close()

    with open(file2) as json_data:
        gDoor = json.load(json_data)
        json_data.close()

    with open(file3) as json_data:
        indeed = json.load(json_data)
        json_data.close()

    with open(file4) as json_data:
        monster = json.load(json_data)
        json_data.close()

    with open(file5) as json_data:
        cb = json.load(json_data)
        json_data.close()

    master = {}

    # Aggregating all dictionaries
    master.update(simplyH)
    master.update(gDoor)
    master.update(indeed)
    master.update(monster)
    master.update(cb)

    # Final list will contain all job postings
    final =[]
    pro =0

    import csv
    import collections



    # Below code is for generating state level statistics
    jobItems = master.items()
    jobItems.sort(key=lambda x: (x[1][0][1][2]))

    for p in jobItems:
        # State will be present in below location of each item
        state = p[1][0][1][2]
        if (state in USA.keys()):
            final.append(state)
        else:
            pro+=1

    counter = collections.Counter(final)
    # State level statistics will be written to "summary.csv"
    with open('summary.csv','wb') as f:
        w = csv.writer(f)
        w.writerows(counter.items())
print "CareerBuilder"
cb()
print "Monster"
monster()
print "SimplyHired"
#simplyhired()
print "Indeed"
indeed()
print "GlassDoor"
glassdoor()
print "Aggregate"
aggregate()
