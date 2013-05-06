# -*- coding: utf-8 -*-
# This file intends to parse the skos RDF directoryskos_nm_parser.py
# ParserType                       :    Node Maker 
# Input                            :    RDF Database - skos 
# Output                           :   A set of nodes G(E) contaning nodes of each unique concept i.e. a category whose broader is available as resource. (shortabsNodes.pick) 
# Structure  of Node:
#                   Node Name: Name of category
#    	    Node Attributes: Maincat - subcat
#
#  status: working

import parser
import re
import networkx as nx
import matplotlib.pyplot as plt
import time
import pickle
import smallutilities as sm
import numpy as np
import time

#EXtract data from one line of RDF dataset
def makeNode():
    l1=line
    regex = re.compile(">")
    n1=regex.split(l1)[:3]
    #print n1
    #extracting resource
#    if len(n1)!=3:
#        ntoreturn=''
#        return ntoreturn
    r1=n1[0].split(':')
    lr1=len(r1)
    r1=r1[lr1-1]
#    if r1.find("200px")!=-1:
#        r1=r1.replace('200px-',"")
#    if r1.find(".svg")!=-1:
#        r1=r1.replace('.svg', "")
#    if r1.find(".png")!=-1:
#        r1=r1.replace('.png', "")
    #print 'resource',  r1
    ntoreturn=[r1]
    #extracting property
    pp1= n1[1].split('/')
    p1= pp1[len(pp1)-1]
    #print 'property' , p1
    ntoreturn.append(p1)
    #extracting subcat
    v1=n1[2].split(':')
    lv1=len(v1)
    v1=v1[lv1-1]
    v = v1.replace('>',"")
    #print 'value',  v1
    ntoreturn.append(v)
    return ntoreturn

# Refresh ilist , required to pick up the next image node data
def list_refresh(s):
    del s[:]

# The main function, that builds the nodes from the RDF. 
if __name__ == '__main__':
    #fread=open('dummyskos', 'r')                                                # <<<<<<<<< Test RDF 
    fread=open('./skos_categories_en.nt', 'r')                            # <<<<<<<<<  Original RDF
    #fwrite=open('/home/sdr/dbase/NMParserResults_preview_homepages.txt', 'w')
    #==== set up logistics ============
    starttime = time.clock()
    cur_line=0								 
    begin_line = 869374							# <<<<<<<<<<<<<<<< begin reading entries at this line
    end_line = 79033  + begin_line						# <<<<<<<<<<<<<<<< stop reading entries at this line
    lines_to_process = end_line - begin_line
    lastresource=""                                                   # this contains the last resource
    nnode=0                                                             # this will count the total nodes
    unode=-1 							 	# this is counter for main category
    u2node = 0                                                         # counter for subcategory
    # ======= intiatilize lists ==========
    #plist= {'shortab':[]}
    node_list =[]                                                      # this stores name of nodes, not their ids
    subcatlist = []                                                     # sub category for a category 
    nosubcatlist = []							# these have no sub cat
    sgraph=nx.DiGraph()							# directed graph
   
    print '====== Parsing RDF entries from ', begin_line, ' to ', end_line, '======'
    #====== Begin Parsing RDF ================
    for line in fread:
	#Making sure of RDF range
	cur_line +=1
	if cur_line < begin_line:
	    continue
	if cur_line > end_line:
	    break
        
        n=makeNode()     
        if lastresource != n[0]:
        #time to make the previous node, check first if a previous node needs to be made
            if lastresource!="":
                #have we met this category before ?
                match = np.intersect1d_nu([lastresource], node_list) 
                if len(match)<1:
                    # this is a new category, make primary node
                    unode+=1
		    temp1 = 'cat_'+ str(unode)
                    sgraph.add_node(lastresource,  nodeid=temp1, resource=lastresource,  category=lastresource)
                    node_list.append(lastresource)
                    # make secondary nodes
                    try:
			basic_wt = 1.0/len(subcatlist)
		    except ZeroDivisionError:
			#print 'trying to divide by zero at: ', lastresource, 'with subcatlist', subcatlist 
      			nosubcatlist.append(lastresource)              	
		    # Adding subcat nodes to main cat node (should make a function in the future) 
		    for subcat in subcatlist:
                        u2node+=1
                        temp2='subcat_' + str(u2node)                           #unique subcat (not dependent on cat)
                        sgraph.add_node(subcat,  nodeid=temp2, resource=subcat,  category = subcat)
                        node_list.append(subcat)
                        # add edge from cat to subcat
                        sgraph.add_edge(lastresource,  subcat,  weight=basic_wt, color='green')  #in 
                        sgraph[lastresource][subcat]['type'] = 'category'
                else:
                    # main category already exists, which means it is a subcategory to some previous category !
                    # two subcats will have same names ? 
                    # print 'checking same resource:', lastresource, 'has neighbors', sgraph.neighbors(lastresource)
                    #print 'connecting ', subcatlist, ' to previously found resource:' , lastresource 
		    #at this point we do not need to re-distribute weights, since this is a di-graph
                    for subcat in subcatlist:
                        u2node+=1
                        temp2='subcat_' + str(u2node)                           #unique subcat (not dependent on cat)
                        sgraph.add_node(subcat,  nodeid=temp2, resource=subcat,  category = subcat)
                        node_list.append(subcat)
                        # add edge from cat to subcat
                        sgraph.add_edge(lastresource,  subcat,  weight=basic_wt, color='blue')	#out
                        sgraph[lastresource][subcat]['type'] = 'category'

                if (unode % 1000 == 0):
                    print ' ', (1.0 * (cur_line - begin_line)/lines_to_process)*100 , '% Completed'  
                    #time.sleep(5)
                #refresh subcatlist
                del subcatlist[:]
                    #new entry has been added, do some testing here for query 
                    #query_inprocess()
            lastresource=n[0]

            #
            current_property=n[1]
            if current_property.find("broader")!=-1:
                subcatlist.append(n[2])
                
                #add edge ffrom lastresource to this subcat
             #This will store it in output file
