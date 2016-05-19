#!/usr/bin/env bash

function extracttext(){
    # 提取出内容字段
    echo "提取出内容字段"
    sed -n -e  "/^<content>=/p"  $1 > $2
}


function etl(){

    echo "开始清洗工作-ETL."
    # 生成一个临时文件名
    temp=$(mktemp -u tmp.XXXXXXXX)

    # 删除内容头
    echo "删除内容头"
    sed -e "s/^<content>=.*首页分类.*查看我的收藏有用+1 //g"  $1  > ${temp}
    mv ${temp} $1

    # 删除内容尾
    echo "删除内容尾"
    sed -e "s/新手上路.*$//g"  $1  > ${temp}
    mv ${temp} $1

}

files=$(ls --color=auto data*)
echo ${files}

for f in ${files};do
    newf="${f%_content.txt}.txt"

    echo "处理文件$f, 输出文件$newf."
    extracttext "${f}" "${newf}"
    etl "${newf}"
done
