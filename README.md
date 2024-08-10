## STEPS TO RUN THE CODE -

Before running the script, ensure you have Python installed on your machine. Then, install the necessary Python packages using:
# clone repo
 ```sh
    git clone https://github.com/Solana0x/nodepay.git 
    cd nodepay
 ```
# install 
```sh
   pip install -r requirements.txt
```
1. Replace `NP TOken` list in correct formate in `node.py` File Line ```9```.
2. By default 100 proxies will be taken randomly if you wana change then change here `active_proxies = [proxy for proxy in all_proxies[:100] if is_valid_proxy(proxy)]` line 169. Here 100 means 100 proxy will be used at once.
3. Dont Forget to add multiple proxies in the proxy.txt file you can add 1000+ proxy !! Formate # `HTTP://username:pass@ip:port`.
4. You can get Multiple Proxy Ip address from Proxies.fo Website !! [use multiple IP ! `1 IP == ~1400 $NODEPAY per Day `.
5. To Run Script  ```sh python3 node.py  ``` 
6. To Run multiple User ID just copy paste the `node.py` file code and create new python file and repeat the process !!.
