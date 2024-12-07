import streamlit as st
from streamlit_option_menu import option_menu
import Load_data as LD
import PdSQL as PS
import seaborn as sns
# import done to avoid warnings 
from warnings import filterwarnings

def formString(sqllis):
    instr = ''

    if len(sqllis) == 0 :
        instr = "'" + 'All' + "'" 
    
    for i in sqllis:
        if i != 'All':
            if i != 'Blank':
                instr = instr + "'" + i + "',"
            else:
                instr = instr + "'" + ' ' + "',"
        else:
            instr =   "'" + 'All' + "'" 
            break
    instr = instr.strip(',')     
    return instr  

def formInt(sqllis):
    inInt = ''

    if len(sqllis) == 0 :
        inInt = '-99999'

    for i in sqllis:
        if i != 'All':
            inInt = inInt + str(i) + ","
        else:
            inInt =   '-99999'
            break
    inInt = inInt.strip(',')     
    return inInt  

######################################################################################## Main Page code ##########################################

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Data'], 
        icons=['house', 'database'], menu_icon="cast", default_index=0)
    if selected == "Home":
        with st.sidebar:
            selected1 = option_menu("Date Display", ["Dash Board","Competiton Category", 'Complexes', 'Ranking'], 
                menu_icon="cast", default_index=0)    

   
if selected == 'Data' :
    ld = LD.Load_Date()
    if st.button("load data"):
        ld.load_data()
        st.success("Data Loaded")
    if st.button("Delete All data"):
        ld.Delete_tables()
        st.success("Data Deleted")
    if st.button("Delete Current Week Ranking"):
        ld.Delete_Current_week()
        st.success("Current Week Data Deleted")
    ld.close_connection()
    
if selected == "Home":
    ps = PS.PdSQL()
    if selected1 == "Dash Board" :
        try:
            st.write( " # Over All Information")
            c1,c2,c3 = st.columns(3)

            sql = "select count(*) as 'Number of Categories' from guviproj1.Categories"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            c1.dataframe(styled_df, hide_index=True)

            sql = "select count(*) as 'Number of Competitions' from guviproj1.Competitions"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            c2.dataframe(styled_df, hide_index=True)

            sql = "select count(*) as 'Number of Complexes' from guviproj1.Complexes"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            c1.dataframe(styled_df, hide_index=True)

            sql = "select count(*) as 'Number of Venues' from guviproj1.Venues"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            c2.dataframe(styled_df, hide_index=True)

            sql = "select count(*) as 'Number of Competitors' from guviproj1.Competitors"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            c3.dataframe(styled_df, hide_index=True)

            sql = "select count(distinct country) as 'Number of Countries' from  guviproj1.Competitors"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            c3.dataframe(styled_df, hide_index=True)

            st.write( " ## Leaderboards")

            st.write( " ### Top Players")

            sql = f"select  CR.points as Points, \
                    CR.competitions_played as 'Competitions Played',  CR.gender as 'Gender', \
                    CP.name as 'Competitor Name',  CP.Country as 'Country' , \
                    CP.country_code as 'Country Code',  CP.abbreviation as 'Competitor Abbreviation'\
                    from guviproj1.Competitor_Rankings CR, guviproj1.Competitors CP where CR.competitor_id = CP.competitor_id and CR.rank = 1"
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            st.dataframe(styled_df, hide_index=True)

            st.write( " ### Player with Highest Points")

            sql = f"select  CR.points as Points, \
                    CR.competitions_played as 'Competitions Played',  CR.gender as 'Gender', \
                    CP.name as 'Competitor Name',  CP.Country as 'Country' , \
                    CP.country_code as 'Country Code',  CP.abbreviation as 'Competitor Abbreviation'\
                    from guviproj1.Competitor_Rankings CR, guviproj1.Competitors CP where CR.competitor_id = CP.competitor_id and CR.points = ( select max(points) from guviproj1.Competitor_Rankings) "
            print(sql)
            df = ps.getData(sql)
            styled_df = df.style.set_properties(**{'text-align': 'center'})
            st.dataframe(styled_df, hide_index=True)            



        except Exception as e:
            print(f"An error occurred: {e}")

