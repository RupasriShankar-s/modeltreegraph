import os
import streamlit as st

# Ensure Graphviz binary is discoverable
os.environ["PATH"] += os.pathsep + '/usr/bin'

from graphviz import Digraph

st.set_page_config(page_title="Model Tree Generator", layout="centered")

st.title("🧠 Model Transformation Tree")

if "transformations" not in st.session_state:
    st.session_state.transformations = []

with st.form("add_relationship"):
    st.subheader("➕ Add a Model Relationship")
    col1, col2, col3 = st.columns(3)
    with col1:
        input_model = st.text_input("Input Model", placeholder="e.g., Model A")
    with col2:
        transformation = st.selectbox(
            "Transformation Type",
            [
                "4-bit quantization",
                "8-bit quantization",
                "fine-tuned from",
                "distilled from",
                "merged from",
                "adapter on",
                "converted from",
                "continued pretraining",
                "custom (enter below)",
            ],
        )
    with col3:
        output_model = st.text_input("Output Model", placeholder="e.g., Model B")

    custom_transform = st.text_input("Custom Transformation (optional)")
    submit = st.form_submit_button("Add to Tree")

    if submit:
        if not input_model or not output_model:
            st.warning("Please enter both input and output model names.")
        else:
            t_type = custom_transform.strip() if custom_transform else transformation
            st.session_state.transformations.append(
                {"input": input_model.strip(), "transformation": t_type, "output": output_model.strip()}
            )
            st.success(f"Added: {input_model} → {output_model} ({t_type})")

if st.session_state.transformations:
    st.subheader("📄 Current Relationships")
    st.table(st.session_state.transformations)

if st.session_state.transformations:
    st.subheader("🌳 Model Tree Visualization")
    dot = Digraph(format="png")
    dot.attr("node", shape="box", style="filled", color="lightblue2", fontname="Arial")

    for rel in st.session_state.transformations:
        dot.node(rel["input"])
        dot.node(rel["output"])
        dot.edge(rel["input"], rel["output"], label=rel["transformation"])

    st.graphviz_chart(dot)

if st.button("🔁 Reset All"):
    st.session_state.transformations = []
    st.success("Reset complete.")
