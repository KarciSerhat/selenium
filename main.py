from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import tkinter as tk
from tkinter import ttk

def twitterLogin (username, password):
    try:
        driver = webdriver.Chrome()
        
        # Twitter'a giriş yapma
        driver.get("https://twitter.com/login")
        time.sleep(2)  # Sayfanın tam olarak yüklenmesini beklemek için bekleme
        username_field = driver.find_element("xpath", "//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")
        username_field.send_keys(username)

        first_post_like_button = driver.find_element("xpath", "//div[@class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu']")
        first_post_like_button.click()
        
        time.sleep(2)

        password_field = driver.find_element("xpath", "//input[@type='password']")
        password_field.send_keys(password)

        first_post_like_button = driver.find_element("xpath", "//div[@data-testid='LoginForm_Login_Button']")
        first_post_like_button.click()
        time.sleep(2)

        # İsim araması yapma
        search_box = driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']")
        search_box.send_keys("erden timur")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Arama sonuçlarının yüklenmesi için bekleme

        peopleTab = driver.find_element("xpath", "//a[@href='/search?q=erden%20timur&src=typed_query&f=user']")
        peopleTab.click()
        time.sleep(2)


        file = open("begenilen_postlar.txt", "w")

        elements = driver.find_elements("xpath", "//div[@data-testid='cellInnerDiv']")

        if elements:
            first_element = elements[0]
            first_element.click()
        time.sleep(6)
            
        # Sayfanın tamamen yüklenmesini bekleme
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(("xpath", "//div[@data-testid='like']")))

        count = 0
        while count < 10:
            posts = driver.find_elements("xpath", "//div[@data-testid='like']")
            if count >= len(posts):
                break
            
            post = posts[count]
            
            # Tıklanabilir hale gelene kadar kaydırma
            while not post.is_displayed():
                driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(3)
            
            # Tıklama işlemi
            try:
                post.click()
            except:
                # Eğer tıklama engellenirse bir sonraki posta geç
                count += 1
                continue
            
            time.sleep(2)
            
            # Post bilgilerini alıp dosyaya yazma
            post_text = post.text
            post_link = post.get_attribute("href")
            file.write(f"Post Metni: {post_text}\n")
            file.write(f"Post Linki: {post_link}\n")
            file.write(f"Post Data: {count}\n")
            file.write("--------------------\n")

            count += 1
    except Exception as e:
        print(f"Hata: {str(e)}")

    finally:
        # WebDriver'ı kapatma
        driver.quit()

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Kullanıcı adı ve şifreyi kullanarak giriş işlemini gerçekleşti

    twitterLogin(username, password)
    # Giriş işleminden sonra giriş alanlarını temizleme
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
def close_window():
    # Arayüzü kapatma
    window.destroy()

# Pencere oluşturma
window = tk.Tk()
window.title("Twitter Login")

# Pencere boyutunu ayarlama
window.geometry("400x400")  # Genişlik: 300 piksel, Yükseklik: 200 piksel

# Kullanıcı adı etiketi ve giriş alanı
label_username = ttk.Label(window, text="Kullanıcı Adı:")
label_username.pack(pady=10)
entry_username = ttk.Entry(window, width=30)
entry_username.pack()

# Şifre etiketi ve giriş alanı
label_password = ttk.Label(window, text="Şifre:")
label_password.pack(pady=10)
entry_password = ttk.Entry(window, show="*", width=30)
entry_password.pack()

# Giriş yap butonu
button_login = ttk.Button(window, text="Giriş Yap", command=login)
button_login.pack(pady=20)

button_close = ttk.Button(window, text="Kapat", command=close_window)
button_close.pack()

# Pencereyi çalıştırma döngüsü
window.mainloop()

