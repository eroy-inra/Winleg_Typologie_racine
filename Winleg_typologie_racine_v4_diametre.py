'''
Created on 10 mars 2021

@author: EROY
'''
import cv2,math
import numpy as np
import os ,datetime,time
import pandas as pd

flag_choix_Rh=False
flag_choix_ROI_Rh=False
flag_move_ROI_Rh=False
flag_change_img_racine=True
flag_pointage_racine=False
flag_note_mesure_racine=False
flag_ordre_sup=False
flag_init_pointage=False
flag_refresh_w_Rh=False
flag_zoom=False

name_windows_Rh='Fenetre Rhizotrons'
name_windows_Rh_ROI='Fenetre de la zone du Rhizotron selectionne'


id_img_window_Rh=0
id_img_window_racine=0

dossier_image_mesure=''
dossier_image_rhizotrons=''
dossier_resultat=''
list_file_dossier_mesure=[]
list_file_dossier_rhizotrons=[]
list_image_dossier_mesure=[]
list_image_dossier_rhizotrons=[]
nb_image_dossier_mesure=0
nb_image_dossier_rhizotrons=0
extension_img=(".png")


ordre=0
lst_ordre=['primaire','secondaire','nodule']
id_racine=0

nom_rhizotron=""
id_racine=0
diam_racine=0.0
echelle_img_racine=0.0000
nom_complet_racine=''

resultats=[]
resultats_pts=[]
nb_resultat=0
#file_resultat='Winleg_Typologie_racine__v1.csv'


name_img_Rh=''
img_Rh,img_Rh_reduite = np.zeros((20,20,3), np.uint8),np.zeros((20,20,3), np.uint8)
Rh_x,Rh_y,Rh_reduit_x, Rh_reduit_y=0,0,-1,-1

name_img_Rh_Roi=''
img_Rh_ROI = np.zeros((400,400,3), np.uint8)
Rh_ROI_x_max,Rh_ROI_y_max=0,0
Rh_ROI_x1,Rh_ROI_x2,Rh_ROI_y1,Rh_ROI_y2=0,1,0,1
pos_move_rh=[0,0]

img_neutre = np.zeros((400,400,3), np.uint8)
img_rh_src= np.zeros((1000,700,3), np.uint8)
img_ret=np.zeros((400,400,3), np.uint8)
img_ret = cv2.line(img_ret,(200,100),(200,190),(255,255,255),3)
img_ret = cv2.line(img_ret,(200,210),(200,300),(255,255,255),3)
img_ret = cv2.line(img_ret,(100,200),(190,200),(255,255,255),3)
img_ret = cv2.line(img_ret,(210,200),(300,200),(255,255,255),3)

racine_pt1,racine_pt2=[-1,-1],[-1,-1]

f_zoom_rh=4
f_zoom_rh_roi=1

def mesure_racine(event,x,y,flags,param):
    global flags_mesure_racine,flags_zoom,rx,ry

    if flags_zoom:
        if event == cv2.EVENT_LBUTTONDOWN:
            rx,ry = x,y
            flags_mesure_racine=True

