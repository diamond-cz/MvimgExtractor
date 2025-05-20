import os

def show_info():
    """在线生成ASCII码艺术字__https://www.bejson.com/text/ascii_art/"""
    print(f"""
-------------------------------------------------------------------------------------------------------.
|     ______          _                           _     __  __           _                            |
|    |  ____|        | |                         | |   |  \/  |         (_)                           |
|    | |__    __  __ | |_   _ __    __ _    ___  | |_  | \  / | __   __  _   _ __ ___     __ _        |
|    |  __|   \ \/ / | __| | '__|  / _` |  / __| | __| | |\/| | \ \ / / | | | '_ ` _ \   / _` |       |
|    | |____   >  <  | |_  | |    | (_| | | (__  | |_  | |  | |  \ V /  | | | | | | | | | (_| |       |
|    |______| /_/\_\  \__| |_|     \__,_|  \___|  \__| |_|  |_|   \_/   |_| |_| |_| |_|  \__, |       |
|                                                                                        __/ |        |
|                                                                                        |___/        |       
-------------------------------- extract_mvimg 抽取实况图程序 -----------------------------------------.
[提示1]将extract_mvimg.exe放在实况图同级文件夹下,会自动检索并抽取名称形式为：".jpg"或".heic"结尾 的实况图。
[提示2]抽取成功后的图片+视频会存放在同级文件夹photos_extracted和videos_extracted中         
[extract_mvimg.exe]抽取实况照片中的图+视频任务正在执行中......""")


def locate_video_google(data):
    # 小米手机用的是ftypmp42 
    # position - 4 表示MP4数据前有4字节的大小信息要去掉
    signatures = [b'ftypmp42', b'ftypisom', b'ftypiso2']
    for signature in signatures:
        position = data.find(signature)
        if position != -1:
            return position - 4
    return -1


def locate_video_samsumg(data):
    signature = b"MotionPhoto_Data"
    position = data.find(signature)
    if position != -1:
        return position + len(signature)
    return -1


def extract_mvimg(srcfile, photo_dir, video_dir):
    basefile = os.path.splitext(os.path.basename(srcfile))[0]
    offset = None 

    with open(srcfile, 'rb') as file:
        data = file.read() 
        offset = locate_video_google(data) or locate_video_samsumg(data)
        
    if offset != -1:
        # 保存图片部分
        os.makedirs(photo_dir, exist_ok=True)
        with open(os.path.join(photo_dir, f"{basefile}.jpg"), 'wb') as jpgfile:
            jpgfile.write(data[:offset])

        # 保存视频部分
        os.makedirs(video_dir, exist_ok=True)
        with open(os.path.join(video_dir, f"{basefile}.mp4"), 'wb') as mp4file:
            mp4file.write(data[offset:])
    else:
        print(f"Can't find video data in {srcfile}; skipping...")



# 批量抽取
def process_directory(srcdir, photo_dir, video_dir):
    try:
        # files = [f for f in os.listdir(srcdir) if f.startswith("MVIMG_") and f.endswith(".jpg")]
        files = [f for f in os.listdir(srcdir) if f.endswith(".jpg")]
        for filename in files:
            srcfile = os.path.join(srcdir, filename)
            # 调用抽取函数
            extract_mvimg(srcfile, photo_dir, video_dir)
        return len(files)
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
        

if __name__ == "__main__":
    """ 将安卓的jpg实况图转化为 jpg + mp4 """
    base_path = os.path.dirname(os.path.abspath(__file__))
    srcdir = os.path.join(base_path, "pic")                    # 包含实况图的目录
    photo_dir = os.path.join(srcdir, "photos_extracted")    # 保存提取的图片的目录
    video_dir = os.path.join(srcdir, "videos_extracted")    # 保存提取的视频的目录
    
    show_info()

    status_code = process_directory(srcdir, photo_dir, video_dir)

    print(f"Sucess! 共处理{status_code}张实况图-v-")
    input("按 Enter 键退出...")  # 暂停黑窗口