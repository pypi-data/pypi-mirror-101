from pronomial.utils import predict_gender, pos_tag, word_tokenize


class PronomialCoreferenceSolver:
    @staticmethod
    def solve_corefs(sentence, lang="en"):
        if lang.startswith("en"):
            from pronomial.lang.en import NOUN_TAG_EN, PLURAL_NOUN_TAG_EN, \
                CATEGORY_EN, PRONOUN_TAG_EN, SUBJ_TAG_EN, JJ_TAG_EN
            NOUN_TAG = NOUN_TAG_EN
            SUBJ_TAG = SUBJ_TAG_EN
            PRONOUN_TAG = PRONOUN_TAG_EN
            CATEGORY = CATEGORY_EN
            PLURAL_NOUN_TAG = PLURAL_NOUN_TAG_EN
            JJ_TAG = JJ_TAG_EN
        elif lang.startswith("pt"):
            from pronomial.lang.pt import NOUN_TAG_PT, PLURAL_NOUN_TAG_PT, \
                PRONOUN_TAG_PT, SUBJ_TAG_PT, JJ_TAG_PT, CATEGORY_PT
            NOUN_TAG = NOUN_TAG_PT
            SUBJ_TAG = SUBJ_TAG_PT
            PRONOUN_TAG = PRONOUN_TAG_PT
            CATEGORY = CATEGORY_PT
            PLURAL_NOUN_TAG = PLURAL_NOUN_TAG_PT
            JJ_TAG = JJ_TAG_PT
        else:
            raise NotImplementedError

        tags = pos_tag(sentence, lang=lang)

        prev_names = {
            "male": None,
            "female": None,
            "first": None,
            "neutral": None,
            "plural": None,
            "subject": None
        }
        candidates = []

        for idx, (w, t) in enumerate(tags):
            if t in NOUN_TAG:
                if w[0].isupper():
                    gender = predict_gender(w)
                    prev_names[gender] = w
                if not prev_names["neutral"]:
                    prev_names["neutral"] = w
                if not prev_names["subject"]:
                    prev_names["subject"] = w
            elif t in SUBJ_TAG:
                prev_names["subject"] = w
                if not prev_names["neutral"]:
                    prev_names["neutral"] = w
            elif t in PRONOUN_TAG or any(w in items
                                         for k, items in CATEGORY.items()):
                w = w.lower()
                if w in CATEGORY["male"] and prev_names["male"]:
                    candidates.append((idx, w, prev_names["male"]))
                elif w in CATEGORY["female"] and prev_names["female"]:
                    candidates.append((idx, w, prev_names["female"]))
                elif w in CATEGORY["plural"] and prev_names["plural"]:
                    candidates.append((idx, w, prev_names["plural"]))
                elif w in CATEGORY["first"] and prev_names["first"]:
                    candidates.append((idx, w, prev_names["first"]))
                elif w in CATEGORY["neutral"] and prev_names["neutral"]:
                    candidates.append((idx, w, prev_names["neutral"]))
                elif w in CATEGORY["neutral"] and prev_names["subject"]:
                    candidates.append((idx, w, prev_names["subject"]))
                elif w in CATEGORY["plural"] and prev_names["subject"]:
                    candidates.append((idx, w, prev_names["subject"]))
                else:
                    for k, v in CATEGORY.items():
                        if prev_names[k] and w in v:
                            candidates.append((idx, w, prev_names[k]))
                    else:
                        if prev_names["subject"] and \
                                w not in CATEGORY["first"]:
                            candidates.append((idx, w, prev_names["subject"]))

            elif t in PLURAL_NOUN_TAG:
                prev_names["plural"] = w
                if w[0].isupper():
                    gender = predict_gender(w)
                    if not prev_names[gender]:
                        prev_names[gender] = w
            elif t in JJ_TAG:  # common tagger error
                if w[0].isupper():
                    gender = predict_gender(w)
                    if not prev_names[gender]:
                        prev_names[gender] = w
                if not prev_names["neutral"]:
                    prev_names["neutral"] = w
                if not prev_names["subject"]:
                    prev_names["subject"] = w
        return candidates

    @classmethod
    def replace_corefs(cls, text, lang="en"):
        tokens = word_tokenize(text)
        for idx, _, w in cls.solve_corefs(text, lang=lang):
            tokens[idx] = w
        return " ".join(tokens)


def replace_corefs(text, lang="en"):
    return PronomialCoreferenceSolver.replace_corefs(text, lang=lang)

