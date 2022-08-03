import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium 
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from venn import venn

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache
def load_dataframe():
    data_analyst = pd.read_csv('./input_2.csv')
    return data_analyst 
data_analyst = load_dataframe()

background = r"#0E1117"

def load_map():
    map = folium.Map(location=[-2.945311, 119.579316], zoom_start=5)
    mCluster = MarkerCluster(name='jobs').add_to(map)

    for id, lat, lng in zip(data_analyst['id'].dropna(), data_analyst['lat'].dropna(), data_analyst['lng'].dropna()):
        folium.Marker([lat, lng], popup=id).add_to(mCluster)

    return map

def work_type():
    work_type = dict(data_analyst['work_type'].fillna("Not-Specified").value_counts())

    work_type_df = pd.DataFrame.from_dict(work_type, orient='index').reset_index()
    work_type_df.columns = ['work_type', 'count']
    
    return px.pie(work_type_df, values='count', names='work_type', color_discrete_sequence=["#636EFA", "#EF553B"])


def job_applicant():
    jobs_applicant = {
        '0': data_analyst[data_analyst['applicant_count'] == 0]['applicant_count'].count(),
        '1-19': data_analyst[(data_analyst['applicant_count'] >= 1) & (data_analyst['applicant_count'] <= 19)]['applicant_count'].count(),
    }
    for start in range(20, 200, 20):
        jobs_applicant[f"{start}-{start+19}"] = data_analyst[(data_analyst['applicant_count'] >= start) & (data_analyst['applicant_count'] < start+20)]['applicant_count'].count()

    jobs_applicant['200+'] = data_analyst[data_analyst['applicant_count'] >= 200]['applicant_count'].count()

    # convert to df
    jobs_applicant_df = pd.DataFrame.from_dict(jobs_applicant, orient='index').reset_index()
    jobs_applicant_df.columns = ['applicant_count', 'count']
    # use plotly bar
    return px.bar(jobs_applicant_df, x='applicant_count', y='count', width=1200, height=500)


def v1_t1():
    require = [1 if a or b or c or d else 0 for a, b, c, d in zip(data_analyst['python'], data_analyst['scala'], data_analyst['r'], data_analyst['programming'])]
    not_require = len(require) - sum(require)
    require = sum(require)

    programming_languages_pieChart = {
        'required': require,
        'not_required': not_require,
    }
    # convert to dataframe
    programming_languages_pieChart_df = pd.DataFrame.from_dict(programming_languages_pieChart, orient='index').reset_index()
    programming_languages_pieChart_df.columns = ['required', 'count']
    # use plotly
    return px.pie(programming_languages_pieChart_df, values='count', names='required', color_discrete_sequence=["#636EFA", "#EF553B"])



def v1_t2():
    programming_languages = {
        'python': data_analyst['python'].sum(),
        'r': data_analyst['r'].sum(),
        'scala': data_analyst['scala'].sum(),
    }

    # convert programming language to dataframe
    programming_languages_df = pd.DataFrame.from_dict(programming_languages, orient='index').reset_index()
    programming_languages_df.columns = ['programming_language', 'count']
    # sort
    programming_languages_df = programming_languages_df.sort_values(by='count', ascending=False)
    # visualize with plotly barchart
    return px.bar(programming_languages_df, x='programming_language', y='count', color='programming_language')


def v1_t3():
    programming_language_venn = {
        'python': set(),
        'r': set(),
        'scala': set(),
    }
    for id, py, r, sc in zip(
        list(data_analyst['id']), 
        list(data_analyst['python']), 
        list(data_analyst['r']), 
        list(data_analyst['scala'])):
        
        if py: programming_language_venn['python'].add(id)
        if r: programming_language_venn['r'].add(id)
        if sc: programming_language_venn['scala'].add(id)

    # change figsize
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # ax.set_facecolor((0.1, 0.2, 0.5))

    venn(programming_language_venn, figsize=(12, 12), ax=ax)

    return fig

