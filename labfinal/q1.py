import pandas as pd

# task 1---------------
data = {
    "Name":["Ali","Sara","Ahmed","Ayesha","Bilal"],
    "Math":[78,85,90,88,76],
    "Physics":[82,79,91,87,80],
    "Computer":[85,92,89,90,75]
}

df = pd.DataFrame(data)

print(df.head())


#task 2 --------------

# display of maths marks

print(f"\n Marks of Maths only \n {df[["Math"]]}")

# students who have mroe than 85 marks

print(f"\n students who have mroe than 85 marks :\n {df[df["Computer"] > 85 ]}")

# task 3 ---------------



# new column for average marks
df["Average"] = df[["Math", "Physics", "Computer"]].mean(axis=1)

print("\n",df.head())
# add bonus marks 5 physics
df["Physics"] = df["Physics"]+5
print("\n",df.head())

# task 4 ------------------------

print(f" \n Highest in Maths {df['Math'].max()}")

print(f"\n  Overall average in Computer {df['Computer'].mean()}")

# task 5 --------------------------

# sorting dataframe in descending order based on average column in pandas
df_sorted = df.sort_values(by="Average", ascending=False).reset_index(drop=True)
print(f"\n df_sorted  \n {df_sorted}")

# saving to student_report.csv

df.to_csv("student_reprt.csv")

