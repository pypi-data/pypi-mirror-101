'''
Description: 清理数据集处理fps，将相同的人从n_samples.json中移除，并放入p_samples.json
version: 
Author: TianyuYuan
Date: 2021-02-26 14:40:31
LastEditors: TianyuYuan
LastEditTime: 2021-04-06 22:32:35
'''
import json
import os

def total_request(data:dict) -> int:
    """统计data中有多少的request_images"""
    total = 0
    for sample in data['images']:
        total += len(sample['request_images'])
    return total

def get_n_img2sample(n_data:dict) -> dict:
    """从n_data中获得request名和sample的关系"""
    img2sample = {}
    for sample in n_data['images']:
        if len(sample['request_images']) == 0:
            continue
        img_name = sample['request_images'][0].split('/')[-1]
        img2sample[img_name] = sample
    return img2sample

def get_p_ids2index(p_data:dict) -> dict:
    """从p_data中获得register和index的关系，方便后续用index直接修改p_data"""
    index = 0
    register_index = {}
    for sample in p_data['images']:
        register_ids = sample['ids'][0]
        register_index[register_ids] = index
        index += 1
    return register_index

def fp_request2register(fps_path:str,group_id:str) -> list:
    '''
    Description: read the rqst & register need to be del and mv
    - param fps_path & group_name(can be find in n_samples)
    - param group_id
    - return a list fp_rqst_register = [[rqst1,register1],[rqst2,register2],...]
    '''    
    fps_list = os.listdir(fps_path)
    if '.DS_Store' in fps_list:
        fps_list.remove('.DS_Store')
    fp_rqst_register = []
    for score_file in fps_list:
        rqst_and_register = os.listdir(os.path.join(fps_path,score_file)) 
        # remove the '00-' or '.jpg'
        rqst = ''
        register = ''
        for imgs in rqst_and_register:
            if imgs.startswith("00-"):
                rqst = imgs[3:]
            elif imgs.startswith(group_id):
                register = imgs.split('.jpg')[0]
        if rqst!='' and register!='':
            fp_rqst_register.append([rqst,register])
    return fp_rqst_register

def add_n_to_p(n_img2sample:dict,p_ids2index:dict,request_and_register:list,p_data:dict) -> dict:
    """将request信息加入p_samples.json中的sample"""
    for pair in request_and_register:
        img = pair[0]
        request_path = n_img2sample[img]['request_images'][0]
        ids = pair[1]
        index = p_ids2index[ids]
        p_data['images'][index]['request_images'].append(request_path)
    return p_data

def remove_request_in_n(n_data:dict,n_img2sample:dict,request_and_register:list) -> dict:
    """将request 的 sample 从 n_samples.json 中移除"""
    for pair in request_and_register:
        img = pair[0]
        sample = n_img2sample[img]
        n_data['images'].remove(sample)
    return n_data

def deal_with_fps(p_path,n_path,fps_path,group_id):
    """### 清理badcase中的fps
    - p_path: the path of p_samples.json
    - n_path: the path of n_samples.json
    - fps_path: the path of fps/
    - group_id: could be found in p_samples.json
    """
    with open(p_path, 'r') as f:
        p_data = json.load(f)
    with open(n_path, 'r') as f:
        n_data = json.load(f)
    print("p has request_images: ",total_request(p_data))
    print("n has samples: ",len(n_data['images']))

    # 从n_data中获得request名和sample的关系
    n_img2sample = get_n_img2sample(n_data)
    # 从p_data中获得register_ids和index的关系，方便后续用index直接修改p_data
    p_ids2index = get_p_ids2index(p_data)
    # 从fps文件中读取成对的request（00-开头，from n_samples）和register（from p_samples）
    request_and_register = fp_request2register(fps_path,group_id)
    print("Pairs need to be processed: ",len(request_and_register))

    # 将request信息加入p_samples.json中的sample
    new_p_data = add_n_to_p(n_img2sample,p_ids2index,request_and_register,p_data)
    # 将request 的 sample 从 n_samples.json 中移除
    new_n_data = remove_request_in_n(n_data,n_img2sample,request_and_register)

    # Report
    print("new p has request_images: ",total_request(new_p_data))
    print("new n has samples: ",len(new_n_data['images']))

    with open('new_p_samples.json', 'w') as f:
        json.dump(new_p_data, f, indent=4)
    with open('new_n_samples.json', 'w') as f:
        json.dump(new_n_data, f, indent=4)

def main():
    # p_path = sys.argv[1]
    # n_path = sys.argv[2]
    # fps_path = sys.argv[3]
    # group_id = sys.argv[4]

    p_path = './p_samples.json'
    n_path = './n_samples.json'
    fps_path = './fps'
    group_id = 'airport_check_did_1209_union'
    deal_with_fps(p_path,n_path,fps_path,group_id)

if __name__ == '__main__':
    main()