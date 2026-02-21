from connector import mydb, mycursor
from tabulate import tabulate

mycursor.execute(
    "select p.Name, sum(b.Quantity) as Total_Stock " \
    "from Product p " \
    "join Batch b on p.Product_id = b.Product_id " \
    "group by p.name"
)

results = mycursor.fetchall()
print(tabulate(results, headers=["Produktnamn", "Totalt i lager"], tablefmt="grid"))