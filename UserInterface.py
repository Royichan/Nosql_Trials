import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
import SearchAndRetrieve as sr
from math import ceil
import webbrowser

class ProductSearch(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        # application variables
        self.term_var = ttk.StringVar(value='')
        # header and labelframe option container
        option_text = "Enter Product Name"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_term_row()
        self.create_results_view()

    def create_term_row(self):
        """Add term row to labelframe"""
        term_row = ttk.Frame(self.option_lf)
        term_row.pack(fill=X, expand=YES, pady=5)
        term_lbl = ttk.Label(term_row, text="Product", width=8)
        term_lbl.pack(side=LEFT, padx=(15, 0))
        term_ent = ttk.Entry(term_row, textvariable=self.term_var)
        term_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        search_btn = ttk.Button(
            master=term_row, 
            text="Search", 
            command=self.on_search, 
            bootstyle=OUTLINE, 
            width=8
        )
        search_btn.pack(side=LEFT, padx=5)

    def openweb(self,event):
        item = event.widget.focus()
        row = event.widget.index(item)
        if results['flipkart'] != None and results['amazon'] != None:
            webbrowser.open_new_tab(results['flipkart'][row]["productUrl"])
            webbrowser.open_new_tab(results['amazon'][row]["productUrl"])
        elif results['flipkart'] == None and results['amazon'] != None:
            webbrowser.open_new_tab(results['amazon'][row]["productUrl"])
        elif results['flipkart'] != None and results['amazon'] == None:
            webbrowser.open_new_tab(results['flipkart'][row]["productUrl"])
        else:
            pass

    def create_results_view(self):
        """Add result treeview to labelframe"""
        self.Tree = ttk.Treeview(
            master=self, 
            bootstyle=PRIMARY, 
            columns=("FlipkartProduct","FlipkartPrice","FlipkartDiscountPrice","FlipkartRatings","FlipkartComments",
                               "AmazonProduct","AmazonPrice","AmazonDiscountPrice","AmazonRatings","AmazonComments"),
            show=HEADINGS,
            height=40,
            padding=(2),
        )
        
        # setup columns and use `scale_size` to adjust for resolution
        self.Tree.column("FlipkartProduct",anchor=W,stretch=YES)
        self.Tree.column("FlipkartPrice",anchor=W,width=100)
        self.Tree.column("FlipkartDiscountPrice",anchor=W,width=130)
        self.Tree.column("FlipkartRatings",anchor=W,width=120)
        self.Tree.column("FlipkartComments",anchor=W,stretch=YES)
        self.Tree.column("AmazonProduct",anchor=W,stretch=YES)
        self.Tree.column("AmazonPrice",anchor=W,width=100)
        self.Tree.column("AmazonDiscountPrice",anchor=W,width=130)
        self.Tree.column("AmazonRatings",anchor=W,width=120)
        self.Tree.column("AmazonComments",anchor=W,stretch=YES)

        self.Tree.heading("FlipkartProduct",text="Flipkart Product",anchor=W)
        self.Tree.heading("FlipkartPrice",text="Flipkart Price",anchor=W)
        self.Tree.heading("FlipkartDiscountPrice",text="Flipkart Discount Price",anchor=W)
        self.Tree.heading("FlipkartRatings",text="Flipkart Ratings",anchor=W)
        self.Tree.heading("FlipkartComments",text="Flipkart Reviews",anchor=W)
        self.Tree.heading("AmazonProduct",text="Amazon Product",anchor=W)
        self.Tree.heading("AmazonPrice",text="Amazon Price",anchor=W)
        self.Tree.heading("AmazonDiscountPrice",text="Amazon Discount Price",anchor=W)
        self.Tree.heading("AmazonRatings",text="Amazon Ratings",anchor=W)
        self.Tree.heading("AmazonComments",text="Amazon Reviews",anchor=W)

        self.Tree.bind('<Double-1>', self.openweb)

        self.Tree.pack(fill=BOTH, expand=YES,pady=10)

    def insert_rows(self, results):
        """Insert new row in tree search results"""
        if results["flipkart"] != None and results["amazon"] != None:
            for i,(flpt_result,amzn_result) in enumerate(zip(results["flipkart"],results["amazon"]), start=1):
                if flpt_result["comments"] != None:
                    cmt = flpt_result["comments"]
                    cmnt = "Pos - "+str(ceil(cmt["pos"]))+",  Neg - "+str(ceil(cmt["neg"]))+",  Neu - "+str(ceil(cmt["neu"]))
                else:
                    cmnt = "No Reviews"

                if amzn_result["comments"] != None:
                    cmt1 = amzn_result["comments"]
                    cmnt1 = "Pos - "+str(ceil(cmt1["pos"]))+",  Neg - "+str(ceil(cmt1["neg"]))+",  Neu - "+str(ceil(cmt1["neu"]))
                else:
                    cmnt1 = "No Reviews"

                self.Tree.insert(
                    parent="",
                    index="end",
                    iid=i,
                    values=(
                    flpt_result["title"].split()[0:4],flpt_result["originalPrice"],flpt_result["discountPrice"],flpt_result["rating"],cmnt,
                    amzn_result["title"].split()[0:4],amzn_result["originalPrice"],amzn_result["discountPrice"],amzn_result["rating"],cmnt1)
                    )
        elif results["flipkart"] != None and results["amazon"] == None:
            for i,flpt_result in enumerate(results["flipkart"], start=1):
                if flpt_result["comments"] != None:
                    cmt = flpt_result["comments"]
                    cmnt = "Pos - "+str(ceil(cmt["pos"]))+",  Neg - "+str(ceil(cmt["neg"]))+",  Neu - "+str(ceil(cmt["neu"]))
                else:
                    cmnt = "No Reviews"

                self.Tree.insert(
                    parent="",
                    index="end",
                    iid=i,
                    values=(
                    flpt_result["title"].split()[0:4],flpt_result["originalPrice"],flpt_result["discountPrice"],flpt_result["rating"],cmnt,
                    "None","None","None","None","None")
                    )
        elif results["flipkart"] == None and results["amazon"] != None:
            for i,amzn_result in enumerate(results["amazon"], start=1):
                if amzn_result["comments"] != None:
                    cmt = amzn_result["comments"]
                    cmnt = "Pos - "+str(ceil(cmt["pos"]))+",  Neg - "+str(ceil(cmt["neg"]))+",  Neu - "+str(ceil(cmt["neu"]))
                else:
                    cmnt = "No Reviews"

                self.Tree.insert(
                    parent="",
                    index="end",
                    iid=i,
                    values=(
                    "None","None","None","None","None",
                    amzn_result["title"].split()[0:4],amzn_result["originalPrice"],amzn_result["discountPrice"],amzn_result["rating"],cmnt)
                    )
        else:
            self.Tree.insert(
                    parent="",
                    index="end",
                    iid=1,
                    values=(
                    "None","None","None","None","None",
                    "None","None","None","None","None",)
                    )

    def on_search(self):
        """Search for a term based on the search type"""
        search_term = self.term_var.get()
        if search_term == '':
            return
        else:
            self.Tree.delete(*self.Tree.get_children())
            global results
            results = sr.search_products(search_term)
            self.insert_rows(results)

if __name__ == '__main__':
    app = ttk.Window("Product Search", "journal")
    app.state("zoomed")
    ProductSearch(app)
    app.mainloop()