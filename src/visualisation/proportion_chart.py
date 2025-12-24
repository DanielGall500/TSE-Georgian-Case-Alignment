import pandas as pd
from plotnine import (
    ggplot,
    aes,
    after_stat,
    stage,
    geom_bar,
    geom_text,
    geom_label,
    position_dodge2,
    facet_wrap,
    geom_col,
    labs,
    scale_y_continuous,
    position_stack
)
from plotnine.data import mtcars


results_df = pd.read_csv("./evaluation_results/intransitive-nom-subj.csv")

long_df = results_df.melt(id_vars=["model","repo"], var_name="form", value_name="prob")
long_df["pct"] = (
    long_df
    .groupby("model")["prob"]
    .transform(lambda x: x / x.sum())
)
print(long_df)

p = (
    ggplot(long_df, aes(x="model",y="pct",fill="form"))
    + scale_y_continuous(
        labels=lambda l: [f"{v:.0%}" for v in l]
    )
    + labs(y="Percentage")
    + geom_col()
    + geom_text(
        aes(label=long_df["pct"].map(lambda x: f"{x:.0%}")),
        position=position_stack(vjust=0.5),
        size=9
    )
)
p.save("output.png")
