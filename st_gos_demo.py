import streamlit as st
import gosling as gos
import streamlit_gosling as st_gos
 # data = gos.matrix('/path/to/dataset.cool') # local dataset


if __name__=="__main__":

    # data = gos.matrix('/path/to/dataset.cool') # local dataset
    st.set_page_config(layout="wide")
    
    col1, col2 = st.columns([1, 3])

    @st.cache
    def point_chart(chr='1', chartType='point chart'):
        data = gos.multivec(
            url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
            row="sample",
            column="position",
            value="peak",
            categories=["sample 1", "sample 2", "sample 3", "sample 4"],
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
                gos.Tooltip(field='peak', type='quantitative',
                            alt='value', format='.2'),
                gos.Tooltip(field='sample', type='nominal')
            ],
        ).properties(
            layout="linear", width=650, height=200, id='track-1',  experimental={"mouseEvents": True},
            title=''
        )

        if chartType == 'bar chart':
            track = track.mark_bar()
        elif chartType == 'area chart':
            track = track.mark_area().encode(row='sample:N')

        chart = track.view(title='click to select an item')

        return chart

    with col1:
        st.header('Streamlit-Gosling')

        chartType = st.selectbox(
            'Select a chart', ['point plot', 'bar chart', 'area chart']
        )

        chr = st.selectbox(
            'zoom to chromosome', [str(i) for i in range(1, 20)]
        )

    eventType = 'click'
    api = {"action": 'zoomTo', 'viewId': 'track-1', 'position': f'chr{chr}'}

    with col2:

        result = st_gos.from_gos(spec=point_chart(chartType=chartType),
                          id='id', height=350, eventType=eventType, api=api)


    with col1:
        st.write(f'you {eventType}:', result)

# spec = {
#   "title": "Basic Marks: bar",
#   "subtitle": "Tutorial Examples",
#   "tracks": [
#     {
#       "layout": "linear",
#       "width": 800,
#       "height": 180,
#       "data": {
#         "url": "https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
#         "type": "multivec",
#         "row": "sample",
#         "column": "position",
#         "value": "peak",
#         "categories": ["sample 1"],
#         "binSize": 5
#       },
#       "mark": "bar",
#       "x": {"field": "start", "type": "genomic", "axis": "bottom"},
#       "xe": {"field": "end", "type": "genomic"},
#       "y": {"field": "peak", "type": "quantitative", "axis": "right"},
#       "size": {"value": 5}
#     }
#   ]
# }
# st_gos.from_json(id = 'id2', spec = spec, height=350)