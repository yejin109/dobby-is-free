from itertools import product


confs = [
    'AAAI', 'ICML', 'NIPS', 'ICLR'
]
conf_years = [2022]
conf_keywords = [
    'diffusion', 'capacity', 'train', 'curriculum'
]

arxiv_dates = ["Tue, 18 Jul 2023",
               ]

with open('./search.bat', 'w') as f:
    for conf, year, keyword in product(confs, conf_years, conf_keywords):
        f.write(f"python main.py --is_conf --target_conf {conf} --conf_year {year} --conf_keyword {keyword}\n")

    for date in product(arxiv_dates):
        date = date[0]
        # f.write(f'python main.py --target_arxiv --date "{str(date)}"\n')
