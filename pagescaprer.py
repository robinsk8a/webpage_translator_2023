import os
import shutil
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import translators.server as tss



class pageScraper:
    
    # First we install the webdriver and get in the url
    # We put aditional options in the chrome driver to make the process headless
    
    

    def __init__(self, url= str, path_name= str, file_name= str, scroll_iter: int= 0):
        # This initial statement sort the necesary values to work with this class
        self.url = url
        self.path= f"{path_name}"
        self.file= f"{file_name}.html"
        self.full_path= f"./{path_name}/{file_name}.html"
        self.scroll= scroll_iter
        
    
    def chrome_driver_init(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
        driver.get(self.url)
        driver.page_source
        for i in range(int(self.scroll)):
            driver.execute_script("window.scrollBy(0,500)","")
            driver.implicitly_wait(3)
            time.sleep(1)
            i+=1
        
        
        html = driver.page_source
        html.encode('utf-8')
        time.sleep(2)
        driver.close()
        return html
    
    def get_html(self):
        
        print(">>> Extracting html...\n")
        # # Now we store the html source code into a html variable for later uses 
        html= self.chrome_driver_init()
        
        # We parse the information
        soup= BeautifulSoup(html, "html.parser")
        
        # We create the container folder
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            with open(os.path.join(self.path, self.file), "w") as f:
                f.write(str(soup))
                
    
        print(f"Your html file is store in the {self.path} folder:\n >>> File path:  {self.full_path}  <<<")

    
    # This is a method to reset an entire directory or path.
    # This method deletes the whole thing starting from the folder path and replace it with a brand new one
    # use with caution
    def reset_dir(self):
        try:
            print(">>> Reseting...")
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
                self.get_html()
                print(f">>> {self.path} Correctly reset")
            else:
                self.get_html()
                print(f">>> New path created on: {self.path}")
        except ValueError:
            raise ValueError(f">>> {self.path} not found. Please review your path or try other method.")
    
            
    # This method search into an html file the links asociated with it and returns in the 
    def get_js(self, sub_dic= str):      
        # If we have an extra route for our .js files, we create the new directory
        if sub_dic != "" and not os.path.exists(f"{self.path}/{sub_dic}"):
            os.mkdir(f"{self.path}/{sub_dic}")
        
        js_files = []
        
        # Now we open the file we already created and access to the information
        with open(f"{self.path}/{self.file}", "r") as Sp:
            soup = BeautifulSoup(Sp, 'html.parser')
            
        # Looking for .js file links
        for script in soup.find_all("script"):
            if script.attrs.get("src"):
            
                url_src = script.attrs.get("src")
                js_files.append(url_src)      
        
        # Now we scrape for the each code of our .js files in the html given path
        print(F">>> Process start: Getting .js files...")
        for link in js_files:
            if link.startswith("//") or link.startswith("https"):
                pass
            else:
                print(link)
                
                html= self.chrome_driver_init(url=f"{self.url}{link}")               
                soup = BeautifulSoup(html,'lxml')
                js = soup.find('pre').text
                
                file_path= link.replace(f"{sub_dic}", "")
                with open(f"{self.path}/{sub_dic}{file_path}", "w") as fi:
                    fi.write(js)
        print(f">>>Process firished")

    def get_js_html(self, sub_dic= str, ):
        
        # If we have an extra route for our .js files, we create the new directory
        if sub_dic != "" and not os.path.exists(f"{self.path}/{sub_dic}"):
            os.mkdir(f"{self.path}/{sub_dic}")
        
        js_files = []
        
        # Now we open the file we already created and access to the information
        with open(f"{self.path}/{self.file}", "r") as Sp:
            soup = BeautifulSoup(Sp, 'html.parser')
        
        
        for script in soup.find_all("script"):
            if script.attrs.get("src"):
            
                # if the tag has the attribute
                # 'src'
                url_src = script.attrs.get("src")
                js_files.append(url_src)
        
        
        print(F">>> Process start: Getting .js files...")
        for link in js_files:
            if link.startswith("//") or link.startswith("https"):
                pass
            else:
                print(link)
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= options)
                driver.get(url=f"{self.url}{link}")

                html = driver.page_source
                
                time.sleep(2)
                driver.close()
                soup = BeautifulSoup(html,'lxml')
                soup.encode('utf-8')
                
                # This part changes with the previous one
                file_path= link.replace(f"{sub_dic}", "")
                with open(f"{self.path}/{sub_dic}{file_path}.html", "w") as fi:
                    fi.write(str(soup))


    def get_css(self):
        # Let's open the html file to get soup from source
        with open(f"{self.path}/{self.file}", "r") as Sp:
            soup = BeautifulSoup(Sp, 'html.parser')
        
        # Looking for css files
        css_files = []
        for css in soup.find_all("link"):
            if css.attrs.get("href"):
                
                print(css)
                # if the link tag has the 'href'
                # attribute
                url = css.attrs.get("href")
                css_files.append(url)
        
        # Scraping each css file
        print(F">>> Process start: Getting .css files...")
        for link in css_files:
            if link.startswith("//") or link.startswith("https"):
                pass
            else:
                print(link)
                
                html= self.chrome_driver_init(url=f"{self.url}{link}")               
                soup = BeautifulSoup(html,'lxml')
                css = soup.find('pre').text
                
                with open(f"{self.path}{link}", "w") as fi:
                    fi.write(css)
        print(f">>>Process firished")
        
    def get_links(self, link_tag= str, attrs_tag= str):
        
        with open(self.full_path) as Sp:
            soup= BeautifulSoup(Sp, 'html.parser')
        
        links= []
        
        for link_path in soup.find_all(link_tag):
            if link_path.attrs.get(attrs_tag):
                links.append(link_path.attrs.get(attrs_tag))    
        return links
        
    def link_complete(self, link_list, internal_dir= bool):
        
        print(">>> Getting full link...")
        for link in link_list:
            
            if link.startswith("//") or link.startswith("https") or link.startswith("http"):
                pass
            else:
                def completing_link(new_link):
                    with open(f"{self.full_path}", 'r') as f:
                        file = f.read()
                        #new_link= link.replace("/", "", 1)
                        complete = file.replace(f'\"{link}\"', f'\"{self.url}{new_link}\"')
                    print(f'\"{self.url}{new_link}\"')
                    with open(f"{self.full_path}", 'w') as f:
                        f.write(complete)

                print(link)
                
                if internal_dir == True:
                    new_link= link
                    completing_link(new_link)
                else:
                    new_link= link.replace("/", "", 1)
                    completing_link(new_link)
        print(">>> Process complete")

    def translateByTag(self, lang_in=str, lang_out=str, container_tag=str):
        
        # We use in and out lang parameters to specify the type of translation we want
        # Aditionaly we use a tag container to clarify the function the type of tag it needs to search in
        with open(f"{self.full_path}", "r") as Sp:
            soup = BeautifulSoup(Sp, 'html.parser')
            
            print(">>> Starting translation...")
            for text in soup.find_all(container_tag):
                
                if text.string != None:
                    # We get the attribute "string" with the bs4 lib
                    # We translateByTag it with google translateByTag and replace the original with the translation
                    inner_text= text.string
                    print(inner_text)
                    translateByTag = tss.google(inner_text, lang_in, lang_out)
                    inner_text.replace_with(translateByTag)
                    print(translateByTag)
            
                    with open(f"{self.full_path}", 'w') as f:
                        f.write(str(soup))  
                      
            print(">>> Translation finished")

    def translation(self, lang_in=str, lang_out=str):
        
        print(">>> Starting translation...")
        with open(f"{self.full_path}", "r") as Sp:
            soup = BeautifulSoup(Sp, 'html.parser')
        body_soup= soup.find('body')
        #print(body_soup)
        body_soup= BeautifulSoup(str(body_soup), 'html.parser')
        visible_text= []
        out_soup= str(soup)
        
        
        for string in body_soup.stripped_strings:
            translateByTag = tss.google(string, lang_in, lang_out)
            print(string)
            print(translateByTag)
            
            pattern= fr">[\n|\s]*?{string}[\n|\s]*<"
            matches= re.findall(pattern, str(body_soup))
            
            for match in matches:
                if re.search(match, str(body_soup)):
                    
                    match_alter= re.sub(string, translateByTag, match)
                    out_soup= re.sub(match, match_alter, out_soup)
                    
                    with open(self.full_path,'w') as Ns:
                        Ns.write(out_soup)
                
        print(">>> Translation finished")

                
                        



