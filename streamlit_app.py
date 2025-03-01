import streamlit as st
import cohere

co = cohere.Client(st.secrets["COHERE_API_KEY"])  # Replace with your actual API key

st.title("ROI Measurement for Sponsorship Deal")
st.markdown("""
This app helps you measure the ROI of your sponsorship deal with a university’s entrepreneurship cell by combining quantitative metrics (like revenue figures) and qualitative insights (like brand sentiment).
""")

# Sidebar: Input Parameters
st.sidebar.header("Input Parameters")
sponsorship_cost = st.sidebar.number_input("Enter Sponsorship Cost ($):", min_value=0.0, value=10000.0, step=500.0)
direct_revenue = st.sidebar.number_input("Enter Direct Revenue Generated ($):", min_value=0.0, value=15000.0, step=500.0)
indirect_benefits = st.sidebar.number_input("Enter Estimated Indirect Benefits ($):", min_value=0.0, value=5000.0, step=500.0)

st.sidebar.header("Additional KPIs (Optional)")
social_media_impressions = st.sidebar.number_input("Social Media Impressions:", min_value=0, value=10000, step=1000)
website_visits = st.sidebar.number_input("Additional Website Visits:", min_value=0, value=500, step=50)
media_mentions = st.sidebar.number_input("Media Mentions:", min_value=0, value=5, step=1)

# Calculate Total Value and ROI
total_value = direct_revenue + indirect_benefits
roi = (total_value - sponsorship_cost) / sponsorship_cost if sponsorship_cost > 0 else 0

st.header("ROI Calculation Results")
st.write(f"**Total Value Generated:** ${total_value:,.2f}")
st.write(f"**ROI:** {roi*100:.2f}%")

# Qualitative Assessment Section
st.header("Qualitative Assessment")
brand_sentiment = st.slider("Rate the Brand Sentiment Impact (1 = low, 10 = high):", min_value=1, max_value=10, value=5)
st.write("Brand Sentiment Score:", brand_sentiment)

st.markdown("""
### How to Interpret These Results:
- **ROI Calculation:** A positive ROI indicates that the sponsorship is generating more value than it costs. You can simulate different scenarios by adjusting the input parameters.
- **Brand Sentiment:** The qualitative score provides insight into how the sponsorship impacts your brand’s perception among the target audience.
- **Additional KPIs:** Metrics like social media impressions, website visits, and media mentions help quantify the broader impact on brand awareness.
""")

# Cohere Integration: Generate a Summary Report using AI
st.header("Generate Summary Report")
if st.button("Generate Report"):
    prompt_text = f"""
    Write a brief and professional summary report for a sponsorship ROI analysis. 
    The sponsorship cost is ${sponsorship_cost:,.2f}, the direct revenue is ${direct_revenue:,.2f}, 
    and the estimated indirect benefits are ${indirect_benefits:,.2f}. 
    The total value generated is ${total_value:,.2f} with an ROI of {roi*100:.2f}%. 
    The brand sentiment score is {brand_sentiment} out of 10.
    Mention key insights and recommendations based on these numbers.
    """
    response = co.generate(
        model='xlarge',
        prompt=prompt_text,
        max_tokens=150,
        temperature=0.7,
    )
    summary_report = response.generations[0].text.strip()
    st.subheader("Summary Report")
    st.write(summary_report)

st.markdown("""
### Next Steps:
- **Refinement:** Integrate additional data sources and KPIs to further refine your ROI calculations.
- **Comparison:** Use this tool to compare different sponsorship opportunities or track changes over time.
- **Feedback:** Gather post-event feedback to correlate these numbers with actual market impact.
""")
