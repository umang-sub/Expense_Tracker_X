import os
import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


VALID_CATEGORIES = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Shopping', 'Health', 'Other']


class ExpenseValidator:
    def __init__(self):
        self.valid_categories = VALID_CATEGORIES

    def is_valid_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_amount(self, amount_str):
        try:
            val = float(amount_str)
            return val > 0
        except (TypeError, ValueError):
            return False

    def is_valid_category(self, category):
        return category in self.valid_categories


class ExpenseVisualizer:
    def __init__(self, data_frame):
        self.df = data_frame
        sns.set_theme(style="whitegrid")

    def update_data(self, new_data_frame):
        self.df = new_data_frame

    def _get_data(self, data=None):
        return self.df if data is None else data

    def plot_bar_chart(self, data=None):
        df = self._get_data(data)
        if df is None or df.empty:
            return None

        category_totals = df.groupby('Category', as_index=False)['Amount'].sum()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=category_totals, x='Category', y='Amount', palette='muted', ax=ax)
        ax.set_title('Total Expenses by Category', fontsize=16, fontweight='bold')
        ax.set_xlabel('Expense Category')
        ax.set_ylabel('Total Spent')
        ax.tick_params(axis='x', rotation=45)

        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                        ha='center', va='bottom', xytext=(0, 6), textcoords='offset points')

        fig.tight_layout()
        return fig

    def plot_line_graph(self, data=None):
        df = self._get_data(data)
        if df is None or df.empty:
            return None

        temp_df = df.copy()
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])
        daily_totals = temp_df.groupby('Date', as_index=False)['Amount'].sum().sort_values('Date')

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=daily_totals, x='Date', y='Amount', marker='o', linewidth=2.5, ax=ax)
        ax.set_title('Spending Trends Over Time', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount Spent')
        plt.xticks(rotation=45)
        fig.tight_layout()
        return fig

    def plot_pie_chart(self, data=None):
        df = self._get_data(data)
        if df is None or df.empty:
            return None

        category_totals = df.groupby('Category')['Amount'].sum()
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = sns.color_palette('pastel', n_colors=len(category_totals))
        ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', colors=colors,
               startangle=140, shadow=True, wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        ax.set_title('Proportional Spending Distribution by Category', fontsize=16, fontweight='bold')
        fig.tight_layout()
        return fig

    def plot_histogram(self, data=None):
        df = self._get_data(data)
        if df is None or df.empty:
            return None

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['Amount'], bins=20, kde=True, color='purple', ax=ax)
        ax.set_title('Frequency of Expense Amounts', fontsize=16, fontweight='bold')
        ax.set_xlabel('Expense Amount')
        ax.set_ylabel('Frequency')
        fig.tight_layout()
        return fig


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
            except Exception:
                self.df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        else:
            self.df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])

    def clean_data(self):
        if not self.df.empty:
            self.df = self.df.dropna(subset=['Date', 'Amount', 'Category']).copy()
            self.df['Amount'] = pd.to_numeric(self.df['Amount'], errors='coerce')
            self.df = self.df.dropna(subset=['Amount']).copy()
            self.df = self.df[self.df['Amount'] > 0].copy()
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
            self.df = self.df.dropna(subset=['Date']).copy().reset_index(drop=True)

    def save_data(self):
        try:
            self.df.to_csv(self.filename, index=False)
        except Exception:
            pass

    def add_expense(self, date, amount, category, description):
        if not self.validator.is_valid_date(date):
            return False, 'Invalid date format. Expected YYYY-MM-DD.'

        if not self.validator.is_valid_amount(str(amount)):
            return False, 'Invalid amount. Must be a positive number.'

        if not self.validator.is_valid_category(category):
            return False, 'Invalid category. Must be one of the predefined categories.'

        new_row = pd.DataFrame({
            'Date': [date],
            'Amount': [float(amount)],
            'Category': [category],
            'Description': [description or 'N/A']
        })

        if self.df.empty:
            self.df = new_row
        else:
            self.df = pd.concat([self.df, new_row], ignore_index=True)

        self.save_data()
        self.visualizer.update_data(self.df)
        return True, 'Expense added successfully.'

    def get_summary(self):
        if self.df.empty:
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

        return {
            'total_expense': total_expense,
            'average_expense': average_expense,
            'max_expense': max_expense,
            'min_expense': min_expense,
            'top_category': top_category,
            'top_category_amount': top_category_amount,
            'monthly_average': monthly_average,
            'category_breakdown': category_group.to_dict()
        }

    def filter_expenses(self, condition_type, condition_value):
        if self.df.empty:
            return pd.DataFrame()

        if condition_type == 'category':
            return self.df[self.df['Category'].str.lower() == condition_value.lower()].copy()
        if condition_type == 'date':
            return self.df[self.df['Date'] == condition_value].copy()
        if condition_type == 'amount_greater':
            try:
                return self.df[self.df['Amount'] >= float(condition_value)].copy()
            except ValueError:
                return pd.DataFrame()
        if condition_type == 'amount_less':
            try:
                return self.df[self.df['Amount'] <= float(condition_value)].copy()
            except ValueError:
                return pd.DataFrame()
        if condition_type == 'month':
            temp_df = self.df.copy()
            temp_df['Date'] = pd.to_datetime(temp_df['Date'])
            filtered_df = temp_df[temp_df['Date'].dt.strftime('%Y-%m') == condition_value].copy()
            if not filtered_df.empty:
                filtered_df['Date'] = filtered_df['Date'].dt.strftime('%Y-%m-%d')
            return filtered_df

        return pd.DataFrame()


