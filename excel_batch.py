#!/usr/bin/env python3
"""
Excel批处理脚本
从Excel文件加载数据，调用generation_graph_flow_v1进行批处理，
然后将结果保存到新的Excel文件中
"""

import pandas as pd
import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any
import traceback

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import generation_graph_flow_v1
from state import Graph_State
from logger import logger


class ExcelBatchProcessor:
    """Excel批处理器"""
    
    def __init__(self, input_file: str, prompt_file: str, output_file: str = None):
        """
        初始化批处理器
        
        Args:
            input_file: 输入Excel文件路径
            prompt_file: 包含prompt的JSON文件路径
            output_file: 输出Excel文件路径，如果为None则自动生成
        """
        self.input_file = input_file
        self.prompt_file = prompt_file
        if output_file is None:
            # 自动生成输出文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            self.output_file = f"{base_name}_processed_{timestamp}.xlsx"
        else:
            self.output_file = output_file
            
        self.df = None
        self.processed_count = 0
        self.error_count = 0
        self.generation_prompt = ""
        self.reflection_prompt = ""
    
    def load_prompts(self) -> bool:
        """
        从JSON文件加载prompt
        
        Returns:
            bool: 加载是否成功
        """
        try:
            logger.info(f"正在加载prompt文件: {self.prompt_file}")
            
            if not os.path.exists(self.prompt_file):
                logger.error(f"Prompt文件不存在: {self.prompt_file}")
                return False
            
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            # 检查必需的字段
            if 'generation_prompt' not in prompt_data:
                logger.error("JSON文件中缺少 'generation_prompt' 字段")
                return False
            
            if 'reflection_prompt' not in prompt_data:
                logger.error("JSON文件中缺少 'reflection_prompt' 字段")
                return False

            # if 'male_character' not in prompt_data:
            #     logger.error("JSON文件中缺少 'male_character' 字段")
            #     return False
            
            # if 'female_character' not in prompt_data:
            #     logger.error("JSON文件中缺少 'female_character' 字段")
            #     return False
            
            # 将列表转换为字符串
            if isinstance(prompt_data['generation_prompt'], list):
                self.generation_prompt = '\n'.join(prompt_data['generation_prompt'])
            else:
                self.generation_prompt = str(prompt_data['generation_prompt'])
            
            if isinstance(prompt_data['reflection_prompt'], list):
                self.reflection_prompt = '\n'.join(prompt_data['reflection_prompt'])
            else:
                self.reflection_prompt = str(prompt_data['reflection_prompt'])
            
            
            logger.info(f"成功加载prompt文件")
            logger.info(f"Generation prompt长度: {len(self.generation_prompt)}")
            logger.info(f"Reflection prompt长度: {len(self.reflection_prompt)}")
            
            return True
            
        except Exception as e:
            logger.error(f"加载prompt文件失败: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    def load_excel(self) -> bool:
        """
        从Excel或CSV文件加载数据
        
        Returns:
            bool: 加载是否成功
        """
        try:
            logger.info(f"正在加载文件: {self.input_file}")
            
            # 根据文件扩展名选择读取方法
            if self.input_file.lower().endswith('.csv'):
                self.df = pd.read_csv(self.input_file, encoding='utf-8')
            else:
                self.df = pd.read_excel(self.input_file)
            
            # 检查必需的列是否存在
            required_columns = [
                'user_prompt', 
                'generation_content', 
                'reflection_advice', 
                'user_feedback'
            ]
            
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                logger.error(f"Excel文件缺少必需的列: {missing_columns}")
                return False
                
            logger.info(f"成功加载文件，共{len(self.df)}行数据")
            logger.info(f"列名: {list(self.df.columns)}")
            
            return True
            
        except Exception as e:
            logger.error(f"加载文件失败: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    async def process_single_row(self, row_index: int, row: pd.Series) -> Dict[str, Any]:
        """
        处理单行数据
        
        Args:
            row_index: 行索引
            row: 行数据
            
        Returns:
            Dict: 处理结果
        """
        try:
            logger.info(f"正在处理第{row_index + 1}行数据")
            
            # 构造初始state（使用从文件加载的prompt）
            state: Graph_State = {
                "generation_prompt": self.generation_prompt,
                "reflection_prompt": self.reflection_prompt,
                "user_prompt": str(row['user_prompt']) if pd.notna(row['user_prompt']) else "",
                "user_advice": str(row['user_feedback']) if pd.notna(row['user_feedback']) else "",
                "content": str(row['generation_content']) if pd.notna(row['generation_content']) else "",
                "reflecton_advice": str(row['reflection_advice']) if pd.notna(row['reflection_advice']) else "",
                "reflect_count": 0
            }
            
            # 调用graph流程
            logger.info(f"调用generation_graph_flow_v1处理第{row_index + 1}行")
            result_state = await generation_graph_flow_v1.ainvoke(state)
            
            # 提取结果
            new_content = result_state.get("content", "")
            new_reflection_advice = result_state.get("reflecton_advice", "")
            reflect_count = result_state.get("reflect_count", 0)
            
            logger.info(f"第{row_index + 1}行处理完成，反思次数: {reflect_count}")
            logger.info(f"生成内容长度: {len(new_content)}")
            logger.info(f"反思建议长度: {len(new_reflection_advice)}")
            
            return {
                "success": True,
                "generation_content": new_content,
                "reflection_advice": new_reflection_advice,
                "reflect_count": reflect_count,
                "error": None
            }
            
        except Exception as e:
            error_msg = f"处理第{row_index + 1}行时发生错误: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            
            return {
                "success": False,
                "generation_content": "",
                "reflection_advice": "",
                "reflect_count": 0,
                "error": error_msg
            }
    
    async def process_all_rows(self) -> bool:
        """
        处理所有行数据
        
        Returns:
            bool: 处理是否成功
        """
        if self.df is None:
            logger.error("数据未加载，请先调用load_excel()")
            return False
            
        try:
            logger.info(f"开始批处理，共{len(self.df)}行数据")
            
            # 创建结果列
            #self.df['processed_generation_content'] = ""
            #self.df['processed_reflection_advice'] = ""
            self.df['reflect_count'] = 0
            self.df['process_error'] = ""
            self.df['process_timestamp'] = ""
            
            # 逐行处理
            for index, row in self.df.iterrows():
                result = await self.process_single_row(index, row)
                
                # 更新DataFrame
                if result['success']:
                    self.df.at[index, 'generation_content'] = result['generation_content']
                    self.df.at[index, 'reflection_advice'] = result['reflection_advice']
                    self.df.at[index, 'reflect_count'] = result['reflect_count']
                    self.df.at[index, 'process_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.processed_count += 1
                else:
                    self.df.at[index, 'process_error'] = result['error']
                    self.df.at[index, 'process_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.error_count += 1
                
                # 每处理10行输出一次进度
                if (index + 1) % 10 == 0:
                    logger.info(f"已处理{index + 1}/{len(self.df)}行")
            
            logger.info(f"批处理完成！成功: {self.processed_count}行，失败: {self.error_count}行")
            return True
            
        except Exception as e:
            logger.error(f"批处理过程中发生错误: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    def save_results(self) -> bool:
        """
        保存处理结果到新的Excel或CSV文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            logger.info(f"正在保存结果到: {self.output_file}")
            
            # 创建输出目录（如果不存在）
            output_dir = os.path.dirname(self.output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 根据输出文件扩展名选择保存方法
            if self.output_file.lower().endswith('.csv'):
                # 保存为CSV文件
                self.df.to_csv(self.output_file, index=False, encoding='utf-8')
                
                # 创建摘要文件
                summary_file = self.output_file.replace('.csv', '_summary.csv')
                summary_data = {
                    '统计项目': [
                        '总行数',
                        '成功处理行数', 
                        '失败行数',
                        '处理时间',
                        '输入文件',
                        '输出文件'
                    ],
                    '数值': [
                        len(self.df),
                        self.processed_count,
                        self.error_count,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.input_file,
                        self.output_file
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_csv(summary_file, index=False, encoding='utf-8')
                logger.info(f"摘要已保存到: {summary_file}")
                
            else:
                # 保存到Excel文件
                with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
                    # 保存主数据
                    self.df.to_excel(writer, sheet_name='Processed_Data', index=False)
                    
                    # 创建处理摘要
                    summary_data = {
                        '统计项目': [
                            '总行数',
                            '成功处理行数', 
                            '失败行数',
                            '处理时间',
                            '输入文件',
                            '输出文件'
                        ],
                        '数值': [
                            len(self.df),
                            self.processed_count,
                            self.error_count,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            self.input_file,
                            self.output_file
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Processing_Summary', index=False)
            
            logger.info(f"结果已成功保存到: {self.output_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存结果失败: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    async def run(self) -> bool:
        """
        运行完整的批处理流程
        
        Returns:
            bool: 处理是否成功
        """
        try:
            logger.info("开始Excel批处理流程")
            
            # 1. 加载prompt文件
            if not self.load_prompts():
                return False
            
            # 2. 加载Excel文件
            if not self.load_excel():
                return False
            
            # 3. 处理所有行
            if not await self.process_all_rows():
                return False
            
            # 4. 保存结果
            if not self.save_results():
                return False
            
            logger.info("Excel批处理流程完成！")
            return True
            
        except Exception as e:
            logger.error(f"批处理流程失败: {str(e)}")
            logger.error(traceback.format_exc())
            return False


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Excel/CSV批处理脚本')
    parser.add_argument('--input_file', '-i', required=True, help='输入Excel或CSV文件路径')
    parser.add_argument('--prompt_file', '-p', required=True, help='包含generation_prompt和reflection_prompt的JSON文件路径')
    parser.add_argument('-o', '--output', help='输出Excel或CSV文件路径（可选）')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')

    # python excel_batch.py --input_file mtv_graph_batch917.xlsx --prompt_file prompts/veo3_gen_prompt.json -o mtv_graph_batch917_processed.xlsx
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 输入文件不存在: {args.input_file}")
        return False
    
    # 检查prompt文件是否存在
    if not os.path.exists(args.prompt_file):
        print(f"错误: Prompt文件不存在: {args.prompt_file}")
        return False
    
    # 创建批处理器
    processor = ExcelBatchProcessor(args.input_file, args.prompt_file, args.output)
    
    # 运行批处理
    success = await processor.run()
    
    if success:
        print(f"批处理成功完成！")
        print(f"输出文件: {processor.output_file}")
        print(f"处理统计: 成功{processor.processed_count}行，失败{processor.error_count}行")
    else:
        print("批处理失败！")
        return False
    
    return True


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
