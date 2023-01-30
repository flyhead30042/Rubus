# 快速安裝

## 所需環境
* Windows
  * 安裝 WSL2， 安裝說明: https://docs.microsoft.com/zh-tw/windows/wsl/install-win10
  * 安裝 Docker Desktop for Windows，安裝說明: https://docs.docker.com/docker-for-windows/install/ (在Docker Desktop安裝後可略過Tutorial)

## 安裝步驟
* 下載部屬檔 docker-compose.yml 至任意目錄下，比如 C:\Users\<USER_NAME>\AppData\local\Rubus
  * Go to https://github.com/flyhead30042/Rubus
  * Click "docker-compose.yml" to view the contents within the GitHub UI.
  * In the top right, right click the **Raw** button.
  * Save as...
  
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
* 執行下列指令確定 flyhead/rubus images 正確下載，記得要確認 Tag 中的版本編號為最新的版本 (flyhead/rubus:2023.0.2)
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
* 打開瀏覽器，開啟下列網址
```commandline
http://localhost:8501
```

# Change Log
* Build: flyhead/rubus:2023.0.2
  * app
    * Import README.md
  * gpx:
    * Show TWD97 Grid
  * Management
    * New Function
    * Remove the stored gpx files
  * Others
    * Two services in docker-compose.yml for development env. and service env.
    * Use docker volumes for service env. and loca drive for development respectively 
    * Simplify installation steps that no need of .env and local folder

* Build: flyhead/rubus:2023.0.1
  * The first build for preview
  * app
    * Build No
  * gpx
    * Upload gpx files
    * Store and loaded the uploaded files
    * Show track and waypoint on selected map
    * Show the info and chart of track log
    * Select maps
    * Full screen mode
    * Measure distance
  * dual
    * Show the maps side by side
    * Select maps
    

# Backlog
* Setup function
  * Tile layers management: list, add, modify and delete tile resources in resource.yaml
* Maybe slim the image size?  
* More insight about track points
  * Time difference
  * Speed
* Export map
  * 5x7 cells with 4cm length for A4 size