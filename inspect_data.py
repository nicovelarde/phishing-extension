import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

df = pd.read_csv('URL dataset.csv')

# Mapping labels to binary
df['type'] = df['type'].map({'phishing': 1, 'legitimate': 0})
df = df.dropna(subset=['type'])

# Number of legitimate and number of phishing urls in dataset
#print("Label counts:\n", df['type'].value_counts())

# Feature extraction
def extract_url_features(url):
    features = {}
    try:
        if pd.isna(url) or not isinstance(url, str):
            raise ValueError("Invalid URL")

        #Parse the url
        parsed = urlparse(url)
        domain = parsed.netloc #gets the domain  # to check if there is an IP address instead of a domain
        path = parsed.path   #gets the path parsed #to check if the path is trying to mimic a legit site
        query = parsed.query #gets what is after the ? # check if the query is too long to has weird parameters

        #Checks if the domain looks like an IP address in ipv4, ipv6 or hexadecimal format
        # If so there is more likelihood that it is phishing
        ipv4_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        ipv6_pattern = r"^\[?([a-fA-F0-9:]+)\]?$"
        hex_pattern = r"^\[?([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\]?$"
        features['has_ip_address'] = int(bool(re.match(ipv4_pattern, domain) or re.match(ipv6_pattern, domain)  or re.search(hex_pattern, domain)))

        #Check on the length id it is short 0-54 then it is likely safe 0
        #54-75 watchful 1
        #75< suspicious 2
        # Based on research paper long urls are usually phishing
        length = len(url)
        features['url_length_category'] = 0 if length < 54 else 1 if length <= 75 else 2

        # 1 if used a shortening service
        # 0 if it did not
        shortening_services = ["bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "t.co", "is.gd", "buff.ly", "adf.ly", "bit.do", "mcaf.ee"]
        features['uses_shortening_service'] = int(any(service in url for service in shortening_services))

        # @ is a sign of a phishing url
        features['has_at_symbol'] = int("@" in url)

        # // sign of a phishing url
        features['double_slash_position'] = int(url.rfind("//") > 7)

        # - sign of a phishing url
        features['prefix_suffix_in_domain'] = int("-" in domain)

        # Number of subdomains
        dot_count = domain.count(".")
        features['subdomain_level'] = 0 if dot_count == 1 else 1 if dot_count == 2 else 2

        # checks if the word "https" is found in the domain
        features['https_token_in_domain'] = int("https" in domain.lower())

        # Number of digits in the url if too many, phishing
        features['num_digits'] = sum(c.isdigit() for c in url)

        # Too many special characters, phishing
        features['num_special_chars'] = sum(c in "=?.%&#" for c in url)

        # How many = are in the query string
        features['num_parameters'] = query.count("=")

        # Checks how many suspicious words
        suspicious_keywords = ['login', 'secure', 'verify', 'account', 'update', 'bank', 'signin', 'submit']
        features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))

        # Check if it is an executable
        features['ends_with_exe'] = int(url.lower().endswith(".exe"))

        #counts https
        features['count_http_https'] = url.lower().count("http")

    except Exception as e:
        features = {
            'has_ip_address': 0,
            'url_length_category': 0,
            'uses_shortening_service': 0,
            'has_at_symbol': 0,
            'double_slash_position': 0,
            'prefix_suffix_in_domain': 0,
            'subdomain_level': 0,
            'https_token_in_domain': 0,
            'num_digits': 0,
            'num_special_chars': 0,
            'num_parameters': 0,
            'has_suspicious_words': 0,
            'ends_with_exe': 0,
            'count_http_https': 0,
        }

    return features

feature_dicts = df['url'].apply(extract_url_features)
X = pd.DataFrame(feature_dicts.tolist())
y = df['type']  # Target labels

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_probs = clf.predict_proba(X_test)[:, 1]  # Phishing probability
threshold = 0.3
y_pred_custom = (y_probs >= threshold).astype(int)

#print(f"\n Evaluation with Threshold = {threshold}")
#print(confusion_matrix(y_test, y_pred_custom))
#print(classification_report(y_test, y_pred_custom))

# Tried Multiple Thresholds ===
# for t in [0.5, 0.4, 0.3, 0.2]:
#     y_pred = (y_probs >= t).astype(int)
#     print(f"\n🔍 Threshold: {t}")
#     print(classification_report(y_test, y_pred))
