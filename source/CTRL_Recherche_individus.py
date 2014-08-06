#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#-----------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-11 Ivan LUCAS
# Licence:         Licence GNU GPL
#-----------------------------------------------------------

import wx
import OL_Individus
import UTILS_Config

ID_CREER_FAMILLE = wx.NewId()
ID_MODIFIER_FAMILLE = wx.NewId()
ID_SUPPRIMER_FAMILLE = wx.NewId()
ID_PARAMETRES = wx.NewId()
ID_OUTILS = wx.NewId()

ID_ACTUALISER = wx.NewId()
ID_IMPRIMER = wx.NewId()
ID_APERCU = wx.NewId()
ID_EXPORT_EXCEL = wx.NewId()
ID_EXPORT_TEXTE = wx.NewId()
ID_AIDE = wx.NewId()


class ToolBar(wx.ToolBar):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TB_FLAT|wx.TB_TEXT
        wx.ToolBar.__init__(self, *args, **kwds)
        
        # Boutons
        self.AddLabelTool(ID_CREER_FAMILLE, u"Ajouter", wx.Bitmap("Images/32x32/Creer_famille.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Cr�er une nouvelle famille", "")
        self.AddSeparator()
        self.AddLabelTool(ID_MODIFIER_FAMILLE, u"Modifier", wx.Bitmap("Images/32x32/Modifier_famille.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Modifier l'individu s�lectionn�", "")
        self.AddLabelTool(ID_SUPPRIMER_FAMILLE, u"Supprimer", wx.Bitmap("Images/32x32/Supprimer_famille.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Supprimer ou d�tacher l'individu s�lectionn�", "")
        self.AddSeparator()
##        self.AddLabelTool(ID_PARAMETRES, u"Param�tres", wx.Bitmap("Images/32x32/Configuration2.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"S�lectionner les param�tres d'affichage", "")
        self.AddLabelTool(ID_OUTILS, u"Outils", wx.Bitmap("Images/32x32/Configuration.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Outils", "")

        # Binds
        self.Bind(wx.EVT_TOOL, self.Ajouter_famille, id=ID_CREER_FAMILLE)
        self.Bind(wx.EVT_TOOL, self.Modifier_famille, id=ID_MODIFIER_FAMILLE)
        self.Bind(wx.EVT_TOOL, self.Supprimer_famille, id=ID_SUPPRIMER_FAMILLE)
        self.Bind(wx.EVT_TOOL, self.Parametres, id=ID_PARAMETRES)
        self.Bind(wx.EVT_TOOL, self.MenuOutils, id=ID_OUTILS)
        
        self.SetToolBitmapSize((32, 32))
        self.Realize()
    
    def Ajouter_famille(self, event):
        self.GetParent().ctrl_listview.Ajouter(None)

    def Modifier_famille(self, event):
        self.GetParent().ctrl_listview.Modifier(None)

    def Supprimer_famille(self, event):
        self.GetParent().ctrl_listview.Supprimer(None)

    def Parametres(self, event):
        import DLG_Selection_individus
        dlg = DLG_Selection_individus.Dialog(self, afficherPresents=False)
        dlg.SetTitle(u"Param�tres d'affichage de la liste d'individus")
        parametres = UTILS_Config.GetParametre("liste_individus_parametre_activites", defaut=None)
        if parametres != None :
            dlg.radio_inscrits.SetValue(True)
            dlg.OnRadio(None)
            code, liste = parametres.split("###")
            listeID = []
            for ID in liste.split(";") :
                listeID.append(int(ID))
            if code == "liste_groupes_activites" :
                dlg.ctrl_activites.SetValeurs("groupes", listeID) 
            if code == "liste_activites" :
                dlg.ctrl_activites.SetValeurs("activites", listeID) 
            
            
        if dlg.ShowModal() == wx.ID_OK :
            # Tous les individus
            if dlg.GetMode() == "tous" :
                parametre = None
            # Uniquement les inscrits
            if dlg.GetMode() == "inscrits" :
                mode, listeIDtemp = dlg.ctrl_activites.GetValeurs() 
                listeID = []
                for ID in listeIDtemp :
                    listeID.append(str(ID))
                if mode == "groupes" : 
                    parametre = "liste_groupes_activites###%s" % ";".join(listeID)
                if mode == "activites" : 
                    parametre = "liste_activites###%s" % ";".join(listeID)
            # M�morisation du param�tre
            UTILS_Config.SetParametre("liste_individus_parametre_activites", parametre)
        dlg.Destroy() 
        
        # Actualise la liste d'individus
        self.GetParent().ActualiseParametresAffichage() 
        self.GetParent().ctrl_listview.MAJ(forceActualisation=True)
        
    def MenuOutils(self, event):
        # Cr�ation du menu Outils
        menuPop = wx.Menu()
            
        item = wx.MenuItem(menuPop, ID_APERCU, u"Aper�u avant impression", u"Imprimer la liste des effectifs affich�e")
        item.SetBitmap(wx.Bitmap("Images/16x16/Apercu.png", wx.BITMAP_TYPE_PNG))
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Apercu, id=ID_APERCU)
        
        item = wx.MenuItem(menuPop, ID_IMPRIMER, u"Imprimer", u"Imprimer la liste des effectifs affich�e")
        item.SetBitmap(wx.Bitmap("Images/16x16/Imprimante.png", wx.BITMAP_TYPE_PNG))
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Imprimer, id=ID_IMPRIMER)
        
        menuPop.AppendSeparator()

        item = wx.MenuItem(menuPop, ID_EXPORT_TEXTE, u"Exporter au format Texte", u"Exporter au format Texte")
        item.SetBitmap(wx.Bitmap("Images/16x16/Texte2.png", wx.BITMAP_TYPE_PNG))
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.GetParent().ctrl_listview.ExportTexte, id=ID_EXPORT_TEXTE)
        
        item = wx.MenuItem(menuPop, ID_EXPORT_EXCEL, u"Exporter au format Excel", u"Exporter au format Excel")
        item.SetBitmap(wx.Bitmap("Images/16x16/Excel.png", wx.BITMAP_TYPE_PNG))
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.GetParent().ctrl_listview.ExportExcel, id=ID_EXPORT_EXCEL)
        
        menuPop.AppendSeparator()

        item = wx.MenuItem(menuPop, ID_ACTUALISER, u"Actualiser", u"Actualiser l'affichage")
        item.SetBitmap(wx.Bitmap("Images/16x16/Actualiser2.png", wx.BITMAP_TYPE_PNG))
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Actualiser, id=ID_ACTUALISER)

        menuPop.AppendSeparator()
        
        item = wx.MenuItem(menuPop, ID_AIDE, u"Aide", u"Aide")
        item.SetBitmap(wx.Bitmap("Images/16x16/Aide.png", wx.BITMAP_TYPE_PNG))
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Aide, id=ID_AIDE)

        self.PopupMenu(menuPop)
        menuPop.Destroy()

    def Apercu(self, event):
        self.GetParent().ctrl_listview.Apercu(None)

    def Imprimer(self, event):
        self.GetParent().ctrl_listview.Imprimer(None)

    def Actualiser(self, event):
        self.GetParent().MAJ()

    def Aide(self, event):
        self.GetParent().Aide()


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name="recherche_individus", id=-1, style=wx.TAB_TRAVERSAL)
        
        self.toolBar = ToolBar(self)
        self.ctrl_listview = OL_Individus.ListView(self, id=-1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VRULES)
        self.ctrl_recherche = OL_Individus.BarreRecherche(self, historique=True)
        
        self.__set_properties()
        self.__do_layout()
        
        # Recherche param�tres d'affichage de la liste des individus
