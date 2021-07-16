# https://math.stackexchange.com/questions/2087801/how-to-measure-the-similarity-between-two-graph-networks
# https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py

import networkx as nx
from graph_of_words import GraphOfWords, getMCS_directed
from document import get_webpage_content
import preprocess
import numpy as np
import getSimilarity
from graph_kernel import main as graph_kernel_main

from selenium import webdriver


#########################################################################

# def laplacian(g1, g2):
#     # Idea from: https://math.stackexchange.com/ question answer
#     # Note: graphs must have the same number of vertices , to be able to subtract matrices

#     # The idea is that the graph Laplacian is related to the diffusion in the graph
#     laplacian1 = nx.linalg.laplacianmatrix.directed_laplacian_matrix(g1, None, 'weight')
#     laplacian2 = nx.linalg.laplacianmatrix.directed_laplacian_matrix(g2, None, 'weight')
#     inv1 = np.linalg.pinv(laplacian1)
#     inv2 = np.linalg.pinv(laplacian2)

#     """The i'th column of the inverse matrix is the steady-state-result of putting a constant source of particles
#     at node i and letting them diffuse randomly through the graph, with the probability of transmission
#     between two nodes related to the edge weight between those nodes"""
 
#     # ||inv1-inv2||: measures the difference in the graphs in terms of 
#     # how they physically differ in a diffusion process
#     numerator = pow(np.linalg.norm(inv1-inv2),2)

#     # Dividing by ||inv1||*||inv2|| is done to make the similarity measure scale-invariant,
#     denominator = np.linalg.norm(inv1) * np.linalg.norm(inv2)

#     # The exponential exp(−X) is taken to map the values between 0 and 1
#     laplacian_sim = math.exp(-numerator/denominator)

#     return laplacian_sim

#########################################################################

# def edit_distance(g1, g2):
#     # Code from: https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py
#     """
#     The edit distance between graphs, defined as the number of changes one
#     needs to make to put the edge lists in correspondence.
#     """
#     # Note: graphs must have the same number of vertices , to be able to subtract matrices

#     # Adjacency matrices of graphs to be compared: For directed graphs, entry i,j corresponds to an edge from i to j
#     adj1 = nx.linalg.graphmatrix.adjacency_matrix(g1)
#     adj2 = nx.linalg.graphmatrix.adjacency_matrix(g2)

#     diff = np.abs((adj1-adj2)).sum()
#     edit_dst =  diff / 2

#     if edit_dst == 0:
#         return 0, 1

#     # Getting a similarity value from edit distance value
#     denominator = np.abs((adj1 + adj2)).sum() / 2

#     # Difference score = difference of matrices / average sum of matrices
#     diff_score = diff / denominator

#     # Similarity Value
#     sim_from_edit_dst = np.abs(1 - diff_score) / diff_score
#     if sim_from_edit_dst > 1:
#         sim_from_edit_dst = 1 / sim_from_edit_dst

#     return edit_dst, sim_from_edit_dst

#########################################################################

def graphs_jaccard_similarity(g1, g2):
    # graphs not necessary same number of vertices !!

    # Getting sets of vertices & edges
    V1,V2 = [set(G.nodes()) for G in [g1,g2]]
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    len_nodes_union = len(V1|V2)
    len_edges_union = len(E1|E2)
    len_edges_intersection = len(E1&E2)
    len_nodes_intersection = len(V1&V2)

    # Jaccard Similarity = (sum of intersections) / (sum of unions)
    jaccard_similarity = (len_edges_intersection + len_nodes_intersection) / (len_nodes_union + len_edges_union)
    return jaccard_similarity

#########################################################################

