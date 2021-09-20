from http.client import OK
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from PIL import Image,ImageTk
import time
import tkinter
import urllib.request
import os

from selenium.webdriver.support.wait import IGNORED_EXCEPTIONS
from comment import Comment,Post
comments_to_delete = []


def startup(driver, username, pwd):
    driver.get("https://www.instagram.com")

    #gives time for page to load
    WebDriverWait(driver,15).until(EC.presence_of_element_located((By.NAME,"username")))

    #finding the elements
    username_input = driver.find_element_by_name("username")
    pwd_input = driver.find_element_by_name("password")
    #login_button = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")

    #sending the input and logging in
    username_input.send_keys(username)
    pwd_input.send_keys(pwd)
    #login_button.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    #time.sleep(5)
    #clear pop ups
   #WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME,"aOOlW   HoLwm ")))
    #not_now_button = driver.find_element_by_class_name("aOOlW   HoLwm ").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

    #time.sleep(20)
    #WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.XPATH,"/html/body/div[6]/div/div/div")))
    #time.sleep(5)
    #WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div/div[3]/button[2]")))
    #not_now_button = driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    
    #getting to user's page
    driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div/div[2]/div[1]/div/div/a").click()
    time.sleep(3)
    #getting the posts
    posts = get_posts(driver)
    
    #if no posts
    if (len(posts) == 0):
        print("no posts available") #TODO change to a pop up
        return posts
    

    build_gui(driver,posts)
    return posts
        

def add_to_list(top,text):
   comments_to_delete.append(text)
   entry.delete
   
def get_posts(driver):
    posts = []
    links_of_posts = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//a[starts-with(@href,'/p/')]")))
    # gets all elements with tag a and puts them in a list
    #links_of_posts = driver.find_elements_by_class_name('eLAPa')
    if len(links_of_posts) == 0:
        return
    for links in links_of_posts:
        links = links.get_attribute('href')
        post = Post()
        post.link = links
        #if hasattr(links,'href'):   #ERROR: no elements successfully enter the if, removing the if causes a stale element reference exception
            #post.link = links.get_attribute('href')
           # if '/p/' in post.link:
        posts.append(post)
    
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"FFVAD")))
    post_images = driver.find_elements_by_class_name("FFVAD")
    i = 0
    for i in range(0,len(post_images)):
        post_images[i] = post_images[i].get_attribute('src')
    a = 0
    b = 0    
    while a < len(posts) and b < len(post_images):
        shortcode = str(a) #posts[a].link.split("/")[-2] #singles out the url of post
        if os.path.exists(shortcode + '.jpg'):
            posts[a].image_loc = shortcode + '.jpg'
            a += 1
            b += 1
            continue
        else:
            urllib.request.urlretrieve(post_images[b], '{}.jpg'.format(shortcode))
            posts[a].image_loc = shortcode + ".jpg"
            a += 1
            b += 1
    return posts            


def build_gui(driver,posts):
    top = tkinter.Tk()
    top.title("Choose the post")
    prompt = tkinter.Label(text="Please select the post you would like to delete comments from: \n ")
    #prompt.grid(row = 0, column = 1,rowspan = len(posts)*2, columnspan = 6)
    i = 1
    for post in posts:
        #path = "" #/Users/arnavkolli/Desktop/practics/" 
        path = post.get_image()
        im = Image.open(path)
        newsize=(100,100)
        im = im.resize(newsize)
        ph = ImageTk.PhotoImage(im)
        btn = tkinter.Button(top, image = ph, command = lambda:[check_comments(driver,post),top.destroy])
        btn.image = ph
        btn.pack()
        #btn.grid(row = i, column =3)
        i += 2
    top.mainloop()
    return posts

def check_comments(driver,post):
    driver.get(post.link)
    
    return 

driver = webdriver.Chrome("/Library/Frameworks/Python.framework/chromedriver")
posts =[]
top = tkinter.Tk()
top.title("InstaBot")
top.geometry("300x300")
l1 = tkinter.Label(top,text="please enter all the blocked words")
entry = tkinter.Entry(top)
btn1 = tkinter.Button(top,text = "add",command = add_to_list(top,entry.get()))
btn2 = tkinter.Button(top, text = "done", command = top.destroy)
l1.grid(column = 1)
entry.grid(row = 1, column = 1)
btn1.grid(row=2)
btn2.grid(row=2, column = 1)
top.mainloop()
try:
    posts = startup(driver,"definitelynotbot24","**D8$(ph~Cx&k3f")

except TimeoutException:
    top = tkinter.Tk()
    top.title("ERROR")
    l2 = tkinter.Label(text = "wifi might be slow.. please try again")
    b1 = tkinter.Button(top,text = "OK", command = top.destroy, fg="#0000FF")
    l2.pack()
    b1.pack()
    top.destroy
    top.mainloop()

#except :
 #   top = tkinter.Tk()
  #  top.title("ERROR")
   # l1 = tkinter.Label(text = "run into an error")
    #b1 = tkinter.Button(top,text = "OK", command = top.quit())
    #l1.pack()
    #b1.pack()

finally :   
    #clear all the downloaded documents
    for post in posts:
        filepath = "/Users/arnavkolli/Desktop/practics/" + post.get_image()
        os.rmdir(filepath)
    driver.quit()

