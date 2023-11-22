## Install:  
cd to the project root  
`pip install .`

## Fetching Data:   

cd to the project root   

```bash
PS C:\Users\realgu\tech\betslip> python ./main.py -symbol 'SZ159915' -begin '2023-01-01 00:00:00' -period day
2023-11-22 23:40:45 - INFO - Start fetching data with symbol: SZ159915, begin: 2023-01-01 00:00:00, period: day, source: xueqiu, save_fmt: ['pkl']
2023-11-22 23:40:46 - INFO - Sending HTTP request with symbol: SZ159915, begin: 2023-11-22 23:40:45, period: day, count: -284
2023-11-22 23:40:46 - INFO - New data fetched: 2022-09-19 16:00:00 to 2023-11-21 16:00:00
2023-11-22 23:40:46 - INFO - Data fetched:
               timestamp     volume   open   high    low  close    chg  percent  turnoverrate        amount volume_post amount_post   
0   2022-09-19 16:00:00  360217200  2.295  2.327  2.285  2.297  0.012     0.53           0.0  8.304858e+08        None        None    
1   2022-09-20 16:00:00  521184289  2.284  2.289  2.256  2.265 -0.032    -1.39           0.0  1.181944e+09        None        None    
2   2022-09-21 16:00:00  367288984  2.250  2.280  2.236  2.252 -0.013    -0.57           0.0  8.288182e+08        None        None    
3   2022-09-22 16:00:00  531741668  2.245  2.268  2.209  2.239 -0.013    -0.58           0.0  1.189493e+09        None        None    
4   2022-09-25 16:00:00  528002975  2.226  2.288  2.220  2.253  0.014     0.63           0.0  1.194645e+09        None        None    
..                  ...        ...    ...    ...    ...    ...    ...      ...           ...           ...         ...         ...    
279 2023-11-15 16:00:00  742839749  1.961  1.962  1.925  1.925 -0.038    -1.94           0.0  1.439597e+09        None        None    
280 2023-11-16 16:00:00  369854251  1.920  1.935  1.918  1.934  0.009     0.47           0.0  7.130184e+08        None        None    
281 2023-11-19 16:00:00  602010387  1.934  1.947  1.918  1.942  0.008     0.41           0.0  1.162760e+09        None        None    
282 2023-11-20 16:00:00  759957242  1.949  1.962  1.928  1.931 -0.011    -0.57           0.0  1.477950e+09        None        None    
283 2023-11-21 16:00:00  773629987  1.923  1.930  1.899  1.899 -0.032    -1.66           0.0  1.478990e+09        None        None    

[284 rows x 12 columns]
2023-11-22 23:40:46 - INFO - DataFrame saved successfully to c:\Users\realgu\tech\betslip\betslip\resource\data\SZ159915-day.pkl      

```
   
- Default frequency of data is 'day'.   
- Note that the returned data usually include a few entries before the 'begin' timestamp.   
- Replace with your browser cookies for the 'Cookie' config in `resource/sample_config.json` (maybe not required).  
- To see a full list arguments, check `python.exe ./main.py -h`