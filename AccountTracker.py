class Category:
    def __init__(self, name):
        # Initialize a Category object with a name and an empty ledger list
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        # Add a deposit to the ledger with optional description
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # Withdraw funds only if there are sufficient funds
        if self.check_funds(amount):
            # Add withdrawal as a negative amount to the ledger
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        # Calculate and return the current balance by summing amounts in ledger
        total = sum(item["amount"] for item in self.ledger)
        return total

    def transfer(self, amount, category):
        # Transfer funds to another Category object
        if self.check_funds(amount):
            # Withdraw from self with a note of transfer
            self.withdraw(amount, f"Transfer to {category.name}")
            # Deposit to the other category with a matching note
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        # Check if the current balance is enough for the amount
        return amount <= self.get_balance()

    def __str__(self):
        # Create a formatted string representation of the ledger
        title = f"{self.name:*^30}\n"  # Center category name with '*' to fill 30 characters
        items = ""
        for item in self.ledger:
            # Trim description to 23 chars and format amount to 2 decimal places, right-aligned
            desc = item["description"][:23]
            amt = f"{item['amount']:.2f}"
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

    def create_spend_chart(categories):
        # Header for the chart
        chart = "Percentage spent by category\n"

        withdrawals = []  # To store withdrawal amounts per category
        total_spent = 0   # Total of all withdrawals

        # Step 1: Calculate total withdrawals for each category
        for category in categories:
            spent = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
            withdrawals.append(spent)
            total_spent += spent

        # Step 2: Convert each withdrawal to percentage (rounded down to nearest 10)
        percentages = [(int((spent / total_spent) * 100) // 10) * 10 for spent in withdrawals]

        # Step 3: Build the vertical bar chart, from 100 down to 0
        for i in range(100, -1, -10):
            line = f"{i:>3}|"  # Align percentage labels (e.g., '100|', ' 90|')
            for percent in percentages:
                line += " o " if percent >= i else "   "  # 'o' if bar reaches this level
            chart += line + " \n"

        # Step 4: Add horizontal line under bars
        chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

        # Step 5: Build the vertical names below the bars
        max_len = max(len(category.name) for category in categories)  # Longest name length

        for i in range(max_len):
            line = "     "  # Start with 5 spaces to align with chart
            for category in categories:
                # Add character from each category name or space if it's too short
                if i < len(category.name):
                    line += category.name[i] + "  "
                else:
                    line += "   "
            chart += line.rstrip() + "  \n"  # Trim end and add extra two spaces

        return chart.rstrip("\n")  # Remove final newline to pass test #22


'''
food = Category("Food")
clothing = Category("Clothing")
entertainment = Category("Auto")

food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food")
food.transfer(50, clothing)

print(food)
print(clothing)
print(create_spend_chart([food, clothing, entertainment]))


'''