**About**

This is the code for a store management system that connects to your own database.

**Setup**

Set the values for host, user, password, and database correctly to match your own database server. If the database server does not have any data or if you just want to test the project, there is an option to fill the tables with fake data.

**Functionality**

Storage Optimization: Analyzes if the store needs to buy more of a product.

Store Space Optimization: Recommends if the store should adjust its space in order to increase revenue.

Recall System: Sends an email to the affected customers who have purchased a product from a certain batch.

Waste Reduction: Recommends discounts in order to sell more of a soon-to-expire product.

Data Generator: Allows filling the database with fake data in order to test the functionality.

Delete Data: Allows the erasing of data from the database.

**HOW TO RUN** 

In order to run the program, the first step after the setup is running the main.py file.

The main.py file prints the following:

"What do you want to do? (1: setup, 2: fill with fake data, 3: clean database, 4: insert transaction item, 5: show stock, 6: send recall emails, 7: waste reduction analysis, 8: store space optimization, 9: supply chain analysis):"

In order to test the functionality, you must first input "1"; this creates the database structure.

The next step is to either fill the database with your store data or test the functionality by using choice "2".

Choice 2 allows you to fill the database with fake data. When the input "2" is entered, the following menu is printed:

"What tables do you want to fill with fake data?

Product,

Customers,

Batch,

Transaction,

Transaction_Item,

Cancel

Enter the numbers corresponding to your choice, separated by commas:"

The first five choices in "2: fill with fake data" allow the adding of data to the database. The fifth choice adds Transaction_Item, which represents a customer purchase. This allows for the testing of the other functionalities.

Back in the main menu, the rest of the choices ("4: insert transaction item, 5: show stock, 6: send recall emails, 7: waste reduction analysis, 8: store space optimization, 9: supply chain analysis") test the respective functions.

**Project Structure** 

main.py: The main menu.

connector.py: The database connector.

data_generator.py: Script for filling the database with fake data.

delete_data.py: Cleans the database.

Recall_system.py: Code for the recall system.

setup_db.py: Creates the database structure.

storage_optimization.py: Code for the storage optimization function.

store_space_optimization.py: Code for the store space optimization function.

waste_reduction.py: Code for the waste reduction function.

**Comments** 

Error for transaction Iteam


Waste reduction only works if 

