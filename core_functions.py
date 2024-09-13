#import all libraries needed
import polars as pl
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

def read_data():
    arguments = pd.read_csv('data/argument_predictions.csv')
    meta = pd.read_csv('data/argument_metadata.csv')

    return meta, arguments

def clean_data(arguments, threshold):
    return  arguments[arguments["probs"] >= threshold]

def sizes(threshold, data):
    arguments_old = data
    arguments = clean_data(data, threshold)

    print('Arguments complete set:')
    print(arguments_old.shape)

    print('Arguments set with prediction threshold: ' + str(threshold))
    print(arguments.shape)
    print()

    gb = arguments[arguments["ID"].str.contains("-GB")]
    ua = arguments[arguments["ID"].str.contains("-UA")]
    sl = arguments[arguments["ID"].str.contains("-SI")]

    print('Great Britain')

    print(arguments_old[arguments_old["ID"].str.contains("-GB")].shape)
    print(gb.shape)
    print()

    print('Ukraine')

    print(arguments_old[arguments_old["ID"].str.contains("-UA")].shape)
    print(ua.shape)
    print()


    print('Slovenia')
    print(arguments_old[arguments_old["ID"].str.contains("-SI")].shape)
    print(sl.shape)
    print()

def classification_probs(arguments, save_str):
    gb = arguments[arguments["ID"].str.contains("-GB")]
    ua = arguments[arguments["ID"].str.contains("-UA")]
    sl = arguments[arguments["ID"].str.contains("-SI")]
    
        
    summary = {
        'Great Britain': {'mean': np.nanmean(gb['probs']), 'std': np.nanstd(gb['probs']), 'min': np.nanmin(gb['probs']), 'max': np.nanmax(gb['probs'])},
        'Ukraine': {'mean': np.nanmean(ua['probs']), 'std': np.nanstd(ua['probs']), 'min': np.nanmin(ua['probs']), 'max': np.nanmax(ua['probs'])},
        'Slovenia': {'mean': np.nanmean(sl['probs']), 'std': np.nanstd(sl['probs']), 'min': np.nanmin(sl['probs']), 'max': np.nanmax(sl['probs'])}
    }

    box_plot_data = []

    for key, stats in summary.items():
        mean = stats['mean']
        std = stats['std']
        minimum = stats['min']
        maximum = stats['max']
        q1 = mean - std
        q3 = mean + std
        box_plot_data.append([minimum, q1, mean, q3, maximum])

    # Create a box plot
    fig, ax = plt.subplots()
    ax.boxplot(box_plot_data, vert=True)

    # Set the labels
    ax.set_xticklabels(summary.keys())
    ax.set_title('Classification probabilities for argument classes by country')
    ax.set_ylabel('Probabilities')

    plt.savefig('figures/' + save_str)

def plot_piechart(freqs, categories, save_str, title):
    #colors = plt.cm.tab20(np.linspace(0, 1, 42))
    
    explode = [0.1 if freq == max(freqs) else 0 for freq in freqs]
    #colors = [color_map[category] for category in categories]

    plt.figure(figsize=(12, 12))
    plt.pie(freqs, labels=categories, autopct='%1.1f%%',  textprops={'fontsize': 11}, startangle=140)

    plt.title(title, fontsize=16)

    plt.savefig('figures/' + save_str)

def argument_categories(country_str, save_str, arguments):
    country_str = '-' + country_str

    country = arguments[arguments["ID"].str.contains(country_str)]
    freqs = country['codes'].value_counts().sort_index()
    plot_piechart(freqs, ['Value', 'Under threat', 'Leverage', 'Other'], save_str, 'Distribution of argument classes, ' + country_str[1:])
    print('Argument type frequencies:')
    print(freqs)
    print('')

def get_freqs(arguments):
    gb = arguments[arguments["ID"].str.contains("-GB")]
    ua = arguments[arguments["ID"].str.contains("-UA")]
    sl = arguments[arguments["ID"].str.contains("-SI")]
    
    gb_freqs = gb['codes'].value_counts().sort_index()
    ua_freqs = ua['codes'].value_counts().sort_index()
    sl_freqs = sl['codes'].value_counts().sort_index()

    return gb_freqs, ua_freqs, sl_freqs

def argument_class_compare(save_str, arguments):
    gb_freqs, ua_freqs, sl_freqs = get_freqs(arguments)

    value = [gb_freqs[0], ua_freqs[0], sl_freqs[0]]
    threat = [gb_freqs[1], ua_freqs[1], sl_freqs[1]]
    leverage = [gb_freqs[2], ua_freqs[2], sl_freqs[2]]
    other = [gb_freqs[3], ua_freqs[3], sl_freqs[3]]

    # Sample data
    data = {
        'Country': ['Great Britain', 'Ukraine', 'Slovenia'],
        'Value': value,
        'Threat': threat,
        'Leverage':leverage,
        'Other': other
    }
    df = pd.DataFrame(data)
    df_normalized = df.set_index('Country').apply(lambda x: x / x.sum(), axis=1)

    fig, ax = plt.subplots(figsize=(15, 10))
    bars = df_normalized.plot(kind='bar', stacked=True, ax=ax)


    plt.style.use('ggplot')
    # percentages to the bars
    for container in ax.containers:
        #  percentages on the bars
        for rect in container:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height:.1%}', 
                            xy=(rect.get_x() + rect.get_width() / 2, rect.get_y() + height / 2),
                            xytext=(0, 0),  # Offset
                            textcoords="offset points",
                            ha='center', va='center', fontsize=8, color='white')

    ax.set_ylabel('Portion of argument class in the data set')
    ax.set_xlabel('')
    ax.set_title('Distribution of argument classes per country')
    plt.xticks(rotation=0)

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.savefig('figures/' + save_str)

