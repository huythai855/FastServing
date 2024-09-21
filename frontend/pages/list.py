import requests
import streamlit as st
from numpy.ma.core import empty


st.write('List of deployments running on your cluster')
st.text("")
st.text("")

deployments = requests.get('http://127.0.0.1:1409/api/deployments/').json()

container = []
box = st.container(border=True)
empty_string = ""

for deployment in deployments:
    # st.write(deployment)
    deployment_name = list(deployment.keys())[0]
    deployment_info = deployment[deployment_name]
    box = st.container(border=True)
    container.append(box)
    col1, col2 = box.columns(2)
    with col1:
        st.markdown(
            f"""
                #### {deployment_name}
                **Age**: {deployment_info['AGE']}
    
                **Available**: {deployment_info['AVAILABLE']}
            """
        )
    with col2:
        st.markdown(
            f"""
                        #### {empty_string}

                        **Readiness**: {deployment_info['READY']}

                        **Up-to-date**: {deployment_info['UP-TO-DATE']}
                    """
        )

    box.link_button("View details", "http://localhost:8501/detail")