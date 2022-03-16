'''
Created on 10 mars 2021

@author: EROY
'''
import cv2
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

f_zoom_rh=1
f_zoom_rh_roi=1


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
    if flag_choix_Rh==False:
        pass
        if event == cv2.EVENT_LBUTTONDOWN:
            if 0<=id_img_window_Rh<nb_image_dossier_rhizotrons-1:
                id_img_window_Rh=id_img_window_Rh+1
                img_Rh,img_Rh_reduite = np.zeros((20,20,3), np.uint8),np.zeros((20,20,3), np.uint8)
        elif event == cv2.EVENT_RBUTTONDOWN:
            if 0<id_img_window_Rh<=nb_image_dossier_rhizotrons:
                id_img_window_Rh=id_img_window_Rh-1
                img_Rh,img_Rh_reduite = np.zeros((20,20,3), np.uint8),np.zeros((20,20,3), np.uint8)
        #print (id_img_window_Rh)
    else:
        if event == cv2.EVENT_MOUSEMOVE:
            Rh_x,Rh_y = x,y
            flag_move_ROI_Rh=True
            #print (Rh_x,Rh_y)
            
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

#wd_ = r'E:\\Eric\\Projets\\Winleg\\2021_01_18_PLAT18_U4_2021_03_19'#r'D:\INRAE_4PMI\2021_01_18_PLAT18_U4_2021_03_19'
wd_=dossier_image_rhizotrons
root_file = 'plat18_rhizocabimages.csv'
code_file = 'plat18_plantcodes.csv'
shoot_file = 'plat18_images.csv'

datroot = pd.read_csv(os.path.join(wd_, root_file),sep=";")
datcodes = pd.read_csv(os.path.join(wd_, code_file),sep=";")
datshoot = pd.read_csv(os.path.join(wd_, shoot_file),sep=";")

#listage des photos des rhizotrons
for id in list_id_plante:
    for dos_pl in list_dossier_plante:
        info_pl=datroot[datroot["taskid"] == dos_pl][ datroot["plantid"] == id]
        print (info_pl['acquisitiondate'].values)
        list_image_dossier_rhizotrons.append([id,dos_pl,os.path.join(dossier_image_rhizotrons,str(dos_pl),str(info_pl['imgguid'].values[0])+".png"),str(info_pl['acquisitiondate'].values[0]),str(info_pl['imgguid'].values[0])])
nb_image_dossier_rhizotrons=len(list_image_dossier_rhizotrons)
#list_image_dossier_rhizotrons.sort()

#Creation du dossier resultat
dossier_resultat=os.path.join(dossier_image_rhizotrons,'Resultat_{:%Y_%m_%d_%H%M%S}'.format(datetime.datetime.utcfromtimestamp(time.time())))
#dossier_resultat=os.path.join(dossier_image_rhizotrons,'Image_Typologie')
if not os.path.isdir(dossier_resultat):
    os.mkdir(dossier_resultat)
# f_data = open(os.path.join(dossier_image_rhizotrons,file_resultat), "a")
# if f_data.tell()==0:
#     f_data.write("plantid;taskid;acquisitiondate;nom_point_racine;ordre_txt;ordre_num;id_ordre;id_point;coord_x;coord_y;date_pointage\n")
# f_data.close()



#Creation des fenetres
cv2.namedWindow(name_windows_Rh)
cv2.setMouseCallback(name_windows_Rh,mouse_act_Rh)
cv2.namedWindow(name_windows_Rh_ROI)