def plot_dist(df, title, save_str):
    
    fig, ax = plt.subplots(figsize=(15,10))
    bars = df.plot(kind='bar', stacked=True, ax=ax)


    plt.style.use('ggplot')
    # Adding percentages to the bars
    for container in ax.containers:
        # Adding percentages on the bars
        for rect in container:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height:.1%}', 
                            xy=(rect.get_x() + rect.get_width() / 2, rect.get_y() + height / 2),
                            xytext=(0, 0),  # Offset
                            textcoords="offset points",
                            ha='center', va='center', fontsize=8, color='white')

    # Adding labels
    ax.set_ylabel('Portion of argument class in the data set')
    ax.set_xlabel('')
    ax.set_title(title)

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_xticks(range(len(df.index)))  # Set the positions of the ticks
    
    plt.savefig('figures/ ' + save_str)

def get_normalized_freqs(ds_set, index, cats):
    freqs = []
    for ds in ds_set:
        ds_add = ds['codes'].value_counts().sort_index()
        
        if 'LABEL_0' not in ds_add.index:
            ds_add.loc['LABEL_0'] = 0
        if 'LABEL_1' not in ds_add.index:
            ds_add.loc['LABEL_1'] = 0
        if 'LABEL_2' not in ds_add.index:
            ds_add.loc['LABEL_2'] = 0
        if 'LABEL_3' not in ds_add.index:
            ds_add.loc['LABEL_3'] = 0
        
        ds_add.sort_index()
    
        sum(ds_add)
        freqs.append(ds_add)
    
    print(freqs)
    
    data = {
        index: cats,
        'Value': np.array(freqs)[:,0],
        'Threat': np.array(freqs)[:,1],
        'Leverage': np.array(freqs)[:,2],
        'Other': np.array(freqs)[:,3]
    }

    df = pd.DataFrame(data)
    
    print(df)
    df_normalized = df.set_index(index).apply(lambda x: x / x.sum(), axis=1)
    
    return df_normalized

def by_gender(arg_meta, save_str):
    arg_meta = arg_meta[arg_meta["probs"] >= 75]

    women = arg_meta[arg_meta['gender'] == 'F']
    men  = arg_meta[arg_meta['gender'] == 'M']
    df_norm = get_normalized_freqs([women, men], 'Gender', ['Women', 'Men'])

    plot_dist(df_norm, 'Distribution of argument classes per gender', save_str)


def get_party_subsets(ds, party_list):
    ds_set = []
    for party in party_list:
        party_ds = ds[ds['parties'].apply(lambda x: party in x)]
        ds_set.append(party_ds)
    
    return ds_set

def uk_lc(arg_meta, save_str):
    gb_meta = arg_meta[arg_meta["ID"].str.contains("-GB")]
    party_ds_set = get_party_subsets(gb_meta, ['Conservative', 'Labour'])

    gb_party_norm = get_normalized_freqs(party_ds_set, 'Party', ['Conservative', 'Labour'])
    plot_dist(gb_party_norm, 'Distribution of argument classes, UK parliament', save_str)

def uk_selected(arg_meta, save_str):
    gb_meta = arg_meta[arg_meta["ID"].str.contains("-GB")]
    interest_parties = ['Labour','Conservative','Ulster Unionist Party','Scottish National Party','Liberal Democrat','UK Independence Party','Democratic Unionist Party']
    testi_ = ['LAB', 'CON', 'UCUNF', 'SNP', 'LB', 'UKIP', 'DUP']
    ds_interest_set = get_party_subsets(gb_meta, interest_parties)
    ds_interest_freqs = get_normalized_freqs(ds_interest_set, 'Party', interest_parties)
    plot_dist(ds_interest_freqs, 'Argument classes, selected parties in British Parliament', save_str)

def ua_parties(arg_meta, save_str):
    ua_meta = arg_meta[arg_meta["ID"].str.contains("-UA")]

    interest_parties_ua = ['Політична партія "Партія регіонів"',
    'Блок Петра Порошенка',
    'Блок "НАША УКРАЇНА": Політична партія "Народний Союз Наша Україна", Народний Рух України, Партія промисловців і підприємців України, Конгрес Українських Націоналістів, Українська республіканська партія "Собор", Партія Християнсько-Дем.Союз',]


    ds_interest_set_ua = get_party_subsets(ua_meta, interest_parties_ua)
    ds_interest_freqs_ua = get_normalized_freqs(ds_interest_set_ua, 'Party', interest_parties_ua)
    ds_interest_freqs_ua
    plot_dist(ds_interest_freqs_ua, 'Argument classes, selected parties in the Ukranian Parliament', save_str)

def sl_parties(arg_meta, save_str):
    sl_meta = arg_meta[arg_meta["ID"].str.contains("-SI")]

    interest_parties_sl = ['Socialdemokratska stranka Slovenije', 'Socialni demokrati', 'Slovenska nacionalna stranka', 'Nova Slovenija – Krščanski demokrati', 'Združena levica', 'Slovenska demokratska stranka']
    ds_interest_set_sl = get_party_subsets(sl_meta, interest_parties_sl)
    ds_interest_freqs_sl = get_normalized_freqs(ds_interest_set_sl, 'Party', interest_parties_sl)
    plot_dist(ds_interest_freqs_sl, 'Argument classes, selected parties in the Slovenian Parliament', save_str)