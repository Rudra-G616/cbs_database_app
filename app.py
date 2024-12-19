import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load the course database
data_path = 'merged_data.csv'  # Ensure this file is in the same directory or provide the full path
data = pd.read_csv(data_path)

# Streamlit app
st.title("CBS Database")

# Input field for course name or course code
user_input = st.text_input("Enter Course Name or Course Code:", "")

# Button to show details
if st.button("Show Details"):
    if user_input.strip() == "":
        st.warning("Please enter a valid course name or course code.")
    else:
        # Search for matching courses
        results = data[(data['Course Code'].str.contains(user_input, case=False, na=False)) |
                       (data['Course Name'].str.contains(user_input, case=False, na=False))]
        
        if not results.empty:
            st.success(f"Found {len(results)} matching course(s):")
            st.markdown("<p style='font-weight: bold; color: #2ad490;'>A CBS of 0 implies very poor grading while CBS of 10 implies extremely good grading.</p>", unsafe_allow_html=True)
            for index, row in results.iterrows():
                st.subheader(f"Course: {row['Course Name']} ({row['Course Code']})")

                # Display course details
                st.write(f"**Course Type**: {row['Course Type']}")

                # CBS Score as a scale with markings using Plotly
                st.write("### CBS Score")
                cbs_score = row['CBS']
                cbs_fig = go.Figure()
                cbs_fig.add_trace(go.Bar(
                    x=[cbs_score],
                    y=['CBS Score'],
                    orientation='h',
                    marker=dict(color='green' if cbs_score >= 8 else 'lightgreen' if cbs_score >= 6 else 'yellow' if cbs_score >= 4 else 'orange' if cbs_score >=2 else 'red'),  # Constant turquoise
                    width=0.4  # Reduces the thickness of the bar
                ))
                cbs_fig.update_layout(
                    xaxis=dict(
                        range=[0, 10],
                        tickvals=list(range(11)),
                        ticktext=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                    ),
                    yaxis=dict(showticklabels=False),
                    height=150,  # Reduces overall height
                    margin=dict(l=10, r=10, t=30, b=10),
                    title=f"CBS Score: {cbs_score:.2f}"
                )
                st.plotly_chart(cbs_fig, use_container_width=True)

                # Average Grade as a scale with markings using Plotly
                st.write("### Average Grade")
                avg_grade = row['Average Grade']
                avg_fig = go.Figure()
                avg_fig.add_trace(go.Bar(
                    x=[avg_grade - 4],
                    y=['Average Grade'],
                    orientation='h',
                    marker=dict(color='green' if avg_grade >= 8 else 'turquoise' if avg_grade >= 6 else 'yellow' if avg_grade >= 4 else 'red'),  
                    width=0.4  # Reduces the thickness of the bar
                ))
                avg_fig.update_layout(
                    xaxis=dict(
                        range=[0, 6],
                        tickvals=list(range(7)),
                        ticktext=["4", "5", "6", "7", "8", "9", "10"]
                    ),
                    yaxis=dict(showticklabels=False),
                    height=150,  # Reduces overall height
                    margin=dict(l=10, r=10, t=30, b=10),
                    title=f"Average Grade: {avg_grade:.2f}"
                )
                st.plotly_chart(avg_fig, use_container_width=True)

                st.divider()
        else:
            st.error("No matching course found. Please check the input.")