####################################################### Competiton Category ####################################################################
    if selected1 == "Competiton Category" :
        try:
            st.title("Competiton Category")
            Gen, Cat = st.columns(2)

    ########################################### Gender Filter ####################################################################
            sql = "select distinct gender from guviproj1.Competitions"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Gen.multiselect('Gender',resList )
            GenStr = formString(GenSel)

    ########################################### Parent ID Filter / displaying the parent id in the gender column ####################################################################
            sql = "select distinct parent_id from guviproj1.Competitions"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            resList.insert(1,'Blank')            
            GenSel = Gen.multiselect('Parent ID',resList )
            PaIDStr = formString(GenSel) 

    ########################################### Type Filter / displaying in the category column####################################################################
            sql = "select distinct type from guviproj1.Competitions"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Cat.multiselect('Type',resList )
            TypStr = formString(GenSel)

    ########################################### Category Filter  ####################################################################
            sql = "select distinct category_name from guviproj1.Categories"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            
            GenSel = Cat.multiselect('Category',resList )

            CatStr = formString(GenSel)

            sql = f"select  CP.competition_name as 'Competition Name', CP.gender as Gender, CP.parent_id as 'Parent ID', \
                    CP.type as Type,  CT.category_name as 'Category Name' from guviproj1.Competitions CP ,  \
                        guviproj1.Categories CT where CP.category_id = CT.category_id and \
                              (CP.gender in ( {GenStr} ) or  'All' in ({GenStr})) and (CP.parent_id in ( {PaIDStr} ) or  'All' in ({PaIDStr})) \
                                and (CP.type in ( {TypStr} ) or  'All' in ({TypStr})) and (CT.category_name in ( {CatStr} ) or  'All' in ({CatStr}));" 
            
            #CP.competition_id as 'Competition ID', CT.category_id as 'Category ID',
            print(sql)
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)

            c1,c2 = st.columns(2)

            sql = "select count(*) as 'Number of Competitions' from guviproj1.Competitions"
            resList = ps.getDataAsList(sql)
            c1.write(f"Over Total Competitions: {resList[0]} ")          

            sql = f"select count(*) from guviproj1.Competitions CP ,  \
                        guviproj1.Categories CT where CP.category_id = CT.category_id and \
                              (CP.gender in ( {GenStr} ) or  'All' in ({GenStr})) and (CP.parent_id in ( {PaIDStr} ) or  'All' in ({PaIDStr})) \
                                and (CP.type in ( {TypStr} ) or  'All' in ({TypStr})) and (CT.category_name in ( {CatStr} ) or  'All' in ({CatStr}));" 
            resList = ps.getDataAsList(sql)
            c2.write(f"Total Competition as per filter: {resList[0]} ")   

            st.title("Competiton per Category")

            sql = f"select CT.category_name as 'Category', count(CP.competition_name ) as 'Number of Competitions' from guviproj1.Competitions CP , guviproj1.Categories CT where CP.category_id = CT.category_id group by CT.category_name;" 
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)  

            st.title("Distribution of Competiton by Category")

            st.bar_chart(df, x='Category', y='Number of Competitions')

        except Exception as e:
            print(f"An error occurred: {e}")


