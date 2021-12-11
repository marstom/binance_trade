# Setup

Create secret.py

```
api_key = "xxx"
api_secret = "yyy"
```


# Start buying
Run 2 processes

Save datapoints to sql database
```bash
python read_client.py
```

It buying and selling crypto and store trasactions info in sql database
```bash
python buy_strategy.py --fake
```





# WIP

new flow

Save datapoints to sql database
```bash
python read_client.py
```


It buying and selling crypto and store trasactions info in sql database
```bash
python buy_crypto.py --fake
```
