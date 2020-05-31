from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import wordcloud
import matplotlib.pyplot as plt
import codecs

def readTXT(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return f.read()

def tokenize(corpus):
    tokens = RegexpTokenizer(r'\w+').tokenize(corpus)
    return tokens

def reduceAndClean(tokens, sw=None):
    sw_list = stopwords.words('portuguese')
    if(sw):
        sw_list = list(set(sw_list).union(set(sw)))
    tokens = [token.lower() for token in tokens]
    return [x for x in tokens if x not in sw_list]

def groupBySection(tokens):
    tokens = tokens[tokens.index("Súmula"):]
    idx = 0

    summary, idx = groupBySummary(tokens)
    summary = reduceAndClean(summary)
    tokens = tokens[idx:]

    objectives, idx = groupByObjectives(tokens)
    objectives = reduceAndClean(objectives)
    tokens = tokens[idx:]

    programContent, idx = groupByProgramContent(tokens)
    programContent = reduceAndClean(programContent, ["conteúdo", "semana", "título"])
    tokens = tokens[idx:]

    methodology, idx = groupByMethodolody(tokens)
    methodology = reduceAndClean(methodology)
    tokens = tokens[idx:]
 
    learningExperience = reduceAndClean(groupByLearningExperience(tokens))
    return [summary, objectives, programContent, methodology, learningExperience]


# Clustering baseado nas informações contidas na seção "Objetivos"
def groupByObjectives(tokens):
    strt_idx = tokens.index("Objetivos")
    end_idx0 = tokens.index("Conteúdo")
    end_idx1 = tokens.index("Programático")
    end_idx = end_idx0 if end_idx0 + 1 == end_idx1 else end_idx1 - 1
    return tokens[strt_idx + 1: end_idx], end_idx

# Clustering baseado nas informações contidas na seção "Súmula"
def groupBySummary(tokens):
    strt_idx = tokens.index("Súmula")
    end_idx = tokens.index("Currículos")
    return tokens[strt_idx + 1: end_idx], end_idx

# Clustering baseado nas informações contidas na seção "Metodologia"
def groupByMethodolody(tokens):
    strt_idx = tokens.index("Metodologia")
    end_idx0 = tokens.index("Carga")
    end_idx1 = tokens.index("Horária")
    end_idx = end_idx0 if end_idx0 + 1 == end_idx1 else end_idx1 - 1
    return tokens[strt_idx + 1: end_idx], end_idx

# Clustering baseado nas informações contidas na seção "Experiências de Aprendizagem"
def groupByLearningExperience(tokens):
    strt_idx0 = tokens.index("Experiências")
    strt_idx1 = tokens.index("Aprendizagem")
    strt_idx = strt_idx1 if strt_idx0 + 2 == strt_idx1 else strt_idx0 + 2
    end_idx0 = tokens.index("Critérios")
    end_idx1 = tokens.index("avaliação")
    end_idx = end_idx0 if end_idx0 + 1 == end_idx1 else end_idx1 - 1
    return tokens[strt_idx + 1: end_idx]


# Clustering baseado nas informações contidas na seção "Conteúdo Programático"
def groupByProgramContent(tokens):
    strt_idx0 = tokens.index("Conteúdo")
    strt_idx1 = tokens.index("Programático")
    strt_idx = strt_idx1 if strt_idx0 + 1 == strt_idx1 else strt_idx0 + 1
    end_idx = tokens.index("Metodologia")
    return tokens[strt_idx: end_idx], end_idx

def generateWordCloud(content, title):
    cloud = wordcloud.WordCloud(background_color="white").generate(' '.join(content))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.show()

def clusterAll(corpora):
    word_set = set(word for corpus in corpora for word in corpus)
    dict_lst = []
    for corpus in corpora:
        dict_lst.append(dict.fromkeys(word_set, 0))
        for word in corpus:
            for word in dict_lst[-1]:
                dict_lst[-1][word] += 1

if __name__=="__main__":
    corpus = readTXT("out.txt")
    tokens = tokenize(corpus)

    groups = groupBySection(tokens)

    generateWordCloud(groups[0], "Súmula")

    generateWordCloud(groups[1], "Objetivos")

    generateWordCloud(groups[2], "Conteúdo Programático")

    generateWordCloud(groups[3], "Metodologia")

    generateWordCloud(groups[4], "Experiências de Aprendizagem")
