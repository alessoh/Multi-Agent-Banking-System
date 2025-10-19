import json
from datetime import datetime, timedelta
import random

class BankDataWrapper:
    """
    Simulates banking data access through A2A protocol.
    In a real implementation, this would connect to actual banking APIs.
    """
    
    def __init__(self):
        self.mock_data = self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize mock banking data for demonstration"""
        return {
            "user_profile": {
                "user_id": "user_123",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "account_type": "Premium Checking"
            },
            "transactions": self._generate_mock_transactions(),
            "goals": self._generate_mock_goals(),
            "investments": self._generate_mock_investments(),
            "debts": self._generate_mock_debts(),
            "perks": self._generate_mock_perks(),
            "advisors": self._generate_mock_advisors()
        }
    
    def _generate_mock_transactions(self):
        """Generate sample transaction data"""
        categories = ["Groceries", "Dining", "Transportation", "Entertainment", "Utilities", "Shopping"]
        merchants = {
            "Groceries": ["Whole Foods", "Trader Joe's", "Safeway"],
            "Dining": ["Chipotle", "Starbucks", "Local Cafe"],
            "Transportation": ["Uber", "Gas Station", "Public Transit"],
            "Entertainment": ["Netflix", "Movie Theater", "Spotify"],
            "Utilities": ["Electric Company", "Water Utility", "Internet Provider"],
            "Shopping": ["Amazon", "Target", "Best Buy"]
        }
        
        transactions = []
        for i in range(90):
            date = datetime.now() - timedelta(days=i)
            category = random.choice(categories)
            merchant = random.choice(merchants[category])
            amount = round(random.uniform(10, 200), 2)
            
            transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "merchant": merchant,
                "category": category,
                "amount": amount,
                "description": f"Purchase at {merchant}"
            })
        
        return transactions
    
    def _generate_mock_goals(self):
        """Generate sample financial goals"""
        return [
            {
                "id": "goal_1",
                "name": "Emergency Fund",
                "target_amount": 10000,
                "current_amount": 4500,
                "target_date": "2025-12-31",
                "status": "active"
            },
            {
                "id": "goal_2",
                "name": "Vacation to Italy",
                "target_amount": 5000,
                "current_amount": 2100,
                "target_date": "2026-06-01",
                "status": "active"
            },
            {
                "id": "goal_3",
                "name": "Down Payment",
                "target_amount": 50000,
                "current_amount": 12000,
                "target_date": "2027-01-01",
                "status": "active"
            }
        ]
    
    def _generate_mock_investments(self):
        """Generate sample investment portfolio data"""
        return {
            "total_value": 45000,
            "holdings": [
                {"type": "Stocks", "value": 25000, "allocation": 55.6},
                {"type": "Bonds", "value": 12000, "allocation": 26.7},
                {"type": "Real Estate", "value": 5000, "allocation": 11.1},
                {"type": "Cash", "value": 3000, "allocation": 6.7}
            ],
            "performance": {
                "ytd_return": 8.5,
                "one_year_return": 12.3,
                "three_year_return": 10.8
            }
        }
    
    def _generate_mock_debts(self):
        """Generate sample debt information"""
        return [
            {
                "type": "Credit Card",
                "balance": 3200,
                "interest_rate": 18.9,
                "minimum_payment": 96,
                "due_date": "2025-11-15"
            },
            {
                "type": "Student Loan",
                "balance": 18500,
                "interest_rate": 4.5,
                "minimum_payment": 180,
                "due_date": "2025-11-20"
            },
            {
                "type": "Auto Loan",
                "balance": 12000,
                "interest_rate": 5.2,
                "minimum_payment": 350,
                "due_date": "2025-11-10"
            }
        ]
    
    def _generate_mock_perks(self):
        """Generate sample banking perks and offers"""
        return [
            {
                "id": "perk_1",
                "name": "Cashback on Dining",
                "description": "Get 3% cashback on all dining purchases",
                "estimated_savings": 45.00,
                "category": "Dining",
                "status": "active"
            },
            {
                "id": "perk_2",
                "name": "Travel Points Bonus",
                "description": "Earn 2x points on travel bookings",
                "estimated_savings": 120.00,
                "category": "Travel",
                "status": "available"
            },
            {
                "id": "perk_3",
                "name": "Gas Rewards",
                "description": "Save 5 cents per gallon at partner stations",
                "estimated_savings": 30.00,
                "category": "Transportation",
                "status": "active"
            }
        ]
    
    def _generate_mock_advisors(self):
        """Generate sample financial advisors"""
        return [
            {
                "id": "advisor_1",
                "name": "Sarah Johnson",
                "specialty": "Retirement Planning",
                "rating": 4.8,
                "availability": "Available for appointments"
            },
            {
                "id": "advisor_2",
                "name": "Michael Chen",
                "specialty": "Investment Strategy",
                "rating": 4.9,
                "availability": "Next available: Nov 25"
            },
            {
                "id": "advisor_3",
                "name": "Emily Rodriguez",
                "specialty": "Debt Management",
                "rating": 4.7,
                "availability": "Available for appointments"
            }
        ]
    
    # Public methods for data access
    
    def get_user_profile(self):
        """Get user profile information"""
        return self.mock_data["user_profile"]
    
    def get_transactions(self, days=90):
        """Get transaction history"""
        return self.mock_data["transactions"][:days]
    
    def get_spending_by_category(self, days=90):
        """Get spending aggregated by category"""
        transactions = self.get_transactions(days)
        spending = {}
        for txn in transactions:
            category = txn["category"]
            spending[category] = spending.get(category, 0) + txn["amount"]
        return spending
    
    def get_goals(self):
        """Get financial goals"""
        return self.mock_data["goals"]
    
    def get_investments(self):
        """Get investment portfolio"""
        return self.mock_data["investments"]
    
    def get_debts(self):
        """Get debt information"""
        return self.mock_data["debts"]
    
    def get_net_worth(self):
        """Calculate net worth"""
        total_assets = self.mock_data["investments"]["total_value"]
        total_debts = sum(debt["balance"] for debt in self.mock_data["debts"])
        return {
            "total_assets": total_assets,
            "total_liabilities": total_debts,
            "net_worth": total_assets - total_debts
        }
    
    def get_perks(self):
        """Get banking perks and offers"""
        return self.mock_data["perks"]
    
    def get_advisors(self):
        """Get financial advisors"""
        return self.mock_data["advisors"]

# Global instance
bank_data = BankDataWrapper()