def main():
    st.set_page_config(page_title='Smart Expense Tracker', page_icon='💸', layout='wide')
    st.title('💸 Smart Expense Tracker')
    st.caption('Track, filter, and analyze spending from a single Streamlit dashboard.')

    tracker = ExpenseTracker('expenses.csv')

    with st.sidebar:
        st.header('Add a new expense')
        with st.form('expense_form', clear_on_submit=True):
            date_input = st.date_input('Date', datetime.date.today())
            amount_input = st.number_input('Amount ($)', min_value=0.01, value=0.0, step=0.01, format='%.2f')
            category_input = st.selectbox('Category', VALID_CATEGORIES)
            description_input = st.text_input('Description', 'N/A')
            submitted = st.form_submit_button('Add expense')

            if submitted:
                success, message = tracker.add_expense(
                    date_input.isoformat(),
                    f'{amount_input:.2f}',
                    category_input,
                    description_input
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    summary = tracker.get_summary()
    if summary is None or tracker.df.empty:
        st.info('No expenses recorded yet. Add your first expense from the sidebar.')
        return

    st.subheader('Overview')
    summary_cols = st.columns(4)
    summary_cols[0].metric('Total spent', f"${summary['total_expense']:.2f}")
    summary_cols[1].metric('Average expense', f"${summary['average_expense']:.2f}")
    summary_cols[2].metric('Top category', f"{summary['top_category']} (${summary['top_category_amount']:.2f})")
    summary_cols[3].metric('Monthly average', f"${summary['monthly_average']:.2f}")

    st.subheader('Expense data')
    filter_col_1, filter_col_2, filter_col_3 = st.columns(3)
    category_filter = filter_col_1.selectbox('Category filter', ['All'] + VALID_CATEGORIES)
    month_filter = filter_col_2.text_input('Month filter (YYYY-MM)', '')
    min_amount = filter_col_3.number_input('Minimum amount', min_value=0.0, value=0.0, step=0.01)

    filtered_df = tracker.df.copy()
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category_filter].copy()
    if month_filter:
        filtered_df = filtered_df[filtered_df['Date'].str.startswith(month_filter)].copy()
    if min_amount > 0:
        filtered_df = filtered_df[filtered_df['Amount'] >= min_amount].copy()

    st.dataframe(filtered_df, use_container_width=True)

    st.subheader('Visual insights')
    chart_tabs = st.tabs(['Category totals', 'Spending trend', 'Category split', 'Expense distribution'])

    bar_chart = tracker.visualizer.plot_bar_chart(filtered_df)
    line_chart = tracker.visualizer.plot_line_graph(filtered_df)
    pie_chart = tracker.visualizer.plot_pie_chart(filtered_df)
    histogram_chart = tracker.visualizer.plot_histogram(filtered_df)

    with chart_tabs[0]:
        if bar_chart is not None:
            st.pyplot(bar_chart)
        else:
            st.info('No category data available.')

    with chart_tabs[1]:
        if line_chart is not None:
            st.pyplot(line_chart)
        else:
            st.info('No trend data available.')

    with chart_tabs[2]:
        if pie_chart is not None:
            st.pyplot(pie_chart)
        else:
            st.info('No category split data available.')

    with chart_tabs[3]:
        if histogram_chart is not None:
            st.pyplot(histogram_chart)
        else:
            st.info('No histogram data available.')

    st.subheader('Detailed report')
    category_breakdown = summary['category_breakdown']
    report_data = pd.DataFrame(
        [
            {'Category': category, 'Amount': amount, 'Share (%)': (amount / summary['total_expense']) * 100}
            for category, amount in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)
        ]
    )
    st.dataframe(report_data, use_container_width=True)


if __name__ == '__main__':
    main()