def v2_t1():
    require = [
        1 if i or b or c or d or e or f or g or h or a else 0 for a, b, c, d, e, f, g, h, i in zip(
            data_analyst['talend'], 
            data_analyst['dataiku'], 
            data_analyst['pentaho'], 
            data_analyst['snowflake'], 
            data_analyst['hive'], 
            data_analyst['spark'], 
            data_analyst['kafka'], 
            data_analyst['kinesis'], 
            data_analyst['etl']
        )
    ]
    not_require = len(require) - sum(require)
    require = sum(require)

    software_pieChart = {
        'required': require,
        'not_required': not_require,
    }
    # convert to dataframe
    software_pieChart_df = pd.DataFrame.from_dict(software_pieChart, orient='index').reset_index()
    software_pieChart_df.columns = ['required', 'count']
    # use plotly bar
    
    return px.pie(software_pieChart_df, values='count', names='required', color_discrete_sequence=["#EF553B", "#636EFA"])

def v2_t2():
    etl_counts = {
        'talend': data_analyst[data_analyst['talend'] == True].shape[0],
        'dataiku': data_analyst[data_analyst['dataiku'] == True].shape[0],
        'pentaho': data_analyst[data_analyst['pentaho'] == True].shape[0],
        'snowflake': data_analyst[data_analyst['snowflake'] == True].shape[0],
        'hive': data_analyst[data_analyst['hive'] == True].shape[0],
        'spark': data_analyst[data_analyst['spark'] == True].shape[0],
        'kafka': data_analyst[data_analyst['kafka'] == True].shape[0],
        'kinesis': data_analyst[data_analyst['kinesis'] == True].shape[0],
        'etl': data_analyst[data_analyst['etl'] == True]['etl'].count(),
    }
    # convert to dataframe
    etl_counts_df = pd.DataFrame.from_dict(etl_counts, orient='index').reset_index()
    etl_counts_df.columns = ['etl', 'count']
    # sort
    etl_counts_df = etl_counts_df.sort_values(by='count', ascending=False)
    # use plotly
    return px.bar(etl_counts_df, x='etl', y='count', color='etl')

def v3_t1():
    require = [
        1 if a or b or c or d or e or f or g or h else 0 for a, b, c, d, e, f, g, h in zip(
            data_analyst['matplotlib'],
            data_analyst['seaborn'],
            data_analyst['plotly'],
            data_analyst['bokeh'],
            data_analyst['tableau'],
            data_analyst['redash'],
            data_analyst['powerbi'],
            data_analyst['data_visualization'])
    ]
    not_require = len(require) - sum(require)
    require = sum(require)

    software_pieChart = {
        'required': require,
        'not_required': not_require,
    }
    # convert to dataframe
    software_pieChart_df = pd.DataFrame.from_dict(software_pieChart, orient='index').reset_index()
    software_pieChart_df.columns = ['required', 'count']
    # use plotly bar

    
    return px.pie(software_pieChart_df, values='count', names='required', color_discrete_sequence=["#636EFA", "#EF553B"])

def v3_t2():
    data_vis={
        'matplotlib': data_analyst[data_analyst['matplotlib'] == True]['matplotlib'].count(),
        'seaborn': data_analyst[data_analyst['seaborn'] == True]['seaborn'].count(), 
        'plotly':  data_analyst[data_analyst['plotly'] == True]['plotly'].count(),
        'bokeh': data_analyst[data_analyst['bokeh'] == True]['bokeh'].count(),
        'tableau': data_analyst[data_analyst['tableau'] == True]['tableau'].count(),
        'redash': data_analyst[data_analyst['redash'] == True]['redash'].count(),
        'powerbi': data_analyst[data_analyst['powerbi'] == True]['powerbi'].count(),
        'data_visualization': data_analyst[data_analyst['data_visualization'] == True]['data_visualization'].count(),
    }
    # convert to dataframe
    data_vis_df = pd.DataFrame.from_dict(data_vis, orient='index').reset_index()
    data_vis_df.columns = ['data_visualization', 'count']
    # sort
    data_vis_df = data_vis_df.sort_values(by='count', ascending=False)
    # use plotly
    return px.bar(data_vis_df, x='data_visualization', y='count', color='data_visualization')

def v3_t3():
    data_vis_venn = {
        'tableau': set(),
        'redash': set(),
        'powerbi': set(),
    }
    for id, tableau, redash, powerbi in zip(
        list(data_analyst['id']), 
        list(data_analyst['tableau']),
        list(data_analyst['redash']),
        list(data_analyst['powerbi'])):

        if tableau: data_vis_venn['tableau'].add(id)
        if redash: data_vis_venn['redash'].add(id)
        if powerbi: data_vis_venn['powerbi'].add(id)

    # change figsize
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # ax.set_facecolor((0.1, 0.2, 0.5))

    venn(data_vis_venn, figsize=(12, 12), ax=ax)

    return fig