def vertex_edge_overlap(g1,g2):
    # Code from: https://github.com/peterewills/NetComp/blob/master/netcomp/distance/exact.py
    # graphs not necessary same number of vertices !!
    
    # Getting sets of vertices & edges
    V1,V2 = [set(G.nodes()) for G in [g1,g2]]
    E1,E2 = [set(G.edges()) for G in [g1,g2]]

    V_overlap = len(V1|V2)
    E_overlap = len(E1|E2)
    vertex_edge_overlap_value = (V_overlap + E_overlap) / (len(V1)+len(V2)+len(E1)+len(E2))

    # Similarity Value from Vertex_Edge Overlap Value
    vertex_edge_sim = np.abs(1-vertex_edge_overlap_value)/vertex_edge_overlap_value
    if vertex_edge_sim > 1:
        vertex_edge_sim = 1 / vertex_edge_sim

    return vertex_edge_overlap_value, vertex_edge_sim

#########################################################################

# def get_len_edges_intersection(g1, g2):
#     intersection_len = 0
#     if g1.number_of_nodes() > g2.number_of_nodes():
#         for n1,n2 in g1.edges():
#             if g2.has_edge(n1, n2):
#                 intersection_len += 1
#     else:
#         for n1,n2 in g2.edges():
#             if g1.has_edge(n1, n2):
#                 intersection_len += 1

#     return intersection_len

# def edge_overlap(g1,g2):
#     # graphs not necessary same number of vertices !! 
#     E1 = len(g1.edges())
#     E2 = len(g2.edges())

#     E_intersection_len = get_len_edges_intersection(g1, g2)

#     edge_overlap_value = E_intersection_len / (E1+E2)
#     if edge_overlap_value == 0:
#         edge_overlap_sim = 0
#     else:
#         edge_overlap_sim = np.abs(1-edge_overlap_value)/edge_overlap_value
#         if edge_overlap_sim > 1:
#             edge_overlap_sim = 1 / edge_overlap_sim

#     return edge_overlap_value, edge_overlap_sim

#########################################################################
### FALSEEEE FUNCTION
# def MCS_based_similarity(graph1, graph2):
#     # Note: graphs must have the same number of vertices , to be able to subtract matrices
#     # graph1 & graph2 :  GraphOfWords
#     mcs = getMCS_directed(graph1, graph2)
#     mcs1 = nx.DiGraph(mcs)
#     mcs2 = nx.DiGraph(mcs)

#     g1 = graph1.graph
#     g2 = graph2.graph

#     # 1) Compare the maximum common subgraph to both graph1 & graph2 in terms of number of vertices & edges
#     g1_nodes = g1.number_of_nodes()
#     g1_edges = g1.number_of_edges()
#     g2_nodes = g2.number_of_nodes()
#     g2_edges = g2.number_of_edges()
#     mcs_nodes = mcs.number_of_nodes()
#     mcs_edges = mcs.number_of_edges()
    
#     mcs_g1_common_nodes_rate = mcs_nodes / g1_nodes
#     mcs_g1_common_edges_rate = mcs_edges / g1_edges
#     mcs_g1_sim = (mcs_g1_common_nodes_rate + mcs_g1_common_edges_rate) / 2

#     mcs_g2_common_nodes_rate = mcs_nodes / g2_nodes
#     mcs_g2_common_edges_rate = mcs_edges / g2_edges
#     mcs_g2_sim = (mcs_g2_common_nodes_rate + mcs_g2_common_edges_rate) / 2
    
#     g1_g2_sim_rate = mcs_g1_sim if mcs_g1_sim > mcs_g2_sim else mcs_g2_sim

#     # 2) Compare the maximum common subgraph to both graph1 & graph2 in terms of laplacian similarities
#     # 2.1) Make the graphs have the same set of vertices
#     # for node in g1.nodes():
#     #     if not node in mcs1.nodes():
#     #         mcs1.add_node(node)
#     # for node in g2.nodes():
#     #     if not node in mcs2.nodes():
#     #         mcs2.add_node(node)

