import streamlit as st
import matplotlib.pyplot as plt

# Configure the app
st.set_page_config(page_title="Personal Finance Planner", layout="wide")

# App title and description
st.title("💰 Personal Finance Projection Tool")
st.markdown("""
Plan your financial future with this interactive calculator. 
Enter your details in the sidebar and see how your savings grow over time.
""")

# Industry growth rates
INDUSTRY_GROWTH = {
    'finance': 0.05,
    'technology': 0.06,
    'healthcare': 0.04,
    'education': 0.03,
    'manufacturing': 0.035,
    'retail': 0.025,
    'government': 0.02,
    'consulting': 0.045
}

# Main calculation function
def calculate_projection(params):
    results = []
    salary = params['starting_salary']
    savings = 0
    invested = 0
    
    for year in range(1, params['years'] + 1):
        # Apply salary growth
        salary *= (1 + INDUSTRY_GROWTH.get(params['industry'], 0.03))
        
        # Adjust rent if married
        rent = params['rent']
        if params['marriage_age'] and (params['current_age'] + year - 1) >= params['marriage_age']:
            rent *= 0.8  # 20% reduction when married
            
        # Calculate savings
        expenses = rent + (params['monthly_expenses'] * 12)
        annual_savings = salary - expenses
        
        # Split savings between cash and investments
        to_invest = annual_savings * params['invest_ratio']
        to_cash = annual_savings * (1 - params['invest_ratio'])
        
        # Grow investments
        invested = invested * (1 + params['investment_rate']) + to_invest
        savings += to_cash
        total = savings + invested
        
        results.append({
            'Year': year,
            'Age': params['current_age'] + year - 1,
            'Salary': round(salary, 2),
            'Rent': round(rent, 2),
            'Expenses': round(expenses, 2),
            'Savings': round(annual_savings, 2),
            'Invested': round(invested, 2),
            'Cash': round(savings, 2),
            'Total': round(total, 2)
        })
    
    return results

# Sidebar inputs - NO DEFAULT VALUES
with st.sidebar:
    st.header("📊 Your Financial Details")
    
    # Required inputs with no defaults
    starting_salary = st.number_input("Your Net Salary (CHF)", min_value=0)
    rent = st.number_input("Your Annual Rent (CHF)", min_value=0)
    monthly_expenses = st.number_input("Your Monthly Expenses (CHF)", min_value=0)
    years = st.slider("Years to Project", 1, 50)
    
    # Investment settings
    industry = st.selectbox("Your Industry", list(INDUSTRY_GROWTH.keys()))
    investment_rate = st.slider("Expected Investment Return Rate", 0.0, 0.20, step=0.01)
    invest_ratio = st.slider("Percentage of Savings to Invest", 0.0, 1.0, step=0.05)
    
    # Optional marriage settings
    marriage_check = st.checkbox("Will you get married during this period?")
    current_age = None
    marriage_age = None
    if marriage_check:
        current_age = st.number_input("Your Current Age", min_value=18, max_value=100)
        marriage_age = st.number_input("Planned Marriage Age", min_value=18, max_value=100)

# Only calculate if all required inputs are provided
if starting_salary > 0 and rent > 0 and monthly_expenses > 0:
    params = {
        'starting_salary': starting_salary,
        'rent': rent,
        'monthly_expenses': monthly_expenses,
        'years': years,
        'industry': industry,
        'investment_rate': investment_rate,
        'invest_ratio': invest_ratio,
        'current_age': current_age,
        'marriage_age': marriage_age
    }

    results = calculate_projection(params)

    # Display results
    st.header("📈 Your Projection Results")

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Total Savings", f"CHF {results[-1]['Total']:,.0f}")
    col2.metric("Total Invested", f"CHF {results[-1]['Invested']:,.0f}")
    col3.metric("Final Salary", f"CHF {results[-1]['Salary']:,.0f}")

    # Charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Chart 1: Savings growth
    years_list = [x['Year'] for x in results]
    ax1.plot(years_list, [x['Total'] for x in results], color='green')
    ax1.set_title('Your Savings Growth')
    ax1.set_xlabel('Years')
    ax1.set_ylabel('CHF')
    ax1.grid(True)
    
    # Chart 2: Salary vs Expenses
    ax2.plot(years_list, [x['Salary'] for x in results], label='Salary', color='blue')
    ax2.plot(years_list, [x['Expenses'] for x in results], label='Expenses', color='red')
    ax2.set_title('Salary vs Expenses')
    ax2.set_xlabel('Years')
    ax2.legend()
    ax2.grid(True)
    
    st.pyplot(fig)
    plt.close()

    # Data table
    st.dataframe(results)
else:
    st.warning("Please enter all your financial details in the sidebar to see your projection")