def v4_t1():
    require = [
        1 if a or b or c or d or e or f or g or h or i else 0 for a, b, c, d, e, f, g, h, i in zip(
            data_analyst['mysql'],
            data_analyst['postgresql'],
            data_analyst['sql'],
            data_analyst['mongodb'],
            data_analyst['redis'],
            data_analyst['sqlite'],
            data_analyst['sql server'],
            data_analyst['bigquery'],
            data_analyst['nosql'])
    ]
    not_require = len(require) - sum(require)
    require = sum(require)

    database_pieChart = {
        'required': require,
        'not_required': not_require,
    }

    # convert to dataframe
    database_pieChart_df = pd.DataFrame.from_dict(database_pieChart, orient='index').reset_index()
    database_pieChart_df.columns = ['required', 'count']
    # use plotly bar
    return px.pie(database_pieChart_df, values='count', names='required', color_discrete_sequence=["#636EFA", "#EF553B"])

def v4_t2():
    data_db= {
        'sql': [1 if a or b or c or d else 0 for a, b, c, d in zip(
            data_analyst['mysql'],
            data_analyst['postgresql'],
            data_analyst['sql'],
            data_analyst['sqlite'])
        ],
        'nosql': [1 if a or b or c else 0 for a, b, c in zip(
            data_analyst['mongodb'],
            data_analyst['redis'],
            data_analyst['bigquery'])
        ],
        'big query': [1 if a else 0 for a in data_analyst['bigquery']]
    }

    data_db['sql'] = sum(data_db['sql'])
    data_db['nosql'] = sum(data_db['nosql'])
    data_db['big query'] = sum(data_db['big query'])

    # convert to dataframe
    data_db_df = pd.DataFrame.from_dict(data_db, orient='index').reset_index()
    data_db_df.columns = ['database', 'count']
    # sort
    data_db_df = data_db_df.sort_values(by='count', ascending=False)
    # use plotly
    return px.bar(data_db_df, x='database', y='count', color='database')

def v4_t3():
    database_venn = {
        'sql': set(),
        'nosql': set(),
        'big query': set(),
    }

    for id, mysql, postgresql, sql, mongodb, redis, sqlite, sql_server, bigquery, nosql in zip(
        list(data_analyst['id']),
        list(data_analyst['mysql']),
        list(data_analyst['postgresql']),
        list(data_analyst['sql']),
        list(data_analyst['mongodb']),
        list(data_analyst['redis']),
        list(data_analyst['sqlite']),
        list(data_analyst['sql server']),
        list(data_analyst['bigquery']),
        list(data_analyst['nosql'])):
            
            if mysql: database_venn['sql'].add(id)
            if postgresql: database_venn['sql'].add(id)
            if sql: database_venn['sql'].add(id)
            if sqlite: database_venn['sql'].add(id)
            if sql_server: database_venn['sql'].add(id)
            if bigquery: database_venn['big query'].add(id)
            if mongodb: database_venn['nosql'].add(id)
            if redis: database_venn['nosql'].add(id)
            if nosql: database_venn['nosql'].add(id)
  
    
    # change figsize
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # ax.set_facecolor((0.1, 0.2, 0.5))

    venn(database_venn, figsize=(12, 12), ax=ax)

    return fig


def v4_t4():
    data_db= {
        'mysql': [1 if a else 0 for a in data_analyst['mysql']],
        'postgresql': [1 if a else 0 for a in data_analyst['postgresql']],
        'sql': [1 if a else 0 for a in data_analyst['sql']],
        'sqlite': [1 if a else 0 for a in data_analyst['sqlite']],
        'big query': [1 if a else 0 for a in data_analyst['bigquery']],
    }

    data_db['mysql'] = sum(data_db['mysql'])
    data_db['postgresql'] = sum(data_db['postgresql'])
    data_db['sql'] = sum(data_db['sql'])
    data_db['sqlite'] = sum(data_db['sqlite'])
    data_db['big query'] = sum(data_db['big query'])


    # convert to dataframe
    data_db_df = pd.DataFrame.from_dict(data_db, orient='index').reset_index()
    data_db_df.columns = ['SQL Database', 'count']
    # sort
    data_db_df = data_db_df.sort_values(by='count', ascending=False)
    # use plotly
    return px.bar(data_db_df, x='SQL Database', y='count', color='SQL Database')


