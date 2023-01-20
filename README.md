# 快速安裝

## 所需環境
* 安裝 WSL2， 安裝說明: https://docs.microsoft.com/zh-tw/windows/wsl/install-win10
* 安裝 Docker Desktop for Windows，安裝說明: https://docs.docker.com/docker-for-windows/install/ (在Docker Desktop安裝後可略過Tutorial)

## 安裝步驟
* 建立目錄 Rubus 目錄
  * 目錄位置可以指向任意本機上喜好路徑
```commandline
$ cd C:\Users\<USER_NAME>\AppData\Local
$ mkdir Rubus
$ cd Rubus
$ mkdir tracklogs
$ mkdir configurations
```

* 下載部屬檔 https://github.com/flyhead30042/Rubus/blob/master/docker-compose.yml 至 Rubus 目錄下
* 建立環境變數檔 .env，
* 複製下列內容至 .env 中
  * 注意!!! RUBUS_ROOT_DIR 環境變數必須與前一步驟中的 Rubus 目錄相同
  * RUBUS_HOST_PORT 可以設定本機上任意未使用port
```commandline
RUBUS_ROOT_DIR=C:\Users\<USER_NAME>\AppData\Local\Rubus
RUBUS_TRACKLOGS_DIR=${RUBUS_ROOT_DIR}/tracklogs
RUBUS_CONFIGURATIONS_DIR=${RUBUS_ROOT_DIR}/configurations
RUBUS_HOST_PORT=8501
```


* 切換到 Rubus 目錄下
```commandline
$ cd C:\Users\<USER_NAME>\AppData\local\Rubus
```

* 執行下列指令先移除舊 container
```commandline
$ docker-compose -f docker-compose.yml down
```
* 執行下列指令進行部屬，第一次執行需下載 image ，會需要較久的時間
```commandline
$ docker-compose -f docker-compose.yml up -d rubus
```
* 執行下列指令確定 flyhead/rubus images 正確下載，記得要確認 Tag 中的版本編號為最新的版本
```commandline
$ docker images --all

REPOSITORY                    TAG                IMAGE ID       CREATED         SIZE
flyhead/rubus                 2023.0.1           b5fa974b333a   3 hours ago     657MB
```
* 執行下列指令確定 rubus container 正確執行
```commandline
$ docker ps --all

CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                    NAMES
cf358afee478   flyhead/rubus:2023.0.1   "streamlit run app.py"   4 minutes ago   Up 4 minutes   0.0.0.0:8501->8501/tcp   rubus-rubus-1
```

# Change Log
* Build: flyhead/rubus:2023.0.1
  * The first build for preview

# Backlog
* Setup function
  * Tile layers management: list, add, modify and delete tile resources in resource.yaml  
  * Stored gpx file management: list and delete gpx files under tracklogs
* Improve installation guide
* Maybe slim the image size?  
* More insight about track points
  * Time difference
  * Speed
* TWD 97 Grid
* Export map
  * 5x7 cells with 4cm length for A4 size