##        self.ActualiseParametresAffichage() 

    def __set_properties(self):
        pass

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=3, cols=1, vgap=0, hgap=0)
        grid_sizer_base.Add(self.toolBar, 1, wx.EXPAND|wx.ALL, 0)
        grid_sizer_base.Add(self.ctrl_listview, 1, wx.EXPAND|wx.ALL, 0)
        grid_sizer_base.Add(self.ctrl_recherche, 1, wx.EXPAND|wx.ALL, 0)
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableCol(0)
        self.SetSizer(grid_sizer_base)
        self.Layout()
        
    def MAJ(self):
        self.ctrl_listview.MAJ()

    def Aide(self):
        import UTILS_Aide
        UTILS_Aide.Aide("Lalistedesindividus")
    
    def ActualiseParametresAffichage(self):
        self.ctrl_listview.listeActivites = []
        self.ctrl_listview.listeGroupesActivites = []
        parametres = UTILS_Config.GetParametre("liste_individus_parametre_activites", defaut=None)
        if parametres != None :
            code, liste = parametres.split("###")
            listeID = []
            for ID in liste.split(";") :
                listeID.append(int(ID))
            if code == "liste_activites" : 
                self.ctrl_listview.listeActivites = listeID
            if code == "liste_groupes_activites" : 
                self.ctrl_listview.listeGroupesActivites = listeID


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        panel = wx.Panel(self, -1)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)
        self.ctrl= Panel(panel)
        self.ctrl.MAJ() 
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.ctrl, 1, wx.ALL|wx.EXPAND, 4)
        panel.SetSizer(sizer_2)
        self.Layout()
        self.CentreOnScreen()

if __name__ == '__main__':
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "TEST", size=(800, 400))
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()