#     # # 2.2) Compute laplacian similarities
#     # lap_sim_g1_mcs = laplacian(mcs1, g1)
#     # lap_sim_g2_mcs = laplacian(mcs2, g2)
#     # # Average Laplacian Similarity
#     # avg_lap_sim = (lap_sim_g1_mcs + lap_sim_g2_mcs)/2

#     #return avg_lap_sim, g1_g2_sim_rate
#     return g1_g2_sim_rate

 

#########################################################################

def get_similarities(driver, url1, url2):

    # results to return in dictionary
    results = {}

    results['url1'] = url1
    results['url2'] = url2

    # get websites content
    website_title1, page_title1, list_of_subtitles1, list_of_urls1, body_text1 = get_webpage_content(driver, url1)
    website_title2, page_title2, list_of_subtitles2, list_of_urls2, body_text2 = get_webpage_content(driver, url2) 

    #get website titles, page titles, subtitles, and URLs similarity
    website_titles_sim = getSimilarity.get_cosine_of_2_sentences(website_title1, website_title2)
    page_titles_sim = getSimilarity.get_cosine_of_2_sentences(page_title1, page_title2)
    subtitles_sim = getSimilarity.get_jaccard_of_two_lists_of_sentences(list_of_subtitles1, list_of_subtitles2)
    urls_sim = getSimilarity.get_jaccard_of_two_lists_of_sentences(list_of_urls1, list_of_urls2)

    results['website_titles_sim'] = website_titles_sim
    results['page_titles_sim'] = page_titles_sim
    results['subtitles_sim'] = subtitles_sim
    results['urls_sim'] = urls_sim

    # Syntactic & Semantic Preprocessing
    syntactically_preprocessed_body_text1 = preprocess.get_syntactically_preprocessed_paragraph(body_text1)
    syntactically_preprocessed_body_text2 = preprocess.get_syntactically_preprocessed_paragraph(body_text2)

    semantically_preprocessed_paragraph1, semantically_preprocessed_paragraph_as_list_of_sentences1 = preprocess.get_semantically_preprocessed_paragraph(body_text1)
    semantically_preprocessed_paragraph2, semantically_preprocessed_paragraph_as_list_of_sentences2 = preprocess.get_semantically_preprocessed_paragraph(body_text2)

    # Get Cosine similarities for both: Syntactic & Semantic Preprocessing
    cosine_similarity_syntactic_preprocessing = getSimilarity.get_cosine_of_2_sentences(syntactically_preprocessed_body_text1, syntactically_preprocessed_body_text2)
    cosine_similarity_semantic_preprocessing  = getSimilarity.get_cosine_of_2_sentences(semantically_preprocessed_paragraph1, semantically_preprocessed_paragraph2)

    results['cosine_similarity_syntactic_preprocessing'] = cosine_similarity_syntactic_preprocessing
    results['cosine_similarity_semantic_preprocessing'] = cosine_similarity_semantic_preprocessing

    # Graph Representation
    graph1 = GraphOfWords(window_size=4)
    graph1.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences1, workers=4)
    g1 = graph1.graph

    graph2 = GraphOfWords(window_size=4)
    graph2.build_graph(semantically_preprocessed_paragraph_as_list_of_sentences2, workers=4)
    g2 = graph2.graph  

    # Graph Kernels for similarity
    sp_sim = graph_kernel_main(g1, g2) # Shortest Path Kernel
    results['sp_sim'] = sp_sim

    # Other Graph Similarity Metrics
    graphs_jaccard_sim = graphs_jaccard_similarity(g1, g2)
    results['graphs_jaccard_sim']=graphs_jaccard_sim

    veo_val, veo_sim = vertex_edge_overlap(g1, g2)
    results['veo_val']=veo_val
    results['veo_sim']=veo_sim

    # eo_val, eo_sim = edge_overlap(g1, g2)
    # results['eo_val']=eo_val
    # results['eo_sim']=eo_sim

    # graphs_edges_value_based_similarity = graphs_similarity_value_based_on_edges_values(edges1, edges2)
    # results['graphs_edges_value_based_similarity']=graphs_edges_value_based_similarity

    # similarties that do not require graphs with same set of vertices
    # first, make 2 graphs same vertices:
    # all_nodes = nx.compose(g1, g2).nodes()
    # for node in all_nodes:
    #     if not node in g1.nodes():
    #         g1.add_node(node)
    #     if not node in g2.nodes():
    #         g2.add_node(node)

    # laplacian_sim = laplacian(g1, g2)
    # results['laplacian_sim']=laplacian_sim

    # edit_dst_val, edit_dst_sim = edit_distance(g1, g2)
    # results['edit_dst_val']=edit_dst_val
    # results['edit_dst_sim']=edit_dst_sim

    ## False Function
    #mcs_based_avg_lap_sim, mcs_based_g1_g2_sim_rate = MCS_based_similarity(graph1, graph2)
    #mcs_based_g1_g2_sim_rate = MCS_based_similarity(graph1, graph2)
    # False
    #results['mcs_based_avg_lap_sim']=mcs_based_avg_lap_sim
    #results['mcs_based_g1_g2_sim_rate']=mcs_based_g1_g2_sim_rate

    return results

