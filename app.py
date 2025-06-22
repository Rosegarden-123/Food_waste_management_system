import streamlit as st
st.title("Food Waste Management System")
st.markdown("""
Welcome to the Food Wastage Management System Dashboard.
This platform helps track and analyze food donations from providers to receivers to combat food waste effectively.
""")
st.image(r"C:\Users\Pitchamani\Desktop\FWMS\env\Scripts\image.png")
import pandas as pd
df_foodlist=pd.read_csv(r"C:\Users\Pitchamani\Desktop\FWMS\food_listings_data.csv")
st.sidebar.header("Food donation availability")
location_filter=st.sidebar.selectbox("Select Location",options=["All"]+sorted(df_foodlist["Location"].unique()))
Provider_filter=st.sidebar.selectbox("Select Provider",options=["All"]+sorted(df_foodlist["Provider_Type"].unique()))
food_filter=st.sidebar.selectbox("Select Food type",options=["All"]+sorted(df_foodlist["Food_Type"].unique()))
filter_df=df_foodlist.copy()

if location_filter!= "All":
    filter_df=filter_df[filter_df["Location"]==location_filter]

if Provider_filter!= "All":
    filter_df=filter_df[filter_df["Provider_Type"]==Provider_filter]

if food_filter!= "All":
    filter_df=filter_df[filter_df["Food_Type"]==food_filter]

st.subheader("Food Donation details")
st.dataframe(filter_df)

import pymysql
# MySQL connection setup
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="food_data"

)
cursor = conn.cursor()

st.sidebar.header("Users Record")
Options=st.sidebar.selectbox("Select",("Create","Update","Delete"))

if Options=="Create":
    st.sidebar.subheader("Create record")
    Name=st.sidebar.text_input("Enter your name")
    Type=st.sidebar.selectbox("Category",("Supermarket","Grocery Store","Restaurant","Catering Service"))
    Address=st.sidebar.text_input("Enter your Address")
    City=st.sidebar.text_input("Enter your City")
    Contact=st.sidebar.text_input("Enter your Contact")
    if st.sidebar.button("Create"):
        sql="INSERT INTO Providers(Name,Type,Address,City,contact) VALUES (%s,%s,%s,%s,%s)" 
        val=(Name,Type,Address,City,Contact)
        cursor.execute(sql,val)
        conn.commit()
        st.success("Record created")

elif Options=="Update":
    st.sidebar.subheader("Update record")
    Provider_ID=st.sidebar.number_input("Enter ID",min_value=1,step=1)
    Name=st.sidebar.text_input("Enter new name")
    Type=st.sidebar.selectbox("New Category",("Supermarket","Grocery Store","Restaurant","Catering Service"))
    Address=st.sidebar.text_input("Entncity")
    City=st.sidebar.text_input("Enter new City")
    Contact=st.sidebar.text_input("Enter new Contact")
    if st.sidebar.button("Update"):
        sql="Update Providers set Name=%s,Type=%s,Address=%s,City=%s,Contact=%s where Provider_ID=%s"
        val=(Name,Type,Address,City,Contact,Provider_ID)
        cursor.execute(sql,val)                                                                                                                                                                                                                                                                                             
        conn.commit()
        st.success("Record Updated")

elif Options=="Delete":
    st.sidebar.subheader("Delete record")
    Provider_ID=st.sidebar.number_input("Enter ID",min_value=1,step=1)
    if st.sidebar.button("Delete"):
        sql="Delete from providers where Provider_ID=%s"
        val=(Provider_ID,)
        cursor.execute(sql,val)
        conn.commit()
        st.success("Record deleted")


