from idlelib.zoomheight import set_window_geometry

import matplotlib.pyplot as plt
import logging as log
import pandas as pd


log.basicConfig(
    level=log.INFO,
    format='%(asctime)s | %(filename)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Cleaner():


    def __init__(self):
        self.df = pd.read_csv("superstore.csv")
        self.before_cleaning = {}
        self.after_cleaning = {}


    def get_insights(self):
        duplicate_columns = int(self.df.duplicated("Order ID").sum())
        self.before_cleaning = {
            "duplicates" : duplicate_columns,
            "rows": len(self.df),
            "columns" : len(self.df.columns),
            "Total Null Values" : self.df.isnull().sum()
        }
        return self.before_cleaning


    def cleaning_data(self):
        # Cleaning Column
        self.df.columns = self.df.columns.str.strip() # This removes the spacng from sides
        self.df.columns = self.df.columns.str.lower().str.replace(" ","-") # this adds the '-' on the column name if there is a space

        # Removing duplicates
        self.df = self.df.drop_duplicates(subset=["order-id"])

        self.df["order-date"] = pd.to_datetime(self.df["order-date"],  format="%d/%m/%Y", dayfirst=True)
        self.df["ship-date"] = pd.to_datetime(self.df["ship-date"],   format="%d/%m/%Y", dayfirst=True)



    def get_after_insights(self):
        duplicate_columns = int(self.df.duplicated("order-id").sum())

        self.after_cleaning = {
                "duplicates": duplicate_columns,
                "rows": len(self.df),
                "columns": len(self.df.columns),
                "Total Null Values": self.df.isnull().sum()
            }
        return self.after_cleaning


    def graph_analysis(self):
        sales_by_subcatagory = self.df.groupby("category")["sales"].sum().sort_values(ascending=False).head()
        sales_by_subcatagory.plot(kind="barh", color="green")
        plt.title("Top 5 Category By Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("graph/top_category_by_sales_chart.png")

        top_regions_by_sales =  self.df.groupby("region")["sales"].sum().sort_values(ascending=False).head()
        top_regions_by_sales.plot(kind="barh", color="green")
        plt.title("Top 5 Category By Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("graph/top_regions_by_sales_chart.png")

        top_subcategory_by_sales =  self.df.groupby("sub-category")["sales"].sum().sort_values(ascending=False).head()
        top_subcategory_by_sales.plot(kind="barh", color="green")
        plt.title("Top 5 Category By Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("graph/top_subcategory_by_sales_chart.png")
        plt.close()

        self.df["year"] = self.df["order-date"].dt.to_period("Y")
        year_sales = self.df.groupby("year")["sales"].sum()
        year_sales.plot(kind="barh", color="blue")
        plt.title("Total Sales per Year")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("graph/yearly sales.png")

        segments = self.df.groupby("segment")["sales"].sum()
        segments.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Sales by Customer Segment")
        plt.tight_layout()
        plt.savefig("graph/segment_pie.png")
        plt.close()

        self.df["ship-mode"].value_counts().plot(kind="bar", color="purple")
        plt.title("Orders by Shipping Mode (Which shipping mode is most used)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("graph/ship_mode.png")


        leading_category_name = sales_by_subcatagory.idxmax()
        leading_category_sales = sales_by_subcatagory.max().round(2)

        top_region_name = top_regions_by_sales.idxmax()
        top_region_sales = top_regions_by_sales.max().round(2)


        top_segment_name = segments.idxmax()
        top_segment_sales = segments.max().round(2)

        with open("insights.txt", "w") as file:
            insights = f"""
            Data Insights:
                - Total Sales: ${self.df["sales"].sum().round(2)}
                - {leading_category_name} is the leading category by sales: ${leading_category_sales}
                - The {top_region_name} region generated the highest sales reaching ${top_region_sales}
                - The {top_segment_name} segment generated the highest sales with ${top_segment_sales}.
            """
            file.write(insights.strip())


def main():
    c = Cleaner()
    c.get_insights()
    c.cleaning_data()
    c.get_after_insights()
    c.df.to_csv("cleaned_superstore.csv", index=False)
    c.graph_analysis()



if __name__ == '__main__':
    main()