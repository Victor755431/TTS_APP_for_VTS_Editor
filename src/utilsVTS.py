def recolLignes(lignes):
    """Fonction qui permet de retirer les passages à la ligne au sein d'un seuke et même réplique"""
    def findLigne (lignes):
        c=0
        i=0
        listeElements = [""]
        while(listeElements[-1]!='\n'):
            newData = lignes[i].split('\t')
            listeElements[c] = listeElements[c][:-1]
            listeElements[c] += newData[0]
            listeElements += newData [1:]
            c+=len(newData)-1
            i+=1
        return listeElements,i
    res=[]
    i=0
    while lignes!= []:
        l,iPlus = findLigne(lignes)
        i = iPlus
        lignes = lignes[i:]
        newLine = '\t'.join(l)[:-1]
        res.append(newLine)
    return res