def run_query(query):
   
    conn = pymysql.connect(
        host="localhost",         
        user="root",
        password="root",
        database="food_data",
        
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df



QUERIES ={"Providers List summary" :"select * from Providers;",
          "Providers and receivers count in each city" :"select city,sum(provider_count) as total_provider_count,sum(receiver_count) as total_receiver_count from (select city ,count(*) as provider_count, 0 as receiver_count from providers group by city union all select city, 0 as provider_count, count(*) as receiver_count from receivers group by city) as combined group by city order by total_provider_count desc;",
          "Highest Food Contributor by category":"select type ,count(*) as provider_count from providers group by type limit 1;",
          "Food provider contact no for city New carol":"select contact from providers where city='New carol';",
          "top claimer":"""select claims.receiver_id,receivers.name,sum(foodlist.quantity) as total_quantity from claims join foodlist on claims.food_id=foodlist.food_id join receivers on claims.receiver_id =receivers.receiver_id where claims.status="completed" group by claims.receiver_id, receivers.name order by total_quantity desc limit 1;""",
          "Total_qty_By_providers":"""select sum(quantity)as Total_quantity from foodlist join providers on foodlist.provider_id=providers.provider_id;""",
          "Highest foodlist countcity_wise":"select location,food_name,count(*) as Total_food_count from foodlist group by location,food_name order by Total_food_count desc LIMIT 1;",
          "Most common food_type_donation":"select Food_Type,count(*) as Food_Type_count from foodlist group by food_type order by Food_Type_count desc;",
          "sucessful_Foodclaim_list":"""select foodlist.food_name,count(*) as food_count from claims join foodlist on claims.food_id=foodlist.food_id where claims.status="completed" group by food_name order by food_count desc;""",
          "Foodclaim_status_%":"""select status,count(*) as status_count,round(count(*)*100/(select count(*) from claims),2)as percentage from claims group by status order by percentage desc;""",
          "avgfoodclaimed per receiver":"""select receivers.receiver_id,receivers.name,avg(foodlist.quantity) as Avg_quantity_claimed from claims join foodlist ON claims.food_id = foodlist.food_id join receivers ON claims.receiver_id = receivers.receiver_id WHERE claims.status = "completed" GROUP BY receivers.receiver_id, receivers.name ORDER BY avg_quantity_claimed DESC;""",
          "Meal_type_cliamed_most":"""select foodlist.meal_type,count(*) as mealtype_count from claims join foodlist on claims.food_id=foodlist.food_id where claims.status = "completed" group by meal_type order by mealtype_count desc limit 1;""",
          "Total qty food donated by provider type":"select providers.type,sum(foodlist.quantity) as total_qty from foodlist join providers on foodlist.provider_id=providers.provider_id group by providers.type order by total_qty desc;",
          "Total qty food donated by provider type":"select providers.provider_id,providers.name,sum(foodlist.quantity) as total_qty from foodlist join providers on foodlist.provider_id=providers.provider_id group by providers.provider_id,providers.name order by total_qty  desc;",
          "Provider list based on food_type":"""select providers.provider_id,providers.name,providers.type,providers.city,providers.contact from providers join foodlist on providers.provider_id=foodlist.provider_id where foodlist.food_type="Non-Vegetarian";""",
          "Provider list based on food_type and Meal Type":"""select providers.provider_id,providers.name,providers.type,providers.city,providers.contact from providers join foodlist on providers.provider_id=foodlist.provider_id where foodlist.food_type="Non-Vegetarian" and foodlist.Meal_type="Lunch";""",
          "Total qty _claimed by receiever based on mealtype":"""select sum(foodlist.quantity)as Total_qty from foodlist join claims on foodlist.food_id=claims.food_id where claims.status="completed" and foodlist.Meal_type="Lunch";""",
          "Total qty _claimed by specific receiever type":"""select sum(foodlist.quantity) as total_qty_rec_type from foodlist join claims on foodlist.food_id=claims.food_id join receivers on claims.receiver_id=receivers.receiver_id where receivers.type="NGO";""",
          "Total qty _claimed by each receiever type":"select receivers.type,sum(foodlist.quantity) as total_qty from foodlist join claims on foodlist.food_id=claims.food_id join receivers on claims.receiver_id=receivers.receiver_id group by receivers.type order by total_qty DESC;",
          "Total % _claimed by each receiever type":"""select receivers.type as Rec_Type,sum(foodlist.quantity) as total_qty,round(sum(foodlist.quantity)*100/(select sum(foodlist.quantity) from foodlist JOIN claims ON foodlist.food_id = claims.food_id WHERE claims.status = 'completed'),2)as claim_percentage from foodlist join claims on foodlist.food_id=claims.food_id join receivers on claims.receiver_id=receivers.receiver_id where claims.status="completed"group by receivers.type order by total_qty DESC;""",
          "Top 3cities with providers and receierlist":"""select city,sum(provider_count) as total_provider_count,sum(receiver_count) as total_receiver_count,sum(provider_count+receiver_count) as total_count from (select city ,count(*) as provider_count, 0 as receiver_count from providers group by city union all select city, 0 as provider_count, count(*) as receiver_count from receivers group by city) as combined group by city order by total_count desc;"""
         }

st.title("Food waste management Queries")
query_name=st.selectbox("Select query",list(QUERIES.keys()))
query= QUERIES[query_name]
df=run_query(query)

st.subheader(f"Result:{query_name}")
print(df)
st.dataframe(df)
