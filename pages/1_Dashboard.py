
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

try:
    from fpdf import FPDF
except ImportError:
    import os
    os.sysmtem('pip install fpdf2')
    from fpdf import FPDF

st.set_page_config(page_title='ThreadFlip Data Product Manager Dashboard', layout='wide')
st.title('ThreadFlip Data Product Manager Dashboard')
st.subheader('Smart Bundle Engine Lifecycle Analytics & ROI Validation Framework')

# Mock Data initialization for app state
if 'arpu' not in st.session_state:
    st.session_state.arpu = 45.50
if 'clv' not in st.session_state:
    st.session_state.clv = 240.00

# Sidebar Control Platform
st.sidebar.header('Global Operational Assumptions')
market_size = st.sidebar.number_input('Monthly Active Users (MAU)',value=120000,step=5000)
baseline_conv = st.sidebar.slider('Current Cart Conversion %',0.0,100.0,12.5) / 100
projected_lift = st.sidebar.slider('Expected Optimization Lift %',0.0,20.0,2.8) / 100

# Module 1: Feature Strategy Recommendation Generator & PDF Generator
st.header('1. Automated Feature Strategy Validation Board')
st.write('Evaluate engineering initiatives mapped directly to computed top-line marketplace financial opportunites')

feature_catalog = {
    'Smart Multi-Item Shipping Integration': {
        'Why': 'Bundling orders from identical sellers removes duplicate carrier costs, eliminating the main point of checkout drop-off.',
        'AOV_Impact': 5.50
    },
    'Dynamic Seller Showcase in Cart':{
        'Why': 'Prompts alternative listings within the viewport at the exact moment purchase intent is highest.',
        'AOV_Impact': 3.20
    }
}

selected_feat = st.selectbox('Select Candidate Feature to Analyze: ',list(feature_catalog.keys()))

# Calculations
current_monthly_orders = market_size * baseline_conv
optimized_conversion = baseline_conv + projected_lift
new_monthly_orders = market_size * optimized_conversion
delta_orders = new_monthly_orders - current_monthly_orders
potential_revenue_gain = (delta_orders * st.session_state.arpu) + (new_monthly_orders * feature_catalog[selected_feat]['AOV_Impact'])

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'### **Strategic Justification (The Why)**')
    st.info(feature_catalog[selected_feat]['Why'])

with col2:
    st.markdown(f'### **Financial Projection**')
    st.metric(label='Estimated Monthly Revenue Optimization', value=f'€{potential_revenue_gain:,.2f}',delta=f'+{(projected_lift*100):.1f}% Conversion Lift')


# PDF Generation Function
def create_pdf(title,rationale,money_gain):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.cell(40,10,'ThreadFlip Product Management Briefing')
    pdf.ln(15)
    pdf.set_font('Arial','',12)
    pdf.cell(40,10,f'Proposed Strategy Inititative: {title}')
    pdf.ln(10)
    pdf.multi_cell(10,10, f'Strategic Rationale: {rationale}')
    pdf.ln(10)
    pdf.set_font('Arial','B',12)
    pdf.cell(40,10,f'Projected Monthly Marketplace GMV Contribution: {money_gain:,.2f} EUR')
    return pdf.output(dest='S')

pdf_data = create_pdf(selected_feat,feature_catalog[selected_feat]['Why'],potential_revenue_gain)
st.download_button(label='📥 Export Product Initiative Briefing as PDF', data=BytesIO(pdf_data), file_name='Product_Initiative_Briefing.pdf',mime='application/pdf')

st.markdown('---')

# Moduler 2: Qualitative User Pain Point Word Cloud & Satisfaction (CSAT)
st.header('2. Customer Sentiment & Pain Point Breakdown')

col3, col4 = st.columns([2,1])

with col3:
    st.write('### **User Review Frequency Analysis**')
    word_freqs = {
        'shipping-fees': 95, 'seller-ghosting': 82, 'bundle-pricing': 70, 'size-mismatch': 45,
        'chat-latency': 30, 'return-policy': 55, 'counterfeit': 20, 'ui-clutter': 15
    }
    cloud_html = "".join([f"<span style='font-size: {size*0.5+12}pt; margin: 12px; display: inline-block; color: np.random.choice(['#2C3E50','#E74C3C','#3498DB']);'>{word}</span>" for word, size in word_freqs.items()])
    st.markdown(f"<div style='border: 1px solid #E0E0E0; border-radius: 8px; padding: 25px; text-align: center; background-color: #FAFAFA;'>{cloud_html}</div>",unsafe_allow_html=True)

with col4:
    st.write('### **Marketplace Mean CSAT**')
    mean_csat_score  = 7.4
    fig_gauge = go.Figure(go.Indicator(
        mode= 'gauge+number',
        value = mean_csat_score,
        domain= {'x':[0,1], 'y':[0,1]},
        title= {'text': 'Aggregated Rating (0-10)'},
        gauge = {
            'axis': {'range':[0,10]},
            'bar': {'color':'#3498DB'},
            'steps': [
                {'range':[0,5], 'color':'#FADBD8'},
                {'range': [5,8], 'color':'#FCF3CF'},
                {'range':[8,10], 'color':'#D4EFDF'}
            ]
        }
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=10,r=10,t=40,b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown('---')

# Module 3: ARPU & Customer Lifetime Value Segmentation Model$

st.header('3. Unit Economics Modeling Engine')

col5, col6, col7 = st.columns(3)

with col5:
    avg_order_value =st.number_input('Average Order Value (AOV) (€)', value=44.20, step=1.0)

with col6:
    purchase_freq = st.number_input('Annual Purchase Frequency (per User)',value=4.2,step=0.5)

with col7:
    churn_rate = st.slider('Monthly Logo Churn Rate %',1.0,30.0,5.5) / 100

# Re-compute indicators dynamically
computed_arpu = avg_order_value * (purchase_freq / 12)
computed_clv = computed_arpu / churn_rate

st.session_state.arpu = computed_arpu
st.session_state.clv = computed_clv

col8, col9 = st.columns(2)
with col8:
    st.metric(label = 'Calculated ARPU (Monthly)', value=f'€{st.session_state.arpu:.2f}')
with col9:
    st.metric(label='Modeled Customer Lifetime Value (CLV)', value=f'€{st.session_state.clv:.2f}')

