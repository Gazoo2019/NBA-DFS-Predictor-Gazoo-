# Setup Instructions
---
## Create environment 

To create the working environment, open GitBash and create the following environment by running the following:

<code> conda update conda </code> 

<code> conda create -n Gazoo python=3.7 anaconda </code>

<code> conda activate Gazoo </code>

Install the following libraries by using either

<code> conda install </code> 
or
<code> pip install </code>

<span style="color:red">*Libraries must be installed after activating the environment if using conda install. The list of libraries used is mentioned below: </span>

**Libraries Used**

- [Pandas](https://pandas.pydata.org/docs/) 
- [NBA stats API](https://github.com/swar/nba_api)
- [Plotly](https://github.com/plotly/plotly.py)
- [Streamlit](https://docs.streamlit.io/library/get-started/installation)

Use <code> conda list </code> to check if correct libraries are installed.

## Open App

1. Navigate to the correct folder where the code is stored. 
2. Activate Gazoo environment using <code> conda activate Gazoo </code> 
3. Right click to open GitBash in that folder or navigate using terminal. 
4. In terminal run streamlit app by using <code> streamlit run app.py </code>
5. Streamlit app will open and run in default browser. 

---

# Enjoy! :beers:


