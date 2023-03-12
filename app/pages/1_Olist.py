import sqlalchemy as sql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import pydeck as pdk
import pymysql
from datetime import datetime
import datetime
from PIL import Image
import altair as alt
from datetime import datetime


st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")

st.title(":mag_right: Proyecto OLIST - Visualización de Datos Generales")
st.text("A continuación se observara los resultados del análisis")
st.markdown("---")

st.sidebar.header("Panel General")
st.sidebar.write(
    """El panel general contiene información sobre la evolución de las ventas totales, 
participación de las ventas por categoría y la distribución geográfica de los clientes y vendedores. """
)
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"  #esta es la conexion al contenedor de docker
)

engine1 = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"  #esta es la conexion local con streamlit
)

engine2 = sql.create_engine(
    "mysql+pymysql://root:Haad91280567#@localhost:3306/marketing?charset=utf8mb4"     #esta es la conexion local con my workbench mysql
) 


#------------------------------------------------------------------------------------------#
tab_ventas, tab_clientes, tab_vendedores, tab_method, tab_delivery, tab_mapa, tab_marketing, tab_reviews, tab_kpis = st.tabs(["Ventas", "Clientes", "Vendedores", "Method of Payment", "Delivery", "Mapa", "Marketing", "Reviews", "KPIs"])

with tab_ventas:

    col_ventas, col_categorias = st.columns([1, 1])

    with col_ventas:
        df_ingresos = pd.read_sql(
            """
            SELECT 
                o.order_id AS id,
                o.purchase_timestamp AS fecha,
                sum(oi.price) AS total
            FROM order_items AS oi
            JOIN orders AS o ON(oi.order_id = o.order_id)
            WHERE o.purchase_timestamp < date("2018-09-01")
            GROUP BY o.order_id
            ORDER BY o.purchase_timestamp;
            """,
            con=engine1,
        )
        df_ingresos["fecha"] = pd.to_datetime(df_ingresos["fecha"])
        df_ingresos.set_index(keys="fecha", inplace=True)

        df_ingresos = df_ingresos.resample("M").sum()

        lista = df_ingresos.index # creo una lista de fecha con valores unicos

        clist = st.sidebar.selectbox(
            'Seleccione fecha 👉', lista )
        
        #fig_2 = px.line(
        #   data_frame=df_ingresos,
        #   x=df_ingresos[df_ingresos['fecha'] == clist],
        #    y="total",
        #   title="Evolución mensual de las ventas",
        #   labels={"fecha": "Fecha", "total": "Total de ventas"},
        #)

        fig = px.line(
            data_frame=df_ingresos,
            x=df_ingresos.index,
            y="total",
            title="Evolución mensual de las ventas",
            labels={"fecha": "Fecha", "total": "Total de ventas"},
        )

        
        st.plotly_chart(fig, use_container_width=True)

        

    with col_categorias:

        df_categorias = pd.read_sql(
            """
            SELECT 
                p.category_name AS categoria,
                sum(oi.price) AS total
            FROM order_items AS oi
            LEFT JOIN products AS p ON (oi.product_id = p.product_id)
            GROUP BY p.category_name
            ORDER BY sum(oi.price) DESC
            LIMIT 5;""",
            con=engine1,
        )


        #categoria = df_categorias['categoria']
        categoria = st.sidebar.selectbox(
            'Seleccione categoria 👉', df_categorias['categoria']
            
            )
        
        show_data = st.sidebar.checkbox("Mostrar Datos")
 
        if show_data:
            st.dataframe(df_categorias)

        fil_df = df_categorias[df_categorias.categoria == categoria]
        new_df = pd.melt(fil_df, id_vars=['categoria'], var_name="feature", value_vars=['total'])

        logy = True
        textauto = True
        title = f'categoria:{categoria}'
        
        fig = px.bar(
            df_categorias,
            x="categoria",
            y="total",
            title="Top 5 ventas por categoría",
        )

        fig_1 = px.bar(
            new_df,
            x="feature",
            y="value",
            log_y=logy,
            text_auto=textauto,
            title="Top 5 ventas por categoría",
        )
        st.plotly_chart(fig_1, use_container_width=True)

    

with tab_clientes:

    col_graph, col_fig = st.columns([3, 2])
    with col_graph:

        df_customers = pd.read_sql(
            sql="""
            SELECT 
                count(c.unique_id) AS weight,
                g.latitude AS latitude,
            	g.longitude AS longitude,
            	min(g.state) AS estado
            FROM customers AS c
            LEFT JOIN geolocations AS g ON (c.zip_code = g.zip_code)
            GROUP BY g.latitude, g.longitude;
        """,
            con=engine1,
        )

        view = pdk.data_utils.compute_view(df_customers[["longitude", "latitude"]])
        view.zoom = 3.3
        view.pitch = 30

        st.pydeck_chart(
            pdk.Deck(
                map_style="dark",
                initial_view_state=view,
                tooltip=True,
                layers=[
                    pdk.Layer(
                        type="HeatmapLayer",
                        data=df_customers,
                        get_position="[longitude, latitude]",
                        get_weight="weight",
                    )
                ],
            ),
            use_container_width=True,
        )

    with col_fig:
        fig = px.bar(
            data_frame=df_customers.groupby(by="estado")
            .sum()
            .reset_index()
            .sort_values("weight", ascending=False)
            .head(5),
            x="estado",
            y="weight",
            title="Top 5 de estados por cantidad de clientes",
            labels={"weight": "Cantidad clientes", "estado": "Estado"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_vendedores:

    col_graph, col_fig = st.columns([3, 2])
    with col_graph:
        df_sellers = pd.read_sql(
            sql="""
            SELECT 
                count(s.seller_id) AS weight,
                g.latitude AS latitude,
                g.longitude AS longitude,
                min(g.state) AS estado
            FROM sellers AS s
            LEFT JOIN geolocations AS g ON (s.zip_code = g.zip_code)
            GROUP BY g.latitude, g.longitude;
        """,
            con=engine1,
        )

        view = pdk.data_utils.compute_view(df_sellers[["longitude", "latitude"]])
        view.zoom = 3.3
        view.pitch = 30

        st.pydeck_chart(
            pdk.Deck(
                map_style="dark",
                initial_view_state=view,
                tooltip=True,
                layers=[
                    pdk.Layer(
                        type="HeatmapLayer",
                        data=df_sellers,
                        get_position="[longitude, latitude]",
                        get_weight="weight",
                    )
                ],
            )
        )

    with col_fig:
        fig = px.bar(
            data_frame=df_sellers.groupby(by="estado")
            .sum()
            .reset_index()
            .sort_values("weight", ascending=False)
            .head(5),
            x="estado",
            y="weight",
            title="Top 5 de estados por cantidad de vendedores",
            labels={"weight": "Cantidad vendedores", "estado": "Estado"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)


with tab_method:

    col_metodos, col_cuotas = st.columns(2)

    with col_metodos:
        df_payments = pd.read_sql(
            "order_payments",
            con=engine,
        )

        fig = px.pie(
            data_frame=df_payments.groupby(by="type")
            .count()
            .reset_index()
            .rename(columns={"value": "cantidad"}),
            values="cantidad",
            names="type",
            title="Proporción por método de pago",
            # color_discrete_sequence=px.colors.sequential.Inferno,
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_cuotas:

        fig = px.bar(
            data_frame=df_payments.groupby(by="installments")
            .count()
            .reset_index()
            .rename(columns={"value": "cantidad"}),
            x="installments",
            y="cantidad",
            range_x=[0.4, df_payments["installments"].max()],
            title="Distribución de pagos por cantidad de cuotas",
            labels={
                "cantidad": "Cantidad de pagos",
                "installments": "Cantidad de cuotas",
            },
        )

        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_delivery:
    col_dias, col_peso = st.columns(2)

    with col_dias:
        delivery_rango = pd.read_sql(
            """
                SELECT count(d.dias) AS 'cantidad',
                    CASE
                        WHEN dias  < 4 THEN '< 4'
                        WHEN dias < 7 THEN '4 - 6'
                        WHEN dias < 11 THEN '7 - 10'
                        WHEN dias < 16 THEN '11 - 15'
                        WHEN dias < 20 THEN '16 - 20'
                        ELSE '> 20'
                    END
                    AS rango_entregas   
                FROM (
                    SELECT 
                        datediff(o.delivered_customer_date, o.purchase_timestamp ) AS dias
                    FROM orders AS o
                    WHERE o.status = 'delivered'
                ) AS d
                GROUP BY rango_entregas
                ORDER BY  
                    CASE rango_entregas
                        WHEN '< 4' THEN 1
                        WHEN '4 - 6' THEN 2
                        WHEN '7 - 10' THEN 3
                        WHEN '11 - 15' THEN 4
                        WHEN '16 - 20' THEN 5
                        WHEN '> 20' THEN 6
                        ELSE 7
                    END;""",
            con=engine1,
        )

        fig = px.bar(
            delivery_rango,
            x="rango_entregas",
            y="cantidad",
            title="Productos entregados según rango de días",
            labels={
                "rango_entregas": "Rango de dias",
                "cantidad": "Cantidad de envíos",
            },
        )

        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_peso:
        delivery_peso = pd.read_sql(
            """
            SELECT avg(d.freight_value) AS 'promedio_flete',
                CASE
                    WHEN d.weight_g  < 501 THEN '< 0,5'
                    WHEN d.weight_g < 1001 THEN '0,5 - 1'
                    WHEN d.weight_g < 5001 THEN '1 - 5'
                    WHEN d.weight_g < 10001 THEN '5 - 10'
                    WHEN d.weight_g < 20001 THEN '10 - 20'
                    ELSE '> 20'
                END
                as rango_peso
            FROM (SELECT i.product_id, i.freight_value, p.weight_g
                FROM order_items AS i
                LEFT JOIN products as p ON(i.product_id = p.product_id)
                    ) AS d
            GROUP BY rango_peso
            ORDER BY 
                CASE rango_peso
                    WHEN  '< 0,5' THEN 1
                    WHEN  '0,5 - 1' THEN 2
                    WHEN  '1 - 5' THEN 3
                    WHEN  '5 - 10' THEN 4
                    WHEN  '10 - 20' THEN 5
                    WHEN  '> 20' THEN 6
                    ELSE 7
                END;""",
            con=engine1,
        )

        fig = px.bar(
            data_frame=delivery_peso,
            x="rango_peso",
            y="promedio_flete",
            title="Promedio valor flete por rango de peso",
            labels={
                "rango_peso": "Rango de peso [kg]",
                "promedio_flete": "Precio promedio del flete [R$]",
            },
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_mapa:
    col_graph, col_text = st.columns([3, 2])
    with col_graph:
        df_cust_sell = pd.read_sql(
            sql="""
            SELECT 
                avg(cg.latitude) AS c_latitude,
                avg(cg.longitude) AS c_longitude,
                avg(sg.latitude) AS s_latitude,
                avg(sg.longitude) AS s_longitude
            FROM order_items AS oi
            LEFT JOIN sellers AS s ON(oi.seller_id = s.seller_id)
            LEFT JOIN orders AS ord ON (oi.order_id = ord.order_id)
            LEFT JOIN customers AS c ON (ord.customer_id = c.customer_id)
            LEFT JOIN geolocations AS cg ON (c.zip_code = cg.zip_code)
            LEFT JOIN geolocations AS sg ON (s.zip_code = sg.zip_code)
            GROUP BY oi.product_id, oi.seller_id, ord.customer_id
            ORDER BY rand()
            LIMIT 10000;
            """,
            con=engine1,
        )
        view = pdk.data_utils.compute_view(df_cust_sell[["c_longitude", "c_latitude"]])
        view.zoom = 3
        view.pitch = 30
        st.pydeck_chart(
            pdk.Deck(
                map_style="dark",
                initial_view_state=view,
                tooltip=True,
                layers=[
                    pdk.Layer(
                        "ArcLayer",
                        data=df_cust_sell,
                        get_source_position=["s_longitude", "s_latitude"],
                        get_target_position=["c_longitude", "c_latitude"],
                        get_source_color=[0, 255, 0, 80],
                        get_target_color=[255, 0, 0, 80],
                    )
                ],
            )
        )
    with col_text:
        st.text(
            """
            Se toma una muestra aleatoria de 10.000 envíos de productos. 
            Cada arco representa una orden de compra que parte desde el 
            vendedor (verde) y finaliza en el comprador (rojo).
            """
        )

with tab_marketing:
    col_contactos, col_cerrados = st.columns([3, 2])

    with col_contactos:
        df_marketing = pd.read_sql(
            sql="""
            SELECT mql_id, first_contact_date, origin AS  Origen
            FROM marketing_qualified_leads;
            """,
            con=engine,
        )
        df_marketing["first_contact_date"] = pd.to_datetime(
            df_marketing["first_contact_date"]
        )
        df_marketing["año_mes"] = df_marketing["first_contact_date"].dt.to_period("M")
        df_grouped = (
            df_marketing.groupby(["Origen", "año_mes"])
            .aggregate({"mql_id": "count", "first_contact_date": "first"})
            .reset_index()
        )

        fig = px.line(
            data_frame=df_grouped,
            x="first_contact_date",
            y="mql_id",
            title="Cantidad de contactos por canal",
            color="Origen",
            labels={
                "first_contact_date": "Fecha de contacto",
                "mql_id": "Cantidad de contactos",
            },
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_cerrados:
        df_closed_deals = pd.read_sql(
            sql="""
            SELECT 
                mql.origin AS origen,
                count(cd.mql_id)/count(mql.mql_id)*100 AS porcentaje
            FROM marketing_qualified_leads AS mql
            LEFT JOIN closed_deals AS cd ON (cd.mql_id = mql.mql_id)
            GROUP BY mql.origin
            ORDER BY porcentaje DESC;
            """,
            con=engine1,
        )

        fig = px.bar(
            data_frame=df_closed_deals,
            x="origen",
            y="porcentaje",
            title="Porcentaje de cierre por canal de contacto",
            labels={"origen": "Origen", "porcentaje": "Porcentaje de cierre"},
        )

        st.plotly_chart(figure_or_data=fig, use_container_width=True)


with tab_reviews:
    col_1, col_2 = st.columns(2)

    with col_1:
        df_category_score = pd.read_sql(
            """
            SELECT 
                avg(a.score) as prom_score, 
                c.category_name AS categoria
            FROM order_reviews AS a
                LEFT JOIN order_items AS b ON (a.order_id = b.order_id)
                LEFT JOIN products AS c ON (b.product_id = c.product_id)
            GROUP BY categoria
            ORDER BY prom_score DESC
            LIMIT 10;
            """,
            con=engine1,
        )

        fig = px.bar(
            df_category_score,
            x="prom_score",
            y="categoria",
            orientation="h",
            title="Top 10 puntuación por categoría",
            labels={"categoria": "Categoría", "prom_score": "Puntuación promedio"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_2:
        df_reviews = pd.read_sql(
            """
            SELECT ordr.score AS score, o.purchase_timestamp AS fecha
            FROM order_reviews AS ordr
            LEFT JOIN orders AS o ON (ordr.order_id = o.order_id)
            WHERE o.purchase_timestamp > date("2016-12-31") 
            AND o.purchase_timestamp < date("2018-09-01");
            """,
            con=engine1,
        )

        df_reviews["fecha"] = pd.to_datetime(df_reviews["fecha"])
        df_reviews.set_index("fecha", inplace=True)
        df_reviews = df_reviews.resample("M").aggregate({"score": "mean"}).reset_index()

        fig = px.line(
            df_reviews,
            x="fecha",
            y="score",
            title="Evolución de la puntuación promedio",
            labels={"fecha": "Fecha", "score": "Puntuación promedio"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_kpis:
# KPI Variación porcentual del volumen de ventas por mes (VVV)
    st.markdown("---")
    st.markdown("#### Variación porcentual del volumen de ventas (VVV)")
    st.text("Objetivo: Evaluar el cambio de porcentual de las ventas")
    st.text("Frecuencia de evaluación: Mensual")
    st.text("Valor objetivo: 10%")

    kpi_vvv = pd.read_sql(
    """ 
        SELECT date(CONCAT(CAST(s.año AS UNSIGNED), '/', CAST(s.mes AS UNSIGNED), "/1")) AS fecha, sum(s.total) AS total
        FROM (
	        SELECT avg(year(o.purchase_timestamp)) AS año, avg(month(o.purchase_timestamp)) AS mes, sum(i.price) AS total
            FROM orders AS o
            RIGHT JOIN order_items AS i ON (o.order_id = i.order_id)
            WHERE o.status != "canceled" AND o.status != "unavailable"
            GROUP BY o.order_id
        ) AS s
        GROUP BY s.año, s.mes
        HAVING s.año = 2017
        ORDER BY s.año, s.mes DESC;""",
    con=engine1,
    )

    kpi_vvv["diff"] = kpi_vvv["total"].pct_change(periods=-1)

    left_column, right_column = st.columns([1, 1])

    with left_column:

        st.metric(
            label="Total de ventas en R$",
            value=int(kpi_vvv.loc[0, "total"]),
            delta=int(kpi_vvv.loc[0, "total"] - kpi_vvv.loc[1, "total"]),
        )

    with right_column:

        st.metric(
            label="Variación porcentual",
            value=format(kpi_vvv.loc[0, "diff"], ".2%"),
            delta=format(kpi_vvv.loc[0, "diff"] - kpi_vvv.loc[1, "diff"], ".2%"),
        )


# KPI Puntuación neta del promotor (PN)
    st.markdown("---")
    st.markdown("#### Puntuación neta del promotor (PN)")
    st.text("Objetivo: Medir la satisfacción del cliente")
    st.text("Frecuencia de evaluación: Trimestral")
    st.text("Valor objetivo: 60%")

    kpi_pn = pd.read_sql(
    """ 
    SELECT
	    year(orders.delivered_customer_date) AS año,
        month(orders.delivered_customer_date) AS mes,
        SUM(CASE WHEN score > 3 THEN 1 ELSE 0 END) AS reviews_positivas,
        SUM(CASE WHEN score <= 3 THEN 1 ELSE 0 END) AS reviews_negativas,
        COUNT(*) AS total_reviews
    FROM order_reviews
    LEFT JOIN orders ON (order_reviews.order_id = orders.order_id)
    WHERE year(orders.delivered_customer_date) = 2017
    GROUP BY year(orders.delivered_customer_date), month(orders.delivered_customer_date)
    ORDER BY year(orders.delivered_customer_date), month(orders.delivered_customer_date) DESC
    LIMIT 2;
    """,
    con=engine1,
    )

    pct_act_rp = kpi_pn.loc[0, "reviews_positivas"] / kpi_pn.loc[0, "total_reviews"]
    pct_ant_rp = kpi_pn.loc[1, "reviews_positivas"] / kpi_pn.loc[1, "total_reviews"]

    pct_act_rn = kpi_pn.loc[0, "reviews_negativas"] / kpi_pn.loc[0, "total_reviews"]
    pct_ant_rn = kpi_pn.loc[1, "reviews_negativas"] / kpi_pn.loc[1, "total_reviews"]

    pct_act_pn = pct_act_rp - pct_act_rn
    pct_ant_pn = pct_ant_rp - pct_ant_rn

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.metric(
            label="Porcentaje Calificaciones Positivas",
            value=format(pct_act_rp, ".2%"),
            delta=format(pct_act_rp - pct_ant_rp, ".2%"),
        )

    with middle_column:
        st.metric(
            label="Porcentaje Calificaciones Negativas",
            value=format(pct_act_rn, ".2%"),
            delta=format(pct_act_rn - pct_ant_rn, ".2%"),
            delta_color="inverse",
        )

    with right_column:
        st.metric(
            label="Puntuación Neta",
            value=format(pct_act_pn, ".2%"),
            delta=format(pct_act_pn - pct_ant_pn, ".2%"),
        )


# KPI Fidelidad del cliente (FC)
    st.markdown("---")
    st.markdown("#### Fidelidad del Cliente (FC)")
    st.text("Objetivo: Medir la tasa de clientes que vuelven a comprar")
    st.text("Frecuencia de evaluación: Trimestral")
    st.text("Valor objetivo: 5%")

    kpi_fc = pd.read_sql(
    sql=""" 
    WITH current_quarter AS ( SELECT 2017 AS year, 4 AS quarter)
    SELECT 
	    (SELECT year FROM current_quarter) AS año,
	    (SELECT quarter FROM current_quarter) AS mes, 
        COUNT(customers.unique_id) AS clientes_fieles
    FROM orders
    LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    AND quarter(orders.purchase_timestamp) = (SELECT quarter FROM current_quarter)
    AND customers.unique_id IN (
	    SELECT customers.unique_id 
        FROM orders 
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
	    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
	    AND quarter(orders.purchase_timestamp) = (SELECT quarter - 1 FROM current_quarter)
        AND orders.status != "canceled" AND orders.status != "unavailable") 
    AND orders.status != "canceled" AND orders.status != "unavailable"
    UNION 
    SELECT 
    	(SELECT year FROM current_quarter) AS año,
    	(SELECT quarter - 1 FROM current_quarter) AS mes, 
        COUNT(customers.unique_id) AS clientes_fieles
    FROM orders
    LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    AND quarter(orders.purchase_timestamp) = (SELECT quarter - 1 FROM current_quarter)
    AND customers.unique_id IN (
    	SELECT customers.unique_id 
        FROM orders 
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    	WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    	AND quarter(orders.purchase_timestamp) = (SELECT quarter - 2 FROM current_quarter)
        AND orders.status != "canceled" AND orders.status != "unavailable") 
    AND orders.status != "canceled" AND orders.status != "unavailable";
    """,
    con=engine1,
    )

    kpi_fc_total = pd.read_sql(
    sql=""" 
        SELECT 
        	year(orders.purchase_timestamp) AS año, 
            quarter(orders.purchase_timestamp) AS mes, 
            count(DISTINCT customers.unique_id) AS cantidad_total_clientes
        FROM orders
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
        WHERE  year(orders.purchase_timestamp) = 2017
        AND orders.status != "canceled" AND orders.status != "unavailable"
        GROUP BY año, mes
        ORDER BY año, mes DESC
        LIMIT 2;
    """,
    con=engine1,
)

    pct_act_fc = (
        kpi_fc.loc[0, "clientes_fieles"] / kpi_fc_total.loc[0, "cantidad_total_clientes"]
    )

    pct_ant_fc = (
        kpi_fc.loc[1, "clientes_fieles"] / kpi_fc_total.loc[1, "cantidad_total_clientes"]
    )

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.metric(
            label="Cantidad clientes fieles",
            value=int(kpi_fc.loc[0, "clientes_fieles"]),
            delta=int(kpi_fc.loc[0, "clientes_fieles"] - kpi_fc.loc[1, "clientes_fieles"]),
        )

    with middle_column:
        st.metric(
            label="Cantidad clientes total",
            value=int(kpi_fc_total.loc[0, "cantidad_total_clientes"]),
            delta=int(
             kpi_fc_total.loc[0, "cantidad_total_clientes"]
                - kpi_fc_total.loc[1, "cantidad_total_clientes"]
        ),
    )

    with right_column:
        st.metric(
            label="Porcentaje fidelidad de clientes",
            value=format(pct_act_fc, ".2%"),
            delta=format(pct_act_fc - pct_ant_fc, ".2%"),
        )


# KPI Tasa de Conversión (TC)
    st.markdown("---")
    st.markdown("#### Tasa de Conversión (TC)")
    st.text(
    "Objetivo: Determinar la cantidad vendedores potenciales que se unen a la empresa"
    )
    st.text("Frecuencia de evaluación: Trimestral")
    st.text("Valor objetivo: 15%")
    kpi_tc = pd.read_sql(
    """ 
    SELECT 
        max(year(marketing_qualified_leads.first_contact_date)) AS año,
        max(quarter(marketing_qualified_leads.first_contact_date)) AS mes,
        count(marketing_qualified_leads.mql_id) AS cantidad_interesados,
        count(closed_deals.mql_id) AS cantidad_convertidos,
        count(closed_deals.mql_id)/count(marketing_qualified_leads.mql_id) AS tasa_conversion
    FROM marketing_qualified_leads
    LEFT JOIN closed_deals ON (marketing_qualified_leads.mql_id = closed_deals.mql_id)
    WHERE year(marketing_qualified_leads.first_contact_date) <= 2017
    AND quarter(marketing_qualified_leads.first_contact_date) <= 4
    UNION
    SELECT 
    	max(year(marketing_qualified_leads.first_contact_date)) AS año,
        max(quarter(marketing_qualified_leads.first_contact_date)) AS mes,
        count(marketing_qualified_leads.mql_id) AS cantidad_interesados,
        count(closed_deals.mql_id) AS cantidad_convertidos,
        count(closed_deals.mql_id)/count(marketing_qualified_leads.mql_id) AS tasa_conversion
    FROM marketing_qualified_leads
    LEFT JOIN closed_deals ON (marketing_qualified_leads.mql_id = closed_deals.mql_id)
    WHERE year(marketing_qualified_leads.first_contact_date) <= 2017
    AND quarter(marketing_qualified_leads.first_contact_date) <= 3;
    """,
    con=engine1,
)

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.metric(
            label="Cantidad de interesados",
            value=int(kpi_tc.loc[0, "cantidad_interesados"]),
            delta=int(
             kpi_tc.loc[0, "cantidad_interesados"]
                - kpi_tc.loc[1, "cantidad_interesados"]
        ),
    )

    with middle_column:
        st.metric(
            label="Cantidad de convertidos",
            value=int(kpi_tc.loc[0, "cantidad_convertidos"]),
            delta=int(
             kpi_tc.loc[0, "cantidad_convertidos"]
                - kpi_tc.loc[1, "cantidad_convertidos"]
        ),
    )

    with right_column:
        st.metric(
            label="Tasa de conversión",
            value=format(kpi_tc.loc[0, "tasa_conversion"], ".2%"),
            delta=format(
                kpi_tc.loc[0, "tasa_conversion"] - kpi_tc.loc[1, "tasa_conversion"], ".2%"
        ),
    )


# KPI Puntualidad de la entrega (PE)
    st.markdown("---")
    st.markdown("#### Puntualidad de la Entrega (PE)")
    st.text("Objetivo: Medir el porcentaje de entregas que se realizan a tiempo")
    st.text("Frecuencia de evaluación: Mensual")
    st.text("Valor objetivo: 95%")

    kpi_pe = pd.read_sql(
    """ 
    SELECT 
    	year(ord.fecha) AS año,
        month(ord.fecha) AS mes,
        sum(ord.a_tiempo) AS cantidad_a_tiempo,
        count(*) AS cantidad_total,
        sum(ord.a_tiempo)/count(*) AS puntualidad
    FROM (
    	SELECT
    		purchase_timestamp AS fecha,
            (CASE WHEN datediff(estimated_delivery_date, delivered_customer_date) >= 0 THEN 1 ELSE 0 END) AS a_tiempo
    	FROM orders
        WHERE status = "delivered" AND year(purchase_timestamp) = 2017
    ) AS ord
    GROUP BY año, mes
    ORDER BY año, mes DESC
    LIMIT 2;
    """,
    con=engine1,
)


    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.metric(
            label="Cantidad total de pedidos",
            value=int(kpi_pe.loc[0, "cantidad_total"]),
            delta=int(kpi_pe.loc[0, "cantidad_total"] - kpi_pe.loc[1, "cantidad_total"]),
    )

    with middle_column:
        st.metric(
            label="Cantidad de pedidos entregados puntualmente",
            value=int(kpi_pe.loc[0, "cantidad_a_tiempo"]),
            delta=int(
                kpi_pe.loc[0, "cantidad_a_tiempo"] - kpi_pe.loc[1, "cantidad_a_tiempo"]
        ),
    )

    with right_column:
        st.metric(
            label="Puntualidad de Entrega",
            value=format(kpi_pe.loc[0, "puntualidad"], ".2%"),
            delta=format(
                kpi_pe.loc[0, "puntualidad"] - kpi_pe.loc[1, "puntualidad"], ".2%"
        ),
    )

# KPI: Tiempo total del proceso (TTP)
    st.markdown("---")
    st.markdown("#### Tiempo total del proceso (TTP)")
    st.text("Objetivo: Optimizar los tiempos de compra y envío")
    st.text("Frecuencia de evaluación: Mensual")
    st.text("Valor objetivo: 8 días")

    kpi_ttp = pd.read_sql(
    sql="""
        SELECT 
            year(purchase_timestamp) AS año,
            month(purchase_timestamp) AS mes,
            avg(datediff(delivered_customer_date,purchase_timestamp)) AS tiempo_prom
        FROM orders
        WHERE year(purchase_timestamp) = 2017 AND status = "delivered"
        GROUP BY año, mes
        ORDER BY año, mes DESC;
    """,
    con=engine1,
    )

    graf_col, kpi_col = st.columns([2, 1])

    with graf_col:
        fig = px.area(
            data_frame=kpi_ttp,
            x="mes",
            y="tiempo_prom",
            title="Tiempo promedio de envío",
            range_y=[6, 16],
            labels={"mes": "Mes", "tiempo_prom": "Tiempo promedio"},
        )
    st.plotly_chart(figure_or_data=fig)

with kpi_col:
    st.metric(
        label="Tiempo total promedio",
        value=round(float(kpi_ttp.loc[0, "tiempo_prom"]), 2),
        delta=round(
            float(kpi_ttp.loc[0, "tiempo_prom"] - kpi_ttp.loc[1, "tiempo_prom"]), 2
        ),
        delta_color="inverse",
    )
st.markdown("---")