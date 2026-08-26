import os
import sys
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class ExpenseValidator:
    def __init__(self):
        self.valid_categories = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Shopping', 'Health', 'Other']

    def is_valid_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_amount(self, amount_str):
        try:
            val = float(amount_str)
            if val > 0:
                return True
            return False
        except ValueError:
            return False

    def is_valid_category(self, category):
        if category in self.valid_categories:
            return True
        return False

class ExpenseVisualizer:
    def __init__(self, data_frame):
        self.df = data_frame
        sns.set_theme(style="whitegrid")

    def update_data(self, new_data_frame):
        self.df = new_data_frame

    def plot_bar_chart(self):
        if self.df is None or self.df.empty:
            print("No data available to plot bar chart.")
            return
        
        category_totals = self.df.groupby('Category')['Amount'].sum().reset_index()
        plt.figure(figsize=(12, 7))
        ax = sns.barplot(x='Category', y='Amount', data=category_totals, palette='muted')
        plt.title('Total Expenses by Category', fontsize=18, fontweight='bold')
        plt.xlabel('Expense Category', fontsize=14)
        plt.ylabel('Total Spent', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')
                        
        plt.tight_layout()
        plt.show()

    def plot_line_graph(self):
        if self.df is None or self.df.empty:
            print("No data available to plot line graph.")
            return
            
        temp_df = self.df.copy()
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])
        daily_totals = temp_df.groupby('Date')['Amount'].sum().reset_index()
        daily_totals = daily_totals.sort_values(by='Date')
        
        plt.figure(figsize=(14, 7))
        sns.lineplot(x='Date', y='Amount', data=daily_totals, marker='o', color='b', linewidth=2.5)
        plt.title('Spending Trends Over Time', fontsize=18, fontweight='bold')
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Amount Spent', fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def plot_pie_chart(self):
        if self.df is None or self.df.empty:
            print("No data available to plot pie chart.")
            return
            
        category_totals = self.df.groupby('Category')['Amount'].sum()
        
        plt.figure(figsize=(10, 10))
        colors = sns.color_palette('pastel')[0:len(category_totals)]
        plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', 
                colors=colors, startangle=140, shadow=True, 
                wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        plt.title('Proportional Spending Distribution by Category', fontsize=18, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def plot_histogram(self):
        if self.df is None or self.df.empty:
            print("No data available to plot histogram.")
            return
            
        plt.figure(figsize=(12, 7))
        sns.histplot(self.df['Amount'], bins=20, kde=True, color='purple')
        plt.title('Frequency of Expense Amounts', fontsize=18, fontweight='bold')
        plt.xlabel('Expense Amount', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.tight_layout()
        plt.show()

class ExpenseTracker:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.validator = ExpenseValidator()
        self.df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        self.load_data()
        self.visualizer = ExpenseVisualizer(self.df)

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                self.df = pd.read_csv(self.filename)
                self.clean_data()
            except Exception as e:
                print("Error loading dataset.")
                self.df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        else:
            self.df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])

    def clean_data(self):
        if not self.df.empty:
            self.df.dropna(subset=['Date', 'Amount', 'Category'], inplace=True)
            self.df['Amount'] = pd.to_numeric(self.df['Amount'], errors='coerce')
            self.df.dropna(subset=['Amount'], inplace=True)
            self.df = self.df[self.df['Amount'] > 0]
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
            self.df.dropna(subset=['Date'], inplace=True)
            self.df.reset_index(drop=True, inplace=True)

    def save_data(self):
        try:
            self.df.to_csv(self.filename, index=False)
        except Exception as e:
            print("Failed to save data.")

    def add_expense(self, date, amount, category, description):
        if not self.validator.is_valid_date(date):
            print("Invalid date format. Expected YYYY-MM-DD.")
            return False
            
        if not self.validator.is_valid_amount(amount):
            print("Invalid amount. Must be a positive number.")
            return False
            
        if not self.validator.is_valid_category(category):
            print("Invalid category. Must be one of the predefined categories.")
            return False

        new_row = pd.DataFrame({
            'Date': [date],
            'Amount': [float(amount)],
            'Category': [category],
            'Description': [description]
        })
        
        if self.df.empty:
            self.df = new_row
        else:
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            
        self.save_data()
        self.visualizer.update_data(self.df)
        print("Expense added successfully.")
        return True

    def get_summary(self):
        if self.df.empty:
            print("No expenses recorded yet.")
            return None

        amounts_array = self.df['Amount'].to_numpy()
        
        total_expense = np.sum(amounts_array)
        average_expense = np.mean(amounts_array)
        max_expense = np.max(amounts_array)
        min_expense = np.min(amounts_array)
        
        category_group = self.df.groupby('Category')['Amount'].sum()
        top_category = category_group.idxmax()
        top_category_amount = category_group.max()

        temp_df = self.df.copy()
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])
        temp_df['MonthYear'] = temp_df['Date'].dt.to_period('M')
        monthly_group = temp_df.groupby('MonthYear')['Amount'].sum()
        monthly_average = monthly_group.mean() if not monthly_group.empty else 0

        summary = {
            'total_expense': total_expense,
            'average_expense': average_expense,
            'max_expense': max_expense,
            'min_expense': min_expense,
            'top_category': top_category,
            'top_category_amount': top_category_amount,
            'monthly_average': monthly_average,
            'category_breakdown': category_group.to_dict()
        }
        
        return summary

    def filter_expenses(self, condition_type, condition_value):
        if self.df.empty:
            print("No expenses to filter.")
            return pd.DataFrame()

        filtered_df = pd.DataFrame()

        if condition_type == 'category':
            filtered_df = self.df[self.df['Category'].str.lower() == condition_value.lower()]
        elif condition_type == 'date':
            filtered_df = self.df[self.df['Date'] == condition_value]
        elif condition_type == 'amount_greater':
            try:
                val = float(condition_value)
                filtered_df = self.df[self.df['Amount'] >= val]
            except ValueError:
                print("Invalid amount value for filtering.")
        elif condition_type == 'amount_less':
            try:
                val = float(condition_value)
                filtered_df = self.df[self.df['Amount'] <= val]
            except ValueError:
                print("Invalid amount value for filtering.")
        elif condition_type == 'month':
            temp_df = self.df.copy()
            temp_df['Date'] = pd.to_datetime(temp_df['Date'])
            filtered_df = temp_df[temp_df['Date'].dt.strftime('%Y-%m') == condition_value]
            if not filtered_df.empty:
                filtered_df['Date'] = filtered_df['Date'].dt.strftime('%Y-%m-%d')
        else:
            print("Invalid condition type.")
            
        return filtered_df

    def generate_report(self):
        summary = self.get_summary()
        if not summary:
            return

        print("="*50)
        print("          SMART EXPENSE TRACKER REPORT          ")
        print("="*50)
        print(f"Total Expenses Logged: {len(self.df)}")
        print(f"Overall Total Spent:   ${summary['total_expense']:.2f}")
        print(f"Overall Average Spent: ${summary['average_expense']:.2f}")
        print(f"Highest Single Expense:${summary['max_expense']:.2f}")
        print(f"Lowest Single Expense: ${summary['min_expense']:.2f}")
        print(f"Monthly Avg Spending:  ${summary['monthly_average']:.2f}")
        print("-" * 50)
        print("Spending by Category:")
        
        cat_breakdown = summary['category_breakdown']
        for cat, amt in sorted(cat_breakdown.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / summary['total_expense']) * 100
            print(f"  - {cat.ljust(15)}: ${amt:8.2f}  ({pct:5.2f}%)")
            
        print("-" * 50)
        print(f"Top Spending Category: {summary['top_category']} (${summary['top_category_amount']:.2f})")
        print("="*50)