def v5():
    other_skills = ['communication', 'deployment', 'english']
    require = data_analyst.loc[:, other_skills].sum(axis=0)


    communication = {
        'required': require['communication'],
        'not_required': len(data_analyst) - require['communication'],
    }
    deployment = {
        'required': require['deployment'],
        'not_required': len(data_analyst) - require['deployment'],
    }
    english = {
        'required': require['english'],
        'not_required': len(data_analyst) - require['english'],
    }

    communication_df = pd.DataFrame.from_dict(communication, orient='index').reset_index()
    deployment_df = pd.DataFrame.from_dict(deployment, orient='index').reset_index()
    english_df = pd.DataFrame.from_dict(english, orient='index').reset_index()

    communication_df.columns = ['required', 'count']
    deployment_df.columns = ['required', 'count']
    english_df.columns = ['required', 'count']
    
    # visualize
    return (
        px.pie(communication_df, values='count', names='required', color_discrete_sequence=["#EF553B", "#636EFA"]),
        px.pie(deployment_df, values='count', names='required', color_discrete_sequence=["#EF553B", "#636EFA"]),
        px.pie(english_df, values='count', names='required', color_discrete_sequence=["#EF553B", "#636EFA"])
    )

@st.cache
def _how_many_jobs_df():
    all_skills = ['python', 'r', 'scala', 'spark', 'kafka', 'talend', 'pentaho', 'hive', 'tableau', 'powerbi', 'redash', 'sql', 'nosql', 'bigquery', 'communication', 'deployment', 'english']
    return data_analyst.loc[:, all_skills]

def how_many_jobs(core_skills, soft_skills):
    jobs = _how_many_jobs_df()

    all_skills = ['python', 'r', 'scala', 'spark', 'kafka', 'talend', 'pentaho', 'hive', 'tableau', 'powerbi', 'redash', 'sql', 'nosql', 'bigquery', 'communication', 'deployment', 'english']

    skills = {k: True if k in core_skills + soft_skills else False for k in all_skills}

    can_apply = 0
    cannot_apply = 0
    for _, job in jobs.iterrows():
        can_apply_current_job = True
        for skill, state in skills.items():
            if job[skill] == True and state == False:
                can_apply_current_job = False
                break
        if can_apply_current_job:
            can_apply += 1
        else:
            cannot_apply += 1

    my_jobs = {
        '100% Match': can_apply,
        'Missing at least 1 skill': cannot_apply,
    }

    my_jobs_df = pd.DataFrame.from_dict(my_jobs, orient='index').reset_index()
    my_jobs_df.columns = ['can_apply', 'count']
    
    colors = ['#EF553B', '#636EFA']

    if can_apply > cannot_apply:
        # reverse colors
        colors = colors[::-1]

    return px.pie(my_jobs_df, values='count', names='can_apply', color_discrete_sequence=colors)





st.markdown("<h1 style='text-align: center; color: white;'>The State of Data Analyst Jobs in Indonesia LinkedIn Jobs</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Jobs Location</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Mayoritas pekerjaan berada pada Jakarta atau Jawa Barat.</p>", unsafe_allow_html=True)
st_folium(load_map(), width=1800)

col_work_type_graph, col_work_type_graph_explanation = st.columns([3, 2])

with col_work_type_graph_explanation:
    st.markdown("<h3 style='text-align: center; color: white;'>Work Type</h3>", unsafe_allow_html=True)
    st.write(f"""
        Kita dapat melihat Hybrid dan On-Site mulai menjadi dominan.\n
        Jika kita asumsi Not-Specified adalah on-site, on-site memiliki {round(34.7 + 36.6, 2)}% dari total jobs.\n
        Hybrid terdiri dari 21.1% jobs dan Remote terdiri dari 7.51% jobs.

        Oleh karena itu kita dapat asumsi bahwa pekerjaan sudah dominan offline lagi.
     """)

with col_work_type_graph:
    st.write(work_type())

