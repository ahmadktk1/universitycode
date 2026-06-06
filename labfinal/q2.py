
import numpy as np

# task 1 -------
arr = np.array([
    [120,135,150,145,160,170,175],
    [130,125,140,155,165,180,190],
    [110,115,120,125,130,140,145],
    [150,160,170,175,180,195,200]
])

print("arr \n ",arr)


# task 2 ----------------------- 


# braodcasting

broadcasted = arr + 2

print(f"\n 1. Broadcasted : \n {broadcasted}")
# creating sales_revenue

sales_revenue = arr * 50

print(f"\n Sales_revenue : \n {sales_revenue}")


# task 3 ----------------------------

# extract for sat and sunday
print(f"Sales_revenues for sat and sunday",sales_revenue[:,5:])
# sales on 2nd week thursday
print("Sales revenue on thursday of 2nd week",sales_revenue[1,3])


# task 4 -----------------------------
for avg in range(4):
    print("Average of sales for 2nd week:\n",sales_revenue[avg].mean())


# higest recorded
print("Highest recorded :",sales_revenue.max())

# sales over 160
salesover = arr[arr>160]

print("display of number of days over  160 ",salesover,"\n total count: ",salesover.shape[0])


# task 5 -----------------------------
flattenarray = arr.flatten()

print(flattenarray)

# boolean mask: values less than 130
arr[arr < 130] = 130
print(arr)
