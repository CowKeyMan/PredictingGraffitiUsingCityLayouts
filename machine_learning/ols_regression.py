import pandas as pd
import statsmodels.formula.api as smf
import itertools


def build_formula(x):
    s = ''
    for t, z in itertools.combinations(x, 2):
        s += " + " + t + ':' + z
    return s


df = pd.read_csv('resources/data/generated/buildings_model_features.csv')
y = df['graffiti_count']
x = df.drop(columns=['graffiti_count'])

singular_variables = ' + '.join(x.columns.tolist())
joint_variables = build_formula(x.columns.tolist())
# formula = "graffiti_count ~ " + s + joint_variables
formula = "graffiti_count ~ " + singular_variables

fit = smf.ols(formula, data=df).fit()
print(fit.summary())
