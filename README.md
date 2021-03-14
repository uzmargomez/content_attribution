# Content Attribution with Markov Chains

Python code for Markov Attribution. This is not intended to be production code, as is too slow, it was created just to land ideas.

Example code:

```
from MarkovAttribution import MarkovAttribution

sep = " > "

B = MarkovAttribution(
    dataset=df_final,
    var_path="path",
    var_conv="conversion",
    var_value="value",
    separator=sep,
)
```