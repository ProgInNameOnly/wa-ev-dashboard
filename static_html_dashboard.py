import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html

# Function to generate an HTML dashboard with static charts
def generate_dashboard():
    try:
        # Load the EV data
        df = pd.read_csv('attached_assets/Electric_Vehicle_Population_Data.csv')
        
        # Simple preprocessing
        df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
        df = df.dropna(subset=['Model Year'])
        
        # Generate static charts
        charts_html = []
        
        # 1. Top Makes Chart
        make_counts = df['Make'].value_counts().head(10).reset_index()
        make_counts.columns = ['Make', 'Count']
        
        fig1 = px.bar(
            make_counts,
            x='Count',
            y='Make',
            orientation='h',
            title='Top 10 EV Manufacturers',
            color_discrete_sequence=['#FF5E5E'] * len(make_counts)
        )
        fig1.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_color='black'
        )
        charts_html.append(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        
        # 2. Top Models Chart
        model_counts = df.groupby(['Make', 'Model']).size().reset_index(name='Count')
        model_counts = model_counts.sort_values('Count', ascending=False).head(10)
        model_counts['Full Model'] = model_counts['Make'] + ' ' + model_counts['Model']
        
        fig2 = px.bar(
            model_counts,
            x='Count',
            y='Full Model',
            orientation='h',
            title='Top 10 EV Models',
            color_discrete_sequence=['#00B0FF'] * len(model_counts)
        )
        fig2.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_color='black'
        )
        charts_html.append(fig2.to_html(full_html=False, include_plotlyjs=False))
        
        # 3. County Distribution
        county_counts = df['County'].value_counts().head(15).reset_index()
        county_counts.columns = ['County', 'Count']
        
        fig3 = px.bar(
            county_counts,
            x='County',
            y='Count',
            title='EV Distribution by County',
            color_discrete_sequence=['#FFD166'] * len(county_counts)
        )
        fig3.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_color='black',
            xaxis_tickangle=-45
        )
        charts_html.append(fig3.to_html(full_html=False, include_plotlyjs=False))
        
        # 4. EV Type Distribution
        ev_type_counts = df['Electric Vehicle Type'].value_counts().reset_index()
        ev_type_counts.columns = ['Type', 'Count']
        
        fig4 = px.pie(
            ev_type_counts,
            names='Type',
            values='Count',
            title='EV Type Distribution',
            color_discrete_sequence=['#FF5E5E', '#00B0FF']
        )
        fig4.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_color='black'
        )
        charts_html.append(fig4.to_html(full_html=False, include_plotlyjs=False))
        
        # 5. Year Trend
        year_counts = df.groupby('Model Year').size().reset_index(name='Count')
        year_counts = year_counts.sort_values('Model Year')
        
        fig5 = px.line(
            year_counts,
            x='Model Year',
            y='Count',
            markers=True,
            title='EV Adoption by Year',
            color_discrete_sequence=['#FF00FF']
        )
        fig5.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font_color='black'
        )
        charts_html.append(fig5.to_html(full_html=False, include_plotlyjs=False))
        
        # Create the HTML dashboard
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Washington State EV Population Dashboard</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    text-align: center;
                    padding: 20px 0;
                    background-color: #333;
                    color: white;
                    margin-bottom: 20px;
                    border-radius: 5px;
                }}
                .chart-container {{
                    background-color: white;
                    padding: 15px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .row {{
                    display: flex;
                    flex-wrap: wrap;
                    margin: 0 -10px;
                }}
                .column {{
                    flex: 50%;
                    padding: 0 10px;
                    box-sizing: border-box;
                }}
                @media screen and (max-width: 800px) {{
                    .column {{
                        flex: 100%;
                    }}
                }}
                .footer {{
                    text-align: center;
                    padding: 20px 0;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Washington State EV Population Dashboard</h1>
                <p>Analysis of Electric Vehicle Population Data</p>
            </div>
            
            <div class="row">
                <div class="column">
                    <div class="chart-container">
                        <h2>Top EV Manufacturers</h2>
                        {charts_html[0]}
                    </div>
                    
                    <div class="chart-container">
                        <h2>Top EV Models</h2>
                        {charts_html[1]}
                    </div>
                </div>
                
                <div class="column">
                    <div class="chart-container">
                        <h2>County Distribution</h2>
                        {charts_html[2]}
                    </div>
                    
                    <div class="chart-container">
                        <h2>EV Type Distribution</h2>
                        {charts_html[3]}
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>EV Adoption Trend</h2>
                {charts_html[4]}
            </div>
            
            <div class="footer">
                <p>Data source: Electric Vehicle Population Data from Washington State Department of Licensing</p>
            </div>
        </body>
        </html>
        """
        
        # Write to file
        with open('ev_dashboard.html', 'w') as f:
            f.write(html_content)
        
        print("Dashboard HTML file created successfully: ev_dashboard.html")
        return True
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        return False


# Create a simple server to serve the static HTML file
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def serve_dashboard():
    # Generate the dashboard if it doesn't exist
    try:
        generate_dashboard()
        return send_file('ev_dashboard.html')
    except Exception as e:
        return f"Error serving dashboard: {e}"

if __name__ == '__main__':
    # Generate the dashboard first
    if generate_dashboard():
        print("Starting server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Dashboard generation failed. Please check errors above.")