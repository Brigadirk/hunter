import os
import streamlit as st

def sidebar():
    with st.sidebar:

        st.markdown("## Welcome to Hunter's office.")

        st.image('app/ui_components/imgs/hunters.png')

        st.title('Set env variables')

        user_input = st.text_input('Enter your OpenAI API key:')

        if st.button('Set'):
            os.environ['OPENAI_API_KEY'] = user_input
            st.success(f'Environment variable set to: {user_input}')
