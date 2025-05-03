from flask import Blueprint, render_template, request
import requests
import os
from datetime import datetime
from .models import SearchHistory, db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    cve_data = []
    error = None
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

    if request.method == 'POST':
        keyword = request.form.get('keyword')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        api_key = os.environ.get('NVD_API_KEY')

        headers = {
            'apiKey': api_key
        }

        params = {
            'keywordSearch': keyword,
            'resultsPerPage': 10
        }
        if start_date:
            params['pubStartDate'] = f"{start_date}T00:00:00:000 UTC-00:00"
        if end_date:
            params['pubEndDate'] = f"{end_date}T23:59:59:999 UTC-00:00"

        try:
            response = requests.get('https://services.nvd.nist.gov/rest/json/cves/2.0', headers=headers, params=params)

            if response.status_code == 200:
                json_data = response.json()
                cve_data = json_data.get('vulnerabilities', [])

                # Count severities safely
                for item in cve_data:
                    metrics = item['cve'].get('metrics', {})
                    if 'cvssMetricV31' in metrics:
                        severity = metrics['cvssMetricV31'][0]['cvssData'].get('baseSeverity', '').upper()
                        if severity in severity_counts:
                            severity_counts[severity] += 1
                # Save search history
                new_search = SearchHistory(
                keyword=keyword,
                start_date=start_date or '',
                end_date=end_date or ''
                )
                db.session.add(new_search)
                db.session.commit()

            elif response.status_code == 404:
                cve_data = []
            else:
                error = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            error = f"Exception occurred: {str(e)}"
    # Fetch history for display
    history = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(10).all()
    return render_template('index.html', cve_data=cve_data, error=error, severity_counts=severity_counts, history=history)