while(1):
    k = cv2.waitKey(100) & 0xFF
    #print(k)
    if k == ord('q'):#lettre q pour quitter
        if flag_choix_Rh :
            print("Impossible de quitter avant de finir le pointage")
        else:
            break

    elif k==ord('v'):#lettre v pour valider le Rhizotrons
        flag_choix_Rh=True
        print("Image validee")

    if k==13 : #entree
        if flag_choix_Rh:
            nom_complet_racine=str(ordre)+'-'+str(id_racine)
            print("Racine {} {} : [-:-]".format(lst_ordre[ordre],nom_complet_racine))
            resultats.append(str(list_image_dossier_rhizotrons[id_img_window_Rh][0])+";"+str(list_image_dossier_rhizotrons[id_img_window_Rh][1])+";"+str(list_image_dossier_rhizotrons[id_img_window_Rh][3])       \
                     +";"+nom_complet_racine+";"+lst_ordre[ordre]+";"+str(ordre)+";"+str(id_racine)+";"+str(-1)+";"+str(-1)    \
                     +";"+'{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(time.time())))
            resultats_pts.append([id_racine,ordre,lst_ordre[ordre],[-1,-1]])

            id_racine+=1
    if k==ord('z') : 
        if flag_choix_Rh:
            resultats.pop(-1)
            resultats_pts.pop(-1)
            cv2.putText(img_Rh,str("---"),(coord_x_nom_racine+15,coord_y_nom_racine), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,0,255),1,cv2.LINE_AA)
            cv2.putText(img_Rh,str("."),(coord_x_nom_racine-4,coord_y_nom_racine+1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,0,255),1,cv2.LINE_AA)
            nom_complet_racine=str(ordre)+'-'+str(id_racine)
            print("Racine {} {} : supprimee".format(lst_ordre[ordre],nom_complet_racine))
            flag_refresh_w_Rh=True
            id_racine-=1
        
    if k==27 : #echap
        flag_choix_Rh , flag_choix_ROI_Rh ,flag_refresh_w_Rh= False, False,False
        flag_change_img_racine=True
        nom_rhizotron=""
        id_racine=0
        img_Rh,img_Rh_reduite = np.zeros((20,20,3), np.uint8),np.zeros((20,20,3), np.uint8)
        
    elif k==ord('o'):#lettre o pour ordre suivant
        if flag_choix_Rh :
            flag_ordre_sup=True

    elif k==56 or k==50 or  k==52 or k==54:
        #print ("move",k)
        img_Rh_red_move,pos_move_rh=move_rh(img_rh_src,img_Rh_reduite,k,pos_move_rh)
        cv2.imshow(name_windows_Rh,img_Rh_red_move)
    elif k==ord('s'):#lettre s pour suivant Rh
        if flag_choix_Rh :
            print ("Image suivante")
            flag_choix_Rh=False    
            name_img_Rh=str(list_image_dossier_rhizotrons[id_img_window_Rh][0])+"_"+str(list_image_dossier_rhizotrons[id_img_window_Rh][1])+"_"+str(list_image_dossier_rhizotrons[id_img_window_Rh][4])