st.plotly_chart(job_applicant())
_, middle, _ = st.columns([1, 3, 1])
with middle:
    st.markdown("<h3 style='text-align: center; color: white;'>Applicants Count</h3>", unsafe_allow_html=True)

    with st.expander("See Explanation"):
        st.markdown("Pekerjaan dalam linkedin memiliki cap 200, dalam kata lain jika sudah lebih dari 200 kita tidak dapat melihat jumlah applicant")
        st.markdown("Terdapat banyak pekerjaan yang memiliki 200+ applicant hal ini dikarenakan adanya perusahan yang popular")
        st.markdown(r"Namun mayoritas pekerjaan terdapat pada 1-39 jumlah applicant oleh karena itu perlu menjadi top 2.5% untuk mendapatkan mayoritas pekerjaan")

    

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Core Skills</h2>", unsafe_allow_html=True)



visualization_1, explanation_1 = st.columns([3, 2])

with visualization_1:
    tab1, tab2, tab3 = st.tabs(["Pie Chart", "Bar Plot", "Venn Diagram"])
    with tab1:
        st.plotly_chart(v1_t1())
    with tab2:
        st.plotly_chart(v1_t2())
    with tab3:
        st.pyplot(v1_t3())

with explanation_1:
    st.markdown("<h3 style='text-align: center; color: white;'>Programming Languages</h3>", unsafe_allow_html=True)
    st.markdown("61% Pekerjaan menyebutkan antara 3 bahasa pemograman atau dengan kata \"pemograman\" secara langsung.")
    st.markdown("Kita dapat melihat 110+ perkejaan menyebutkan Python. Sedangkan R hanya sedikit melewati 80 pekerjaan. Scala yang paling kecil hanya memiliki 11 pekerjaan yang menyebutkannya.")
    st.markdown("Jika kita liat secara venn diagram, semua pekerjaan menyebutkan python. Kemungkinan hal ini terjadi karena bias dari pemgambilan data. Namun, Python tetap memiliki prioritas dibanding bahasa lainnya.")
    st.markdown("Sedangkan Scala hanya memiliki 11 mention dimana semua mentionnya menyebutkan Python dan mayoritas menyebutkan R sebagai alternatif")
    st.markdown("Dalam kata lain sangat disarankan untuk mempelajari Python diantara seluruh bahasa pemograman lainnya. R merupakan alternatif yang masih cukup baik")

explanation_2, visualization_2 = st.columns([2, 3])

with visualization_2:
    tab1, tab2 = st.tabs(["Pie Chart", "Bar Plot"])
    with tab1:
        st.plotly_chart(v2_t1())
    with tab2:
        st.plotly_chart(v2_t2())

with explanation_2:
    st.markdown("<h3 style='text-align: center; color: white;'>ETL Softwares</h3>", unsafe_allow_html=True)
    st.markdown(r"""17.4% Secara explicit menyebutkan sebuah ETL software atau keyword ETL.""")
    st.markdown("Mayoritas yang menyebutkan ETL hanya menggunakan keywordnya saja tidak softwarenya. Hal ini menunjukan pengalaman ETL meruapakan hal penting namun tidak dipengaruhi software yang digunakan")
    st.markdown("Tidak ada cukup banyak perbedaan antara software yang digunakan, sehingga software ETL apapun yang dipelajari cukup.")


visualization_3, explanation_3 = st.columns([3, 2])

with visualization_3:
    tab1, tab2, tab3 = st.tabs(["Pie Chart", "Bar Plot", "Venn Diagram"])
    with tab1:
        st.plotly_chart(v3_t1())
    with tab2:
        st.plotly_chart(v3_t2())
    with tab3:
        st.pyplot(v3_t3())

with explanation_3:
    st.markdown("<h3 style='text-align: center; color: white;'>Data Visualizations</h3>", unsafe_allow_html=True)
    st.markdown(r"""55.4% Menyebutkan skill data visualization. Angka tersebut lebih kecil dari yang diduga, hal ini mungkin dikarenakan hal tersebut merupakan hal yang terekspektasi dari sebuah data analyst, atau kurang pengetahuan istilah data visualisasi pada HR atau Job Poster.""")
    st.markdown("Selain itu dapat dilihat tableau merupakan alat visualisasi yang paling banyak disebutkan. Lebih daripada istilah visualisasi itu sendiri, oleh karena itu sangat disarankan mempelajari visualisasi ini.")
    st.markdown("Library visualisasi lainnya tidak disebutkan, hal ini kemungkinan dikarenakan perusahan tidak peduli library yang digunakan untuk prototyping, berbeda dengan tableau atau powerbi yang digunakan untuk kolaborasi dan membagikan hasil juga")
    st.markdown("Dapat dilihat terdapat 35 pekerjaan yang hanya menyebutkan tableau tanpa menyebutkan powerbi atau redash, oleh karena ini kesempatan terbaik yaitu mempelajari tableau")