####################################################### Complexes ####################################################################
    if selected1 == "Complexes" :
        try:
            st.title("Complexes")


            Gen, Cat = st.columns(2)

    ########################################### Complex Filter ####################################################################
            sql = "select distinct complex_name from guviproj1.complexes"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Gen.multiselect('Complex Name',resList )

            cplxStr = formString(GenSel)

    ########################################### venue_name Filter / displaying the venue_name in the gender column ####################################################################
            sql = "select distinct venue_name from guviproj1.venues"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            # resList.insert(1,'Blank ')            
            GenSel = Gen.multiselect('Venue Name',resList )

            vnstr = formString(GenSel)


    ########################################### City Name Filter / displaying in the category column####################################################################
            sql = "select distinct city_name from guviproj1.venues"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Cat.multiselect('City Name',resList )

            ctysty = formString(GenSel)

    ########################################### Country Name Filter  ####################################################################
            sql = "select distinct country_name from guviproj1.venues"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Cat.multiselect('Country Name',resList )

            constr = formString(GenSel)

    ########################################### Country Code Filter / displaying in the category column####################################################################
            sql = "select distinct country_code from guviproj1.venues"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Cat.multiselect('Country Code',resList )

            ccstr = formString(GenSel)

    ########################################### timezone Filter  ####################################################################
            sql = "select distinct timezone from guviproj1.venues"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Gen.multiselect('Time Zone',resList )

            tzstr = formString(GenSel)


            sql = f"select CP.complex_name as 'Complex Name', \
                        VN.venue_name as 'Venue Name', VN.city_name as 'City Name', \
                        VN.country_name as 'Country Name', VN.country_code as 'Country Code',\
                        VN.timezone as 'Time Zone' from guviproj1.complexes CP left join guviproj1.venues VN on \
                        CP.complex_id = VN.complex_id where \
                        (CP.complex_name in ({cplxStr}) or 'All' in ({cplxStr}) ) and \
                        (VN.venue_name in ({vnstr}) or 'All' in ({vnstr}) ) and \
                        (VN.city_name in ({ctysty}) or 'All' in ({ctysty}) ) and \
                        (VN.country_name in ({constr}) or 'All' in ({constr}) ) and \
                        (VN.country_code in ({ccstr}) or 'All' in ({ccstr}) ) and \
                        (VN.timezone in ({tzstr}) or 'All' in ({tzstr}) ); "
                        #  (VN.complex_id is null or 'Blank ' not in ({vnstr}) ) and \
            print(sql)
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)

            st.title("Complex and Venus count")

            sql = f"select CP.complex_name as 'Complex', \
                        count(VN.venue_name ) as 'Venue Count' from guviproj1.complexes CP left join guviproj1.venues VN on \
                        CP.complex_id = VN.complex_id  \
                        group by  CP.complex_name;"
            print(sql)
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)            

            st.markdown( "## Complex with More than One Venue")

            sql = f"select CP.complex_name as 'Complex', \
                        count(VN.venue_name ) as 'Venue Count' from guviproj1.complexes CP left join guviproj1.venues VN on \
                        CP.complex_id = VN.complex_id  \
                        group by  CP.complex_name having count(VN.venue_name ) > 1;"
            print(sql)
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)     


            st.markdown( "## Venue Count By Country")

            sql = f"select VN.country_name as 'Country ', \
                        count(VN.venue_name ) as 'Venue Count' from guviproj1.venues VN \
                        group by  VN.country_name ;"
            print(sql)
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)     



        except Exception as e:
            print(f"An error occurred: {e}")


