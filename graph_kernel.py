import grakel
from represent_document import get_webpage_content
import preprocess
from graph_of_words import GraphOfWords
import graph_of_words as gow
from grakel import Graph
from grakel.kernels import WeisfeilerLehman, VertexHistogram, WeisfeilerLehmanOptimalAssignment
from grakel.kernels import ShortestPath, RandomWalkLabeled, RandomWalk, SubgraphMatching
import networkx as nx
from getSimilarity import get_cosine_of_2_sentences

sp_kernel = ShortestPath(normalize=True)
# wl_kernel = WeisfeilerLehman(base_graph_kernel=VertexHistogram, normalize=True)
# wloa_kernel = WeisfeilerLehmanOptimalAssignment(normalize=True)
# rwl_kernel = RandomWalkLabeled(normalize=True, method_type='fast')
# rw_kernel = RandomWalk(normalize=True, method_type='fast')
# sm_kernel = SubgraphMatching(normalize=True)


def main(g1, g2):

    # list_of_text_paragraphs1 = get_webpage_content(url1)
    # list_of_text_paragraphs2 = get_webpage_content(url2)

    # list_of_text_paragraphs1 = ["Turkey (Turkish: Türkiye) is a bi-continental country: while geographically most of the country is situated in Asia, Eastern Thrace is part of Europe and many Turks have a sense of European identity. Turkey offers a wealth of destination varieties to travellers: from dome-and-minaret filled skyline of Istanbul to Roman ruins along the western and southern coasts, from heavily indented coastline against a mountainous backdrop of Lycia and wide and sunny beaches of Pamphylia to cold and snowy mountains of the East, from crazy foam parties of Bodrum to Middle Eastern-flavoured cities of Southeastern Anatolia, from verdant misty mountains of Eastern Black Sea to wide steppe landscapes of Central Anatolia, there is something for everyone's taste—whether they be travelling on an extreme budget by hitchhiking or by a multi-million yacht.",
    # "There is evidence that the bed of the Black Sea was once an inhabited plain, before it was flooded in prehistoric times by rising sea levels. Mount Ararat (Ağrı Dağı), at 5,165 m, is Turkey's highest point and the legendary landing place of Noah's Ark on the far eastern edge of the country. The area that is now Turkey has been part of many of the world's greatest empires throughout history. The city of Troy, famously destroyed by the Greeks in Homer's Illiad, has always been associated to the entrance to the Dardanelles strait in northwestern Anatolia. Subsequently, the area was to become part of the Roman Empire, and subsequently the Eastern Roman (Byzantine) Empire after the Roman empire spit into two, with the city of Constantinople (now Istanbul) as the regional capital, as well as the Eastern Roman capital after the split. The Ottoman Empire subsequently defeated the Eastern Roman Empire, and dominated the eastern Mediterranean, until its defeat by the Allies in World War I.",
    # "The Turkish Republic (Türkiye Cumhuriyeti) was founded in 1923 from the remnants of the Ottoman Empire. Soon thereafter the country instituted secular laws to replace traditional religious fiats, and instigated many other radical reforms to rapidly modernise the state. Changing from Arabic script to the 29-letter Turkish alphabet, based on the Roman alphabet, was one of many personal initiatives of the founder of the Turkish Republic, Mustafa Kemal Atatürk. Atatürk continues to be revered and you can see his face gazing down on or up into the distance fatherly, visionarily or determinedly in many, many places around Turkey. Atatürk died in 1938 and was succeeded by his right hand İsmet İnönü who had been the first prime minister of the new Republic. It was Inönü that majorly boosted the cult of personality around Atatürk and who led Turkey for a longer time than his larger-than-life predecessor. In 1945 Turkey joined the UN, and in 1952 became a member of NATO.",
    # "Turkey occupies a landmass slightly larger than Texas, at just over 750,000 km², and is more than three times the size of the United Kingdom. In terms of the variety of terrain and particularly the diversity of its plant life, however, Turkey exhibits the characteristics of a small continent. There are, for example, some 10,000 plant species in the country (compared with some 13,000 in all of Europe) — one in three of which is endemic to Turkey. Indeed, there are more native plant species within Istanbul city limits (2,000) than in the whole of the United Kingdom. While many people know of Turkey's rich archaeological heritage, it possesses an equally valuable array of ecosystems — peat bogs, heath lands, steppes, and coastal plains. Turkey possesses much forest (about a quarter of the land) but, as importantly, some half of the country is semi-natural landscape that has not been entirely remodelled by man.",
    # "While it may sound like a tourism brochure cliché, Turkey really is a curious mix of the west and the east—you may swear you were in a Balkan country or in Greece when in northwestern and western parts of the country (except that Byzantine-influenced churches are substituted with Byzantine-influenced mosques), which are indeed partly inhabited by people from Balkan countries, who immigrated during the turmoil before, during, and after World War I, while southeastern reaches of the country exhibit little if any cultural differences from Turkey's southern and eastern neighbours. Influences from the Caucasus add to the mix in the northeast part of the country. It can be simply put that Turkey is the most oriental of western nations, or, depending on the point of view, the most occidental of eastern nations. Perhaps one thing common to all of the country is Islam, the faith of the bulk of the population. However, interpretation of it varies vastly across the country: many people in northwestern and western coasts are fairly liberal about the religion (being nominal Muslims sometimes to the point of being irreligious), while folk of the central steppes are far more conservative (don't expect to find a Saudi Arabia or an Afghanistan even there, though). The rest of the country falls somewhere in between, with the coastal regions being relatively liberal while inland regions are relatively conservative as a general rule. The largest religious minority in the country are the Alevites, who constitute up to 20% of the population and who subscribe to a form of Islam closer to that of the Shiite version of Islam and whose rituals draw heavily from the shamanistic ceremonies of ancient Turks. Other religious minorities—the Greek Orthodox, Armenian Apostolic, Jews, Syriac Oriental Orthodox, and Roman Catholics, the latter of whom mainly settled in Turkey within the last 500 years from Western European countries—once numerous across the country, are now mostly confined to the large cities of Istanbul and Izmir, or parts of Southeastern Anatolia in the case of the Syriac Oriental Orthodox. Despite its large Muslim majority population, Turkey officially remains a secular country, with no declared state religion.",
    # "There are several holidays that can cause delays in travel, traffic congestion, booked up accommodations and crowded venues. Banks, offices and businesses are closed during official holidays and traffic intensifies during all of the following holidays so do your research before you visit. Do not be put off by these holidays, it is not that difficult and often quite interesting to travel during Turkish holidays; plan ahead as much as possible."]
    # list_of_text_paragraphs2 = ["There are several holidays that can cause delays in travel, traffic congestion, booked up accommodations and crowded venues. Banks, offices and businesses are closed during official holidays and traffic intensifies during all of the following holidays so do your research before you visit. Do not be put off by these holidays, it is not that difficult and often quite interesting to travel during Turkish holidays; plan ahead as much as possible.",
    # "There is evidence that the bed of the Black Sea was once an inhabited plain, before it was flooded in prehistoric times by rising sea levels. Mount Ararat (Ağrı Dağı), at 5,165 m is the country's highest point and legendary landing place of Noah's Ark, lies in the mountains on the far eastern edge of the country.",
    # "Turkey was founded in 1923 from the remnants of the Ottoman Empire. Soon thereafter the country instituted secular laws to replace traditional religious fiats. In 1945 Turkey joined the UN, and in 1952 it became a member of NATO.",
    # "Turkey offers a wealth of destination varieties to travellers: from dome-and-minaret filled skyline of Istanbul to Roman ruins along the western and southern coasts, from heavily indendated coastline against a mountainous backdrop of Lycia and wide and sunny beaches of Pamphylia to cold and snowy mountains of the East, from crazy foam parties of Bodrum to Middle Eastern-flavoured cities of Southeastern Anatolia, from verdant misty mountains of Eastern Black Sea to wide steppe landscapes of Central Anatolia, there is something for everyone's taste—whether they be travelling on an extreme budget by hitchhiking or by a multi-million yacht.",
    # "Turkey is the 37th largest country out of a list of 195. At just over 750,000 square kilometers, Turkey is larger than some European countries such as Italy, France, and Germany and more than three times the size of the United Kingdom. Regarding U.S. comparisons, it is slightly larger than Texas, and twice the size of California. However, in terms of the variety of terrain and diversity of plant life, Turkey exhibits the characteristics of a small continent. There are, for example, some 10,000 plant species in the country (compared with some 13,000 in all of Europe) — one in three of which is endemic to Turkey. Indeed, there are more species in Istanbul Province (2,000) than in the whole of the United Kingdom. While many people know of Turkey's rich archaeological heritage, it possesses an equally valuable array of ecosystems — peat bogs, heathlands, steppes, and coastal plains. Turkey possesses much forest (about a quarter of the land), but just as importantly, some half of the country is a semi-natural landscape that has not been entirely remodeled by man.",
    # "Turkey is a curious mix of west and east—you may swear you were in a Balkan country or in Greece when in northwestern and western parts of the country (except that Byzantine-influenced churches are substituted with Byzantine-influenced mosques), which are indeed partly inhabited by people from Balkan countries, who immigrated during the turmoil before, during, and after WWI, while southeastern reaches of the country exhibit little if any cultural differences from Turkey's southern and eastern neighbors. Influences from the Caucasus add to the mix in the northeast part of the country. It can be simply put that Turkey is the most oriental of western nations, or, depending on the point of view, the most occidental of eastern nations.",
    # "Perhaps one thing common to all of the country is Islam, the faith of the bulk of the population. However, interpretation of it varies vastly across the country: many people in northwestern and western coasts are fairly liberal about the religion (being nominal Muslims sometimes to the point of being irreligious), while folk of the central steppes are far more conservative (don't expect to find a Saudi Arabia or an Afghanistan even there, though). The rest of the country falls somewhere in between, with the coastal regions being relatively liberal while inland regions are relatively conservative as a general rule. The largest religious minority in the country are the Alevites, who constitute up to 20% of the population and who subscribe to a form of Islam closer to that of the Shiite version of Islam and practice Shamanistic rituals of ancient Turks. Other religious minorities—the Greek Orthodox, Armenian Apostolic, Jews, Syriac Oriental Orthodox, and Roman Catholics, the latter of whom mainly settled in Turkey within the last 500 years from Western European countries—once numerous across the country, are now mostly confined to the large cities of Istanbul and Izmir, or parts of Southeastern Anatolia in the case of the Syriac Oriental Orthodox. Despite its large Muslim majority population, Turkey officially remains a secular country, with no declared state religion.",
    # "The savvy traveller should remember that when travelling into, in or around Turkey there are several holidays to keep in mind as they can cause delays in travel, traffic congestion, booked up accommodation and crowded venues. Banks, offices and businesses are closed during official holidays and traffic intensifies during all of the following holidays so do your research before you visit. Do not be put off by these holidays, it is not that difficult and often quite interesting to travel during Turkish holidays, simply plan ahead as much as possible."]

    # # Preprocessing for graph representation (semantic similarity): list of sentences
    # print("Preprocess:")
    # list_of_semantically_preprocessed_sentences_from_list_of_text_paragraphs1 = preprocess.get_semantically_preprocessed_list_of_strings(list_of_text_paragraphs1)
    # list_of_semantically_preprocessed_sentences_from_list_of_text_paragraphs2 = preprocess.get_semantically_preprocessed_list_of_strings(list_of_text_paragraphs2)

    # s1 = " ".join(list_of_semantically_preprocessed_sentences_from_list_of_text_paragraphs1)
    # s2 = " ".join(list_of_semantically_preprocessed_sentences_from_list_of_text_paragraphs2)

    # cosine = get_cosine_of_2_sentences(s1, s2)
    #print("Cosine=", cosine)

    # Graph Representation
    #print("Representation:")
    # graph1 = GraphOfWords(window_size=4)
    # graph1.build_graph(list_of_semantically_preprocessed_sentences_from_list_of_text_paragraphs1, workers=4)
    # g1 = graph1.graph

    # graph2 = GraphOfWords(window_size=4)
    # graph2.build_graph(list_of_semantically_preprocessed_sentences_from_list_of_text_paragraphs2, workers=4)
    # g2 = graph2.graph

    #print("graph Kernel graph_from_networkx:")
    gks1 = grakel.graph_from_networkx([g1, g2], node_labels_tag='node_labels')
    #gks2 = grakel.graph_from_networkx([g1, g2], node_labels_tag='node_labels', edge_labels_tag='edge_labels')
    # gks3 = grakel.graph_from_networkx([g1, g2], node_labels_tag='node_labels')
    # gks4 = grakel.graph_from_networkx([g1, g2], node_labels_tag='node_labels')
    # gks5 = grakel.graph_from_networkx([g1, g2], node_labels_tag='node_labels')
    # gks6 = grakel.graph_from_networkx([g1, g2], node_labels_tag='node_labels')

    ############ Shortest Path Kernel ############
    try:
        sp_array = sp_kernel.fit_transform(gks1)
        sp_sim = sp_array[0][1]
        #print("Shortest Path Kernel:",sp_sim)
    except Exception as e:
        print('Shortest Path Kernel Exception: '+ str(e))

    ############ Subgraph Matching Kernel ############
    # try:
    #     sm_array = sm_kernel.fit_transform(gks2)
    #     sm_sim = sm_array[0][1]
    #     #print("Subgraph Matching Kernel:",sm_sim)
    # except Exception as e:
    #     print('Subgraph Matching Kernel Exception: '+ str(e))

    ############ Random Walk Kernel ############
    # try:
    #     rw_array = rw_kernel.fit_transform(gks3)
    #     rw_sim = rw_array[0][1]
    #     print("Random Walk Kernel:",rw_sim)
    # except Exception as e:
    #     print('Random Walk Kernel Exception: '+ str(e))

    ############ Random Walk Labeled Kernel ############
    # try:
    #     rwl_array = rwl_kernel.fit_transform(gks4)
    #     rwl_sim = rwl_array[0][1]
    #     print("Random Walk Labeled Kernel:",rwl_sim)
    # except Exception as e:
    #     print('Random Walk Labeled Kernel Exception: '+ str(e))

    ############ Weisfeiler Lehman Kernel ############
    # try:
    #     wl_array = wl_kernel.fit_transform(gks5)
    #     wl_sim = wl_array[0][1]
    #     print("Weisfeiler Lehman Kernel:",wl_sim)
    # except Exception as e:
    #     print('Weisfeiler Lehman Kernel Exception: '+ str(e))

    ############ Weisfeiler Lehman Optimal Assignment Kernel ############
    # try:
    #     wloa_array = wloa_kernel.fit_transform(gks6)
    #     wloa_sim = wloa_array[0][1]
    #     print("Weisfeiler Lehman Optimal Assignment Kernel:",wloa_sim)
    # except Exception as e:
    #     print('Weisfeiler Lehman Optimal Assignment Kernel Exception: '+ str(e))
    
    #return sp_sim, sm_sim
    return sp_sim

