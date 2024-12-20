import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load the course database
data_path = 'merged_data.csv'  
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
            st.markdown("<p style='font-weight: bold; color: #2bd9ad; padding: 5px; border-radius: 5px;'>A CBS of 0 implies very poor grading while CBS of 10 implies extremely good grading.</p>", unsafe_allow_html=True)
            for index, row in results.iterrows():
                st.subheader(f"Course: {row['Course Name']} ({row['Course Code']})")

                # Display course details
                st.write(f"**Course Type**: {row['Course Type']}")

                # CBS Score as a scale with gradient dots and markers
                st.write("### CBS Score")
                cbs_score = row['CBS']
                cbs_fig = go.Figure()

                # Gradient dots for CBS scale
                gradient_colors = [[0, 'red'], [0.25, 'orange'], [0.5, 'yellow'], [0.75, 'lightgreen'], [1, 'green']]
                x_values = np.linspace(0, 10, 50)
                colors = [gradient_colors[int(i * (len(gradient_colors) - 1) / 10)][1] for i in x_values]

                cbs_fig.add_trace(go.Scatter(
                    x=x_values,
                    y=[0] * len(x_values),
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=colors,
                        colorscale=gradient_colors
                    ),
                    showlegend=False
                ))

                # Add CBS point marker
                cbs_fig.add_trace(go.Scatter(
                    x=[cbs_score],
                    y=[0],
                    mode='markers+text',
                    marker=dict(size=14, color='black'),
                    text=[f"{cbs_score:.2f}"],
                    textposition='top center',
                    name = 'CBS Score'
                ))

                # Update layout for CBS scale
                cbs_fig.update_layout(
                    xaxis=dict(
                        range=[0, 10],
                        tickvals=[0, 2.5, 5, 7.5, 10],
                        ticktext=["Very Bad", "Bad", "Okay", "Good", "Very Good"],
                        showgrid=False
                    ),
                    yaxis=dict(showticklabels=False),
                    height=150,  
                    margin=dict(l=10, r=10, t=30, b=10),
                    title=f"CBS Score: {cbs_score:.2f}"
                )
                st.plotly_chart(cbs_fig, use_container_width=True)

                # Average Grade as a scale with markings using Plotly
                st.write("### Average Grade")
                avg_grade = row['Average Grade']
                avg_fig = go.Figure()
                avg_fig.add_trace(go.Bar(
                    x=[avg_grade],
                    y=['Average Grade'],
                    orientation='h',
                    marker=dict(color='turquoise'), 
                    width=0.2  
                ))
                avg_fig.update_layout(
                    xaxis=dict(
                        range=[0, 10],
                        tickvals=list(range(11)),
                        ticktext=["4", "5", "6", "7", "8", "9", "10"]
                    ),
                    yaxis=dict(showticklabels=False),
                    height=150,  
                    margin=dict(l=10, r=10, t=30, b=10),
                    title=f"Average Grade: {(avg_grade):.2f}"
                )
                st.plotly_chart(avg_fig, use_container_width=True)

                st.divider()
        else:
            st.error("No matching course found. Please check the input.")





