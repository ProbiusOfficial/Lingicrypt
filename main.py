import argparse
import sys

def mushroom_spore_encode(text):
    mapping = {'0': '菇', '1': '哩', '2': '哇擦'}
    spore = "灵感菇🍄"
    
    encoded = []
    for char in text:
        # 三进制转换
        num = ord(char)
        digits = []
        while num > 0:
            num, rem = divmod(num, 3)
            digits.append(str(rem))
        # 补零对齐到5位并反转
        ternary = ''.join(reversed(digits)).zfill(5)
        # 转换为灵感菇🍄
        mushroom = ''.join([mapping[d] for d in ternary])
        # 封装孢子结构
        encoded.append(f"{spore}{mushroom}{spore}")
    
    return ''.join(encoded)

def mushroom_spore_decode(encoded_str):
    spore = "灵感菇🍄"
    reverse_map = {'菇':'0', '哩':'1', '哇擦':'2'}
    
    parts = encoded_str.split(spore)
    # 过滤空值和标记残留
    codes = [p for p in parts if p and not p.startswith('灵感菇')]
    
    decoded = []
    for code in codes:
        # 双指针解析变长编码
        ptr = 0
        digits = []
        while ptr < len(code):
            # 最长匹配优先
            if code.startswith('哇擦', ptr):
                digits.append('2')
                ptr += 2
            elif code[ptr] == '哩':
                digits.append('1')
                ptr += 1
            elif code[ptr] == '菇':
                digits.append('0')
                ptr += 1
            else:
                raise ValueError(f"非法字符在位置 {ptr}: {code[ptr:ptr+2]}")
        
        # 三进制转十进制
        value = sum(int(d)*3**(4-i) for i,d in enumerate(digits))
        decoded.append(chr(value))
    
    return ''.join(decoded)

def main():
    
    parser = argparse.ArgumentParser(
        prog='灵感菇编解码器',
        description='🌱 将文本与灵感菇🍄相互转换的神奇工具',
        epilog='使用示例：\n'
               '  编码文本: python main.py -e "Hello"\n'
               '  解码文本: python main.py -d "灵感菇🍄..."\n'
               '  文件操作: python main.py -e -f input.txt -o encoded.mush\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', 
                      action='store_true',
                      help='启用编码模式')
    group.add_argument('-d', '--decode',
                      action='store_true',
                      help='启用解码模式')
    
    parser.add_argument('-f', '--file',
                       metavar='FILE',
                       help='输入文件路径')
    parser.add_argument('-o', '--output',
                       metavar='OUTPUT',
                       help='输出文件路径')
    parser.add_argument('text',
                       nargs='?',
                       default=None,
                       help='直接输入的文本内容（当未使用-f时）')
    
    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        else:
            if not args.text:
                raise ValueError("未提供输入文本或文件")
            content = args.text
    except FileNotFoundError:
        sys.exit(f"错误：文件 {args.file} 不存在")
    except Exception as e:
        sys.exit(f"输入错误: {str(e)}")

    try:
        if args.encode:
            result = mushroom_spore_encode(content)
        else:
            result = mushroom_spore_decode(content)
    except ValueError as e:
        sys.exit(f"处理失败: {str(e)}")

    try:
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
        else:
            print("处理结果：")
            print(result)
    except IOError:
        sys.exit(f"无法写入文件 {args.output}")

if __name__ == "__main__":
    main()
