from math import ceil
from tkinter import *
import re
import webbrowser
import SearchAndRetrieve as sr

window = Tk()
window.state("zoomed")

def SearchPage():
    pass

def ResultPage():
    results = sr.search_products("wall fan")
    #print(results)
    FlipkartFrame = Frame(window,borderwidth=1,relief=SOLID)
    FlipkartFrame.grid(row=0, column=0, sticky="nsew")
    #FlipkartFrame.pack(side=LEFT,fill=Y)

    AmazonFrame = Frame(window,borderwidth=1,relief=SOLID)
    AmazonFrame.grid(row=0, column=1, sticky="nsew")
    #AmazonFrame.pack(side=RIGHT,fill=Y)

    window.grid_columnconfigure(0, weight=9)
    window.grid_columnconfigure(1, weight=9)

    flpkt = Label(FlipkartFrame, text="FLIPKART")
    flpkt.grid(row=0,column=0)
    

    amzn = Label(AmazonFrame, text="AMAZON")
    amzn.grid(row=0,column=1)


    if results["flipkart"] != None:
        #headers
        pd_title = Label(FlipkartFrame, text="Title")
        pd_price = Label(FlipkartFrame, text="Price")
        pd_discount = Label(FlipkartFrame, text="Discount Price")
        pd_reviews = Label(FlipkartFrame, text="Ratings")
        pd_comments = Label(FlipkartFrame, text="Comments")
        pd_link = Label(FlipkartFrame,text="Product Link")

        pd_title.grid(row=1,column=0)
        pd_price.grid(row=1,column=1)
        pd_discount.grid(row=1,column=2)
        pd_reviews.grid(row=1,column=3)
        pd_comments.grid(row=1,column=4)
        pd_link.grid(row=1,column=5)


        #datas
        for i,flpt_result in enumerate(results["flipkart"], start=2):
            #if i==10:
            #    break
            #title = re.split(pattern = r"[\|\,\(\/\-]",string = flpt_result["title"])[0]
            title = flpt_result["title"].split()[0:4]
            pd_title = Label(FlipkartFrame, text=title)
            pd_price = Label(FlipkartFrame, text=flpt_result["originalPrice"])
            pd_discount = Label(FlipkartFrame, text=flpt_result["discountPrice"])
            pd_rating = Label(FlipkartFrame, text=flpt_result["rating"])
            if flpt_result["comments"] != None:
                cmt = flpt_result["comments"]
                cmnt = "Positive:"+str(ceil(cmt["pos"]))+"  Negative:"+str(ceil(cmt["neg"]))+"  Neutral:"+str(ceil(cmt["neu"]))
                pd_comments = Label(FlipkartFrame, text=cmnt)
            else:
                pd_comments = Label(FlipkartFrame, text="No Comments")
            pd_link = Label(FlipkartFrame, text="Product", fg="blue", cursor="hand2")
            pd_link.bind("<Button-1>", lambda e,link=flpt_result["productUrl"]: webbrowser.open(link))
            print(flpt_result["productUrl"])

            pd_title.grid(row=i,column=0)
            pd_price.grid(row=i,column=1)
            pd_discount.grid(row=i,column=2)
            pd_rating.grid(row=i,column=3)
            pd_comments.grid(row=i,column=4)
            pd_link.grid(row=i,column=5)

            pd_title.grid_columnconfigure(0, weight=1)
            pd_price.grid_columnconfigure(1, weight=1)
            pd_discount.grid_columnconfigure(2, weight=1)
            pd_rating.grid_columnconfigure(3, weight=1)
            pd_comments.grid_columnconfigure(4, weight=1)
            pd_link.grid_columnconfigure(5, weight=1)

    else:
        pass

    if results["amazon"] != None:
        #headers
        pd_title = Label(AmazonFrame, text="Title")
        pd_price = Label(AmazonFrame, text="Price")
        pd_discount = Label(AmazonFrame, text="Discount Price")
        pd_reviews = Label(AmazonFrame, text="Ratings")
        pd_comments = Label(AmazonFrame, text="Comments")
        pd_link = Label(AmazonFrame,text="Product Link")


        pd_title.grid(row=1,column=0)
        pd_price.grid(row=1,column=1)
        pd_discount.grid(row=1,column=2)
        pd_reviews.grid(row=1,column=3)
        pd_comments.grid(row=1,column=4)
        pd_link.grid(row=1,column=5)

        #datas
        for i,amzn_result in enumerate(results["amazon"],start=2):
            #if i==10:
            #    break
            #title = re.split(pattern = r"[\|\,\(\/\-]",string = amzn_result["title"])[0]
            title = amzn_result["title"].split()[0:4]
            pd_title = Label(AmazonFrame, text=title)
            pd_price = Label(AmazonFrame, text=amzn_result["originalPrice"])
            pd_discount = Label(AmazonFrame, text=amzn_result["discountPrice"])
            pd_rating = Label(AmazonFrame, text=amzn_result["rating"])
            if amzn_result["comments"] != None:
                cmt = amzn_result["comments"]
                cmnt = "Positive:"+str(ceil(cmt["pos"]))+"  Negative:"+str(ceil(cmt["neg"]))+"  Neutral:"+str(ceil(cmt["neu"]))
                pd_comments = Label(AmazonFrame, text=cmnt)
            else:
                pd_comments = Label(AmazonFrame, text="No Comments")
            pd_link = Label(AmazonFrame, text="Product", fg="blue", cursor="hand2")
            pd_link.bind("<Button-1>", lambda e,link=amzn_result["productUrl"]: webbrowser.open(link))


            pd_title.grid(row=i,column=0)
            pd_price.grid(row=i,column=1)
            pd_discount.grid(row=i,column=2)
            pd_rating.grid(row=i,column=3)
            pd_comments.grid(row=i,column=4)
            pd_link.grid(row=i,column=5)

            pd_title.grid_columnconfigure(0, weight=1)
            pd_price.grid_columnconfigure(1, weight=1)
            pd_discount.grid_columnconfigure(2, weight=1)
            pd_rating.grid_columnconfigure(3, weight=1)
            pd_comments.grid_columnconfigure(4, weight=1)
            pd_link.grid_columnconfigure(5, weight=1)
    else:
        pass


if __name__ == "__main__":
    ResultPage()
    window.mainloop()