#             cv2.imwrite(os.path.join(dossier_resultat,(name_img_Rh+".png")),img_Rh_resized)
            
            img_rh_typ=trace_typologie(img_Rh,resultats_pts)
            #img_rh_typ=cv2.addWeighted(img_Rh,1,img_rh_typ,0.5,0)
            cv2.imwrite(os.path.join(dossier_resultat,(name_img_Rh+"_typologie.jpg")),img_rh_typ)
            
            file_resultat=name_img_Rh+"_typologie.csv"
            f_data = open(os.path.join(dossier_resultat,file_resultat), "w")
            f_data.write("plantid;taskid;acquisitiondate;nom_point_racine;ordre;id_ordre;id_point;coord_x;coord_y;date_pointage\n")
            for j in range(0,len(resultats)):
                f_data.write(resultats[j]+"\n")
                #f_data.write("\n")
            f_data.close()
            
            resultats=[]
            resultats_pts=[]
            flag_choix_Rh , flag_choix_ROI_Rh ,flag_refresh_w_Rh= False, False,False
            flag_change_img_racine=True
            nom_rhizotron=""
            id_racine=0
            ordre=0
            if id_img_window_Rh>=nb_image_dossier_rhizotrons:
                id_img_window_Rh+=1
                #img_Rh=np.zeros((20,20,3), np.uint8)
            img_Rh,img_Rh_reduite = np.zeros((20,20,3), np.uint8),np.zeros((20,20,3), np.uint8)
            cv2.imshow(name_windows_Rh_ROI,img_neutre)
            print ("Choisissez la nouvelle image")
    
    if flag_choix_Rh==False:
        if img_Rh.shape[0]==20: 
            if os.path.isfile(list_image_dossier_rhizotrons[id_img_window_Rh][2]):
                print("open_img_rhizotron",id_img_window_Rh,list_image_dossier_rhizotrons[id_img_window_Rh][2])
                img_Rh=cv2.imread(list_image_dossier_rhizotrons[id_img_window_Rh][2])
                
                img_Rh_0=np.where(img_Rh[:,:,0]>127,127,img_Rh[:,:,0])
                img_Rh_1=np.where(img_Rh[:,:,1]>127,127,img_Rh[:,:,1])
                img_Rh_2=np.where(img_Rh[:,:,2]>127,127,img_Rh[:,:,2])
                img_Rh=cv2.merge((img_Rh_0,img_Rh_1,img_Rh_2))
                img_Rh=(img_Rh*2)

                
                img_Rh_reduite=np.copy(img_Rh)
                for f in range(f_zoom_rh):
                    img_Rh_reduite=cv2.pyrDown(img_Rh_reduite)
                img_Rh_red_move,pos_move_rh=move_rh(img_rh_src,img_Rh_reduite,0,pos_move_rh)
                Rh_ROI_x_max,Rh_ROI_y_max=img_Rh_reduite.shape[1],img_Rh_reduite.shape[0]
            else :
                print("Impossible de trouver l'image : {}".format(list_image_dossier_rhizotrons[id_img_window_Rh][2]))
                
        cv2.imshow(name_windows_Rh,img_Rh_red_move)
        Rh_x,Rh_y,Rh_reduit_x, Rh_reduit_y=0,0,-1,-1

    else:
        if flag_refresh_w_Rh:
            img_Rh_reduite=np.copy(img_Rh)
            for f in range(f_zoom_rh):
                img_Rh_reduite=cv2.pyrDown(img_Rh_reduite)
            img_Rh_red_move,pos_move_rh=move_rh(img_rh_src,img_Rh_reduite,0,pos_move_rh)
            Rh_ROI_x_max,Rh_ROI_y_max=img_Rh_reduite.shape[1],img_Rh_reduite.shape[0]
            cv2.imshow(name_windows_Rh,img_Rh_red_move)
            flag_refresh_w_Rh=False

        if flag_move_ROI_Rh==True:
            Tx,Ty=0,0
            #print(Rh_x,Rh_y)
            Rh_x_z=(Rh_x+(pos_move_rh[1]))#/(2**f_zoom_rh)))
            Rh_y_z=(Rh_y+(pos_move_rh[0]))#/(2**f_zoom_rh)))
            if Rh_x_z<200/(2**f_zoom_rh):
                Rh_ROI_x1,Rh_ROI_x2=0,400#((Rh_x_z*4)+200)
                Tx=200-Rh_x_z*(2**f_zoom_rh)
            elif 200/(2**f_zoom_rh)<Rh_x_z<Rh_ROI_x_max-200/(2**f_zoom_rh):
                Rh_ROI_x1,Rh_ROI_x2=((Rh_x_z*(2**f_zoom_rh))-200),((Rh_x_z*(2**f_zoom_rh))+200)
            elif Rh_x_z>Rh_ROI_x_max-(200/(2**f_zoom_rh)):
                Rh_ROI_x1,Rh_ROI_x2=(Rh_ROI_x_max*(2**f_zoom_rh))-400,Rh_ROI_x_max*(2**f_zoom_rh)
                Tx=-(200-(Rh_ROI_x_max-Rh_x_z)*(2**f_zoom_rh))
            if Rh_y_z<200/(2**f_zoom_rh):
                Rh_ROI_y1,Rh_ROI_y2=0,400#((Rh_y_z*4)+200)
                Ty=200-Rh_y_z*(2**f_zoom_rh)
            elif 200/(2**f_zoom_rh)<Rh_y_z<Rh_ROI_y_max-200/(2**f_zoom_rh):
                Rh_ROI_y1,Rh_ROI_y2=((Rh_y_z*(2**f_zoom_rh))-200),((Rh_y_z*(2**f_zoom_rh))+200)        
            elif Rh_y_z>Rh_ROI_y_max-(200/(2**f_zoom_rh)):
                Rh_ROI_y1,Rh_ROI_y2=(Rh_ROI_y_max*(2**f_zoom_rh))-400,Rh_ROI_y_max*(2**f_zoom_rh)
                Ty=-(200-(Rh_ROI_y_max-Rh_y_z)*(2**f_zoom_rh))
            
            img_Rh_ROI= img_Rh [int(Rh_ROI_y1):int(Rh_ROI_y2),int(Rh_ROI_x1):int(Rh_ROI_x2)]
            #print(Rh_x_z,Rh_y_z,Tx,Ty)
            M = np.float32([[1,0,Tx],[0,1,Ty]])
            img_Rh_ROI_T = cv2.warpAffine(img_Rh_ROI,M,(400,400))
            img_Rh_ROI_zoom=np.copy(img_Rh_ROI_T)
            img_ret_zoom=np.copy(img_ret)
            for f in range(f_zoom_rh_roi):
                img_Rh_ROI_zoom=cv2.pyrUp(img_Rh_ROI_zoom)
                img_ret_zoom=cv2.pyrUp(img_ret)
            img_Rh_ROI_zoom = cv2.addWeighted(img_Rh_ROI_zoom,1,img_ret_zoom,0.3,0)
            cv2.imshow(name_windows_Rh_ROI,img_Rh_ROI_zoom)
            flag_move_ROI_Rh=False

        if flag_ordre_sup:
            ordre+=1
            if ordre==0:
                id_racine=0
            else:
                id_racine=1
            print("")
            print("Ordre racine : ",ordre, lst_ordre[ordre])
            flag_ordre_sup=False
            flag_init_pointage=False
        
        if flag_note_mesure_racine:
            Rh_x_p=int(Rh_x+(pos_move_rh[1]))
            Rh_y_p=int(Rh_y+(pos_move_rh[0]))
            coord_x_nom_racine,coord_y_nom_racine=Rh_x_p*(2**f_zoom_rh),Rh_y_p*(2**f_zoom_rh)
            nom_complet_racine=str(ordre)+'-'+str(id_racine)
            #print("Racine {} {} : [{}:{}][{}:{}][{}:{}]".format(lst_ordre[ordre],nom_complet_racine,coord_x_nom_racine,coord_y_nom_racine,Rh_x,Rh_y,pos_move_rh[1],pos_move_rh[0]))
            print("Racine {} {} : [{}:{}]".format(lst_ordre[ordre],nom_complet_racine,coord_x_nom_racine,coord_y_nom_racine,Rh_x,Rh_y,pos_move_rh[1],pos_move_rh[0]))
            cv2.putText(img_Rh,str(nom_complet_racine),(coord_x_nom_racine+15,coord_y_nom_racine), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(img_Rh,str("."),(coord_x_nom_racine-4,coord_y_nom_racine+1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255),1,cv2.LINE_AA)
            resultats.append(str(list_image_dossier_rhizotrons[id_img_window_Rh][0])+";"+str(list_image_dossier_rhizotrons[id_img_window_Rh][1])+";"+str(list_image_dossier_rhizotrons[id_img_window_Rh][3])       \
                                 +";"+nom_complet_racine+";"+lst_ordre[ordre]+";"+str(ordre)+";"+str(id_racine)+";"+str(coord_x_nom_racine)+";"+str(coord_y_nom_racine)    \
                                 +";"+'{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(time.time())))
            resultats_pts.append([id_racine,ordre,lst_ordre[ordre],[coord_x_nom_racine,coord_y_nom_racine]])
            id_racine+=1
            flag_note_mesure_racine=False
            flag_init_pointage=False

            flag_refresh_w_Rh=True
cv2.destroyAllWindows()
