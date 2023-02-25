# neeraj.gupta@cyware.com

class User:
    def __init__(self, username):
        self.username = username
        self.groups = []
        self.expense_records = []

    def get_all_expense_records(self):
        return self.expense_records


class Group:
    def __init__(self, groupname, memebers: list):
        self.groupname = groupname
        self.groupmemebers = []
        for i in memebers:
            self.groupmemebers.append(i)
        self.split_expense = {}
        for i in memebers:
            self.split_expense[i.username] = {}

    def add_user(self, user: User):
        self.groupmemebers.append(user)
        self.split_expense[user.username] = {}

    def split_equal_amount(self, paidby: User, memebrs: list[User], amount: float):
        individual_amount = amount // (len(memebrs))
        for user in memebrs:
            paidby.expense_records.append(Expense(paidby, user, individual_amount))
            user.expense_records.append(Expense(paidby, user, individual_amount))
            if user != paidby:
                if paidby.username not in self.split_expense[user.username]:
                    self.split_expense[user.username][paidby.username] = 0
                if user.username not in self.split_expense[paidby.username]:
                    self.split_expense[paidby.username][user.username] = 0
                self.split_expense[user.username][paidby.username] += individual_amount
                self.split_expense[paidby.username][user.username] -= individual_amount

    # no tested
    def split_by_given_amount(self, paidby: User, paid_info: map):
        for user in paid_info:
            paidby.expense_records.append(Expense(paidby, user, paid_info[user]))
            user.expense_records.append(Expense(paidby, user, paid_info[user]))
            if user != paidby:
                if paidby.username not in self.split_expense[user.username]:
                    self.split_expense[user.username][paidby.username] = 0
                if user.username not in self.split_expense[paidby.username]:
                    self.split_expense[paidby.username][user.username] = 0
                self.split_expense[user.username][paidby.username] += paid_info[user]
                self.split_expense[paidby.username][user.username] -= paid_info[user]
        print(self.split_expense)

    def calculate_all_user_expense(self):
        result = {}
        for user in self.groupmemebers:
            result[user.username] = {}
            for mem in self.split_expense[user.username]:
                if self.split_expense[user.username][mem] > 0:
                    result[user.username][mem] = "you owe " + mem + " " + str(self.split_expense[user.username][mem])
                elif self.split_expense[user.username][mem] < 0:
                    result[user.username][mem] = mem + " owes you " + str(-self.split_expense[user.username][mem])
                else:
                    result[user.username][mem] = "0"
        return result


class Expense:
    def __init__(self, paidBy: User, paidTo: User, expense: float):
        self.paidBy = paidBy
        self.paidTo = paidTo
        self.expense_amount = expense


class SplitWise:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def createUser(self, username: str):
        self.users[username] = User(username)

    def getUserObj(self, username: str):
        return self.users[username]

    def getGroup(self, username: str, groupname: str):
        for i in self.users[username].groups:
            if groupname is i.groupname:
                return self.groups[groupname]
        return "user is not part of group"

    def createGroup(self, grpname: str, users: list):
        grp = Group(grpname, users)
        self.groups[grpname] = grp
        for i in users:
            i.groups.append(grp)


import unittest


class SplitwiseTesting(unittest.TestCase):

    def test_splitwise_create_user(self):
        self.split_wise = SplitWise()
        for i in ["raj", "kaaml", "less"]:
            self.split_wise.createUser(i)
            self.assertEqual(self.split_wise.users[i].username, User(i).username)

    def test_splitwise_create_group(self):
        self.split_wise = SplitWise()
        grpname = "home"
        userlist = []
        linames = ["raj", "kaaml", "less"]
        for i in linames:
            self.split_wise.createUser(i)
            userlist.append(self.split_wise.users[i])
        self.split_wise.createGroup(grpname, userlist)
        self.assertEqual(self.split_wise.getGroup(linames[0], grpname).groupname, grpname)
        for i in userlist:
            li = []
            for j in i.groups:
                li.append(j.groupname)
            self.assertTrue(grpname in li)

    def test_splitwise_expense_calculation(self):
        self.split_wise = SplitWise()
        grpname = "home"
        userlist = []
        linames = ["raj", "kaaml", "less"]
        for i in linames:
            self.split_wise.createUser(i)
            userlist.append(self.split_wise.users[i])
        self.split_wise.createGroup(grpname, userlist)

        # raj has paid 90 rs for whole group, so everyone except raj ,owes raj 30 rs
        self.split_wise.getGroup(linames[0], grpname).split_equal_amount(userlist[0], userlist, 90)
        res = self.split_wise.getGroup(linames[0], grpname).calculate_all_user_expense()
        for i in res[linames[0]]:
            self.assertTrue("owes you 30" in res[linames[0]][i])

        # kaaml has paid 90 rs for whole group, what kaam owes to raj is now 0 , and less owes kaaml and raj 30rs each
        self.split_wise.getGroup(linames[0], grpname).split_equal_amount(userlist[1], userlist, 90)
        res = self.split_wise.getGroup(linames[0], grpname).calculate_all_user_expense()
        # less owes kaaml 30
        self.assertTrue("owes you 30" in res[linames[1]][linames[2]])
        # kaam owes to raj is now 0
        self.assertTrue("0" in res[linames[1]][linames[0]])


if __name__ == '__main__':
    unittest.main()
