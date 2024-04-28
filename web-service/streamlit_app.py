import streamlit as st
import pandas as pd
import plotly.express as px




st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Dashboard `ikanam 1218`')

#st.sidebar.subheader('Heat map parameter')
#time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Distribution parameter')
donut_theta = st.sidebar.selectbox('Select data', ('relevant', 'positive'))

if donut_theta == 'positive':
    st.sidebar.subheader('Class parameter')
    Class_theta = st.sidebar.selectbox('Select data', ('positive', 'negative'))
else:
    st.sidebar.subheader('Class parameter')
    Class_theta = st.sidebar.selectbox('Select data', ('relevant', 'not relevant'))

#st.sidebar.subheader('Line chart parameters')
#plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
#plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)





st.sidebar.markdown('''
---
Created with ❤️ by ikanam 1218.
''')


# Row A
#st.markdown('### Metrics')
#col1, col2, col3 = st.columns(3)
#col1.metric("Temperature", "70 °F", "1.2 °F")
#col2.metric("Wind", "9 mph", "-8%")
#col3.metric("Humidity", "86%", "4%")

# Row B
metrics = pd.read_csv('https://raw.githubusercontent.com/ikanam-ai/Analysis-of-webinar-reviews/master/web-service/train_data.csv?token=GHSAT0AAAAAACQTB5IBSVNSIUDZGHV7DDCEZRNVOOA')

def process_dataframe_is_relevant_is_not_positive(df):
    df = df.drop(['timestamp'], axis=1).sort_values(by='question_1')
    df = df[(df['is_relevant'] == 1) & (df['is_positive'] == 0)]
    df = df.set_index(['is_relevant'])
    return df

def process_dataframe_is_relevant_is_positive(df):    
    df = df.drop(['timestamp'], axis=1).sort_values(by='question_1')
    df = df[(df['is_relevant'] == 1) & (df['is_positive'] == 1)]
    df = df.set_index(['is_relevant'])
    return df

def otchet(df):    
    df = df[['is_relevant', 'is_positive', 'object']]
    df = df.describe().T
    df = df.drop(['count'], axis=1)
    return df

df_not_positive = process_dataframe_is_relevant_is_not_positive(metrics)
df_positive = process_dataframe_is_relevant_is_positive(metrics)
df_otchet = otchet(metrics)

def download_excel(df1, df2, df3):
    # Создаем Excel-файл с двумя листами
    with pd.ExcelWriter('data.xlsx', engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='Положительные', index=False)
        df2.to_excel(writer, sheet_name='Негативные', index=False)
        df3.to_excel(writer, sheet_name='Статистика', index=False)
    
    # Предоставляем кнопку для скачивания
    with open('data.xlsx', 'rb') as f:
        data = f.read()
    st.download_button(
        label="Скачать отчёт",
        data=data,
        file_name='информативные_отзывы.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


#if st.button('Скачать отчёт'):
st.markdown('### Report')

download_excel(df_positive, df_not_positive, df_otchet)





def plot_distribution(df, column):
    # Посчитайте распределение значений в колонке
    distribution = df[column].value_counts(normalize=True)

    # Создайте DataFrame для построения графика
    data = {'Value': distribution.index, 'Percentage': distribution.values * 100}
    df_plot = pd.DataFrame(data)

    # Постройте график с помощью plotly
    fig = px.bar(df_plot, x='Value', y='Percentage', color='Value',
                 labels={'Value': column, 'Percentage': 'Percentage (%)'},
                 title=f'Distribution of {column}')
    
    # Отобразите график в streamlit
    st.plotly_chart(fig)

    # Выведите процент 1 и процент 0
    st.write("Percentage of 1:", distribution[1]*100)
    st.write("Percentage of 0:", distribution[0]*100)




if donut_theta == 'relevant':

    st.markdown(f'### Distribution of {donut_theta}')
    plot_distribution(metrics, 'is_relevant')
else:
    st.markdown(f'### Distribution of {donut_theta}')
    plot_distribution(metrics, 'is_positive')

#st.markdown('### positive')
#plot_distribution(metrics, donut_theta)

# Row C
#st.markdown('### Line chart')
#st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)
st.markdown('### Feedback on a given parameter')


def display_questions_0(df, column):
    relevant_questions = df[df[column] == 0][['question_1', 'question_2', 'question_3', 'question_4', 'question_5']]
    for index, row in relevant_questions.iterrows():
        st.write(f"Row {index + 1}:")
        st.write(row)

def display_questions_1(df, column):
    relevant_questions = df[df[column] == 1][['question_1', 'question_2', 'question_3', 'question_4', 'question_5']]
    for index, row in relevant_questions.iterrows():
        st.write(f"Row {index + 1}:")
        st.write(row)

if Class_theta == 'positive':
    display_questions_1(metrics, 'is_positive')
elif Class_theta == 'negative':
    display_questions_0(metrics, 'is_positive')
elif Class_theta == 'relevant':
    display_questions_1(metrics, 'is_relevant')
elif Class_theta == 'not relevant':
    display_questions_0(metrics, 'is_relevant')