def main():

    urls = (["https://www.webmd.com/drugs/2/index","https://www.webmd.com/drugs/2/alpha/a/"],
            ["https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters#:~:text=Most%20people%20who%20get%20COVID,facility%20by%20telephone%20first.","https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters#:~:text=The%20coronavirus%20disease%20(COVID,19%20hotline%20for%20assistance."],
            ["https://www.bbc.co.uk/news/health-51665497","https://www.bbc.com/news/health-51665497"],
            ["http://teacher.scholastic.com/paperairplane/airplane.htm","https://www.scholastic.com/teachers/articles/teaching-content/what-makes-paper-airplanes-fly/"],
            ["https://www.emedicinehealth.com/anise/vitamins-supplements.htm","https://www.rxlist.com/anise/supplements.htm"],
            ["https://medium.com/@ashukumar27/similarity-functions-in-python-aa6dfe721035","https://dataaspirant.com/five-most-popular-similarity-measures-implementation-in-python/"],
            ["https://www.geeksforgeeks.org/python-word-embedding-using-word2vec/","https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72"],
            ["https://www.newadvent.org/cathen/03096a.htm", "https://www.livius.org/articles/misc/byzantine-empire/"],
            ["https://www.encyclopedia.com/history/modern-europe/turkish-and-ottoman-history/ottoman-empire", "https://www.jstor.org/stable/j.ctt1b67wfz"],
            ["https://www.amacad.org/publication/ottoman-experience", "https://www.encyclopedia.com/history/modern-europe/turkish-and-ottoman-history/ottoman-empire"],
            ["https://www.socialwatch.org/node/18372", "https://blogs.lse.ac.uk/mec/2019/10/24/lebanons-revolution-makes-its-own-rules/"],
            ["https://www.ancient.eu/Byzantine_Empire/", "https://www.thebritishacademy.ac.uk/blog/what-is-byzantine-studies/"],
            ["https://www.ushistory.org/civ/3e.asp", "https://www.goaheadtours.com/travel-blog/articles/pyramids-of-giza-facts"], 
            ["https://www.cairn.info/revue-napoleonica-la-revue-2013-1-page-88.htm", "https://www.euronews.com/2021/02/13/french-and-russian-soldiers-who-fought-in-napoleon-s-18-12-campaign-are-finally-buried"],
            ["https://www.thebalancesmb.com/simple-ways-make-money-online-2531879", "https://www.lifehack.org/articles/money/5-real-ways-actually-make-money-online.html"],
            ["https://opensource.com/resources/python", "https://www.infoworld.com/article/3204016/what-is-python-powerful-intuitive-programming.html"],
            ["https://www.metmuseum.org/toah/hd/grot/hd_grot.htm", "https://www.amacad.org/publication/ottoman-experience"],
            ["https://courses.lumenlearning.com/waymaker-psychology/chapter/reading-parts-of-the-brain/", "https://www.news-medical.net/health/The-Anatomy-of-the-Human-Brain.aspx"],
            ["https://www.oracle.com/internet-of-things/what-is-iot/","https://www.oracle.com/in/internet-of-things/what-is-iot/"],
            ["https://www.thoughtco.com/anatomy-of-the-stomach-373482", "https://www.nursingtimes.net/clinical-archive/gastroenterology/gastrointestinal-tract-2-the-structure-and-function-of-the-stomach-24-06-2019/"],
            ["https://courses.lumenlearning.com/boundless-worldhistory/chapter/the-ottoman-empire/", "https://www.laits.utexas.edu/cairo/history/ottoman/ottoman.html"],
            ["https://en.wikivoyage.org/wiki/Istanbul","https://wikitravel.org/en/Istanbul"],
            ["https://en.wikivoyage.org/wiki/Turkey","https://wikitravel.org/en/Turkey"],
            ["https://courses.lumenlearning.com/atd-tcc-worldciv2/chapter/ottoman-empire/","https://en.wikipedia.org/wiki/History_of_the_Ottoman_Empire"],
            ["https://en.citizendium.org/wiki/Crusades","https://en.wikipedia.org/wiki/Crusades"],
            ["https://en.wikipedia.org/wiki/Crusades","https://chem.libretexts.org/Courses/Lumen_Learning/Book%3A_Western_Civilization_I_(Lumen)/15%3A_Week_13%3A_The_Crusades_and_The_Late_Middle_Ages/15.2%3A_Reading%3A_The_Crusades"],
            ["https://en.wikipedia.org/wiki/Decline_of_Buddhism_in_the_Indian_subcontinent","https://en.wikipedia.org/wiki/History_of_Buddhism_in_India"],
            ["https://en.wikipedia.org/wiki/Galata","https://www.wikiwand.com/en/Galata"],
            ["https://en.wikipedia.org/wiki/Ottoman_Empire","https://en.wikipedia.org/wiki/History_of_the_Ottoman_Empire"]
        )

    driver = webdriver.Chrome('chromedriver')

    i = 1
    for urls_pair in urls:
        results_file = open("graph_similarity_results.txt", "a")
        print("Pair number", i)

        url1 = urls_pair[0]
        url2 = urls_pair[1]
        results = get_similarities(driver, url1, url2)

        results_file.write("url1: "+ results['url1'] + "\n")
        results_file.write("url2: "+ results['url2'] + "\n")

        results_file.write("website_titles_sim: "+ str(results['website_titles_sim']) + "\n")
        results_file.write("page_titles_sim: "+ str(results['page_titles_sim']) + "\n")
        results_file.write("subtitles_sim: "+ str(results['subtitles_sim']) + "\n")
        results_file.write("urls_sim: "+ str(results['urls_sim']) + "\n")

        results_file.write("cosine_similarity_syntactic_preprocessing: " + str(results['cosine_similarity_syntactic_preprocessing']) + "\n")
        results_file.write("cosine_similarity_semantic_preprocessing: "+ str(results['cosine_similarity_semantic_preprocessing']) + "\n")
        
        results_file.write("shortest_path_kernel_sim: "+ str(results['sp_sim']) + "\n")
        results_file.write("graphs_jaccard_sim: "+ str(results['graphs_jaccard_sim']) + "\n")
        results_file.write("veo_sim: "+ str(results['veo_sim']) + "\n")
        
        results_file.write("\n######################################################################\n\n")

        print("Pair number", i, "done")
        print("######################################################################")
        i += 1
        results_file.close()
    
    driver.close()

if __name__ ==  '__main__':
    main()