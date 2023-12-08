import pandas as pd
import random as rd

class ProductLoader:
    def __init__(self) -> None:
        self.__categories = ['Clothes', 'Home Products', 'Beauty Products', 'Healthcare and Sanitization', 'Watches', 'Kitchenware', 
                             'Mobile Phones', 'Furniture', 'Headphones', 'Computer Accessories', 'Toys', 'Shoes']
        self.__weights = [0.06, 0.03, 0.17, 0.08, 0.06, 0.13, 0.03, 0.03, 0.16, 0.06, 0.13, 0.06]
        self.__product_df = pd.read_csv('resources/category_wise_products.csv')        

    def pick_a_product(self, category):
        df_temp = self.__product_df[self.__product_df['category']==category].reset_index(drop=True)
        val = df_temp.loc[rd.randint(0, df_temp.shape[0]-1), ['product_name', 'retail_price']]
        return val['product_name'], val['retail_price']
    
    def pick_a_category(self):
        return rd.choices(population=self.__categories, weights=self.__weights)[0]


if __name__=='__main__':
    import sys
    n = int(sys.argv[1])
    pl = ProductLoader()
    for _ in range(n):
        cat = pl.pick_a_category()
        print(cat)
        prod = pl.pick_a_product(cat)
        print(prod)
