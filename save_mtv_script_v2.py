#!/usr/bin/env python3
"""
将MTV镜头脚本保存到Excel文件
"""

import pandas as pd
import os
import json
from datetime import datetime

def save_mtv_script_to_excel():
    """将MTV镜头脚本保存到Excel文件"""
    
    # 镜头数据
    mtv_data = {
        "sections": [
            {
                "镜头序号": 1,
                "镜头描述": "高空俯拍暮色城市，灯光如星河点点。雨丝在灯光下形成金色光斑，镜头缓慢向下拉近至街道的水洼，水面映出'城市足印'四个字的霓虹投影。",
                "景别": "全景",
                "角度": "俯视",
                "运镜方式": "轨道缓慢拉近 → 稳定器轻推",
                "对应台词/时间点": "00:00‑00:07 前奏",
                "备注": "暖金调色 + 轻微雾化；加入0.4s雨滴特写作为呼吸镜头。"
            },
            {
                "镜头序号": 2,
                "镜头描述": "水面特写，雨滴落下激起涟漪，涟漪中心出现一枚鞋底的倒影，随即镜头下滑至鞋底，金色光环在鞋底边缘轻轻闪烁。",
                "景别": "特写",
                "角度": "正面",
                "运镜方式": "手持慢摇 → 稳定器下推",
                "对应台词/时间点": "00:07‑00:12 留意街灯的金光",
                "备注": "金色光环CG，颜色从 #D4A35F 渐变至 #F2C1C1（柔粉）保持自然光感。"
            },
            {
                "镜头序号": 3,
                "镜头描述": "男女主角在雨中相遇，抬眉轻挑，眼中映出街灯的金色光辉。两人微笑，雨滴在背景灯光中轻舞。",
                "景别": "中景",
                "角度": "正面",
                "运镜方式": "稳拍 → 轻微横移",
                "对应台词/时间点": "00:12‑00:18 留意足印交错",
                "备注": "保持暖金色温度，避免眉头皱起；0.3s霓虹灯闪烁作呼吸。"
            },
            {
                "镜头序号": 4,
                "镜头描述": "俯视足印，金光随步轻拂。每一步留下微微发光的足印，CG光环在足尖轻轻闪烁，形成连绵的光轨。",
                "景别": "特写",
                "角度": "俯视",
                "运镜方式": "慢速平移 → 稳定器轻推",
                "对应台词/时间点": "00:18‑00:24 留意足印交错，光环在脚尖闪烁",
                "备注": "粒子效果金粉 → 柔粉渐变；0.5s雨水镜头作过渡。"
            },
            {
                "镜头序号": 5,
                "镜头描述": "长曝光车灯光轨，车辆驶过形成金色丝带般的光轨，宛如星河划过夜空。",
                "景别": "全景",
                "角度": "平视",
                "运镜方式": "三脚架固定 + ND滤镜 1.5s 曝光",
                "对应台词/时间点": "00:24‑00:30 车流如星河，光轨在夜空划过",
                "备注": "光轨随音乐节拍轻微亮度脉冲（Audio‑Driven Brightness）。"
            },
            {
                "镜头序号": 6,
                "镜头描述": "呼吸镜头——雨滴落在霓虹招牌上，水珠滚动形成金色光环，随后画面渐变为蓝色地铁站灯光。",
                "景别": "特写",
                "角度": "俯视",
                "运镜方式": "静止 → 渐变淡入",
                "对应台词/时间点": "00:30‑00:38 相遇的那一刻，雨滴在灯光里轻舞，映出你的笑颜",
                "备注": "蓝调仅作0.3‑0.5s过渡，随后渐入暖金。"
            },
            {
                "镜头序号": 7,
                "镜头描述": "地铁平台全景，冷蓝灯光柔和。镜头左侧出现金色咖啡店招牌灯光逐渐向右扩散，画面颜色从蓝转金。",
                "景别": "全景",
                "角度": "平视",
                "运镜方式": "推拉 + 渐变滤镜",
                "对应台词/时间点": "00:38‑00:45 地铁灯光柔和，咖啡香在空气里漂浮",
                "备注": "使用现场灯光渐变滤镜，确保色温自然过渡。"
            },
            {
                "镜头序号": 8,
                "镜头描述": "咖啡店内部，两人坐在靠窗位置，窗外雨滴在灯光中轻舞。咖啡蒸汽上升，形成柔粉色的心形雾纹，随即淡化为金粉点点。",
                "景别": "中景",
                "角度": "斜侧",
                "运镜方式": "稳拍 → 轻微推拉",
                "对应台词/时间点": "01:00‑01:07 相遇的那一刻，雨滴在灯光里轻舞，映出你的笑颜",
                "备注": "金粉→柔粉渐变，保持低饱和度；0.3s咖啡杯蒸汽特写作呼吸。"
            },
            {
                "镜头序号": 9,
                "镜头描述": "特写两人的手指轻触，指尖点燃微光，金色光点在指尖跳动，随后随手势向上飘散成细小光粒。",
                "景别": "特写",
                "角度": "正面",
                "运镜方式": "手持微推",
                "对应台词/时间点": "01:07‑01:12 眉梢轻挑，眼里映出星光",
                "备注": "光粒与现场灯光方向一致，保持暖金调。"
            },
            {
                "镜头序号": 10,
                "镜头描述": "俯视足印再次出现，金光随步轻拂，足印中心缓缓被金粉覆盖，形成柔粉心形足印。",
                "景别": "特写",
                "角度": "俯视",
                "运镜方式": "慢速平移 → 稳定器轻推",
                "对应台词/时间点": "01:12‑01:18 足印交错，金光随步轻拂，指尖点燃微光",
                "备注": "粒子系统颜色曲线 #D4A35F → #F2C1C1，0.5s呼吸雨滴镜头在足印出现前。"
            },
            {
                "镜头序号": 11,
                "镜头描述": "长曝光车灯再次出现，这次灯轨在空中形成金色螺旋，缓缓收束至两人脚下的足印。",
                "景别": "全景",
                "角度": "低角度",
                "运镜方式": "三脚架固定 + ND滤镜 1‑2s 曝光",
                "对应台词/时间点": "01:18‑01:24 车流如星河，光轨在夜空划过",
                "备注": "光轨随音乐节拍轻微闪烁（Audio‑Driven Brightness）。"
            },
            {
                "镜头序号": 12,
                "镜头描述": "呼吸镜头——霓虹灯牌从蓝色渐变为金色，灯光在玻璃上形成柔和的光晕，随后切入下一场景。",
                "景别": "特写",
                "角度": "斜侧",
                "运镜方式": "静止 → 渐变淡入",
                "对应台词/时间点": "01:24‑01:28 过渡",
                "备注": "仅0.4‑0.5秒，保持色调连贯。"
            },
            {
                "镜头序号": 13,
                "镜头描述": "两人在咖啡店门口并肩走出，街灯金光洒在身后，足印在路面上留下金色光环，CG光环随步伐轻轻闪烁。",
                "景别": "中景",
                "角度": "斜侧",
                "运镜方式": "手持稳拍 → 轻推",
                "对应台词/时间点": "01:30‑01:38 副歌第一遍",
                "备注": "加入重复的歌词钩子：'足印在灯火里，写下我们的光年'。"
            },
            {
                "镜头序号": 14,
                "镜头描述": "特写足印，金粉缓缓覆盖，颜色自然过渡至柔粉，形成柔软的心形足印。",
                "景别": "特写",
                "角度": "俯视",
                "运镜方式": "微推 → 稳定器轻摇",
                "对应台词/时间点": "01:38‑01:45 金粉缓缓覆上足印，化作柔粉心形",
                "备注": "粒子颜色曲线平滑，避免突兀。"
            },
            {
                "镜头序号": 15,
                "镜头描述": "夜空慢动作延时拍摄，两束自然烟火轨迹交叉形成∞形，颜色保持低饱和蓝紫，光点逐渐淡出金粉色调。",
                "景别": "全景",
                "角度": "仰视",
                "运镜方式": "固定拍摄 → 后期慢速回放",
                "对应台词/时间点": "02:00‑02:07 烟火缓缓相拥，化作星光∞",
                "备注": "使用真实烟火避免硬CG，后期轻度金粉叠加。"
            },
            {
                "镜头序号": 16,
                "镜头描述": "呼吸镜头——雨滴在街灯玻璃上滚动，光斑随之扩散，随后切入下一段歌词。",
                "景别": "特写",
                "角度": "俯视",
                "运镜方式": "静止 → 渐变淡出",
                "对应台词/时间点": "02:07‑02:10 过渡",
                "备注": "0.4秒，保持画面呼吸。"
            },
            {
                "镜头序号": 17,
                "镜头描述": "两人站在桥头，背对镜头，城市灯光在背后形成金色光环，足印在桥面上闪耀，随风轻轻晃动。",
                "景别": "全景",
                "角度": "背面",
                "运镜方式": "滑轨平移 → 稳定器轻推",
                "对应台词/时间点": "02:12‑02:18 足印在灯火里，写下我们的光年（副歌重复）",
                "备注": "暖金调色，加入轻微风吹树叶的声音作为环境层。"
            },
            {
                "镜头序号": 18,
                "镜头描述": "特写两人的眼神交汇，眼中映出城市灯光的金色倒影，微笑轻启。",
                "景别": "特写",
                "角度": "正面",
                "运镜方式": "手持稳拍 → 轻微推拉",
                "对应台词/时间点": "02:18‑02:24 眉梢轻挑，眼里映出星光",
                "备注": "保持暖金色温度，避免任何皱眉。"
            },
            {
                "镜头序号": 19,
                "镜头描述": "足印俯视慢动作回放，金光沿足迹流动，光环在每一步的脚尖轻轻闪烁，形成节奏感的视觉脉冲。",
                "景别": "特写",
                "角度": "俯视",
                "运镜方式": "慢速平移 → 稳定器轻推",
                "对应台词/时间点": "02:30‑02:38 副歌第二遍",
                "备注": "每次出现歌词'足印在灯火里'时，CG光环同步轻微放大（Audio‑Driven Fusion）。"
            },
            {
                "镜头序号": 20,
                "镜头描述": "长曝光车灯再次出现，但这次灯光被调成金色丝带，缓缓在街道上划过，形成柔和的光轨，随音乐节拍轻微跳动。",
                "景别": "全景",
                "角度": "低角度",
                "运镜方式": "三脚架固定 + ND滤镜 1.5s 曝光",
                "对应台词/时间点": "02:38‑02:45 车流如星河，光轨在夜空划过",
                "备注": "光轨颜色保持在 #D4A35F 范围，避免蓝色突变。"
            },
            {
                "镜头序号": 21,
                "镜头描述": "呼吸镜头——霓虹灯牌灯光从蓝色渐变为金色，光晕在画面左侧扩散，随后切入咖啡店内部。",
                "景别": "特写",
                "角度": "斜侧",
                "运镜方式": "静止 → 渐变淡入",
                "对应台词/时间点": "02:45‑02:48 过渡",
                "备注": "0.4秒，确保色调平滑过渡。"
            },
            {
                "镜头序号": 22,
                "镜头描述": "咖啡店内部，两人相视而笑，咖啡蒸汽上升形成柔粉色心形雾纹，随即淡出为金粉轻轻飘散。",
                "景别": "中景",
                "角度": "正面",
                "运镜方式": "手持稳拍 → 轻推",
                "对应台词/时间点": "02:48‑02:55 金粉缓缓覆上足印，化作柔粉心形",
                "备注": "粒子颜色曲线金→粉，光晕软化，保持自然灯光投射。"
            },
            {
                "镜头序号": 23,
                "镜头描述": "特写两人的手指轻触，指尖点燃微光，光点在指间跳动，随后随手势向上漂散成细小星光。",
                "景别": "特写",
                "角度": "正面",
                "运镜方式": "手持微推",
                "对应台词/时间点": "03:00‑03:07 指尖点燃微光，星光随步舞动",
                "备注": "光点与现场灯光方向一致，0.3s雨滴特写作呼吸。"
            },
            {
                "镜头序号": 24,
                "镜头描述": "全景回到城市街道，足印在灯火中闪耀，金色光环在每一步上持续闪烁，镜头缓慢拉远，城市灯光与足印交织成一幅温暖的画卷。",
                "景别": "全景",
                "角度": "平视",
                "运镜方式": "稳拍 → 轨道缓慢拉远",
                "对应台词/时间点": "03:07‑03:14 足印在灯火里，写下我们的光年（副歌重复）",
                "备注": "统一暖金+柔粉调色，加入0.4s雨滴镜头作呼吸。"
            },
            {
                "镜头序号": 25,
                "镜头描述": "夜空慢动作延时拍摄，两束自然烟火轨迹自然相交形成∞形，光点低饱和蓝紫，随后淡出为金粉心形足印的余晖。",
                "景别": "全景",
                "角度": "仰视",
                "运镜方式": "固定拍摄 → 后期慢速回放",
                "对应台词/时间点": "03:14‑03:21 结尾/尾奏",
                "备注": "保持颜色从蓝紫渐变至金粉，避免突变；0.5s雨滴特写作收尾呼吸。"
            },
            {
                "镜头序号": 26,
                "镜头描述": "黑屏淡出，画面中央出现金色足印的轮廓，缓慢淡出至全黑，留下余音与城市的灯光回响。",
                "景别": "特写",
                "角度": "正面",
                "运镜方式": "静止 → 渐隐",
                "对应台词/时间点": "03:21 尾奏结束",
                "备注": "音频淡出时同步最后一次亮度脉冲；保持整体暖金调性收尾。"
            }
        ]
    }
    
    try:
        print("开始创建MTV镜头脚本Excel文件...")
        
        # 提取镜头数据
        shots = mtv_data["sections"]
        
        # 创建DataFrame
        df = pd.DataFrame(shots)
        
        print(f"DataFrame创建成功，包含{len(df)}个镜头")
        print("列名:", list(df.columns))
        
        # 保存为Excel文件
        output_file = "mtv_city_xu.xlsx"
        print(f"正在保存到文件: {output_file}")
        
        # 使用openpyxl引擎保存Excel文件，并设置格式
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 保存主数据到第一个工作表
            df.to_excel(writer, sheet_name='镜头脚本', index=False)
            
            # 获取工作表对象以调整列宽
            worksheet = writer.sheets['镜头脚本']
            
            # 设置列宽
            column_widths = {
                'A': 8,   # 镜头序号
                'B': 50,  # 镜头描述
                'C': 10,  # 景别
                'D': 10,  # 角度
                'E': 25,  # 运镜方式
                'F': 20,  # 对应台词/时间点
                'G': 40   # 备注
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # 创建统计摘要工作表
            summary_data = {
                '统计项目': [
                    '总镜头数',
                    '全景镜头数',
                    '中景镜头数', 
                    '特写镜头数',
                    '创建时间',
                    '文件名称'
                ],
                '数值': [
                    len(df),
                    len(df[df['景别'] == '全景']),
                    len(df[df['景别'] == '中景']),
                    len(df[df['景别'] == '特写']),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    output_file
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='统计摘要', index=False)
        
        print(f"MTV镜头脚本Excel文件已创建: {output_file}")
        print(f"包含{len(df)}个镜头")
        
        # 验证文件是否创建成功
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"文件创建成功，大小: {file_size} bytes")
            
            # 显示一些统计信息
            print("\n镜头统计:")
            print(f"- 全景镜头: {len(df[df['景别'] == '全景'])}个")
            print(f"- 中景镜头: {len(df[df['景别'] == '中景'])}个") 
            print(f"- 特写镜头: {len(df[df['景别'] == '特写'])}个")
            
            # 显示角度统计
            print("\n角度统计:")
            angle_counts = df['角度'].value_counts()
            for angle, count in angle_counts.items():
                print(f"- {angle}: {count}个")
                
        else:
            print("错误: 文件创建失败")
            return None
            
        return output_file
        
    except Exception as e:
        print(f"创建MTV镜头脚本Excel文件时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def save_graph_batch_to_excel(json_file: str, output_file: str = None) -> str:
    """
    从JSON文件读取镜头数据，生成包含指定列的Excel文件，用于批处理
    
    Args:
        json_file: 包含镜头数据的JSON文件路径
        output_file: 输出Excel文件路径，如果为None则自动生成
    
    Returns:
        str: 生成的Excel文件路径
    """
    try:
        print("开始生成批处理Excel文件...")
        
        # 检查JSON文件是否存在
        if not os.path.exists(json_file):
            print(f"错误: JSON文件不存在: {json_file}")
            return None
        
        # 读取JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查数据结构
        if 'sections' not in data:
            print("错误: JSON文件中缺少 'sections' 字段")
            return None
        
        shots = data['sections']
        if not isinstance(shots, list):
            print("错误: 'sections' 字段应该是列表类型")
            return None
        
        # 如果没有指定输出文件，自动生成文件名
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            output_file = f"{base_name}_batch_{timestamp}.xlsx"
        
        # 创建DataFrame数据
        data_rows = []
        for index, shot in enumerate(shots):
            # 构建user_prompt内容
            user_prompt_parts = []
            
            # 添加镜头描述
            if '镜头描述' in shot:
                desc_shot = shot['镜头描述']
                # if '林远' in desc_shot:
                #     print('change male line:', index)
                #     desc_shot = desc_shot.replace('林远', '一名32岁的中国男人，身材精瘦健硕，中等身高，拥有一头浓密笔直的乌黑短发，纹理短发，因工作时习惯用手拨弄而常略显凌乱。椭圆形脸庞轮廓分明，颌线利落，高耸的颧骨，鼻梁笔直宽度适中，眉骨突出，深陷的杏仁形深褐色眼睛目光直视。肤色温暖浅棕，因常年户外活动，眼周显露细微风化痕迹')
                
                # if '苏晴' in desc_shot:
                #     print('change female line:', index)
                #     desc_shot = desc_shot.replace('苏晴', '一位28岁的中国女人，身材纤细优雅，身高中等，天生挺拔端庄。她留着一头笔直的乌黑长发，发际线整齐地中分，发尾顺滑利落地垂至肩头，泛着健康的光泽。脸型柔和的椭圆形，下颌线纤细精致，颧骨微微高耸。鼻梁笔直纤巧，眉宇间平滑无痕，两只圆润的暖棕色大眼间距匀称，常透着耐心专注的神情，搭配清透如瓷的浅色肌肤。')

                user_prompt_parts.append(f"{desc_shot}, ")
            
            # 添加景别
            if '景别' in shot:
                user_prompt_parts.append(f"{shot['景别']}, ")
            
            # 添加角度
            if '角度' in shot:
                user_prompt_parts.append(f"{shot['角度']}, ")
            
            # 添加运镜方式
            if '运镜方式' in shot:
                user_prompt_parts.append(f"{shot['运镜方式']}, ")
            
            # 添加备注
            if '备注' in shot:
                user_prompt_parts.append(f"{shot['备注']}, ")
            
            # 组合user_prompt
            user_prompt = " ".join(user_prompt_parts)
            
            # 创建行数据
            row_data = {
                'user_prompt': user_prompt,
                'generation_content': '',  # 空内容
                'reflection_advice': '',   # 空内容
                'user_feedback': ''        # 空内容
            }
            
            data_rows.append(row_data)
        
        # 创建DataFrame
        df = pd.DataFrame(data_rows)
        
        print(f"创建了{len(df)}行数据")
        
        # 保存为Excel文件
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 保存主数据
            df.to_excel(writer, sheet_name='Batch_Data', index=False)
            
            # 获取工作表对象以调整列宽
            worksheet = writer.sheets['Batch_Data']
            
            # 设置列宽
            column_widths = {
                'A': 80,  # user_prompt - 较宽以容纳长文本
                'B': 50,  # generation_content
                'C': 50,  # reflection_advice
                'D': 50   # user_feedback
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # 创建说明工作表
            instructions_data = {
                '列名': [
                    'user_prompt',
                    'generation_content', 
                    'reflection_advice',
                    'user_feedback'
                ],
                '说明': [
                    '用户输入的镜头信息，包含镜头序号、镜头描述、景别、角度、运镜方式、台词/时间点和备注',
                    'AI生成的内容（批处理后自动填充）',
                    'AI反思建议（批处理后自动填充）',
                    '用户反馈（需要手动填写）'
                ],
                '示例': [
                    '镜头序号：1，镜头描述：高空俯拍暮色城市，景别：全景，角度：俯视，运镜方式：轨道缓慢拉近',
                    'A wide aerial shot of a twilight cityscape...',
                    'The prompt effectively captures cinematic elements...',
                    '请增加更多关于雨滴特效的细节描述'
                ]
            }
            instructions_df = pd.DataFrame(instructions_data)
            instructions_df.to_excel(writer, sheet_name='使用说明', index=False)
            
            # 调整说明工作表的列宽
            instructions_worksheet = writer.sheets['使用说明']
            instructions_worksheet.column_dimensions['A'].width = 20
            instructions_worksheet.column_dimensions['B'].width = 60
            instructions_worksheet.column_dimensions['C'].width = 50
        
        print(f"批处理Excel文件已创建: {output_file}")
        print(f"包含{len(df)}行数据")
        
        # 验证文件是否创建成功
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"文件创建成功，大小: {file_size} bytes")
        else:
            print("错误: 文件创建失败")
            return None
            
        return output_file
        
    except Exception as e:
        print(f"生成批处理Excel文件时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import sys

    json_file = "mtv_script_gen.json"
    output_file = "mtv_graph_batch1018.xlsx"

    result = save_graph_batch_to_excel(json_file, output_file)
    if result:
        print(f"批处理Excel文件生成成功: {result}")
    else:
        print("批处理Excel文件生成失败")
    
    
