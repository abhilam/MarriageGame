"""

# Created on  3/23/2022

# Author: Abhishes Lamsal 

# Purpose: 

# Purpose Description

"""
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.write("# web App to calculated Marriage Card game")
st.write('Author: Abhishes Lamsal')

def maximum_value_in_column(column):

    highlight = 'background-color: palegreen;'
    default = ''
    maximum_in_column = column.max()
    # must return one string per cell in this column
    return [highlight if v == maximum_in_column else default for v in column]
def highlight_winingplayer(column,winingPlayer):
    highligh='background-color: palegreen'
    default =''

    return [highlight if v == winingPlayer else default for v in column]




def reset():
    import os
    from os.path import exists
    if exists(os.path.join(os.getcwd(),'numberofGame.txt')):
        os.remove('numberofGame.txt')
    if exists(os.path.join(os.getcwd(),'Final_result.csv')):
        os.remove('Final_result.csv')
    from streamlit import caching
    return

numberofPlayer=st.number_input('How many player',2,8,value=5,step=1)
if numberofPlayer!=5:
    reset()

def calculate_points(noofPlayer,ToMal,mal,seen,game,Dubli):
    if not seen :
        return (ToMal+10)*-1
    if  seen and not game :
        if Dubli:
            return (mal*noofPlayer)-ToMal
        if not Dubli:
            return(mal*noofPlayer)-(ToMal+3)

    if game:
        return -99


pl=st.columns(int(numberofPlayer))
newGame=st.button('NewGame')
if newGame:
    reset()
    #st.experimental_memo.clear()
    #st.experimental_singleton.clear()

players=[]
for i,item in enumerate(pl):
    with item:
        name_ofPlayer=st.text_input('player {} Name'.format(i),value='PL_'+str(i))
        players.append(name_ofPlayer)

def create_final_result():
    try:
        Final_result=pd.read_csv('Final_result.csv')
    except:
        Final_result=pd.DataFrame({'Player':players,'Final_owe':[0.0]*int(numberofPlayer)})
        Final_result.to_csv('Final_result.csv',index=False)
    return Final_result

def numbrofGame():
    try:
        with open('numberofGame.txt','r') as f:
            a=f.readline()
            a=0 if a=="" else int(a)
            return a
    except:
        a=0
        return a

with st.form('game input',clear_on_submit = True):

    cl=st.columns(int(numberofPlayer))
    result={'PlayerName':players,'Seen':[],'Mal':[],'Game':[],'Dubli':[]}

    for i,item in enumerate(cl):
        with item:
            name_ofPlayer=players[i]
            seen=st.checkbox('Seen',key=name_ofPlayer)
            result['Seen'].append(seen)
            print('seen',seen)
            Mal=st.number_input('Mal',key=name_ofPlayer, step=1)
            game=st.checkbox('Game',key=name_ofPlayer)
            dubli=st.checkbox('Dubli',key=name_ofPlayer)

            if game and dubli:
                Mal=Mal+5

            result['Mal'].append(Mal)
            result['Game'].append(game)
            result['Dubli'].append(dubli)
    submitted=st.form_submit_button("calculate")
    Final_result=create_final_result()
    if submitted:

        numberofGame=numbrofGame()
        numberofGame+=1
        with open('numberofGame.txt','w') as f:
            f.truncate()
            f.write(f"{numberofGame}")

        resdf=pd.DataFrame(result)
        if sum(resdf.Game)>1 or sum(resdf.Game)<1:
            st.write('more than one player or noone can not do game please check ')
            st.stop()
        resdf['totalMal']=sum(result['Mal'])
        for index,row in resdf.iterrows():
            print(int(numberofPlayer),row['totalMal'],row['Mal'],row['Seen'],row['Game'],row['Dubli'])
            resdf.loc[index,'owe']=calculate_points(int(numberofPlayer),row['totalMal'],row['Mal'],row['Seen'],row['Game'],row['Dubli'])
        resdf.loc[resdf.Game==True,'owe']=resdf[resdf.Game==False]['owe'].sum()*-1
        res=pd.read_csv('Final_result.csv')

        res.loc[:,'Final_owe']=Final_result.Final_owe+resdf.owe#[(resdf[['PlayerName','owe']])
        res['Game_'+str(int(numberofGame))]=resdf['owe']
        res.to_csv('Final_result.csv',index=False)
        a,b = st.columns(2)
        with a:
            final=create_final_result()
            gamePlayer_index=resdf.loc[resdf.Game==True].index[0]#['PlayerName']
            st.write('#Final Game summary')

            def style_specific_cell(x):
                color='background-color: lightred'
                df1=pd.DataFrame('',index=x.index,columns=x.columns)
                df1.iloc[gamePlayer_index,-1]=color
                return df1
            st.table(final.style.apply(maximum_value_in_column, subset=final.columns[1:2], axis=0).apply(style_specific_cell,axis=None))
            #st.table(final.style.apply(style_specific_cell,axis=None))
            st.write('#curent Game Status')
            st.dataframe(resdf)





newGame=st.button('Restart')
if newGame:
    reset()

