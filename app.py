from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import data_manager
import reporter
import utils
import constants
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve static files
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Routes
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses"""
    try:
        expenses = data_manager.load_data()
        return jsonify({
            'success': True,
            'data': expenses,
            'total': len(expenses)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    """Add a new expense"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['amount', 'category']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Validate amount
        if not utils.validate_amount(str(data['amount'])):
            return jsonify({'success': False, 'error': 'Invalid amount'}), 400
        
        # Validate category
        if not utils.validate_category(data['category'].lower()):
            return jsonify({'success': False, 'error': 'Invalid category'}), 400
        
        # Validate date if provided
        date = data.get('date', utils.current_date())
        if date and not utils.validate_date(date):
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400
        
        # Add the expense
        data_manager.add_new_exp(
            amount=float(data['amount']),
            category=data['category'].lower(),
            description=data.get('description', '')
        )
        
        return jsonify({'success': True, 'message': 'Expense added successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an existing expense"""
    try:
        data = request.get_json()
        
        # Validate fields if provided
        if 'amount' in data and not utils.validate_amount(str(data['amount'])):
            return jsonify({'success': False, 'error': 'Invalid amount'}), 400
        
        if 'category' in data and not utils.validate_category(data['category'].lower()):
            return jsonify({'success': False, 'error': 'Invalid category'}), 400
        
        if 'date' in data and not utils.validate_date(data['date']):
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400
        
        # Update the expense
        success = data_manager.edit_expense(
            target_id=expense_id,
            new_date=data.get('date', ''),
            new_amount=data.get('amount', ''),
            new_category=data.get('category', '').lower() if data.get('category') else '',
            new_description=data.get('description', '')
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Expense updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Expense not found or no changes made'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        expenses = data_manager.load_data()
        expense_exists = any(exp['id'] == expense_id for exp in expenses)
        
        if not expense_exists:
            return jsonify({'success': False, 'error': 'Expense not found'}), 404
        
        # Delete the expense (modify delete_expense to not ask for confirmation)
        new_expenses = [exp for exp in expenses if exp['id'] != expense_id]
        data_manager.save_exp(new_expenses)
        
        return jsonify({'success': True, 'message': 'Expense deleted successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses/filter/category/<category>', methods=['GET'])
def filter_by_category(category):
    """Filter expenses by category"""
    try:
        if not utils.validate_category(category.lower()):
            return jsonify({'success': False, 'error': 'Invalid category'}), 400
        
        expenses = data_manager.load_data()
        filtered = [exp for exp in expenses if exp.get('category') == category.lower()]
        sorted_expenses = utils.sort_by_date(filtered)
        total = reporter.total_expense(sorted_expenses)
        
        return jsonify({
            'success': True,
            'data': sorted_expenses,
            'total': total,
            'count': len(sorted_expenses)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses/filter/date', methods=['POST'])
def filter_by_date():
    """Filter expenses by date range"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'success': False, 'error': 'Start date and end date are required'}), 400
        
        if not utils.validate_date(start_date) or not utils.validate_date(end_date):
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400
        
        expenses = data_manager.load_data()
        filtered = [exp for exp in expenses if start_date <= exp['date'] <= end_date]
        sorted_expenses = utils.sort_by_date(filtered)
        total = reporter.total_expense(sorted_expenses)
        
        return jsonify({
            'success': True,
            'data': sorted_expenses,
            'total': total,
            'count': len(sorted_expenses)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/summary/monthly', methods=['GET'])
def monthly_summary():
    """Get monthly expense summary"""
    try:
        summary = reporter.summarize_by_month()
        expenses = data_manager.load_data()
        total = reporter.total_expense(expenses)
        
        return jsonify({
            'success': True,
            'data': summary,
            'total': total
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/summary/category', methods=['GET'])
def category_summary():
    """Get category expense summary"""
    try:
        summary = reporter.summarize_by_category()
        expenses = data_manager.load_data()
        total = reporter.total_expense(expenses)
        
        return jsonify({
            'success': True,
            'data': summary,
            'total': total
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        expenses = data_manager.load_data()
        
        # Calculate various statistics
        total_expenses = reporter.total_expense(expenses)
        total_count = len(expenses)
        
        # Current month expenses
        current_month = datetime.now().strftime('%Y-%m')
        current_month_expenses = [exp for exp in expenses if exp['date'].startswith(current_month)]
        current_month_total = reporter.total_expense(current_month_expenses)
        
        # Last 7 days expenses
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        recent_expenses = [exp for exp in expenses if exp['date'] >= seven_days_ago]
        recent_total = reporter.total_expense(recent_expenses)
        
        # Top category
        category_summary = reporter.summarize_by_category()
        top_category = max(category_summary, key=category_summary.get) if category_summary else None
        
        return jsonify({
            'success': True,
            'data': {
                'total_expenses': total_expenses,
                'total_count': total_count,
                'current_month_total': current_month_total,
                'current_month_count': len(current_month_expenses),
                'recent_total': recent_total,
                'recent_count': len(recent_expenses),
                'top_category': top_category,
                'categories': category_summary
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get valid categories"""
    return jsonify({
        'success': True,
        'data': constants.VALID_CATEGORY
    })

if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    app.run(debug=True, host='0.0.0.0', port=5000)