#print(f"{page1.url}\n{page1.path}\n{page1.file}\n{page1.full_path}")
#page1.get_html()
#page1.reset_dir()
#page1.get_js("/webpack")
#page1.get_css()
# links_link= page1.get_links(link_tag= "link", attrs_tag= "href")
# links_a= page1.get_links(link_tag= "a", attrs_tag= "href")
# links_js= page1.get_links(link_tag= "script", attrs_tag= "src")
# page1.link_complete(link_list=links_link, internal_dir= False)
# page1.link_complete(link_list=links_a, internal_dir= False)
# page1.link_complete(link_list=links_js, internal_dir= True)
# page1.translateByTag(lang_in='en', lang_out='hi', container_tag="a")
# page1.translateByTag(lang_in='en', lang_out='hi', container_tag="p")
# page1.translateByTag(lang_in='en', lang_out='hi', container_tag="h2")
# page1.translateByTag(lang_in='en', lang_out='hi', container_tag="h3")
# page1.translateByTag(lang_in='en', lang_out='hi', container_tag="span")
# page1.translateByTag(lang_in='en', lang_out='hi', container_tag="")


url= "https://www.classcentral.com/"
path= './classcentralcopy'
file= "index"
scroll= 10
page1= pageScraper(url, path, file, scroll)