#            for item in n:
#                fwrite.write("%s  " % item)
#                fwrite.write("\n")
            continue
        # This is run for the first node
        current_property=n[1]
        if current_property.find("broader")!=-1:
            subcatlist.append(n[2])
            nnode+=1
    
    
    # Now making the last group of nodes
    unode+=1
    match = np.intersect1d_nu([lastresource], node_list) 
    if len(match)<1:
        # this is a new category, make primary node
        temp1 = 'cat_'+ str(unode)
        sgraph.add_node(lastresource, nodeid=temp1, resource=lastresource,  category=lastresource)
        node_list.append(lastresource)
        # make secondary nodes
        try:
            basic_wt = 1.0/len(subcatlist)
        except ZeroDivisionError:
            #print 'trying to divide by zero at: ', lastresource, 'with subcatlist', subc$
            nosubcatlist.append(lastresource)

        for subcat in subcatlist:
            u2node+=1
            temp2='subcat_' + str(u2node)                           #unique subcat (not dependent on cat)
            sgraph.add_node(subcat,  nodeid=temp2, resource=subcat,  category = subcat)
            node_list.append(subcat)
            # add edge from cat to subcat
            sgraph.add_edge(lastresource,  subcat,  weight=basic_wt, color='green')   #in
            sgraph[lastresource][subcat]['type'] = 'category'
        else:
            # main category already exists 
            # two subcats will have same names 
            #print 'checking same resource:', lastresource, 'has neighbors', sgraph.neighbors(lastresource)
            #print 'connecting ', subcatlist, ' to previously found resource:' , lastresource
	    for subcat in subcatlist:
            	u2node+=1
                temp2='subcat_' + str(u2node)                           #unique subcat (not dependent on cat)
                sgraph.add_node(subcat,  nodeid=temp2, resource=subcat,  category = subcat)
                node_list.append(subcat)
                # add edge from cat to subca
                sgraph.add_edge(lastresource,  subcat,  weight=basic_wt, color = 'blue') #out
                sgraph[lastresource][subcat]['type'] = 'category'

    #refresh subcatlist
    del subcatlist[:]
    

    elapsed = (time.clock() - starttime)
    print '100 % Done'
    print 'Time Taken to Parse: ', elapsed
    print 'Nodes Created: ',  sgraph.number_of_nodes()
    print 'Edges Created: ', sgraph.number_of_edges()
    #print persongraph.nodes(data='True')
    #print nodes of the graph in a file. 
    #writeGraphNodes()      #if you uncomment this line, make sure line 59 is uncommented, which sets the file in write mode. 
    starttime2 = time.clock()
    # ======== store graph ===================
    nx.write_gpickle(sgraph,  "skosNodes.pick")
    sgraph.graph['Resource']='Categories' 						# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,
    sgraph.graph['listofnodes']= node_list
    #nx.write_pajek(persongraph, "personNodes.net")       #saves the person Node made by Node Maker 
    savetime = (time.clock() - starttime2)
    print 'Time taken to save graph: ', savetime

    print 'Done.. ! '
    
    edge_list = list(sgraph.edges_iter(data="True"))
    edge_color_map = []
    for e in edge_list:
    	edge_color_map.append(e[2]['color'])

    #ndummy = nx.draw_networkx_edges(sgraph, pos = nx.random_layout(sgraph), font_size=8)
    #ndummy=nx.draw_networkx_labels(sgraph,  pos=nx.random_layout(sgraph),  font_size=8)
    #ndummy=nx.draw_networkx_nodes(Gperson,  pos=nx.circular_layout(Gperson),  node_size=50,  node_color='b', vmax=50,  with_labels=True)
    #ndummy=nx.draw_networkx(sgraph,  pos=nx.circular_layout(sgraph),  with_labels=True, font_size=10, node_size=30, edge_color = edge_color_map)
    #colors = "bgrcymk"
    #colormap = [colors[i] for i in range(n/2)]
    #pos = nx.spring_layout(sgraph)
    #ndummy = nx.spectral_layout(sgraph, weighted=True, scale=1)
	
    #plt.show()