class ExpenseAppUI:
    def __init__(self):
        self.tracker = ExpenseTracker('expenses.csv')
        self.running = True

    def display_menu(self):
        print(" " + "*"*40)
        print("  SMART EXPENSE TRACKER MAIN MENU  ")
        print("*"*40)
        print("1. Log a New Expense")
        print("2. View Expense Summary")
        print("3. Generate Detailed Report")
        print("4. Filter Expenses")
        print("5. View Data Visualizations")
        print("6. Show All Raw Data")
        print("7. Exit Application")
        print("*"*40)

    def handle_add_expense(self):
        print("--- Log New Expense ---")
        date_input = input("Enter Date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_input:
            date_input = datetime.datetime.now().strftime("%Y-%m-%d")
            
        amount_input = input("Enter Amount ($): ").strip()
        
        print(f"Valid Categories: {', '.join(self.tracker.validator.valid_categories)}")
        category_input = input("Enter Category: ").strip().capitalize()
        
        description_input = input("Enter Description (optional): ").strip()
        if not description_input:
            description_input = "N/A"
            
        self.tracker.add_expense(date_input, amount_input, category_input, description_input)

    def handle_view_summary(self):
        print("--- Expense Summary ---")
        summary = self.tracker.get_summary()
        if summary:
            print(f"Total Spent: ${summary['total_expense']:.2f}")
            print(f"Average Transaction: ${summary['average_expense']:.2f}")
            print(f"Top Category: {summary['top_category']}")

    def handle_filter_expenses(self):
        print("--- Filter Expenses ---")
        print("1. By Category")
        print("2. By Specific Date (YYYY-MM-DD)")
        print("3. By Specific Month (YYYY-MM)")
        print("4. Amount Greater Than")
        print("5. Amount Less Than")
        
        choice = input("Select a filter option: ").strip()
        
        filtered_df = pd.DataFrame()
        
        if choice == '1':
            cat = input("Enter category to search: ").strip()
            filtered_df = self.tracker.filter_expenses('category', cat)
        elif choice == '2':
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            filtered_df = self.tracker.filter_expenses('date', date_str)
        elif choice == '3':
            month_str = input("Enter month (YYYY-MM): ").strip()
            filtered_df = self.tracker.filter_expenses('month', month_str)
        elif choice == '4':
            amt = input("Enter minimum amount: ").strip()
            filtered_df = self.tracker.filter_expenses('amount_greater', amt)
        elif choice == '5':
            amt = input("Enter maximum amount: ").strip()
            filtered_df = self.tracker.filter_expenses('amount_less', amt)
        else:
            print("Invalid filter selection.")
            return

        if not filtered_df.empty:
            print(f"Found {len(filtered_df)} records:")
            print(filtered_df.to_string(index=False))
        else:
            print("No records found matching that criteria.")

    def handle_visualizations(self):
        print("--- Data Visualizations ---")
        print("1. Bar Chart (Expenses by Category)")
        print("2. Line Graph (Spending Trends Over Time)")
        print("3. Pie Chart (Proportional Spending)")
        print("4. Histogram (Expense Amount Frequencies)")
        print("5. Show All Visualizations Sequentially")
        
        choice = input("Select visualization type: ").strip()
        
        if choice == '1':
            self.tracker.visualizer.plot_bar_chart()
        elif choice == '2':
            self.tracker.visualizer.plot_line_graph()
        elif choice == '3':
            self.tracker.visualizer.plot_pie_chart()
        elif choice == '4':
            self.tracker.visualizer.plot_histogram()
        elif choice == '5':
            self.tracker.visualizer.plot_bar_chart()
            self.tracker.visualizer.plot_line_graph()
            self.tracker.visualizer.plot_pie_chart()
            self.tracker.visualizer.plot_histogram()
        else:
            print("Invalid visualization selection.")

    def handle_show_all(self):
        print("--- All Recorded Expenses ---")
        if self.tracker.df.empty:
            print("No data available.")
        else:
            print(self.tracker.df.to_string(index=False))

    def run(self):
        while self.running:
            self.display_menu()
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.handle_add_expense()
            elif choice == '2':
                self.handle_view_summary()
            elif choice == '3':
                self.tracker.generate_report()
            elif choice == '4':
                self.handle_filter_expenses()
            elif choice == '5':
                self.handle_visualizations()
            elif choice == '6':
                self.handle_show_all()
            elif choice == '7':
                print("Exiting Smart Expense Tracker. Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")

def main():
    try:
        app = ExpenseAppUI()
        app.run()
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
    