import streamlit as st
import json
import time
import datetime

st.set_page_config(page_title='ThreadFlip Data PM',layout='wide')

# Initialize session state for cart and telemetry
if 'cart'not in st.session_state:
    st.session_state.cart = []
if 'telemetry_logs' not in st.session_state:
    st.session_state.telemetry_logs = []

def log_event(event_name, payload):
    st.session_state.telemetry_logs.insert(0,{
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'event_name': event_name,
        'payload': payload
    })

st.title('📱 ThreadFlip: Smart Bundle UI Prototype')
st.markdown('Interact with the mock app on the left. Watch the data contract generate on the right.')

st.markdown('---')

col_app, col_pm = st.columns([1.5,1])

# Left Column: The Front-end Mockup

with col_app:
    st.subheader('👕 Buyer UI: Item View')

    with st.container(border=True):
        st.image('https://images.unsplash.com/photo-1576995853123-5a10305d93c0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80', use_column_width=True)
        st.header('Vintage Levi\'s Denim Jacket - 90s')
        st.subheader('€45,00')
        st.write('Seller: --@vingtage_vault** | ⭐ 4.9 (120 sales)')
        st.write('Size: Large | Condition: Great | Shipping: €5,99')

        if st.button('🛒 Add to Cart',key='main_add'):
            st.session_state.cart.append(45.00)
            log_event('add_to_cart', {'product_id':'p_1001','is_bundle':False,'price': 45.00})
            st.success('Item added to cart!')

    st.write('')

    # The Smart Bundle Section
    st.markdown('### 🎁 Smart Bundle Engine Triggered')
    with st.container(border=True):
        st.info('💡 **Bundle & Save:**Add one more item form @vintage_vault to get 10% off your entire order and combined shipping!')

        if len(st.session_state.telemetry_logs) == 0 or st.session_state.telemetry_logs[0]['event_name'] != 'bundle_recommendation_rendered':
            log_event('bundle_recommendation_rendered', {'anchor_product_id':'p_1001',
             'seller_id':'vintage_vault',
             'algorithm_version':'v1.2_collaborative',
             'recommendation_shown':['p_8832','p_9102']
             })

        c1, c2 = st.columns(2)
        with c1:
            st.image('https://images.unsplash.com/photo-1596755094514-f87e32f85e98?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80')
            st.write('**Retro Graphic Tee**')
            st.write('€18,00')
            if st.button('Add to Bundle', key='bundle_1'):
                st.session_state.cart.append(18.00)
                log_event('bundle_item_added',{'product_id':'p_8832','is_bundle':True,'price':18.00})
                st.success('Bundle activated!')

        with c2:
            st.image('https://images.unsplash.com/photo-1556821840-3a63f95609a7?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80')
            st.write('**Nike Hoodie -Y2K**')
            st.write('€32,00')
        if st.button('Add to Bundle', key='bundle_2'):
            st.session_state.cart.append(32.00)
            log_event('bundle_item_added',{'product_id':'p_9102','is_bundle':True,'price':32.00})
            st.success('Bundle activated!')



# Right Column: The Data Product Manager Console

with col_pm:
    st.subheader('⚙️ Data Product Manager Debug Console')

    # Financial Impact Calculator
    st.markdown('### Live Cart Analytics')
    cart_total = sum(st.session_state.cart)
    is_bundle = len(st.session_state.cart) > 1

    if is_bundle:
        discount = cart_total * 0.10
        final_total = cart_total - discount
        st.metric('Total Cart Value', f'€{final_total:.2f}',delta=f'+ €{cart_total - 45.00:.2f} (Upsell)')
        st.metric('Total Discount Applied', f'€{discount:.2f}',delta='-10%',delta_color='inverse')
    else:
        st.metric('Total Cart Value', f'€{cart_total:.2f}')
    
    st.markdown('---')

    st.markdown('### 📡 Live JSON Telemetry Stream')
    st.write('Display the data contract payload being fired to BigQuery/MixPanel.')

    if st.button('Clear Logs'):
        st.session_state.telemetry_logs = []
        st.rerun
    
    for log in st.session_state.telemetry_logs:
        with st.expander(f'Event: {log["event_name"]}', expanded=True):
            st.json(log)