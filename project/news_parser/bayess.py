from nltk.stem.snowball import SnowballStemmer
from collections import Counter


class TextBayes():

  def __init__(self):
    self.stemmer = SnowballStemmer("russian")
    self.data = dict()
    self.words = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между']
    self.letters = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','ё',' ']

  def fit(self, X_batch: list, y_batch: list):
    self.counts = dict(Counter(y_batch))
    self.all_counts = len(y_batch)
    for item_number in range(len(X_batch)):
      if item_number % 10000 == 0:
        print((100*item_number/self.all_counts), '%')
      for word in self.process(X_batch[item_number]):
        if self.data.get(word) is None:
          self.data[word] = {tag: 0 for tag in self.counts}
          self.data[word][y_batch[item_number]] = 1
        else:
          self.data[word][y_batch[item_number]] += 1
    return(self.data)
  
  def get_settings(self):
    return [self.data, self.counts, self.all_counts]

  def set_settings(self, ar):
    self.data = ar[0]
    self.counts = ar[1]
    self.all_counts = ar[2]

  def set_dict(self, input_dict: dict):
    self.data = input_dict

  def get_prior(self) -> dict:
    self.prior = dict()
    for tag in self.counts:
      self.prior[tag] = self.counts[tag]/self.all_counts
    return self.prior

  def get_likelhood(self, word: str) -> dict:
    likelhood = dict()
    for tag in self.counts:
      likelhood[tag] = self.data[word][tag]/self.counts[tag]
    return likelhood

  def get_reverse_likelhood(self, word: str) -> dict:
    reverse_likelhood = dict()
    for tag in self.counts:
      reverse_likelhood[tag] = (sum(self.data[word].values()) - self.data[word][tag])/(sum(self.counts.values()) - self.counts[tag])
    return reverse_likelhood

  def get_posterior(self, word: str) -> dict: 
    prior = self.get_prior()
    likelhood = self.get_likelhood(word)
    reverse_likelhood = self.get_reverse_likelhood(word)
    post_dict = dict()
    for tag in self.data[word]:
      post_dict[tag] = likelhood[tag]*prior[tag]/(likelhood[tag]*prior[tag] + reverse_likelhood[tag]*(1-prior[tag]))
    return post_dict

  def predict(self, input_str: str) -> dict:
    predicted_dict = dict()
    words = self.process(input_str)
    for tag in self.counts:
      posterior_list = list()
      for word in words:
        if self.data.get(word) is not None:
          posterior_list.append(self.get_posterior(word).get(tag))
      predicted_dict[tag] = self.final_bayes(posterior_list, self.get_prior()[tag], len(words))
    return predicted_dict

  def process(self, input_str: str) -> list:
    input_str = input_str.lower()
    for l in input_str:
      if l not in self.letters:
        input_str = input_str.replace(l, ' ')
    words = input_str.split() 
    return [self.stemmer.stem(word) for word in words if word not in self.words]

  def final_bayes(self, p : list, pS, N, delta=0.00000000001) -> float:
    multi_p = 1
    multi_not_p = 1
    for i in p:
      multi_p *= (i+delta)
      multi_not_p *= (1-i+delta)
    return multi_p/(multi_p + multi_not_p * ((1 - pS)/pS) ** (1-N))
   
