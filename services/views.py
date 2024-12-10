from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from .forms import NgramForm
from nltk import ngrams
from collections import Counter
import re



def test(request):
    return render(request, 'services/test.html')



def remove_stopwords(text):
    with open('stopwords.txt') as stopwords_file:
        stopwords = stopwords_file.readlines()
    stopwords = [line.strip() for line in stopwords]
    if isinstance(text, str):
        text = re.sub(r'[^\w\s]', '', text)  
        words = text.split()  
        filtered_words = [word for word in words if word.lower() not in stopwords]  # حذف کلمات توقف
        print('1')
        return ' '.join(filtered_words)
    else:
        print('2')    
    return text

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def get_ngrams_frequency(texts, n):
    all_ngrams = []
    for text in texts:
        preprocessed_text = preprocess_text(text)
        tokens = preprocessed_text.split()
        n_grams = ngrams(tokens, n)
        try:
            all_ngrams.extend(n_grams)
        except:
            pass
    return Counter(all_ngrams)

@login_required(login_url='/login/')
def service_view(request):
    return render(request, 'services/service_list.html')

@login_required(login_url='/login/')
def generate_excel(request):
    if request.method == 'POST':
        form = NgramForm(request.POST)
        if form.is_valid():
            group_id = form.cleaned_data['group_id']
            frequency_threshold = form.cleaned_data['frequency_threshold']

            # پردازش داده‌ها
            df = pd.read_csv('jam_all_ads.csv')
            df['all_group_id2'] = df['all_group_id2'].astype(int)
            print(df['all_group_id2'].dtype)
            df['all_group_id2'] = df['all_group_id2'].fillna(0)  # به عنوان مثال، جایگزینی `NaN` با صفر

            dfGH = df[df['all_group_id2'] == int(group_id)]
            print(dfGH)

   
            dfGH['ads_name'] = dfGH['ads_name'].apply(remove_stopwords)
            print(dfGH['ads_name'])
            
            texts = dfGH['ads_name'].dropna().tolist()
  

            ngram_freq_df = pd.DataFrame(columns=['N-gram', 'Frequency'])

            for n in range(1, 5):
                ngram_freq = get_ngrams_frequency(texts, n)
                ngram_freq_data = [(f'{" ".join(gram)}', freq,n) for gram, freq in ngram_freq.items()]
                temp_df = pd.DataFrame(ngram_freq_data, columns=['word', 'Frequency','N-gram'])
                ngram_freq_df = pd.concat([ngram_freq_df, temp_df], ignore_index=True)

            # فیلتر کردن بر اساس مقدار فراوانی
            ngram_freq_df = ngram_freq_df[ngram_freq_df['Frequency'] > frequency_threshold]


            # ایجاد فایل اکسل در حافظه
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
            ngram_freq_df.to_excel(response, index=False)
            return response
    else:
        form = NgramForm()

    return render(request, 'services/ngram.html', {'form': form})