explanation_4, visualization_4 = st.columns([2, 3])
with visualization_4:
    tab1, tab2, tab3, tab4 = st.tabs(["Pie Chart", "Bar Plot", "Venn Diagram", "SQL Bar Plot"])
    with tab1:
        st.plotly_chart(v4_t1())
    with tab2:
        st.plotly_chart(v4_t2())
    with tab3:
        st.pyplot(v4_t3())
    with tab4:
        st.plotly_chart(v4_t4())
with explanation_4:
    st.markdown("<h3 style='text-align: center; color: white;'>Databases</h3>", unsafe_allow_html=True)
    st.markdown(r"""73.2% Menyebutkan sebuah database, persentase ini merupakan yang tertinggi yang menunjukan pentingnya database.""")
    st.markdown("Dalam Data Analyst, SQL tetaplah yang menjadi yang paling utama.")
    st.markdown("Semua perusahaan yang menyebutkan database menyebutkan SQL, sebagian menambahkan big query dan NoSQL dalam deskripsi pekerjaannya")
    st.markdown("SQL merupakan database yang paling banyak disebut, hal ini memungkinkan dikarenakan perusahan tidak terlalu memperdulikan sql apa yang digunakan, karena mereka memiliki kemiripan yang cukup tinggi")


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Other Skills</h2>", unsafe_allow_html=True)

other_skills = ['data_mining', 'communication', 'deployment', 'data_scraping', 'english']

tab1, tab2, tab3 = st.tabs(["Communications", "Deployments", "English"])

communications, deployment, english = v5()


with tab1:
    explanation, visualization = st.columns([2, 3])
    with explanation:
        st.markdown("<h3 style='text-align: center; color: white;'>Communications</h3>", unsafe_allow_html=True)
        st.markdown("Komunikasi merupakan softskill terpenting, dimana 42.7% pekerjaan menyebutkan secara eksplisit dalam deskripsi pekerjaannya.")
        st.markdown("Hal ini tentunya wajar, dikarenakan sebuah Data Analyst harus dapat menyampaikan insightnya kepada stake holder.")
    with visualization:
        st.plotly_chart(communications)

with tab2:
    explanation, visualization = st.columns([2, 3])
    with explanation:
        st.markdown("<h3 style='text-align: center; color: white;'>Deployments</h3>", unsafe_allow_html=True)
        st.markdown("Deployment merupakan skill yang sebagian perusahaan cari, dengan 14.6% perusahaan menyebutkannya secara langsung.")
        st.markdown("Oleh karena itu, deployment merupakan skill yang cukup beneficial untuk membedakan dengan kandidat lainnya.")
    with visualization:
        st.plotly_chart(deployment)

with tab3:
    explanation, visualization = st.columns([2, 3])
    with explanation:
        st.markdown("<h3 style='text-align: center; color: white;'>English</h3>", unsafe_allow_html=True)
        st.markdown("27.7% menyebutkan bahasa inggris secara eksplisit. Hal ini tentunya penting sebagai Data Analyst untuk berkomunikasi kepada klien yang tidak dapat berbicara bahasa Indonesia.")
        st.markdown("Selain itu, sebuah Data Analyst akan selalu berhadapan dengan bahasa inggris dalam data-datanya tentunya skill ini akan terpakai dalam day to day jobsnya.")
    with visualization:
        st.plotly_chart(english)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>My 100% Match Jobs</h2>", unsafe_allow_html=True)

options_core_skills = st.multiselect(
     'I Have these core skills',
     ['python', 'r', 'scala', 'spark', 'kafka', 'talend', 'pentaho', 'hive', 'tableau', 'powerbi', 'redash', 'sql', 'nosql', 'bigquery'],
     ['python', 'pentaho', 'sql']
)

options_soft_skills  = st.multiselect(
        'I Have these soft skills',
        ['communication', 'deployment', 'english'],
        ['communication']
)

st.plotly_chart(how_many_jobs(options_core_skills, options_soft_skills))