def trace_typologie (img_rh_typ,list_pts):
    color=[[139,255,149],[139,252,255],[139,187,255]]
    #img_rh = np.ones((12000,12000,3), np.uint8)*255
    try :
        for pts in list_pts:
            if pts[1]!=2:
                img_rh_typ = cv2.circle(img_rh_typ,(pts[3][0]//1,pts[3][1]//1), 10, (color[pts[1]]), -1)
            else:
                img_rh_typ = cv2.circle(img_rh_typ,(pts[3][0]//1,pts[3][1]//1), 20, (color[pts[1]]), 4)
                
            if pts[0]==0:
                pts_old=pts
            else:
                if pts[1]==0:
                    if pts[3][0]>0:
                        img_rh_typ = cv2.line(img_rh_typ,(pts_old[3][0]//1,pts_old[3][1]//1),(pts[3][0]//1,pts[3][1]//1),(color[pts[1]]),4)
                        x_txt=(pts_old[3][0]//1+pts[3][0]//1)//2
                        y_txt=(pts_old[3][1]//1+pts[3][1]//1)//2
                        if pts[0]==1:
                            img_rh_typ = cv2.putText(img_rh_typ,'P1',(x_txt-10,y_txt-8), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,(255,255,255),2,cv2.LINE_AA)
    
                    pts_old=pts
                elif pts[1]==1:
                    if pts[3][0]>0:
                        img_rh_typ = cv2.line(img_rh_typ,(list_pts[pts[0]][3][0]//1,list_pts[pts[0]][3][1]//1),(pts[3][0]//1,pts[3][1]//1),(color[pts[1]]),4)
                        x_txt=(list_pts[pts[0]][3][0]//1+pts[3][0]//1)//2
                        y_txt=(list_pts[pts[0]][3][1]//1+pts[3][1]//1)//2
                        img_rh_typ = cv2.putText(img_rh_typ,'S'+str(pts[0]),(x_txt-10,y_txt-8), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,(255,255,255),2,cv2.LINE_AA)
                        pts_old=pts
                        
    except :
        img_rh_typ = np.ones((12000,12000,3), np.uint8)*255                    
        print ("Probleme de creation de l'image de typologie")    
    return img_rh_typ

def mouse_act_Rh(event,x,y,flags,param):
    global flag_move_ROI_Rh,qflag_choix_Rh,flag_choix_ROI_Rh,id_img_window_Rh,nb_image_dossier_rhizotrons,Rh_x,Rh_y,img_Rh,Rh_x_zoom,Rh_y_zoom
    global nom_complet_racine,Rh_ROI_x1,Rh_ROI_y1,flag_mesure_racine,flag_note_mesure_racine,coord_x_nom_racine,coord_y_nom_racine
    if event == cv2.EVENT_LBUTTONDOWN:
        Rh_x,Rh_y = x,y
        flag_note_mesure_racine=True


def move_rh(img_rh_src,img_rh,chr_move,pos_move_rh,move_xy=[0,0]):
    tbx_roi_rh=[pos_move_rh[0],pos_move_rh[0]+1000,pos_move_rh[1],pos_move_rh[1]+900]
    pos_move_rh_dst=pos_move_rh
    inc=300
    img_rh.shape[0]
    if chr_move==0 :#init
        pass
    elif chr_move==52 :#fleche de gauche
        #print ('fleche de gauche')
        if pos_move_rh[1]>0 and pos_move_rh[1]<=img_rh.shape[0]-inc:
            tbx_roi_rh=[pos_move_rh[0],pos_move_rh[0]+1000,pos_move_rh[1]-inc,pos_move_rh[1]+900-inc]
            pos_move_rh_dst[1]=pos_move_rh[1]-300
    elif chr_move==54 :#fleche de droite
        if pos_move_rh[1]>=0 and pos_move_rh[1]<img_rh.shape[0]-inc:
            tbx_roi_rh=[pos_move_rh[0],pos_move_rh[0]+1000,pos_move_rh[1]+inc,pos_move_rh[1]+900+inc]
            pos_move_rh_dst[1]=pos_move_rh[1]+300
    elif chr_move==56 :#fleche de haut
        if pos_move_rh[0]>0 and pos_move_rh[0]<=img_rh.shape[1]-inc:
            tbx_roi_rh=[pos_move_rh[0]-inc,pos_move_rh[0]+1000-inc,pos_move_rh[1],pos_move_rh[1]+900]
            pos_move_rh_dst[0]=pos_move_rh[0]-300
    elif chr_move==50 :#fleche de bas
        if pos_move_rh[0]>=0 and pos_move_rh[0]<img_rh.shape[1]-inc:
            tbx_roi_rh=[pos_move_rh[0]+inc,pos_move_rh[0]+1000+inc,pos_move_rh[1],pos_move_rh[1]+900]
            pos_move_rh_dst[0]=pos_move_rh[0]+300
    elif chr_move==-1:
            tbx_roi_rh=[move_xy[0],move_xy[0]+1000,move_xy[1],move_xy[1]+900]
            pos_move_rh_dst=move_xy
    
    img_rh_src=img_rh[tbx_roi_rh[0]:tbx_roi_rh[1],tbx_roi_rh[2]:tbx_roi_rh[3],:]
    pos_move_rh=pos_move_rh_dst
    #print (tbx_roi_rh,pos_move_rh,img_rh_src.shape)
    return img_rh_src,pos_move_rh

#Listes des images et des dates a traiter
list_id_plante=[81,84]  
list_dossier_plante=[26204,26246,26276]

#Gestions de dossier image rhizotrons       
dossier_image_rhizotrons= "E:\\Eric\\Projets\\Winleg\\2021_01_18_PLAT18_U4_2021_03_19" 
dossier_resultat_typologie="E:\\Eric\\Projets\\Winleg\\2021_01_18_PLAT18_U4_2021_03_19\\Resultat_2021_05_19_095830"

list_file_typo_brute=os.listdir(dossier_resultat_typologie)
list_file_typo=[]
for f in list_file_typo_brute:
    if f[-13:]=="typologie.csv":
        list_file_typo.append([os.path.join(dossier_resultat_typologie,f),f.split("_")[0],f.split("_")[1]])




#wd_ = r'E:\\Eric\\Projets\\Winleg\\2021_01_18_PLAT18_U4_2021_03_19'#r'D:\INRAE_4PMI\2021_01_18_PLAT18_U4_2021_03_19'
wd_=dossier_image_rhizotrons
root_file = 'plat18_rhizocabimages.csv'
code_file = 'plat18_plantcodes.csv'
shoot_file = 'plat18_images.csv'
typ_file="Winleg_Typologie_racine__v1.csv"

datroot = pd.read_csv(os.path.join(wd_, root_file),sep=";")
datcodes = pd.read_csv(os.path.join(wd_, code_file),sep=";")
datshoot = pd.read_csv(os.path.join(wd_, shoot_file),sep=";")
scale=8
l_img=60

cv2.namedWindow(name_windows_Rh_ROI)
cv2.setMouseCallback(name_windows_Rh_ROI,mesure_racine)
flag_img=True
flag_init_img=True
flags_mesure_racine=False
flags_zoom=False
flag_break=False
flag_move=False
#listage des photos des rhizotrons

for typo in list_file_typo[:]:
    if flag_break:
        break
    typologie=pd.read_csv(os.path.join(typo[0]),sep=";")
    info_pl=datroot[datroot["taskid"] == int(typo[2])][ datroot["plantid"] == int(typo[1])]
    print ("taskid " ,int(typo[2]),"plantid ", int(typo[1]), info_pl['acquisitiondate'].values[0])
    list_image_dossier_rhizotrons=[]
    list_image_dossier_rhizotrons.append([id,typo[2],os.path.join(dossier_image_rhizotrons,str(typo[2]),str(info_pl['imgguid'].values[0])+".png"),str(info_pl['acquisitiondate'].values[0]),str(info_pl['imgguid'].values[0]),typologie])
    list_apex=''
    list_apex=pd.concat([typologie[typologie["id_ordre"]==0][-1:] ,typologie[typologie["id_ordre"]==1]])
    typologie['racine_pt1_x'] = -1.
    typologie['racine_pt1_y'] = -1.
    typologie['racine_pt2_x'] = -1.
    typologie['racine_pt2_y'] = -1.
    typologie['diametre'] = -1.0

    img_Rh=cv2.imread(list_image_dossier_rhizotrons[0][2])
    img_Rh=cv2.convertScaleAbs(img_Rh,alpha=1.8, beta=0)
    
#     img_Rh_0=np.where(img_Rh[:,:,0]>127,127,img_Rh[:,:,0])
#     img_Rh_1=np.where(img_Rh[:,:,1]>127,127,img_Rh[:,:,1])
#     img_Rh_2=np.where(img_Rh[:,:,2]>127,127,img_Rh[:,:,2])
#     img_Rh=cv2.merge((img_Rh_0,img_Rh_1,img_Rh_2))
#     img_Rh=(img_Rh*2)
    for apex in list_apex.index:
        
        print (list_apex.loc[apex]['nom_point_racine'],list_apex.loc[apex]['coord_y'],list_apex.loc[apex]['coord_x'])
        if flag_break:
            break
        print (apex)
        while(flag_img):

            k = cv2.waitKey(100) & 0xFF

            if flag_init_img:
                
                if not flag_move :
                    apex_x=list_apex.loc[apex]['coord_x']
                    apex_y=list_apex.loc[apex]['coord_y']
                else:
                    flag_move=False
                roi=[-1,-1,-1,-1]
                if apex_x-l_img<0:
                    roi[0]=0
                else:
                    roi[0]=apex_x-l_img
                if apex_x+l_img>12000:
                    roi[1]=12000
                else:
                    roi[1]=apex_x+l_img
                if apex_y-l_img<0:
                    roi[2]=0
                else:
                    roi[2]=apex_y-l_img
                if apex_y+l_img>12000:
                    roi[3]=12000
                else:
                    roi[3]=apex_y+l_img

                img_Rh_zoom = cv2.circle(img_Rh,(list_apex.loc[apex]['coord_x'],list_apex.loc[apex]['coord_y']), 20, (255,255,255), 1)
                img_Rh_zoom = cv2.circle(img_Rh,(list_apex.loc[apex]['coord_x'],list_apex.loc[apex]['coord_y']), 2, (255,255,255), -1)
                #zoom_racine=img_Rh[list_apex.loc[apex]['coord_y']-l_img:list_apex.loc[apex]['coord_y']+l_img,list_apex.loc[apex]['coord_x']-l_img:list_apex.loc[apex]['coord_x']+l_img]
                try : 
                    zoom_racine=img_Rh_zoom[roi[2]:roi[3],roi[0]:roi[1]]
                except:
                    zoom_racine=np.zeros((l_img*2,l_img*2,3))
                    print("Erreur zoom")
                #zoom_racine = cv2.circle(zoom_racine,(list_apex.loc[apex]['coord_y'],list_apex.loc[apex]['coord_x']), 2, (255,255,255), -1)
                zoom_racine=cv2.pyrUp(cv2.pyrUp(cv2.pyrUp(zoom_racine)))
                #zoom_racine=cv2.pyrUp(cv2.pyrUp(zoom_racine))
                flag_init_img=False
                #flags_zoom=True
                racine_pt1,racine_pt2=[-1,-1],[-1,-1]
            cv2.imshow(name_windows_Rh_ROI,zoom_racine)
            
            if flags_zoom:
                if flags_mesure_racine==True:
                    if racine_pt1[0]==-1:
                        racine_pt1=[rx,ry]
                        cv2.waitKey(500)
                        cv2.line(zoom_racine,(rx-20,ry),(rx,ry),(0,0,255),1)
                        cv2.line(zoom_racine,(rx,ry-20),(rx,ry+20),(0,0,255),1)
                        typologie._set_value(apex,'racine_pt1_x', apex_x +(((-l_img*scale)+rx)/scale))
                        typologie._set_value(apex,'racine_pt1_y', apex_y +(((-l_img*scale)+ry)/scale))
                        print (racine_pt1,apex_x +(((-l_img*scale)+rx)/scale),apex_y +(((-l_img*scale)+ry)/scale))
                        ix,iy,rx,ry = -1,-1,-1,-1
                        flags_mesure_racine=False
    
                    elif racine_pt2[0]==-1:
                        racine_pt2=[rx,ry]
                        cv2.line(zoom_racine,(rx,ry),(rx+20,ry),(0,0,255),1)
                        cv2.line(zoom_racine,(rx,ry-20),(rx,ry+20),(0,0,255),1)
                        cv2.imshow(name_windows_Rh_ROI,zoom_racine)
                        cv2.waitKey(1000)
                        diam_racine=round(((math.sqrt((racine_pt1[0]-racine_pt2[0])**2 + (racine_pt1[1]-racine_pt2[1])**2))/scale),3)
                        typologie._set_value(apex,'racine_pt2_x', apex_x +(((-l_img*scale)+rx)/scale))
                        typologie._set_value(apex,'racine_pt2_y', apex_y +(((-l_img*scale)+ry)/scale))
                        typologie._set_value(apex,'diametre',diam_racine)
                        print (racine_pt2,apex_x +(((-l_img*scale)+rx)/scale),apex_y +(((-l_img*scale)+ry)/scale))
                        print ("Mesure : ",diam_racine," pixel")
                        ix,iy,rx,ry = -1,-1,-1,-1
                        
                        flags_mesure_racine=False
                        flag_img=False
                        flag_init_img=True
                        flags_zoom=False
            
            if k==56 or k==50 or  k==52 or k==54:
                print ("move",k)
                flag_move=True
                flag_init_img=True
                if k==52 :#fleche de gauche
                    #print ('fleche de gauche')
                    if apex_x>100 and apex_x<=12000:
                        apex_x=apex_x-l_img
                elif k==54 :#fleche de droite
                    if apex_x>100 and apex_x<=12000:
                        apex_x=apex_x+l_img
                elif k==56 :#fleche de haut
                    if apex_y>100 and apex_y<=12000:
                        apex_y=apex_y-l_img
                elif k==50 :#fleche de bas
                    if apex_y>100 and apex_y<=12000:
                        apex_y=apex_y+l_img

            if k==ord('m'):
                print("Cliquer sur les bords exterieurs de la racine")
                flags_zoom=True
            if k==ord('q'):
                flag_break=True
                break
            if k==13 : #entree
                flag_init_img=True
                break
        flag_img=True
    #Sauvegarde des donnees
    typologie.to_csv(typo[0][:-4]+"_diametre.csv",sep=";",index=False)
    del typologie
    
cv2.destroyAllWindows()
