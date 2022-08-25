import matplotlib.pyplot as plt

def process_table(df):
    """
    Process value table by rounding, eliminating items with zero value and calculating shares
    """
    df = df.sort_values(by=['value'],ascending=False)
    df['share'] = df['value']/df['value'].sum()*100
    df['value'] = df['value'].astype(float).round(2)
    df['share'] = df['share'].astype(float).round(2)
    df = df[df['value'] > 0.0]
    df=df.reset_index(drop=True)
    return df

def report_plotting_style():
    """
    Initializes report plot style
    """
    # custom color cycle
    from cycler import cycler
    cols = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    lss = ['-', '--', ':', '-.']
    lscyc = [s for s in lss for i in range(len(cols))]
    colcyc = [c for i in range(len(lss)) for c in cols]
    default_cycler = (cycler(color=colcyc) + cycler(linestyle=lscyc))
    plt.rc('axes', prop_cycle=default_cycler)
