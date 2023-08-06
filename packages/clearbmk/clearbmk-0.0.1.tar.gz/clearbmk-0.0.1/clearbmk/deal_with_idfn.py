'''
Description: 将00-开头的图片移到正确的sample中
version: 
Author: TianyuYuan
Date: 2021-02-26 16:20:40
LastEditors: TianyuYuan
LastEditTime: 2021-04-06 22:37:41
'''
import os
import json

def get_img2index(data:dict) -> dict:
    """从data中获得request名和index的关系"""
    img2index= {}
    index = 0
    for sample in data['images']:
        if len(sample['request_images']) == 0:
            pass
        else:
            for img_path in sample['request_images']:
                img_name = img_path.split('/')[-1]
                img2index[img_name] = index
        index += 1
    return img2index

def get_ids2index(data:dict) -> dict:
    """从p_data中获得register和index的关系，方便后续用index直接修改p_data"""
    index = 0
    register_index = {}
    for sample in data['images']:
        register_ids = sample['ids'][0]
        register_index[register_ids] = index
        index += 1
    return register_index

def idfn_request2register(idfn_path:str,group_id:str) -> list:
    '''
    Description: read the rqst & register need to be del and mv
    --param idfn_path & group_name(can be find in n_samples)
    --return a list idfn_rqst_register = [[rqst1,register1],[rqst2,register2],...]
    '''    
    idfn_list = os.listdir(idfn_path)
    if '.DS_Store' in idfn_list:
        idfn_list.remove('.DS_Store')
    idfn_rqst_register = []
    for score_file in idfn_list:
        rqst_and_register = os.listdir(os.path.join(idfn_path,score_file)) 
        # remove the '00-' or '.jpg'
        rqst = ''
        register = ''
        for imgs in rqst_and_register:
            if imgs.startswith("00-"):
                rqst = imgs[3:]
            elif imgs.startswith(group_id):
                register = imgs.split('.jpg')[0]
        if rqst!='' and register!='':
            idfn_rqst_register.append([rqst,register])
    return idfn_rqst_register

def idfn_process(img2index,ids2index,request_and_ids,p_data):
    count = 0
    for pair in request_and_ids:
        img = pair[0]
        ids = pair[1]
        src_index = img2index[img]
        dest_index = ids2index[ids] 
        request_list = p_data['images'][src_index]["request_images"]
        for img_path in request_list:
            if img in img_path:
                tmp = img_path
                p_data['images'][src_index]["request_images"].remove(tmp)
                count += 1
                break
        p_data['images'][dest_index]["request_images"].append(tmp)
    print("实际操作次数：", count)
    return p_data

def deal_with_idfn(p_path,idfn_path,group_id):
    """清理数据集badcase中的idfn
    - p_path: the path of p_samples.json
    - idfn_path: the path of idfn/
    - group_id: could be found in p_samples.json
    """
    with open(p_path, 'r') as f:
        p_data = json.load(f)
    img2index = get_img2index(p_data)
    ids2index = get_ids2index(p_data)
    request_and_ids = idfn_request2register(idfn_path,group_id)
    print('所需操作次数：',len(request_and_ids))
    new_p_data = idfn_process(img2index,ids2index,request_and_ids,p_data)
    with open('new_p_samples.json','w') as fp:
        json.dump(new_p_data,fp,indent=4)

def main():
    p_path = 'p_samples.json'
    idfn_path = './id_fns'
    group_id = 'airport_check_did_1209_union'
    deal_with_idfn(p_path,idfn_path,group_id)

if __name__ == '__main__':
    main()
