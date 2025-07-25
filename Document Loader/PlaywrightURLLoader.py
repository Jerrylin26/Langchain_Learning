from langchain_community.document_loaders import PlaywrightURLLoader

loader = PlaywrightURLLoader([
    'https://tw.news.yahoo.com/nba-%E5%BA%AB%E6%98%8E%E5%8A%A0%E4%B8%8D%E6%80%A5%E6%8E%A5%E5%8F%97%E5%A0%B1%E5%83%B9-%E6%9B%9D%E6%83%B3%E5%8E%BB%E9%80%992%E9%9A%8A-%E5%8B%87%E5%A3%AB%E6%B2%92%E6%89%93%E7%AE%97%E9%80%99%E6%A8%A3%E6%8F%9B-084400458.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAKeQC-Kt8AEtZSUc61bZImf_CrbqXYP81iKWcBYRB_DCjxx5wW4Q3Xs8kFiIL-jdQTq6C_fUMap6hCY83wGNy7GBmI25oIaH1wgDagRiOIARFolK0T8Uc6Znx-Uz6AWcUH2hAdw8tLnys8aXar4ERS7aVhCGT-UggoWjKWqok7Qk'
])

for x in loader.load():
    print(x)