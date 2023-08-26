# Generic and Scalable Risky Transactions Detection Using Density Flows: Applications to Financial Networks

## Description
This project is a Python achievement for the paper "Generic and Scalable Risky Transactions Detection Using Density Flows: Applications to Financial Networks", which is a novel combinatorial optimization solution for risky transactions detection by iteratively calculating densest flow on transaction graph. 

## Usage
1. Clone the repository. 

2. Install the project dependencies.

    - python 3.8
    - pandas
    - sparse

2. Download datasets. 

    We provide four synthetic datasets and four real world datasets, which can download from https://pan.baidu.com/s/1p8nd8TAZo21Nw1pD8rzrow?pwd=i1ee. 
    
    User can make datasets for the algorithms, which need contain three columns, i.e. from account, to account, and transfer amount. 
    
    File "gen_synthetic.py" provides generation method for random synthetic dataset, which we use Ethereum real transactions as source data.

3. Test algorithm on real world datasets.

    Running notebook "test_on_real_dataset.ipynb".

4. Test algorithm on synthetic datasets.
    
    Running notebook "test_on_synthetic_dataset.ipynb".

## Related hacker addresses of real datasets

|    Datasets   | Related Hacker Address                     |
|:----------:|--------------------------------------------|
|    Ronin   | 0x098b716b8aaf21512996dc57eb0615e2383e2f96 |
|            | 0xe708f17240732bbfa1baa8513f66b665fbc7ce10 |
| BNB Bridge | 0x489a8756c18c0b8b24ec2a2b9ff3d4d447f79bec |
|            | 0xfa0a32e5c33b6123122b6b68099001d9371d14e9 |
|    Euler   | 0xb66cd966670d962c227b3eaba30a872dbfb995db |
|            | 0xebc29199c817dc47ba12e3f86102564d640cbf99 |
|            | 0xc66dfa84bc1b93df194bd964a41282da65d73c9a |
|            | 0xb2698c2d99ad2c302a95a8db26b08d17a77cedd4 |
|            | 0x5f259d0b76665c337c6104145894f4d1d2758b8c |
|   Harmony  | 0xc3f2c8f9d5f0705de706b1302b7a039e1e11ac88 |

## Entitiy labels of Euler top50 dense flows

| #order | #addresses of flow                         | type     | entity label                                 |
|--------|--------------------------------------------|----------|----------------------------------------------|
|    1   | 0xf977814e90da44bfa03b6295a0616a897441acec | address  | Binance Exchange Cold Wallet                 |
|        | 0x28c6c06298d514db089934071355e5743bf21d60 | address  | Binance Exchange Deposit Address             |
|        | 0xdfd5293d8e347dfe59e90efd55b2956a1343963d | address  | Binance Exchange Withdraw Address            |
|    4   | 0x043a80999cee3711d372fb878768909fbe7f71e6 | address  | Binance Exchange Industry Recovery Intiative |
|        | 0xc097431d9050592b71f71bf6d688845be3ef9723 | address  | GOPAX Exchange Address                       |
|    9   | 0x56178a0d5f301baf6cf3e1cd53d9863437345bf9 | address  | Nomad White-Hat Hacker                       |
|        | 0xa57bd00134b2850b2a1c55860c9e9ea100fdd6cf | contract | Maximize Extractable Value Bot               |
|   10   | 0x803466ad7ed0c5dd9762da7f20d61e8e7903cee5 | address  | Unknown                                      |
|        | 0x33566c9d8be6cf0b23795e0d380e112be9d75836 | address  | Fund Institutions                            |
|        | 0x1b8b6098bd71314e4a4e1bb9a0f898399a16c9cc | contract | Unknown                                      |
|        | 0x55fe002aeff02f77364de339a1292923a15844b8 | address  | Circle(Issuer of Stable Coin USDC)           |
|   14   | 0x000000000dfde7deaf24138722987c9a6991e2d4 | contract | Maximize Extractable Value Bot               |
|        | 0x410ed1cbcea3b3990a3f27362c06c3c5d1e75d08 | address  | Binance Exchange User                        |
|   16   | 0xd3b7cea28feb5e537fca4e657e3f60129456eaf3 | contract | Unknown                                      |
|        | 0x036cec1a199234fc02f72d29e596a09440825f1c | contract | Euler Exploit Contract                       |
|        | 0xb66cd966670d962c227b3eaba30a872dbfb995db | address  | Euler Hacker                                 |
|   17   | 0x5754284f345afc66a98fbb0a0afe71e0f007b949 | address  | Tether Treasury Address                      |
|        | 0x77134cbc06cb00b66f4c7e623d5fdbf6777635ec | address  | Bitfinex Exchange Deposit Address            |
|        | 0x7d725aa4be016012e26ad9375cfa6573f99a5111 | contract | Unknown                                      |
|   23   | 0x3835a58ca93cdb5f912519ad366826ac9a752510 | token20  | FraxlendV1(Lending Platform)                 |
|        | 0x7a16ff8270133f063aab6c9977183d9e72835428 | address  | CRV Token Founder                            |
|        | 0x8dae6cb04688c62d939ed9b68d32bc62e49970b1 | token20  | Aave Interest Bearing CRV                    |
|   37   | 0x3ddfa8ec3052539b6c9549f12cea2c295cff5296 | address  | Justin Sun(TRON Blockchain Founder)          |
|        | 0x9f8413454c182369c0200f6cc1031903477f752e | address  | Justin Sun(TRON Blockchain Founder)          |
|   39   | 0xef764bac8a438e7e498c2e5fccf0f174c3e3f8db | address  | Blurr(Refund Coin Founder)                   |
|        | 0x5720eb958685deeeb5aa0b34f677861ce3a8c7f5 | contract | Defi Uniswap V3 Liquidity Pool(USDP/USDC)    |
|   46   | 0xcffad3200574698b78f32232aa9d63eabd290703 | address  | Crypto.com. Exchange Deposit Address         |
|        | 0x46340b20830761efd32832a74d7169b29feb9758 | address  | Crypto.com Exchange Address                  |