def index_translate(page):
    page.get_html()
    links_link= page.get_links(link_tag= "link", attrs_tag= "href")
    links_a= page.get_links(link_tag= "a", attrs_tag= "href")
    links_js= page.get_links(link_tag= "script", attrs_tag= "src")
    page.link_complete(link_list=links_link, internal_dir= False)
    page.link_complete(link_list=links_a, internal_dir= False)
    page.link_complete(link_list=links_js, internal_dir= True)
    page.translation(lang_in='en', lang_out='hi')
    #page.translateByTag(lang_in='en', lang_out='hi', container_tag="a")
    page.translateByTag(lang_in='en', lang_out='hi', container_tag="h3")

def first_level():
    link_to_path= {}
    com_links_a= page1.get_links(link_tag= "a", attrs_tag= "href")
    counter=0
    scroll= page1.scroll
    path = f"classcentralcopy/level"
    print(path)
    print(">>> Begining multilink processing...")
    for link in com_links_a:
        if link != page1.url:
            counter+=1
            file= f"levelone_{counter}"
            full_p=f"{path}/{file}.html"
            if os.path.exists(full_p):
                pass
            else:
                try:
                    link_to_path[link]= f"{file}.html"
                    
                    page1_lv1= pageScraper(link, path, file, scroll)
                    index_translate(page1_lv1)
                except:
                    link_to_path[link]= f"Error: File number: {counter}"
        
        for item in link_to_path:
            if link_to_path[item].startswith("Error:"):
                print(f"Error: \n >>> {item} ----> {link_to_path[item]}")
    
    print(">>> Multilink processig finished")
    with open(f"{link_to_path}.txt", "w") as links:
        links.write(link_to_path)
    return link_to_path  
    
    
new_linkpaths= first_level()
# print(page1.url)
# print(page1.path)
# print(page1.file)