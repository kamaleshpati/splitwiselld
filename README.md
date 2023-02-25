# Splitwise LLD
to run code<br>
##  python main.py 
<p>its not the complete implementation but can be referenced for LLD</p>
<br>
<h2>LOGIC</h2>
<h3>TABLE User:</h3>
<p>only contains user info and the groups it is related to<p>

<h3>TABLE Group:</h3>
<p>maintains the groupmemeber , and split_expense map to track each member calculation</p>
<p>add_user(): to add user to group</p>
<p>split_equal_amount(): split amount equally in group</p>
<p>split_by_given_amount(): split amount by given data in group</p>

<h3>TABLE Expense:</h3>
<p>just a record of transaction</p>

<h3>TABLE Splitwise:</h3>
<p>maintain the whole system in map(used as main db in apps)</p>
<p>createUser(): to add user to system</p>
<p>getUserObj(): to check user in testing</p>
<p>addcreateGroup_user(): to add group to system</p>
<p>getGroup(): to test the group exists or not</p>