# if __name__ ==  '__main__':

#     url1 = "https://www.emedicinehealth.com/anise/vitamins-supplements.htm"
#     url2 = "https://www.rxlist.com/anise/supplements.htm"

#     cosine, sp_sim, sm_sim = main(url1, url2)
#     print(url1)
#     print(url2)
#     print("Cosine:",cosine, "Shortest Path Kernel:", str(sp_sim), "subgraph Matching Kernel:", str(sm_sim))
#     print("###############################################")

#     #########################################################################################

#     url1 = "https://en.wikipedia.org/wiki/Galata"
#     url2 = "https://www.wikiwand.com/en/Galata"

#     cosine, sp_sim, sm_sim = main(url1, url2)
#     print(url1)
#     print(url2)
#     print("Cosine:",cosine, "Shortest Path Kernel:", str(sp_sim), "subgraph Matching Kernel:", str(sm_sim))
#     print("###############################################")

#     #########################################################################################

#     url1 = "https://en.wikivoyage.org/wiki/Turkey"
#     url2 = "https://wikitravel.org/en/Turkey"

#     cosine, sp_sim, sm_sim = main(url1, url2)
#     print(url1)
#     print(url2)
#     print("Cosine:",cosine, "Shortest Path Kernel:", str(sp_sim), "subgraph Matching Kernel:", str(sm_sim))
#     print("###############################################")

