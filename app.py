
import streamlit as st
from recommendation import recommend_schemes

st.set_page_config(
    page_title="Scholarship Finder India",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Scholarship Finder India")
st.write(
    "Find student scholarships based on your education, "
    "state, family income, age, and other eligibility details."
)

st.info(
    "Recommendations are preliminary matches. Always verify "
    "eligibility and application dates on the official website."
)

st.subheader("👩‍🎓 Student Profile")

with st.form("scholarship_form"):
    col1, col2 = st.columns(2)

    with col1:
        state = st.selectbox(
            "State / Union Territory",
            [
                "Karnataka",
                "Andhra Pradesh",
                "Telangana",
                "Tamil Nadu",
                "Kerala",
                "Maharashtra",
                "Other",
            ],
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=20,
            step=1,
        )

        education_level = st.selectbox(
            "Current education level",
            [
                "School",
                "PUC / Class 11–12",
                "Diploma / ITI",
                "Undergraduate",
                "Postgraduate",
                "Research",
                "Other",
            ],
        )

    with col2:
        social_category = st.selectbox(
            "Social category",
            ["Not specified", "General", "OBC", "SC", "ST", "Other"],
        )

        gender = st.selectbox(
            "Gender",
            ["Not specified", "Male", "Female", "Other"],
        )

        annual_income = st.number_input(
            "Annual family income (₹)",
            min_value=0,
            max_value=100000000,
            value=200000,
            step=10000,
        )

    keywords = st.text_input(
        "Optional scholarship keywords",
        placeholder="e.g. engineering, merit, hostel",
    )

    submitted = st.form_submit_button(
        "🔍 Find Scholarships",
        type="primary",
        use_container_width=True,
    )

if submitted:
    profile = {
        "state": state,
        "age": age,
        "education_level": education_level,
        "social_category": social_category,
        "gender": gender,
        "annual_income": annual_income,
    }

    st.divider()
    st.subheader("🎯 Matching Scholarships")

    try:
        schemes = recommend_schemes(
            user_query=keywords,
            profile=profile,
            limit=20,
        )

        if not schemes:
            st.warning(
                "No matching scholarships were found. Try "
                "'Not specified' for optional fields, or check "
                "the eligibility rules in schemes.csv."
            )

        else:
            st.success(
                f"Found {len(schemes)} potential matching scholarship(s)."
            )

            for index, scheme in enumerate(schemes, start=1):
                with st.container(border=True):
                    st.markdown(
                        f"### {index}. {scheme['scheme_name']}"
                    )

                    st.caption(
                        f"Type: {scheme.get('category') or 'Scholarship'}"
                    )

                    st.write(
                        scheme.get("description")
                        or "Description not provided."
                    )

                    st.markdown("**Eligibility details**")
                    st.write(
                        scheme.get("eligibility")
                        or "Please check the official website."
                    )

                    if scheme.get("min_age"):
                        st.write(f"Minimum age: {scheme['min_age']}")

                    if scheme.get("max_age"):
                        st.write(f"Maximum age: {scheme['max_age']}")

                    if scheme.get("max_income"):
                        st.write(
                            "Maximum annual family income: ₹"
                            + scheme["max_income"]
                        )

                    st.caption(
                        f"Keyword matches: {scheme['match_score']} "
                        "(not an eligibility percentage)"
                    )

                    link = scheme.get("official_link", "").strip()

                    if link.startswith(("https://", "http://")):
                        st.link_button(
                            "🌐 Visit Scholarship Website",
                            link,
                        )
                    else:
                        st.warning(
                            "No valid official website is provided "
                            "for this record."
                        )

                    st.caption(
                        "Verify the latest eligibility rules, deadlines, "
                        "documents, and application process before applying."
                    )

    except (FileNotFoundError, ValueError) as error:
        st.error(str(error))

    except Exception as error:
        st.error(f"An unexpected error occurred: {error}")

st.divider()
st.caption("Scholarship Finder India | Student Scholarship Search")
