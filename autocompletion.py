import math
import json
import random

class LaplaceBiGram:
    def __init__(self):
        self.uni_grams = {'<s>': 0}
        self.bi_grams = {}

    def entrainer(self, data):
        self.uni_grams = {'<s>': 0}
        self.bi_grams = {}

        for phrase in data:
            if not phrase:
                continue

            self.uni_grams['<s>'] += 1
            prev = '<s>'

            for mot in phrase:
                # Compter les unigrammes
                if mot not in self.uni_grams:
                    self.uni_grams[mot] = 0 
                self.uni_grams[mot] += 1

                # Compter les bigrammes
                bigram_key = f"{prev}|{mot}"
                if bigram_key not in self.bi_grams:
                    self.bi_grams[bigram_key] = 0
                self.bi_grams[bigram_key] += 1

                prev = mot

    def noter(self, past, current):
        bigram_key = f"{past}|{current}"
        bigram_count = self.bi_grams.get(bigram_key, 0)
        unigram_count = self.uni_grams.get(past, 0)
        vocab_size = len(self.uni_grams)

        # Lissage de Laplace
        return math.log((bigram_count + 1) / (unigram_count + vocab_size ))

    def estimer(self, mots):
        dernier_mot = mots[-1] if mots else '<s>'
        mots_scores = []

        for mot in self.uni_grams.keys():
            if mot != '<s>':
                score = self.noter(dernier_mot, mot)
                mots_scores.append((mot, score))

        return sorted(mots_scores, key=lambda tab: tab[1], reverse=True)

    def exporter_json(self):
        return self.__dict__.copy()

    def importer_json(self, data):
        for cle in data:
            self.__dict__[cle] = data[cle]

class Autocompletion():
    def __init__(self):
        self.modele = LaplaceBiGram()
        self.eval = []

    def entrainer(self, url):
        f = open(url, 'r', encoding='utf-8')
        data = []
        for l in f: # la lecture ligne par ligne
            phrase = l.strip().lower().split()
            if len(phrase) > 0:
                data.append(phrase)
        f.close()
        self.modele.entrainer(data)

    def estimer(self, phrase, nbr):
        mots_scores = self.modele.estimer(phrase.strip().lower().split())
        return mots_scores[:nbr]

    def charger_modele(self, url):
        f = open(url, 'r', encoding='utf-8')
        data = json.load(f)
        self.modele.importer_json(data)
        f.close()

    def sauvegarder_modele(self, url):
        f = open(url, 'w')
        json.dump(self.modele.exporter_json(), f)
        f.close()

    def charger_evaluation(self, url):
        f = open(url, 'r', encoding='utf-8')
        for l in f: # La lecture se fait ligne par ligne
            info = l.strip().lower().split("	")
            if len(info) < 2 :
                continue
            self.eval.append(info)

    def evaluer(self, n, m): 
        if n == -1:
            S = self.eval
            n = len(S)
        else :
            S = random.sample(self.eval, n)
        score = 0.0
        for i in range(n):
            test = S[i]
            print('-> Proba(', test[1], '|',test[0], ')')
            res = self.estimer(test[0], m)
            print('found:', res)
            words = [e[0] for e in res]
            try:
                i = words.index(test[1]) + 1
                score += 1/i
            except ValueError:
                pass
        score = score/n
        print('Score = ', score)
        return score

if __name__ == '__main__':
    program = Autocompletion()
    program.entrainer('data/data_train.txt')
    program.sauvegarder_modele('./autocompletion.json')
    program.charger_evaluation('data/data_test.txt')
    mrr = program.evaluer(-1, 10) # -1 pour prendre toutes les phrases