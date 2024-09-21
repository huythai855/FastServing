import streamlit as st
import requests
from click import option

st.write('Detail of your deployment in the cluster')

st.text("")
st.text("")


deployments = requests.get('http://127.0.0.1:1409/api/deployments/').json()
# st.write(deployments)

deployments_names = []
for deployment in deployments:
    deployment_name = list(deployment.keys())[0]
    deployments_names += [deployment_name]

option = st.selectbox(
    'Select a deployment',
    deployments_names
)

submitted = st.button("Get details")
if submitted:
    st.text("")

    detail = requests.get(f'http://127.0.0.1:1409/api/deployments/describe/{option}').json()


    box1 = st.container(border=True)
    box2 = st.container(border=True)
    box3 = st.container(border=True)

    with box1:
        st.write("### Deployment Details")
        st.write(f"**Name:** {detail['name']}")
        st.write(f"**Namespace:** {detail['namespace']}")
        st.write(f"**Creation Timestamp:** {detail['creation_timestamp']}")
        st.write(f"**Labels:** {detail['labels']}")
        st.write(f"**Annotations:** {detail['annotations']}")
        st.write(f"**Selector:** {detail['selector']}")
        st.write(f"**Replicas:** {detail['replicas']}")
        st.write(f"**Strategy Type:** {detail['strategy_type']}")
        st.write(f"**Min Ready Seconds:** {detail['min_ready_seconds']}")
        st.write(f"**Rolling Update Strategy:** {detail['rolling_update_strategy']}")

    with box2:
        st.write("### Pod Template")
        st.write(f"**Labels:** {detail['pod_template']['labels']}")
        st.write(f"**Container Image:** {detail['pod_template']['containers']['image']}")
        st.write(f"**Container Port:** {detail['pod_template']['containers']['port']}")
        st.write(f"**Host Port:** {detail['pod_template']['containers']['host_port']}")
        st.write(f"**Liveness Probe:** {detail['pod_template']['containers']['liveness_probe']}")
        st.write(f"**Readiness Probe:** {detail['pod_template']['containers']['readiness_probe']}")
        st.write(f"**Mounts:** {detail['pod_template']['containers']['mounts']}")



    with box3:
        st.write("### Conditions")
        for condition in detail['conditions']:
            st.write(f"**Type:** {condition['type']}")
            st.write(f"**Status:** {condition['status']}")
            st.write(f"**Reason:** {condition['reason']}")
            st.text("")
        st.write(f"**Old Replica Sets:** {detail['old_replica_sets']}")
        st.write(f"**New Replica Set:** {detail['new_replica_set']}")
        st.write(f"**Events:** {detail['events']}")