############################################################################# RANK Page #############################################################################


    if selected1 == "Ranking" :
        try:

            
            st.title("COMPETITOR RANKINGS")

    ########################################### Rank Filter ####################################################################
            sql = "select distinct rank from guviproj1.Competitor_Rankings"
            resList = ps.getDataAsList(sql)
            
            rnk_min, rnk_max = st.select_slider('Rank',resList , value=(1,10) )


    ################## create the column #################


            Gen, Cat = st.columns(2)


    ########################################### Movement filter ####################################################################
            sql = "select distinct movement from guviproj1.Competitor_Rankings order by movement"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Gen.multiselect('Movement',resList )
            mntStr = formInt(GenSel) 


    ########################################### Played Filter  ####################################################################
            sql = "select distinct competitions_played from guviproj1.Competitor_Rankings order by competitions_played"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            
            GenSel = Cat.multiselect('Played',resList )
            pldStr = formInt(GenSel)

    ########################################### gender filter ####################################################################
            sql = "select distinct gender from guviproj1.Competitor_Rankings"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
         
            GenSel = Gen.multiselect('Gender',resList )
            GenStr = formString(GenSel) 

    ########################################### Year filter ####################################################################
            sql = "select distinct year from guviproj1.Competitor_Rankings order by year"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
         
            GenSel = Gen.multiselect('Year',resList )
            yrStr = formInt(GenSel) 

    ########################################### week  ####################################################################
            sql = "select distinct week from guviproj1.Competitor_Rankings order by week"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            GenSel = Cat.multiselect('Week',resList )
            wkStr = formInt(GenSel)

    ########################################### Competitor Filter  ####################################################################
            sql = "select distinct name from guviproj1.Competitors order by name"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            
            GenSel = Cat.multiselect('Competitor',resList )
            ComStr = formString(GenSel)

    ########################################### Country Filter  ####################################################################
            sql = "select distinct country from guviproj1.Competitors order by country"
            resList = ps.getDataAsList(sql)
            resList.insert(0,'All')
            
            GenSel = Gen.multiselect('Country',resList )
            ConStr = formString(GenSel)


    ########################################### Rank Filter ####################################################################
            
            sql = "select max(points) as Maxi, min(points) as Mini from guviproj1.Competitor_Rankings"
            dl = ps.getDataAsList(sql)

            pma = dl[0]
            pmi = dl[1]

            pts_min , pts_max = st.slider('Points',pmi,pma, value=(pmi,pma)  )

            # print (pts_min , pts_max)


            sql = f"select  CR.rank as Rank, CR.movement as Movement, CR.points as Points, \
                    CR.competitions_played as 'Competitions Played',  CR.gender as 'Gender', \
                    CR.year as 'Year',  CR.week as 'Week',  \
                    CP.name as 'Competitor Name',  CP.Country as 'Country' , \
                    CP.country_code as 'Country Code',  CP.abbreviation as 'Competitor Abbreviation'\
                    from guviproj1.Competitor_Rankings CR, guviproj1.Competitors CP where CR.competitor_id = CP.competitor_id and \
                    (CR.rank between {rnk_min} and {rnk_max}) and \
                    (CR.points between {pts_min} and {pts_max}) and \
                    (CR.movement in ({mntStr}) or -99999 in ({mntStr})) and \
                    (CR.year in ({yrStr}) or -99999 in ({yrStr})) and \
                    (CR.week in ({wkStr}) or -99999 in ({wkStr})) and \
                    (CR.competitions_played in ({pldStr}) or -99999 in ({pldStr})) and \
                    (CP.Country in ( {ConStr} ) or  'All' in ({ConStr})) and \
                    (CR.gender in ( {GenStr} ) or  'All' in ({GenStr})) and (CP.name in ( {ComStr} ) or  'All' in ({ComStr})) ;"

            
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)
            
            sql = f"select country as Country, count(CR.competitor_id) as 'Number of Competitors', sum(points) as 'Total Points of Competitors', round(avg(points),1) as 'Average of Points' \
                    from guviproj1.Competitor_Rankings CR, guviproj1.Competitors CP where CR.competitor_id = CP.competitor_id  and \
                    (CR.rank between {rnk_min} and {rnk_max}) and \
                    (CR.points between {pts_min} and {pts_max}) and \
                    (CR.movement in ({mntStr}) or -99999 in ({mntStr})) and \
                    (CR.year in ({yrStr}) or -99999 in ({yrStr})) and \
                    (CR.week in ({wkStr}) or -99999 in ({wkStr})) and \
                    (CR.competitions_played in ({pldStr}) or -99999 in ({pldStr})) and \
                    (CP.Country in ( {ConStr} ) or  'All' in ({ConStr})) and \
                    (CR.gender in ( {GenStr} ) or  'All' in ({GenStr})) and (CP.name in ( {ComStr} ) or  'All' in ({ComStr})) \
                    group by country order by country ;"
            
            print (sql)
            df = ps.getData(sql)
            st.dataframe(df, hide_index=True)     

        except Exception as e:
            print(f"An error occurred: {e}")

    ps.close_connection()