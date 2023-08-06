# 清理6个月前大于100M的apk文件
find static/apk/ -type f -size +100M -mtime +120 -exec rm -rf {} \;
# 清理3天前的导出文件
find static/export/ -type f -mtime +3 -exec rm -rf {} \;
