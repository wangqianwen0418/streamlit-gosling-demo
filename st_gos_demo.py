import streamlit as st
import gosling as gos
from streamlit_gosling import streamlit_gosling as st_gos
 # data = gos.matrix('/path/to/dataset.cool') # local dataset


if __name__=="__main__":

    @st.cache
    def point_chart(chr='1', chartType='point chart'):
        data = gos.multivec(
            url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
            row="sample",
            column="position",
            value="peak",
            categories=["sample 1","sample 2", "sample 3", "sample 4"],
            binSize=5,
        )

        domain = gos.GenomicDomain(chromosome=chr)

        track = gos.Track(data).mark_point().encode(
            x=gos.X("position:G", domain=domain, axis="top"),
            y="peak:Q",
            size="peak:Q",
            color=gos.Color("sample:N", legend=True),
            tooltip=[
                gos.Tooltip(field='position', type='genomic'),
                gos.Tooltip(field='peak', type='quantitative', alt='value', format='.2'),
                gos.Tooltip(field='sample', type='nominal')
            ],
        ).properties(
            layout="linear", width=650, height=200, id='track-1',  experimental={"mouseEvents": True},
            title=''
        )

        if chartType=='bar chart':
            track = track.mark_bar()
        elif chartType == 'area chart':
            track =track.mark_area().encode(row ='sample:N')

        chart = track.view(title='click to select an item')

        return chart

    st.markdown('''
    # Streamlit-Gosling 

    Here is an online demo of [streamlit-gosling](https://github.com/gosling-lang/streamlit-gosling)
    ''')

    chartType = st.selectbox(
        'Select a chart', ['point plot', 'bar chart', 'area chart']
        )

    chr = st.selectbox(
        'Select a chromosome', [str(i) for i in range(1, 20)]
        )

    st.subheader(chartType)



    eventType='click'

    result = st_gos(spec=point_chart(chr, chartType), id='id', height=350, eventType= eventType)


    if result:
        st.write(f'you {eventType}:', result)