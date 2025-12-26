import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_jitter,
    geom_boxplot,
    after_stat,
    stage,
    geom_bar,
    geom_text,
    geom_label,
    position_dodge2,
    position_dodge,
    facet_wrap,
    geom_col,
    labs,
    scale_y_continuous,
    position_stack
)
from plotnine.data import mtcars

tasks = {
    "token-level-intransitive-nom-subj": "Nominative (Subj)",
    "token-level-transitive-nom-dat-subj": "Nominative-Dative (Subj)",
    "token-level-transitive-nom-dat-obj": "Nominative-Dative (Obj)",
    "token-level-transitive-erg-nom-subj": "Ergative-Nominative (Subj)",
    "token-level-transitive-erg-nom-obj": "Ergative-Nominative (Obj)",
    "token-level-transitive-dat-nom-subj": "Dative-Nominative (Subj)",
    "token-level-transitive-dat-nom-obj": "Dative-Nominative (Obj)",
}

final_df = pd.DataFrame()
for task in tasks.keys():
    results_df = pd.read_csv(f"../../evaluation_results_remote/evaluation_results/means/{task}.csv")
    print(results_df)
    long_df = results_df.melt(id_vars=["model","repo"], var_name="form", value_name="prob")
    long_df["form"] = long_df["form"].apply(lambda x: x.replace("form_grammatical_","").replace("form_ungrammatical_","").upper())
    long_df["task"] = tasks[task]

    final_df = pd.concat([final_df, long_df])

final_df.to_csv("final.csv")
final_df["form"] = pd.Categorical(
    final_df["form"],
    categories=["NOM","ERG","DAT"],
    ordered=True
)
final_df["task"] = pd.Categorical(
    final_df["task"],
    categories=tasks.values(),
    ordered=True
)

p = (
    ggplot(final_df, aes(x="form", y="prob", color="form"))
    # + geom_jitter(width=0.2, size=3, alpha=0.7)  # each point = one model
    + geom_boxplot(aes(fill="form"), alpha=0.3, outlier_shape=None)  # optional, summary
    + facet_wrap("~ task", nrow=1)
    + scale_y_continuous(labels=lambda l: [f"{v:.0%}" for v in l])
    + labs(y="Proportion assigned", x="Form")
)

p.save(
    "../../vis/proportion_plot.png",
    width=18,   
    height=6,
    dpi=300
)

"""
# OLD
grouped_df = final_df.groupby(["task","form"], as_index=False)["prob"].mean()
grouped_df["pct"] = grouped_df.groupby(["task"], as_index=False)["prob"].transform(lambda x: x / x.sum())
grouped_df["pct_label"] = grouped_df["pct"].map(lambda x: f"{x:.2%}")

grouped_df["form"] = pd.Categorical(
    grouped_df["form"],
    categories=["NOM","ERG","DAT"],
    ordered=True
)
grouped_df["task"] = pd.Categorical(
    grouped_df["task"],
    categories=tasks.values(),
    ordered=True
)

p = (
    ggplot(grouped_df, aes(x="form", y="pct", fill="form"))
    + geom_col()
    + geom_jitter(width=0.2, size=3, alpha=0.7)
    + geom_text(
        aes(label="pct_label"),
        va="bottom",
        size=9
    )
    + facet_wrap("~ task", nrow=1)
    + scale_y_continuous(labels=lambda l: [f"{v:.0%}" for v in l])
    + labs(y="Percentage", x="Form")
)
"""
