import requests
from bs4 import BeautifulSoup
import winsound
import tkinter as tk
from tkinter import messagebox, PhotoImage
import webbrowser
import pyautogui
from PIL import Image
import time
import smtplib


def sendEmail(b):
    gmail_user = 'sender email'
    gmail_password = 'password'

    sent_from = gmail_user
    to = "recipient email"
    subject = 'NEW LISTING'
    body = b

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)


url = 'https://www.ebay.com/sch/i.html?_nkw='

item = input("Enter the item you would like to search for: ").strip()

global new_listings
new_listings = []
global previous_listings
previous_listings = []
response = requests.get(url + item+"&_ipg=240&_sop=10")
soup = BeautifulSoup(response.text, 'html.parser')

listings = soup.find_all("span", {"role": "heading", "aria-level": "3"})
if listings:
    for listing in listings[1:3]:
        previous_listings.append(listing.get_text())


def scrape():
    try:
        response = requests.get(url + item+"&_ipg=240&_sop=10")
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all(
            "span", {"role": "heading", "aria-level": "3"})

        if listings:
            for listing in listings[1:3]:
                global new_listings
                global previous_listings
                new_listings.append(listing.get_text())
            if new_listings != previous_listings:
                print("Something supposedly got listed now!")
                print("NEW✔️ "+new_listings[0])
                sendEmail(new_listings[0].encode('utf-8'))
                winsound.Beep(2500, 500)
            previous_listings.clear()
            for i in new_listings:
                previous_listings.append(i)
            new_listings.clear()

        else:
            messagebox.showinfo("Error", "No listing found for " + item)
    except requests.exceptions.RequestException as e:
        messagebox.showinfo(
            "Error", "Error while trying to connect to eBay: " + str(e))
    except Exception as e:
        messagebox.showinfo("Error", "An error has occurred: " + str(e))


while True:
    scrape()
    time.sleep(30)
    print("Scraping NOW!")
    print(previous_listings)
    print("")
