import pickle
from os.path import isfile, join, dirname
from nltk.tokenize import word_tokenize
import nltk.tag
import nltk
from string import punctuation
from random import shuffle


CATEGORY_PT = {
    'male': ['ele', "lo", "dele", "nele", "seu"],
    'female': ['ela', "la", "dela", "nela", "sua"],
    'first': ['eu', 'me', 'mim', 'nós', "comigo", "meu", "minha", "meus",
              "minhas"],
    'neutral': ["tu", "te", "ti", "lhe", "contigo", "consigo", "si"],
    'plural': ['eles', 'elas', "vós", "vocês", "lhes", "los", "las",
               "neles", "nelas", "convosco", "conosco", "connosco", "teus",
               "tuas", "seus", "suas", "nossos", "vossos", "nossas", "vossas"]
}
PRONOUN_TAG_PT = ['PRON']
NOUN_TAG_PT = ['NOUN']
JJ_TAG_PT = ['ADJ']
PLURAL_NOUN_TAG_PT = ['NOUN']
SUBJ_TAG_PT = ['NOUN']


def train_pt_tagger(path):
    nltk.download('mac_morpho')
    nltk.download('floresta')

    def convert_to_universal_tag(t, reverse=False):
        tagdict = {
            'n': "NOUN",
            'num': "NUM",
            'v-fin': "VERB",
            'v-inf': "VERB",
            'v-ger': "VERB",
            'v-pcp': "VERB",
            'pron-det': "PRON",
            'pron-indp': "PRON",
            'pron-pers': "PRON",
            'art': "DET",
            'adv': "ADV",
            'conj-s': "CONJ",
            'conj-c': "CONJ",
            'conj-p': "CONJ",
            'adj': "ADJ",
            'ec': "PRT",
            'pp': "ADP",
            'prp': "ADP",
            'prop': "NOUN",
            'pro-ks-rel': "PRON",
            'proadj': "PRON",
            'prep': "ADP",
            'nprop': "NOUN",
            'vaux': "VERB",
            'propess': "PRON",
            'v': "VERB",
            'vp': "VERB",
            'in': "X",
            'prp-': "ADP",
            'adv-ks': "ADV",
            'dad': "NUM",
            'prosub': "PRON",
            'tel': "NUM",
            'ap': "NUM",
            'est': "NOUN",
            'cur': "X",
            'pcp': "VERB",
            'pro-ks': "PRON",
            'hor': "NUM",
            'pden': "ADV",
            'dat': "NUM",
            'kc': "ADP",
            'ks': "ADP",
            'adv-ks-rel': "ADV",
            'npro': "NOUN",
        }
        if t in ["N|AP", "N|DAD", "N|DAT", "N|HOR", "N|TEL"]:
            t = "NUM"
        if reverse:
            if "|" in t: t = t.split("|")[0]
        else:
            if "+" in t: t = t.split("+")[1]
            if "|" in t: t = t.split("|")[1]
            if "#" in t: t = t.split("#")[0]
        t = t.lower()
        return tagdict.get(t, "." if all(tt in punctuation for tt in t) else t)

    dataset1 = list(nltk.corpus.floresta.tagged_sents())
    dataset2 = [[w[0] for w in sent]
                for sent in nltk.corpus.mac_morpho.tagged_paras()]

    traindata = [[(w, convert_to_universal_tag(t)) for (w, t) in sent] for sent in dataset1]
    traindata2 = traindata + [[(w, convert_to_universal_tag(t, reverse=True)) for (w, t) in sent] for sent in dataset2]

    shuffle(traindata)
    shuffle(traindata2)

    regex_patterns = [
        (r"^[nN][ao]s?$", "ADP"),
        (r"^[dD][ao]s?$", "ADP"),
        (r"^[pP]el[ao]s?$", "ADP"),
        (r"^[nN]est[ae]s?$", "ADP"),
        (r"^[nN]um$", "ADP"),
        (r"^[nN]ess[ae]s?$", "ADP"),
        (r"^[nN]aquel[ae]s?$", "ADP"),
        (r"^\xe0$", "ADP"),
    ]

    def_tagger = nltk.DefaultTagger('NOUN')
    affix_tagger = nltk.AffixTagger(
        traindata2, backoff=def_tagger
    )
    unitagger = nltk.UnigramTagger(
        traindata2, backoff=affix_tagger
    )
    rx_tagger = nltk.RegexpTagger(
        regex_patterns, backoff=unitagger
    )
    tagger = nltk.BigramTagger(
        traindata, backoff=rx_tagger
    )

    templates = nltk.brill.fntbl37()
    tagger = nltk.BrillTaggerTrainer(tagger, templates)
    tagger = tagger.train(traindata, max_rules=100)
    with open(path, "wb") as f:
        pickle.dump(tagger, f)

    return tagger


def load_pt_tagger(path=None):
    path = path or join(dirname(dirname(__file__)), "res", "pt_tagger.pkl")
    if not isfile(path):
        train_pt_tagger(path)
    with open(path, "rb") as f:
        tagger = pickle.load(f)
    return tagger


_POSTAGGER = load_pt_tagger()


def pos_tag_pt(tokens):
    if isinstance(tokens, str):
        tokens = word_tokenize(tokens)
    return _POSTAGGER.tag(tokens)


