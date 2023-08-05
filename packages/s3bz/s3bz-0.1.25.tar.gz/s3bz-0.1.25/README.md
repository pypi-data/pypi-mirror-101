# S3Bz
> save and load dictionary to s3 using bz compression


full docs here https://thanakijwanavit.github.io/s3bz/

## Install

`pip install s3bz`

## How to use

### Create a bucket and make sure that it has transfer acceleration enabled
#### create a buket
`aws s3 mb s3://<bucketname>`
#### put transfer acceleration
`aws s3api put-bucket-accelerate-configuration --bucket <bucketname> --accelerate-configuration Status=Enabled`

First, import the s3 module

## import package

```
from importlib import reload
from s3bz.s3bz import S3
```

### set up dummy data

## BZ2 compression

### save object using bz2 compression

```
result = S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True)
print(('failed', 'success')[result])
```

    success


### load object with bz2 compression

```
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result[0])
```

    {'ib_prcode': '23238', 'ib_brcode': '1015', 'ib_cf_qty': '703', 'new_ib_vs_stock_cv': '768'}


## other compressions
Zl : zlib compression with json string encoding
pklzl : zlib compression with pickle encoding

```
print(bucket)
%time S3.saveZl(key,sampleDict,bucket)
%time S3.loadZl(key,bucket)
%time S3.savePklZl(key,sampleDict,bucket)
%time result =S3.loadPklZl(key,bucket)
```

    pybz-test
    CPU times: user 23.9 ms, sys: 559 µs, total: 24.5 ms
    Wall time: 155 ms
    CPU times: user 28.3 ms, sys: 3.04 ms, total: 31.4 ms
    Wall time: 154 ms
    CPU times: user 21.6 ms, sys: 228 µs, total: 21.9 ms
    Wall time: 151 ms
    CPU times: user 31.6 ms, sys: 0 ns, total: 31.6 ms
    Wall time: 114 ms


## Bring your own compressor and encoder

```
import gzip, json
compressor=lambda x: gzip.compress(x)
encoder=lambda x: json.dumps(x).encode()
decompressor=lambda x: gzip.decompress(x)
decoder=lambda x: json.loads(x.decode())

%time S3.generalSave(key, sampleDict, bucket = bucket, compressor=compressor, encoder=encoder )
%time result = S3.generalLoad(key, bucket , decompressor=decompressor, decoder=decoder)
assert result == sampleDict, 'not the same as sample dict'
```

    CPU times: user 31 ms, sys: 0 ns, total: 31 ms
    Wall time: 155 ms
    CPU times: user 32.5 ms, sys: 51 µs, total: 32.5 ms
    Wall time: 115 ms


## check if an object exist

```
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = True)
print(('doesnt exist', 'exist')[result])
```

    exist


## presign download object

```
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

    https://pybz-test.s3-accelerate.amazonaws.com/test.dict?AWSAccessKeyId=AKIAVX4Z5TKDSNNNULGB&Signature=BR8Laz3uvkNKGh%2FBZ8x7IhRE3OU%3D&Expires=1616667887


### download using signed link

```
from s3bz.s3bz import Requests
result = Requests.getContentFromUrl(url)
```

## File operations

### save without compression

```
inputPath = '/tmp/tmpFile.txt'
key = 'tmpFile'
downloadPath = '/tmp/downloadTmpFile.txt'
with open(inputPath , 'w')as f:
  f.write('hello world')
```

```
S3.saveFile(key =key ,path = inputPath,bucket = bucket)
##test
S3.exist(key,bucket)
```




    True



### load without compression

```
S3.loadFile(key= key , path = downloadPath, bucket = bucket)
```

```
##test
with open(downloadPath, 'r') as f:
  print(f.read())
```

    hello world


### delete

```
result = S3.deleteFile(key, bucket)
## test
S3.exist(key,bucket)
```




    False



## save and load pandas dataframe

```
### please install in pandas, 
### this is not include in the requirements to minimize the size impact
import pandas as pd
df = pd.DataFrame({'test':[1,2,3,4,5],'test2':[2,3,4,5,6]})
S3.saveDataFrame(bucket,key,df)
S3.loadDataFrame(bucket,key)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>test</th>
      <th>test2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>3</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>4</td>
      <td>5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>5</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



# presign post with conditions

```
from s3bz.s3bz import ExtraArgs, S3
```

```
bucket = 'pybz-test'
key = 'test.dict'
fields = {**ExtraArgs.jpeg}
S3.presignUpload(bucket, key, fields=fields)
```




    {'url': 'https://pybz-test.s3-accelerate.amazonaws.com/',
     'fields': {'Content-Type': 'image/jpeg',
      'key': 'test.dict',
      'AWSAccessKeyId': 'AKIAVX4Z5TKDSNNNULGB',
      'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjEtMDMtMjVUMTA6MjQ6NTJaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAicHliei10ZXN0In0sIHsia2V5IjogInRlc3QuZGljdCJ9XX0=',
      'signature': 'hwC8kIjmjNPU0KT3BE54/TUQ/7w='}}


