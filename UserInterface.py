from tkinter import *
import re
import SearchAndRetrieve as sr

window = Tk()
window.state("zoomed")

def SearchPage():
    pass

def ResultPage():
    results = sr.search_products("samsung s22")
    #print(results)
    FlipkartFrame = Frame(window,borderwidth=2,relief=SOLID)
    FlipkartFrame.grid(row=0, column=0, sticky="nsew")
    #FlipkartFrame.pack(side=LEFT,fill=Y)

    AmazonFrame = Frame(window,borderwidth=2,relief=SOLID)
    AmazonFrame.grid(row=0, column=1, sticky="nsew")
    #AmazonFrame.pack(side=RIGHT,fill=Y)

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    flpkt = Label(FlipkartFrame, text="FLIPKART")
    amzn = Label(AmazonFrame, text="AMAZON")
    flpkt.grid(row=0,column=0)
    amzn.grid(row=0,column=1)

    if True:
        pd_url = Label(FlipkartFrame, text="URL")
        pd_title = Label(FlipkartFrame, text="Title")
        pd_price = Label(FlipkartFrame, text="Price")
        pd_discount = Label(FlipkartFrame, text="Discount Price")
        pd_reviews = Label(FlipkartFrame, text="Reviews")
        pd_url.grid(row=1,column=0)
        pd_title.grid(row=1,column=1)
        pd_price.grid(row=1,column=2)
        pd_discount.grid(row=1,column=3)
        pd_reviews.grid(row=1,column=4)
    else:
        pass

    if True:
        #headers
        pd_title = Label(AmazonFrame, text="Title")
        pd_price = Label(AmazonFrame, text="Price")
        pd_discount = Label(AmazonFrame, text="Discount Price")
        pd_reviews = Label(AmazonFrame, text="Reviews")

        pd_title.grid(row=1,column=0)
        pd_price.grid(row=1,column=1)
        pd_discount.grid(row=1,column=2)
        pd_reviews.grid(row=1,column=3)

        #datas
        for i,amzn_result in zip(range(2,10), results["amazon"]):
            title = re.split(pattern = r"[\|\,]",string = amzn_result["title"])[0]
            pd_title = Label(AmazonFrame, text=title)
            pd_price = Label(AmazonFrame, text=amzn_result["originalPrice"])
            pd_discount = Label(AmazonFrame, text=amzn_result["discountPrice"])
            pd_rating = Label(AmazonFrame, text=amzn_result["rating"])

            pd_title.grid(row=i,column=0)
            pd_price.grid(row=i,column=1)
            pd_discount.grid(row=i,column=2)
            pd_rating.grid(row=i,column=3)

            pd_title.grid_columnconfigure(0, weight=1)
            pd_price.grid_columnconfigure(1, weight=1)
            pd_discount.grid_columnconfigure(2, weight=1)
            pd_rating.grid_columnconfigure(3, weight=1)


if __name__ == "__main__":
    ResultPage()
    window.mainloop()