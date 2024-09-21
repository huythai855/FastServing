import streamlit as st
import requests
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
from tensorflow.python.ops.inplace_ops import empty

st.write('Welcome to FastServing, where you can deploy your models in seconds on your own infrastructure!')


deployments = requests.get('http://127.0.0.1:1409/api/deployments/').json()
# st.write(deployments)

pod_count = 0
ready_count = 0

deployments_names = []
deployments_pod = []




for deployment in deployments:
    # st.write(deployment)
    deployment_name = list(deployment.keys())[0]
    deployments_names += [deployment_name]
    deployment_info = deployment[deployment_name]

    print(deployment_info['READY'].split('/'))
    pod_count += int(deployment_info['READY'].split('/')[1])
    deployments_pod += [int(deployment_info['READY'].split('/')[1])]
    ready_count += int(deployment_info['READY'].split('/')[0])

    #deployment_info['AGE'] "27h"
    #deployment_info['AVAILABLE'] "0"
    #deployment_info['READY'] "0/2"
    #deployment_info['UP-TO-DATE'] "2"



col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
            # Deployments
            ## {len(deployments)}
        """
    )


with col2:
    st.markdown(
        f"""
                # Pods
                ## {pod_count}
            """
    )

with col3:
    st.markdown(
        f"""
                # Ready
                ## {ready_count}
            """
    )

st.text("")
st.text("")

chartbox1, chartbox2 = st.columns(2)

with chartbox1:
    st.markdown("#### Pod using")
    bar_width = 0.35
    spacing = 0.2
    fig2 = plt.figure(figsize=(10, 5))
    plt.bar(deployments_names, deployments_pod, width=bar_width)
    plt.xlabel('Deployments')
    plt.ylabel('Pods')
    st.pyplot(fig2)

with chartbox2:
    pass


