Here's an explanation of the project directory and what's being used:

Currently Active Files
hybrid_dash_app.py: This is the main application file currently running in the "Hybrid Dash" workflow. It contains our complete dashboard with interactive tabs, filters, and charts using a special approach that embeds Plotly charts as iframes within the Dash framework to solve rendering issues.
attached_assets/Electric_Vehicle_Population_Data.csv: The dataset being used for the visualizations.
Supporting Files
data_processor.py: Contains functions for preprocessing the EV dataset.
visualizations.py: Contains functions for creating various chart types and applying the custom theme.
Files from Earlier Iterations (not actively used)
app.py: Original Streamlit dashboard (before conversion to Dash).
dash_app.py: Initial Dash conversion that had rendering issues.
basic_dashboard.py: Simplified test dashboard with fewer features.
simple_dash_test.py: Minimal test dashboard for debugging rendering issues.
static_html_dashboard.py: The static HTML fallback dashboard approach we tried.
test_plotly.py: Single-chart test file used to verify Plotly behavior.
ev_dashboard.html: Generated static HTML dashboard output.
Style and Asset Files
custom.css: Custom styling for the dashboard.
assets/: Directory for static assets.
attached_assets/*.png: Image files for reference/documentation.
Framework Transition
We started with Streamlit (app.py), then attempted a direct conversion to Plotly/Dash (dash_app.py) but encountered rendering issues. After several test approaches (basic_dashboard.py, simple_dash_test.py), we discovered that Plotly charts work correctly as static HTML but not within normal Dash components.

Our current solution (hybrid_dash_app.py) uses a hybrid approach: it maintains the Dash framework for the UI structure but embeds Plotly charts as iframes to ensure proper rendering while preserving your dark theme color scheme (cambridge-blue, charcoal, dark-slate-gray, eerie-black, night).

The dashboard now includes:

Tabbed interface for organized content
Interactive filtering options
Key statistics displayed prominently
Charts properly rendered with your custom dark theme
