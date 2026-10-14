🎓 Scholarship Finder India

Scholarship Finder India is a Python-based web application that helps students discover scholarships based on their personal profile and eligibility criteria.

The application uses student details such as state, age, education level, social category, gender, and annual family income to identify potentially matching scholarships.

✨ Features

- 👩‍🎓 Student-focused scholarship recommendations
- 📍 State-based eligibility matching
- 🎓 Education-level filtering
- 👥 Social category and gender matching
- 💰 Annual family income eligibility checks
- 🔎 Keyword-based search and ranking
- 🔗 Links to official scholarship websites
- 🖥️ Simple and interactive interface using Streamlit

🛠️ Technologies Used

- Python
- Streamlit
- Pandas (if used in the implementation)
- CSV for scholarship data storage

📁 Project Structure

```text
ScholarshipFinder/
├── app.py
├── recommendation.py
├── schemes.csv
├── README.md
└── .gitignore
```

⚙️ Installation and Setup
 1. Install Python

Download Python from https://www.python.org/downloads/

 2. Install the required package

Open a terminal in the project folder and run:

```bash
python -m pip install streamlit
```
 3. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

http://localhost:8501
 🔍 How It Works

1. Students enter their profile details.
2. The application compares the profile with scholarship eligibility criteria in `schemes.csv`.
3. Matching scholarships are displayed with descriptions and eligibility details.
4. Students can follow the provided links to explore official scholarship information.
 📊 Scholarship Dataset

Scholarship information is stored in `schemes.csv`, including:

- Scheme name and category
- Description and eligibility
- Official website
- Education levels and states
- Minimum and maximum age
- Maximum family income
- Social categories and genders

**Note:** Demo records are used for testing. They are not verified scholarship opportunities. Replace them with accurate scheme information and confirm eligibility on official government websites before relying on recommendations.
 🚀 Future Improvements

- Add verified government and state scholarship datasets.
- Improve search and filtering options.
- Add scholarship application deadlines.
- Deploy the application online.
- Add automated data validation and regular updates.
 🎯 Project Objective

The objective is to simplify scholarship discovery for students by matching their profiles against available eligibility information in one convenient application.
 ⚠️ Disclaimer

This is an educational project and is not an official government service. Scholarship availability, deadlines, and eligibility requirements should always be verified through the relevant official website.
